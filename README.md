# mini-rover


## Clone your repo into your catkin workspace
```
cd ~/catkin_ws/src
git clone https://github.com/ShikurM56/mini-rover
cd ~/catkin_ws/
catkin_make
```

## Install all the dependences
```
sudo apt-get install ros-melodic-gmapping
sudo apt-get install ros-melodic-cartographer-ros
sudo apt-get install ros-melodic-map-server
sudo apt-get install ros-melodic-move-base
sudo apt-get install ros-melodic-dwa-local-planner
sudo apt-get install ros-melodic-robot-localization
```

## Connecting to the Mini Rover
```
ssh raul_jetson-2@192.168.0.100
```

## For mapping:

### Start the gmapping node:
```
roslaunch mr_description mr_sim_bringup_mapping.launch 
roslaunch mr_mapping start_mapping.launch
```

### Save the map:
```
rosrun map_server map_saver -f my_map
```

## For navigation:

### Start the navigation node:
```
roslaunch mr_description mr_sim_bringup_mapping.launch 
roslaunch mr_navigation start_navigation.launch 
```
