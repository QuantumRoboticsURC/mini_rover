#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

def get_rotation (msg):
    global roll, pitch, yaw, x, y, yaw_deg
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw_deg = yaw * 180.0 / 3.1416
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    print ("Orientacion: ", yaw_deg, ", Posicion X: ", x, ", Posicion Y: ", y) 

rospy.init_node('my_quaternion_to_euler')

sub = rospy.Subscriber ('/odometry/filtered', Odometry, get_rotation)

r = rospy.Rate(1)
while not rospy.is_shutdown():
    r.sleep()
