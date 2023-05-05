#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Pose, Quaternion
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion


class OdomReader():
	def __init__(self):
		rospy.init_node("odom_reader")
		self.odom_reader_subscriber = rospy.Subscriber("/odom/filtered", Odometry, self.robot_odom_callback)
		self.rate = rospy.Rate(1) # 1hz
		self.robot_quaternion = None
	
	def robot_odom_callback (self, data):
		self.robot_point = data.pose.pose.position
		self.robot_quaternion = data.pose.pose.orientation
	
	def main(self):
		while not rospy.is_shutdown():
			if self.robot_quaternion != None:
				quaternion = [self.robot_quaternion.x, self.robot_quaternion.y, self.robot_quaternion.z, self.robot_quaternion.w]
				(roll,pitch,yaw) = euler_from_quaternion(quaternion)
				print("X: ", self.robot_point.x, "Y: ",self.robot_point.y)
				print("Yaw: ", yaw*180/3.1415926535897932384626323)
				self.rate.sleep()	

if __name__ == "__main__":
	odom_reader = OdomReader()
	odom_reader.main()
