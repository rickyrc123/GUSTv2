#!/usr/bin/env python3
"""
DragonLink MAVLink Control Script

This script connects to a DragonLink antenna system and sends MAVLink commands
to an autonomous vehicle.

Requirements:
- pymavlink
- pyserial
- DragonLink connected via USB and configured for MAVLink pass-through
"""

import time
from pymavlink import mavutil
import argparse

start_lon = None
start_lat = None

def connect_to_dragonlink(port="/dev/ttyUSB0", baudrate=115200):
    """ 
    Connect to the DragonLink system via serial port
    
    Args:
        port (str): Serial port (e.g., '/dev/ttyUSB0' or 'COM3')
        baudrate (int): Baud rate (default: 57600)
    
    Returns:
        mavutil.mavlink_connection: MAVLink connection object
    """
    print(f"Connecting to DragonLink on {port} at {baudrate} baud...")
    connection = mavutil.mavlink_connection(port, baud=baudrate)
    
    # Wait for heartbeat
    print("Waiting for heartbeat...")
    connection.wait_heartbeat()
    print(f"Heartbeat from system (system {connection.target_system}, component {connection.target_component})")
    

    msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=5)
    start_lat = msg.lat / 1E7  # Convert to decimal degrees
    start_lon = msg.lon / 1E7  # Convert to decimal degrees

    print(f"Heartbeat: {msg}")
    print(f"Start Position: {start_lat:.6f}, {start_lon:.6f}")
    return connection

def set_flight_mode(connection, mode):
    """
    Set the vehicle's flight mode
    
    Args:
        connection: MAVLink connection
        mode (str): Flight mode (e.g., 'GUIDED', 'AUTO', 'LOITER')
    """
    print(f"Setting flight mode to {mode}...")
    
    # Get mode ID
    if mode not in connection.mode_mapping():
        print(f"Unknown mode: {mode}")
        print(f"Available modes: {list(connection.mode_mapping().keys())}")
        return
    
    mode_id = connection.mode_mapping()[mode]

    print(f"{mode_id}")

    thing = """connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )"""
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        1,  # Confirmation
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id, 0, 0, 0, 0, 0
    )
    
    # Wait for acknowledgment (not all vehicles send this)
    try:
        ack = connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=10)
        print(f"Mode change result: {ack.result}")
    except:
        print("Mode change command sent (no acknowledgment received)")

def arm_vehicle(connection):
    """Send commands to arm the vehicle"""
    print("Arming vehicle...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # Confirmation
        1,  # Arm (1=arm, 0=disarm)
        0, 0, 0, 0, 0, 0  # Parameters 2-7 (not used)
    )
    
    print("Awaiting Ack...\n")
    
    # Wait for acknowledgment
    ack = connection.recv_match(type='COMMAND_ACK', blocking=True)
    print(f"Command result: {ack.result}")

def takeoff(connection, t_altitude):
    """Command takeoff to specified altitude (meters)"""
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,          # Confirmation
        0, 0, 0, 0,  # Unused params
        0, 0, 0,    # Unused params 
        t_altitude    # Target altitude
    )

    print(f"Takeoff command sent to {t_altitude}m")
    print("Drone takingoff!")

    while True:
        msg = connection.mav.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            altitude = msg.relative_alt / 1000.0  # Convert mm to meters
            print(f"Current Altitude: {altitude:.1f}m")

            if altitude >= t_altitude * 0.95:  # 95% of the target altitude
                print("Reached target altitude!")
                break

        time.sleep(1)

def land(connection):
    """Command landing at current position"""
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,          # Confirmation
        0, 0, 0, 0, # Unused params
        0, 0, 0    # Unused params
    )
    print("Landing...")

def seek_position(
        connection,
        lat : float,
        lon : float,
        alt : float,
    ):
        # Convert latitude & longitude to integer format (scaled by 1E7)
        lat_int = int(lat * 1E7)
        lon_int = int(lon * 1E7)

        # Send position target command
        connection.mav.set_position_target_global_int_send(
            0, connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # Relative to home altitude
            0b0000111111111000,  # Position mask (only lat/lon/alt active)
            lat_int, lon_int, alt,
            0, 0, 0,  # No velocity control
            0, 0, 0,  # No acceleration control
            0,  # No yaw control
            0   # No yaw rate control
        )
        print("📍 Moving to waypoint...")

        while True:
            # Receive position updates
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                current_lat = msg.lat / 1E7  # Convert to decimal degrees
                current_lon = msg.lon / 1E7  # Convert to decimal degrees
                current_alt = msg.relative_alt / 1000.0  # Convert mm to meters

                # Print status
                print(f"📡 Current Position: {current_lat:.6f}, {current_lon:.6f}, Alt: {current_alt:.1f}m")

                # Check if drone is close to target
                lat_reached = abs(current_lat - (lat_int / 1E7)) < 0.00005  # ~5m tolerance
                lon_reached = abs(current_lon - (lon_int / 1E7)) < 0.00005  # ~5m tolerance
                alt_reached = abs(current_alt - alt) < 1  # 1m altitude tolerance

                if lat_reached and lon_reached and alt_reached:
                    print("✅ Reached waypoint!")
                    break

            time.sleep(1)  # Check position every second
        time.sleep(1)  # Wait before sending next command

def execute_path(connection, path):
    """Execute a predefined path"""
    for waypoint in path:
        lat = waypoint[0]
        lon = waypoint[1]
        alt = waypoint[2]
        seek_position(connection, lat, lon, alt)
        time.sleep(1)  # Wait for the vehicle to reach the waypoint
        print(f"Reached waypoint: {lat}, {lon}, {alt}")

def main():

    path = [
        (33.18236,-87.51108,5),
        (33.18236,-87.51108,10),
        (33.18255,-87.51034,5)
    ]

    try:
        # Connect to DragonLink
        dl = connect_to_dragonlink()
        
        # Example commands (modify as needed)
        set_flight_mode(dl, 'GUIDED')

        arm_vehicle(dl)

        takeoff(dl, 10)  # Take off to 10 meters

        execute_path(dl, path)  # Execute the predefined path

        land(dl)  # Land the vehicle

        


    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()