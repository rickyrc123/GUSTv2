from pymavlink import mavutil
import time
import threading


def connectToDrone(index):
    # Connect to ArduPilot SITL
    master = mavutil.mavlink_connection(f'udp:127.0.0.1:{14550 + index}')
    print(f'waiting for heartbeat for drone {index + 1} ')
    master.wait_heartbeat()
    print("Heartbeat received!")
    return master
def getDroneNum():
    x=int(input("Enter number of drones "))
    return x
def getInputNum(dNum) :
    x=int(input(f"Enter number of inputs for drone {dNum + 1} "))
    return x
def getCoords(numInputs):
    print("Enter coordinates")
    lat = []
    lon = []
    for i in range(numInputs):
        num = float(input("Enter latitude "))
        lat.append(num)
        num = float(input("Enter longitude "))
        lon.append(num)  
    return lat,lon
def enterGuided(master) :
    mode = 'GUIDED'
    mode_id = master.mode_mapping()[mode]
    master.set_mode(mode_id)
def droneArm(master,droneNum):
    droneNum=droneNum+1
    master.arducopter_arm()
    master.motors_armed_wait()
    print(f'Drone {droneNum} armed!')
def findGps(master):
    print("⏳ Waiting for GPS lock...")
    while True:
        msg = master.recv_match(type='GPS_RAW_INT', blocking=True)
        if msg.fix_type >= 3:  # 3D Fix (GPS available)
            print("✅ GPS lock acquired!")
            break
        time.sleep(1)
def gainAltitude(master,dNumber):
    target_altitude = 15
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
    print(f"Drone {dNumber + 1} takingoff!")
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            altitude = msg.relative_alt / 1000.0  # Convert mm to meters
            print(f"🔼 Drone {dNumber + 1} current Altitude: {altitude:.1f}m")

            if altitude >= target_altitude * 0.95:  # 95% of the target altitude
                print(f"✅ Drone {dNumber + 1} reached target altitude!")
                break

        time.sleep(1)
    return target_altitude
def moveDrone(master,numInputs,lat,lon,alt_m,dNumber):
    for i in range(numInputs):
        # Convert latitude & longitude to integer format (scaled by 1E7)
        lat_int = int(lat[i] * 1E7)#int(lat * 1E7)
        lon_int = int(lon[i] * 1E7)#int(lon * 1E7)
    # Send position target command

        master.mav.set_position_target_global_int_send(
            0, master.target_system, master.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            0b0000111111111000,  # Position mask (only lat/lon/alt active)
            lat_int, lon_int, alt_m,
            0, 0, 0,  # No velocity control
            0, 0, 0,  # No acceleration control
            0,  # No yaw control
            0   # No yaw rate control
            )
        print(f"📍 Drone {dNumber+1} moving to waypoint...")

        while True:
            # Receive position updates
            msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                current_lat = msg.lat / 1E7  # Convert to decimal degrees
                current_lon = msg.lon / 1E7  # Convert to decimal degrees
                current_alt = msg.relative_alt / 1000.0  # Convert mm to meters

                # Print status
                print(f"📡 Drone {dNumber+1} current Position: {current_lat:.6f}, {current_lon:.6f}, Alt: {current_alt:.1f}m")

                # Check if drone is close to target
                lat_reached = abs(current_lat - lat[i]) < 0.00005  # ~5m tolerance#lat_reached = abs(current_lat - (lat[i])) < 0.00005  # ~5m tolerance
                lon_reached = abs(current_lon - lon[i]) < 0.00005  # ~5m tolerance#lon_reached = abs(current_lon - (lon[i])) < 0.00005  # ~5m tolerance
                alt_reached = abs(current_alt - alt_m) < 1  # 1m altitude tolerance

                if lat_reached and lon_reached and alt_reached:
                    print(f"✅ Drone {dNumber+1} reached waypoint!")
                    break

            time.sleep(1)  # Check position every second
        time.sleep(1)  # Wait before sending next comman
def stopDrone(master,dNumber):
    print(f"🛑 Stopping movement for drone {dNumber}.")
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
def landDrone(master,dNumber):
    dNumber=dNumber+1
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,  # Land command
        0,  # Confirmation
        0, 0, 0, 0,  # Empty parameters (not used)
        0, 0, 0  # Latitude, Longitude, Altitude (ignored for landing)
    )

    print(f"🛬 Drone {dNumber} landing initiated!")

    # Wait for the drone to reach the ground
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            altitude = msg.relative_alt / 1000.0  # Convert mm to meters
            print(f"🔽 Drone {dNumber} current Altitude: {altitude:.1f}m")

            if altitude <= 0.5:  # If the drone is very close to the ground
                print(f"✅ Drone {dNumber} landed successfully!")
                break

        time.sleep(1)
    print(f"Stopping drone {dNumber}!")
def arm_and_takeoff(master, i):
    enterGuided(master)
    droneArm(master, i)
    gainAltitude(master, i)

lat = []#37.61981077 #
lon = []#-122.37742747 #
numInputs = []
#figure out how many drones you need
#droneNum = 2 
droneNum = getDroneNum()

#ask for how many corrdinates are required

#numInputs = 1 


#create multiple drone connections
drones = []
for i in range(droneNum):
    drones.append(connectToDrone(i))
    inputNums = getInputNum(i)
    numInputs.append(inputNums)
    lats, lons = getCoords(numInputs[i])
    lat.append(lats)
    lon.append(lons)
    
# Arm and Takeoff Drones Simultaneously Using Threads
threads = []
for i, master in enumerate(drones):
    t = threading.Thread(target=arm_and_takeoff, args=(master, i))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Move Drones Simultaneously Using Threads
threads = []
for i, master in enumerate(drones):
    t = threading.Thread(target=moveDrone, args=(master,numInputs[i], lat[i], lon[i], 15, i))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Land Drones Simultaneously Using Threads
threads = []
for i, master in enumerate(drones):
    t = threading.Thread(target=landDrone, args=(master, i))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ All drones have completed their mission!")

