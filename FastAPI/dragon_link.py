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

def connect_to_dragonlink(port="udp:10.223.168.1:14550", baudrate=115200):
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
    print(f"Heartbeat: {msg}")

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

def main():
    try:
        # Connect to DragonLink
        dl = connect_to_dragonlink()
        
        # Example commands (modify as needed)
        set_flight_mode(dl, 'LOITER')
        


    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()