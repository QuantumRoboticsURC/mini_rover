#!/usr/bin/env python3

#Declare libraries
import rospy
from lx16a import *
from math import sin, cos
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist


"""Lets move a motor to a desired position using
a value (deg) sent by a program in ROS"""

def callback(data):
	
	# Print the received data
	print("Im hearing: ", data.angular.z)
	servo1.motorMode(int(data.linear.x+data.angular.z)*1000)
	servo3.motorMode(int(data.linear.x+data.angular.z)*1000)
	servo5.motorMode(int(data.linear.x-data.angular.z)*1000)
	servo7.motorMode(int(data.linear.x-data.angular.z)*1000)



'''
	if data.linear.x >0:
		if data.angular.z>0:
			servo1.motorMode(int(data.linear.x*1000))
			servo3.motorMode(int(data.linear.x*1000))
		elif data.angular.z==0:
			servo1.motorMode(int(data.linear.x*1000))
			servo3.motorMode(int(data.linear.x*1000))
			servo5.motorMode(int(data.linear.x*1000))
			servo7.motorMode(int(data.linear.x*1000))
		elif data.angular.z<0:
			servo5.motorMode(int(data.linear.x*1000))
			servo7.motorMode(int(data.linear.x*1000))
	elif data.linear.x < 0:
		if data.angular.z<0:
			servo1.motorMode(int(data.linear.x*1000))
			servo3.motorMode(int(data.linear.x*1000))
		elif data.angular.z==0:
			servo1.motorMode(int(data.linear.x*1000))
			servo3.motorMode(int(data.linear.x*1000))
			servo5.motorMode(int(data.linear.x*1000))
			servo7.motorMode(int(data.linear.x*1000))
		elif data.angular.z>0:
			servo5.motorMode(int(data.linear.x*1000))
			servo7.motorMode(int(data.linear.x*1000))
	else:
		servo1.motorMode(0)
		servo3.motorMode(0)
		servo5.motorMode(0)
		servo7.motorMode(0)
'''		
		
		
			

def program_init():
	# Init the node
	rospy.init_node('main', anonymous=True)

	# Subscribe to a topic named "Received Angle" and call the function "callback"
	rospy.Subscriber("cmd_vel", Twist, callback)

	#Spin the program
	rospy.spin()

if __name__ == '__main__':
	# Select the correct port, otherwise, the program wont continue
	LX16A.initialize("/dev/ttyUSB0")

	# Define the servos, remember you had to set the ID before.
	servo1 = LX16A(1)
	servo3 = LX16A(3)
	servo5 = LX16A(5)
	servo7 = LX16A(7)

	# Define the mode, in this case, servoMode

	# Start the program
	program_init()


