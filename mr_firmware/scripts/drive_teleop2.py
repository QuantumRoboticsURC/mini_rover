#!/usr/bin/env python
import rospy
import rospkg
from geometry_msgs.msg import Twist
from std_msgs.msg import *
from sensor_msgs.msg import Joy
import time
import math
estado=1
buttons, axes = [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]
Vel_map=[float(0.0),float(0.0),float(0.0),float(0.0)]
Angles_map=[0,0,0,0]
Limits_map=[90,-90]
r=0
s=0
t=0
theta=0

def check_limits():
    global Limits_map, Angles_map
    for i in range(4):
        if Limits_map[0]<Angles_map[i]:
            Angles_map[i]=Limits_map[0]
        elif Limits_map[1]>Angles_map[i]:
            Angles_map[i]=Limits_map[1]
            
def on_joy(data):
    global buttons, axes
    buttons = list(data.buttons [:])
    axes = list(data.axes [:])
def control():
    global buttons,axes,Vel_map,Angles_map,estado,r,s,t,theta
    if axes[0]>.5:
        print("Girando sobre eje izquierda")
        Angles_map[0]=-45
        Angles_map[1]=45
        Angles_map[2]=45
        Angles_map[3]=-45
        pubA.publish(str(Angles_map))
        Vel_map[0]=-.5
        Vel_map[1]=-.5
        Vel_map[2]=.5
        Vel_map[3]=.5
        pub.publish(str(Vel_map))
        s=1
    elif axes[0]<-.5:
        print("Girando sobre eje derecha")
        Angles_map[0]=-45
        Angles_map[1]=45
        Angles_map[2]=45
        Angles_map[3]=-45
        pubA.publish(str(Angles_map))
        Vel_map[0]=.5
        Vel_map[1]=.5
        Vel_map[2]=-.5
        Vel_map[3]=-.5
        pub.publish(str(Vel_map))
        s=1
    elif axes[0]==0:
        if s==1:
            print("Alto giro")
            Angles_map[0]=0
            Angles_map[1]=0
            Angles_map[2]=0
            Angles_map[3]=0
            pubA.publish(str(Angles_map))
            Vel_map[0]=0
            Vel_map[1]=0
            Vel_map[2]=0
            Vel_map[3]=0
            s=0
            pub.publish(str(Vel_map))
    if axes[1]>.4 or axes[1]<-.4: 
        Vel_map[0]=float(axes[1])
        Vel_map[1]=float(axes[1])
        Vel_map[2]=float(axes[1])
        Vel_map[3]=float(axes[1])
        print("Adelante o atras")
        pub.publish(str(Vel_map))
        r=1
    elif axes[1]==0:
        if r==1:
            r=0
            Vel_map[0]=float(0)
            Vel_map[1]=float(0)
            Vel_map[2]=float(0)
            Vel_map[3]=float(0)
            print("Alto")
            pub.publish(str(Vel_map))
    if buttons[4]:
        if Angles_map==[0,0,0,0]:
            print("Cambio a modo Holonomico ")
            estado=1
    elif buttons[5]:
        if Angles_map==[0,0,0,0]:
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
                theta=math.atan(axes[2]/axes[5])*180/math.pi
            else:
                if axes[2]>0:
                    theta=90
                else:
                    theta=-90
            Angles_map=[int(theta),int(theta),int(theta),int(theta)]
            pubA.publish(str(Angles_map))
            t=1
        else:
            if t==1:
                theta=0
                Angles_map=[0,0,0,0]
                t=0
                pubA.publish(str(Angles_map))
    else:
        if ((axes[2]**2+axes[5]**2)>=.99) and axes[5]>-0.3:
            print("Direccion Holonomica")
            if axes[5]>0:
                theta=math.atan(axes[2]/axes[5])*180/math.pi
            else:
                if axes[2]>0:
                    theta=90
                else:
                    theta=-90
            Angles_map=[int(theta),-int(theta),int(theta),-int(theta)]
            pubA.publish(str(Angles_map))
            t=1
        else:
            if t==1:
                theta=0
                Angles_map=[0,0,0,0]
                t=0
                pubA.publish(str(Angles_map))
rospy.init_node("drive_teleop")
rospy.Subscriber("joy",Joy,on_joy)
pub = rospy.Publisher('Vel', String, queue_size=1)
pubA= rospy.Publisher('Angles', String, queue_size=1)
rate = rospy.Rate(20)
print("Hola")
while not rospy.is_shutdown():
    control()
    rate.sleep()
