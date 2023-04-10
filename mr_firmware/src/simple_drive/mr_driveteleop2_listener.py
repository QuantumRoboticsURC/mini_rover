#!/usr/bin/env python3

#Declare libraries
import rospy
from lx16a import *
from math import *
from std_msgs.msg import *
from geometry_msgs.msg import Twist


"""Lets move a motor to a desired position using
a value (deg) sent by a program in ROS"""

def my_map(x,in_min,in_max,out_min,out_max):
    x = int(x)
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def callback(data):
	
	# Print the received data
	servo1.motorMode(int(data.linear.x+data.angular.z)*1000)
	servo3.motorMode(int(data.linear.x+data.angular.z)*1000)
	servo5.motorMode(int(data.linear.x-data.angular.z)*1000)
	servo7.motorMode(int(data.linear.x-data.angular.z)*1000)
	print("Vel: ")
	print(int((data.linear.x+data.angular.z)*1000))
		
def callback2(data):
	
	# Print the received data
	servo2.moveTimeWrite(int(my_map(data,-pi/2,pi/2,0,180)))
	print("Angles")
	print(data)		
def callback3(data):
	
	# Print the received data
	servo4.moveTimeWrite(int(my_map(data,-pi/2,pi/2,0,180)))
	print("Angles")
	print(data)		
def callback4(data):
	
	# Print the received data
	servo6.moveTimeWrite(int(my_map(data,-pi/2,pi/2,0,180)))
	print("Angles")
	print(data)		
def callback5(data):
	
	# Print the received data
	servo8.moveTimeWrite(int(my_map(data,-pi/2,pi/2,0,180)))
	print("Angles")
	print(int(my_map(data,-pi/2,pi/2,0,180)))			

def program_init():
	# Init the node
	rospy.init_node('main', anonymous=True)

	# Subscribe to a topic named "Received Angle" and call the function "callback"
	rospy.Subscriber("cmd_vel", Twist, callback)
	rospy.Subscriber("mr/swerve_front_left_link_position_controller/command", Float64, callback2)
	rospy.Subscriber("mr/swerve_back_left_link_position_controller/command", Float64, callback3)
	rospy.Subscriber("mr/swerve_front_right_link_position_controller/command", Float64, callback4)
	rospy.Subscriber("mr/swerve_back_right_link_position_controller/command", Float64, callback5)


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


