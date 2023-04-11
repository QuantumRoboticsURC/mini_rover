#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from std_msgs.msg import Float64

pub_cmd_2 = rospy.Publisher('mr/swerve_back_left_link_position_controller/command', Float64, queue_size=1)
pub_cmd_4 = rospy.Publisher('mr/swerve_back_right_link_position_controller/command', Float64, queue_size=1)
pub_cmd_1 = rospy.Publisher('mr/swerve_front_left_link_position_controller/command', Float64, queue_size=1)
pub_cmd_3 = rospy.Publisher('mr/swerve_front_right_link_position_controller/command', Float64, queue_size=1)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    if (data.linear.x == 0 and data.angular.z != 0):
        pub_cmd_1.publish(-0.785)
        pub_cmd_2.publish(0.785)
        pub_cmd_3.publish(0.785)
        pub_cmd_4.publish(-0.785)
    else:
        pub_cmd_1.publish(0)
        pub_cmd_2.publish(0)
        pub_cmd_3.publish(0)
        pub_cmd_4.publish(0)
    
    
def publish_commands():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('publish_commands', anonymous=True)

    rospy.Subscriber("mr/cmd_vel", Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    publish_commands()
