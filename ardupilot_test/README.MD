Ardupilot commands
start sim with gazebo:sim_vehicle.py -v ArduCopter -f gazebo-iris --model --console --map --out=udp:127.0.0.1:14550

start sim on its own:  sim_vehicle.py -v ArduCopter -L KSFO -I0 --console --map --out=udp:127.0.0.1:14550

"output list" to check output
"output add" to manually change OUTPUT
bring up gazebo sim: gz sim -v4 -r iris_runway.sdf

