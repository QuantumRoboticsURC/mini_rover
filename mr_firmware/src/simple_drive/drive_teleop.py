#!/usr/bin/python

import rospy
import subprocess

from sensor_msgs.msg import Joy
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from actionlib_msgs.msg import GoalID

class DriveTeleop:
    def __init__(self):
        self.speed_setting = 2 # default to medium speed

        #antenna servo
        self.servo_pan_max = rospy.get_param('~servo_pan_max', 90) # max angle of servo rotation horizontal
        self.servo_pan_min = rospy.get_param('~servo_pan_min', 0) # min angle of servo rotation vertical
        self.servo_position = self.servo_pan_min # initial servo position

        #status colors
        self.blue_status = rospy.get_param('~blue_status', 1) # Blue: Teleoperation (Manually driving)
        self.red_status = rospy.get_param('~red_status', 2) # Red: Autonomous operation
        self.flashing_status = rospy.get_param('~flashing_status', 3) # Flashing Green: Successful arrival at a post or passage through a gate.
        self.status_color = self.blue_status # initial status color


        # publisher
        self.cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.goal_cancel_pub = rospy.Publisher("move_base/cancel", GoalID, queue_size=1)
        self.antenna_pub = rospy.Publisher("antenna_pos", Int32, queue_size=1)
        self.status_pub = rospy.Publisher("status_led", Int32, queue_size=1)
        self.joy_sub = rospy.Subscriber("joy", Joy, self.on_joy)

    def on_joy(self, data):
        # Set speed ratio using d-pad
        if data.axes[7] == 1: # full speed (d-pad up)
            self.speed_setting = 1
        if data.axes[6] != 0: # medium speed (d-pad left or right)
            self.speed_setting = 2
        if data.axes[7] == -1: # low speed (d-pad down)
            self.speed_setting = 3

        # Drive sticks
        left_speed = data.axes[1] / self.speed_setting # left stick
        right_speed = data.axes[5] / self.speed_setting # right stick

        # Convert skid steering speeds to twist speeds
        linear_vel  = (left_speed + right_speed) / 2.0 # (m/s)
        angular_vel  = (left_speed - right_speed) / 2.0 # (rad/s)

        # Publish Twist
        twist = Twist()
        twist.linear.x = linear_vel
        twist.angular.z = angular_vel
        self.cmd_vel_pub.publish(twist)

        # Antenna servo control
        if data.buttons[4]: # security button (L1 Button)
            if data.buttons[3]: # up antennas (Triangle button)
                self.servo_position = self.servo_pan_min
            if data.buttons[1]: # down antennas (X Button)
                self.servo_position = self.servo_pan_max
            self.antenna_pub.publish(self.servo_position)
        
        # Status led control
        if data.buttons[5]: # security button (R1 Button)
            if data.buttons[3]: # blue color (Triangle button)
                self.status_color = self.blue_status
                self.status_pub.publish(self.status_color)
            if data.buttons[2]: # red color (Circle button)
                self.status_color = self.red_status
                self.status_pub.publish(self.status_color)
            if data.buttons[1]: # flashing green (X button)
                self.status_color = self.flashing_status
                self.status_pub.publish(self.status_color)


        # Cancel move base goal
        if data.buttons[9]: # Options button
            rospy.loginfo('Cancelling move_base goal')
            cancel_msg = GoalID()
            self.goal_cancel_pub.publish(cancel_msg)

def main():
    rospy.init_node("drive_teleop")
    controller = DriveTeleop()
    rospy.spin()
