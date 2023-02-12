# BlueRov Wiki
## Startup
Vor jedem start sind bestimmte bedingungen herzustellen
- eingeloggt als Root? `sudo -s`
- Sources hinzugefügt? 
  - `source /opt/ros/humble/setup.bash`
  - in den Workspace navigieren `cd ros_bluerov`
  - `source install/local_setup.bash` 

## Starten einer Node
- ros run 'Package' 'Node' `ros2 run bluerov_pkg gps`
