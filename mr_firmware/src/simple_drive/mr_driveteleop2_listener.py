#!/usr/bin/env python3

#Declare libraries
import rospy
from lx16a import *
from math import sin, cos
from std_msgs.msg import String
from geometry_msgs.msg import Twist


"""Lets move a motor to a desired position using
a value (deg) sent by a program in ROS"""

def my_map(x,in_min,in_max,out_min,out_max):
    x = int(x)
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def callback(data):
	
	# Print the received data
    
	info = str(data.data)[1:len(data.data)-1].split(",")
	servo1.motorMode(1000*int(float(info[0])))
	servo3.motorMode(1000*int(float(info[1])))
	servo5.motorMode(1000*int(float(info[2])))
	servo7.motorMode(1000*int(float(info[3])))
	print("Vel: ")
	print(info)
		
def callback2(data):
	
	# Print the received data
    
	info = str(data.data)[1:len(data.data)-1].split(",")
	servo2.moveTimeWrite(int(my_map(info[0],-90,90,0,180)))
	servo4.moveTimeWrite(int(my_map(info[1],-90,90,0,180)))
	servo6.moveTimeWrite(int(my_map(info[2],-90,90,0,180)))
	servo8.moveTimeWrite(int(my_map(info[3],-90,90,0,180)))
	print("Angles")
	print(info)			

def program_init():
	# Init the node
	rospy.init_node('main', anonymous=True)

	# Subscribe to a topic named "Received Angle" and call the function "callback"
	rospy.Subscriber("Vel", String, callback)
	rospy.Subscriber("Angles", String, callback2)


	#Spin the program
	rospy.spin()

if __name__ == '__main__':
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
	# Select the correct port, otherwise, the program wont continue
	LX16A.initialize("/dev/ttyUSB0")

	# Define the servos, remember you had to set the ID before.
	servo1 = LX16A(1)
	servo3 = LX16A(3)
	servo5 = LX16A(5)
	servo7 = LX16A(7)
	servo2 = LX16A(2)
	servo4 = LX16A(4)
	servo6 = LX16A(6)
	servo8 = LX16A(8)
	servo2.servoMode()
	servo4.servoMode()
	servo6.servoMode()
	servo8.servoMode()

	# Define the mode, in this case, servoMode

	# Start the program
	program_init()


