import time
import requests
from pymavlink import mavutil

FASTAPI_URI = 'http://127.0.0.1:8000/'

MAVLINK_ADR = 'udp:127.0.0.1:14550'
MASTER = None


class mavlink_drone:
    
    master = None
    drone_id = None

    def __init__(self):
        self._init_mavlink()
        self._set_mapping_mode()
        self._arm_drone()
        pass
    
    #Step 1: initialize and verify mavlink connection
    def _init_mavlink(self):
        #connect to mavlink at given IP address
        self.master = mavutil.mavlink_connection(MAVLINK_ADR)

        # wait for heartbeat to ensure proper startup
        print("waiting for heartbeat")
        self.master.wait_heartbeat()
        print("Heartbeat received!")
    
    #Step 2: Set the Mapping Mode
    def _set_mapping_mode(self, mode : str):
        #sets mode
        mode_id = self.master.mode_mapping()[mode]
        self.master.set_mode(mode_id)

    #Step 3: Arm the motors
    def _arm_drone(self):
        # Arm the drone
        self.master.arducopter_arm()
        self.master.motors_armed_wait()
        print("Drone armed!")




    # From Ground Position, lift to target alititude
    def takeoff (
        self,
        target_alt : float
    ):  
        master = self.master

        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0, 0, 0,
            0, 0,
            target_alt
        )

        # Wait until the drone reaches the target altitude
        print("Drone takingoff!")
        while True:
            msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                altitude = msg.relative_alt / 1000.0  # Convert mm to meters
                print(f"🔼 Current Altitude: {altitude:.1f}m")

                if altitude >= target_alt * 0.95:  # 95% of the target altitude
                    print("✅ Reached target altitude!")
                    break

            time.sleep(1)
        
        
        print("⏳ Waiting for GPS lock...")
        while True:
            msg = master.recv_match(type='GPS_RAW_INT', blocking=True)
            if msg.fix_type >= 3:  # 3D Fix (GPS available)
                print("✅ GPS lock acquired!")
                break
            time.sleep(1)

    def seek_position(
        self,
        lat : float,
        lon : float,
        alt : float,
    ):
        # Convert latitude & longitude to integer format (scaled by 1E7)
        lat_int = int(lat * 1E7)
        lon_int = int(lon * 1E7)

        # Send position target command
        self.master.mav.set_position_target_global_int_send(
            0, self.master.target_system, self.master.target_component,
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
            msg = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
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

    def stop(self):
        # Stop movement by sending zero velocity
        print("🛑 Stopping movement.")
        for _ in range(10):  # Send stop command for a short time
            self.master.mav.set_position_target_local_ned_send(
                0, self.master.target_system, self.master.target_component,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                0b0000111111000111,  # Mask (only velocity control enabled)
                0, 0, 0,  # Position (not used)
                0, 0, 0,  # Stop movement
                0, 0, 0,  # Acceleration (not used)
                0,
                0  # No yaw change
            )
            time.sleep(0.1)  # Small delay

        print("✅ Done.")
