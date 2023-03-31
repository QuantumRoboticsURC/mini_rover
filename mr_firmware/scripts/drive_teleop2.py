#!/usr/bin/env python
import rospy
import rospkg
from geometry_msgs.msg import Twist
from std_msgs.msg import *
from sensor_msgs.msg import Joy
import time
from math import *
estado=1
buttons, axes = [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]
Vel_map=[float(0.0),float(0.0),float(0.0),float(0.0)]
Angles_map=[0,0,0,0]
r=0
s=0
t=0
theta=0
twist = Twist()
def check_limits():
    global Limits_map, Angles_map
    for i in range(4):
        if Limits_map[0]<Angles_map[i]:
            Angles_map[i]=Limits_map[0]
        elif Limits_map[1]>Angles_map[i]:
            Angles_map[i]=Limits_map[1]

def publish():
    global twist
    pub.publish(twist)
def publishAngles():
    global Angles_map
    pubA1.publish(Angles_map[0])
    pubA2.publish(Angles_map[1])
    pubA3.publish(Angles_map[2])
    pubA4.publish(Angles_map[3])
            
def on_joy(data):
    global buttons, axes,twist
    buttons = list(data.buttons [:])
    axes = list(data.axes [:])
def control():
    global buttons,axes,Vel_map,Angles_map,estado,r,s,t,theta
    if axes[0]>.3:
        twist.angular.z=-axes[0]
        Angles_map=[-0.785,0.785,-0.785,0.785]
        print("Girando sobre eje izquierda")
        publish()
        publishAngles()
        s=1
    elif axes[0]<-.3:
        twist.angular.z=-axes[0]
        Angles_map=[-0.785,0.785,-0.785,0.785]
        print("Girando sobre eje derecha")
        publish()
        publishAngles()
        s=1
    elif axes[0]==0:
        if s==1:
            s=0
            twist.angular.z=0
            Angles_map=[0,0,0,0]
            print("Alto giro")
            publish()
            publishAngles()
### Version 1
#    if axes[0]>.5:
#        print("Girando sobre eje izquierda")
#        Angles_map[0]=pi/4
#        Angles_map[1]=-pi/4
#        Angles_map[2]=-pi/4
#        Angles_map[3]=pi/4
#        Vel_map[0]=-.5
#        Vel_map[1]=.5
#        Vel_map[2]=.5
#        Vel_map[3]=-.5
#        publish()
#        s=1
#    elif axes[0]<-.5:
#        print("Girando sobre eje derecha")
#        Angles_map[0]=pi/4
#        Angles_map[1]=-pi/4
#        Angles_map[2]=-pi/4
#        Angles_map[3]=pi/4
#        Vel_map[0]=.5
#       Vel_map[1]=-.5
#        Vel_map[2]=-.5
#        Vel_map[3]=.5
#        publish()
#        s=1
#    elif axes[0]==0:
#        if s==1:
#            print("Alto giro")
#            Angles_map[0]=pi/2
#            Angles_map[1]=pi/2
#            Angles_map[2]=-pi/2
#            Angles_map[3]=-pi/2
#            Vel_map[0]=0
#            Vel_map[1]=0
#            Vel_map[2]=0
#            Vel_map[3]=0
#            s=0
#            publish()
    if axes[1]>.3 or axes[1]<-.3: 
        twist.linear.x=axes[1]
        print("Adelante o atras")
        publish()
        r=1
    elif axes[1]==0:
        if r==1:
            r=0
            twist.linear.x=0
            print("Alto")
            publish()
    ### Version 1
    #if axes[1]>.4 or axes[1]<-.4: 
    #    Vel_map[0]=float(axes[1])
    #    Vel_map[1]=float(axes[1])
    #    Vel_map[2]=float(axes[1])
    #    Vel_map[3]=float(axes[1])
    #    print("Adelante o atras")
    #    publish()
    #    r=1
    #elif axes[1]==0:
    #    if r==1:
    #        r=0
    #        Vel_map[0]=float(0)
    #        Vel_map[1]=float(0)
    #        Vel_map[2]=float(0)
    #        Vel_map[3]=float(0)
    #        print("Alto")
    #        publish()
    
    if buttons[4]:
        if Angles_map==[pi/2,pi/2,-pi/2,-pi/2]:
            print("Cambio a modo Holonomico ")
            estado=1
    elif buttons[5]:
        if Angles_map==[pi/2,pi/2,-pi/2,-pi/2]:
            print("Cambio a modo no Holonomico ")
            estado=2    
    #Verision 1
    #if axes[2]==1:
    #    if estado==1:
    #        print("Direccion Holonomica Izquierda")
    #        Angles_map[0]+=1
    #        Angles_map[1]+=1
    #        Angles_map[2]+=1
    #        Angles_map[3]+=1
    #        check_limits()
    #        pubA.publish(str(Angles_map))
    #    else:
    #        print("Direccion No Holonomica Izquierda")
    #        Angles_map[0]+=1
    #        Angles_map[1]+=1
    #        Angles_map[2]+=-1
    #        Angles_map[3]+=-1
    #        check_limits()
    #        pubA.publish(str(Angles_map))
    #elif axes[2]==-1:
    #    if estado==1:
    #        print("Direccion Holonomica Derecha")
    #        Angles_map[0]+=-1
    #        Angles_map[1]+=-1
    #        Angles_map[2]+=-1
    #        Angles_map[3]+=-1
    #        check_limits()
    #        pubA.publish(str(Angles_map))
    #    else:
    #        print("Direccion No Holonomica Derecha")
    #        Angles_map[0]+=-1
    #        Angles_map[1]+=-1
    #        Angles_map[2]+=1
    #        Angles_map[3]+=1
    #        check_limits()
    #        pubA.publish(str(Angles_map))
    ###
    #Version 2
        if estado==1:
            if ((axes[2]**2+axes[5]**2)>=.99) and axes[5]>-0.3:
                print("Direccion Holonomica")
                if axes[5]>0:
                    theta=atan(axes[2]/axes[5])
                else:
                    if axes[2]>0:
                        theta=pi/2
                    else:
                        theta=-pi/2
                Angles_map=[theta,theta,-theta,-theta]
                publishAngles()
                t=1
            else:
                if t==1:
                    theta=0
                    Angles_map=[0,0,0,0]
                    t=0
                    publishAngles()
        else:
            if ((axes[2]**2+axes[5]**2)>=.99) and axes[5]>-0.3:
                print("Direccion Holonomica")
                if axes[5]>0:
                    theta=atan(axes[2]/axes[5])
                else:
                    if axes[2]>0:
                        theta=pi/2
                    else:
                        theta=-pi/2
                Angles_map=[theta,-theta,theta,-theta]
                publishAngles()
                t=1
            else:
                if t==1:
                    theta=0
                    Angles_map=[0,0,0,0]
                    t=0
                    publishAngles()
rospy.init_node("drive_teleop")
rospy.Subscriber("joy",Joy,on_joy)
pub=rospy.Publisher('cmd_vel',Twist,queue_size=1)
pubT=rospy.Publisher('VelyAng', String, queue_size=1)
#pub = rospy.Publisher('Vel', String, queue_size=1)
pubA2= rospy.Publisher('mr/swerve_back_left_link_position_controller/command', Float64, queue_size=1)
pubA4= rospy.Publisher('mr/swerve_back_right_link_position_controller/command', Float64, queue_size=1)
pubA1= rospy.Publisher('mr/swerve_front_left_link_position_controller/command', Float64, queue_size=1)
pubA3= rospy.Publisher('mr/swerve_front_right_link_position_controller/command', Float64, queue_size=1)
rate = rospy.Rate(20)
print("Hola")
while not rospy.is_shutdown():
    control()
    rate.sleep()
