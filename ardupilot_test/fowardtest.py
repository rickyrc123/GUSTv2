from pymavlink import mavutil
import time

# Connect to ArduPilot SITL
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')
print("waiting for heartbeat")
master.wait_heartbeat()
print("Heartbeat received!")

mode = 'GUIDED'
mode_id = master.mode_mapping()[mode]
master.set_mode(mode_id)

# Arm the drone
master.arducopter_arm()
master.motors_armed_wait()
print("Drone armed!")

target_altitude = 20
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0,
    0, 0, 0,
    0, 0,
    target_altitude
)
# Wait until the drone reaches the target altitude
print("Drone takingoff!")
while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        altitude = msg.relative_alt / 1000.0  # Convert mm to meters
        print(f"🔼 Current Altitude: {altitude:.1f}m")

        if altitude >= target_altitude * 0.95:  # 95% of the target altitude
            print("✅ Reached target altitude!")
            break

    time.sleep(1)
# Set movement parameters
vx = 1  # Move forward at 1 m/s (velocity in X direction)
vy = 0
vz = 0
yaw_rate = 0

duration = 5
rate = 10
for _ in range(duration * rate):
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,  # Mask (only velocity control enabled)
        0, 0, 0,  # Position (not used)
        vx, vy, vz,  # Velocity (Forward in X direction)
        0, 0, 0,  # Acceleration (not used)
        0,
        yaw_rate  # Yaw rate
    )
    time.sleep(1 / rate)  # Wait before sending next command

# Stop movement by sending zero velocity
print("🛑 Stopping movement.")
for _ in range(10):  # Send stop command for a short time
    master.mav.set_position_target_local_ned_send(
        0, master.target_system, master.target_component,
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

# Stop movement
master.mav.set_position_target_local_ned_send(
    0, master.target_system, master.target_component,
    mavutil.mavlink.MAV_FRAME_LOCAL_NED,
    0b0000111111000111,
    0, 0, 0,
    0, 0, 0,  # Set velocity to zero
    0, 0, 0,
    0,
    0
)

# Send LAND command
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_LAND,  # Land command
    0,  # Confirmation
    0, 0, 0, 0,  # Empty parameters (not used)
    0, 0, 0  # Latitude, Longitude, Altitude (ignored for landing)
)

print("🛬 Landing initiated!")

# Wait for the drone to reach the ground
while True:
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        altitude = msg.relative_alt / 1000.0  # Convert mm to meters
        print(f"🔽 Current Altitude: {altitude:.1f}m")

        if altitude <= 0.5:  # If the drone is very close to the ground
            print("✅ Landed successfully!")
            break

    time.sleep(1)
print("Stopping drone!")
