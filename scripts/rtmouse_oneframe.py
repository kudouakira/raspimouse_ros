#!/usr/bin/env python

import sys, time
import rospy
from raspimouse_ros.srv import *
from raspimouse_ros.msg import *
from std_msgs.msg import UInt16

def switch_motors(onoff):
    rospy.wait_for_service('/raspimouse/switch_motors')
    try:
        p = rospy.ServiceProxy('/raspimouse/switch_motors', SwitchMotors)
        res = p(onoff)
        return res.accepted
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    else:
        return False
    
def raw_control(left_hz,right_hz):
    pub = rospy.Publisher('/raspimouse/motor_raw', LeftRightFreq, queue_size=10)

    if not rospy.is_shutdown():
        d = LeftRightFreq()
        d.left = left_hz
        d.right = right_hz
        pub.publish(d)

def lightsensor_callback(data):
    lightsensors.left_side = data.left_side
    lightsensors.right_side = data.right_side
    lightsensors.left_forward = data.left_forward
    lightsensors.right_forward = data.right_forward

def oneframe(p):
    t=(5*3.14*p)/(400*18)
    raw_control(p,p)
    time.sleep(round(t,1))

def stop_motor():
    raw_control(0,0)
    switch_motors(Fales)

if __name__ == '__main__':
    rospy.init_node('one_frame')
    #sub = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValue, lightsensor_callback)
    raw_control(100,100)
    time.sleep(1)
    while not rospy.is_shutdown():
#        try:
            #raw_input('Press Enter')
            #oneframe(300)
            raw_control(300,300)
            time.sleep(3)
#        except rospy.KeyboardInterrupt:
#            break

    stop_motor()   
