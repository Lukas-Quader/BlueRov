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


## Wie kommuniziere ich im Netzwerk mit Talker und Listener 
- 
