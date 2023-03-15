# BlueRov Wiki
## Startup
Vor jedem start sind bestimmte bedingungen herzustellen
- eingeloggt als Root? `sudo -s`
- Sources hinzugefügt? 
  - `source /opt/ros/humble/setup.bash`
  - in den Workspace navigieren `cd ros_bluerov`
  - `source install/local_setup.bash` 
 
 Alternativ: ~/.bashrc Datei bearbeiten `nano ~/.bashrc`
 - `source /opt/ros/humble/setup.bash`
 - `export ROS_DOMAIN_ID=1` Nummer eventuell anpasssen
 - `export ROS_LOCALHOST_ONLY=0`
 - `source /home/BENUTZER/EIGENER WORKSPACE/install/local_setup.bash`

zum testen der Variablen `printenv | grep -i ROS`

## Starten einer Node
- ros run 'Package' 'Node' `ros2 run bluerov_pkg gps`

## Good to know
- Wenn der GPS Empfänger kein Signal bzw. nicht genügend Satelliten empfängt gibt es kein Output (!!sollte im Code beachtet werden!!)

## Node erstellen
1. in den Workspace wechseln, wen nicht vorhanden erstellen mit `mkdir -p ~/NAME/src`
2. Package erstellen `ros2 pkg create --build-type ament_python py_pubsub`
3. Die eigenen Python Datein kommen in das Package
4. Entrypoint setzen (Finden der startmethode der Pythondatei) in der setup.py im Node
 
`entry_points={
        'console_scripts': [
                'talker = py_pubsub.publisher_member_function:main',
        ],
},`

5. Builden des Package im Workspace `colcon build` (mit `--package-select NAME` können packages einzelnt gebuildet werden um Zeit zu sparen) 
6. Beim ersten erstellen des Package `. install/local_setup.bash` ausführen
7. Node ausführen wie in "Starten einer Node" beschrieben

## Startup für direkte ethernet Connection zwischen DVL und Latte Panda
ifconfig enp1s0 192.168.194.90/24

## rosbag benutzen
Recording starten: ros2 run bag_recorder_nodes_py simple_bag_recorder
Abspielen: ros2 bag play my_bag 


