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

lightsensors=LightSensorValues()

def lightsensor_callbaack(data):
    lightsensors.left_side = data.left_side
    lightsensors.right_side = data.right_side
    lightsensors.left_forward = data.left_forward
    lightsensors.right_forward = data.right_forward

def ls_left():
    return (lightsensors.left_forward)

def ls_right():
    return (lightsensors.right_forward)

if __name__ == "__main__":
    rospy.init_node('raspi_move')
    sub = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValues, lightsensor_callback)
#	raw_control(300,300)
#	time.sleep(10)
	while not rospy.is_shutdown():
	try:
		if :
			raw_control(350,300)
			time.sleep(3)
		
		if lightsensors.right_forward > 1500 :
			raw_control(300,350)
			time.sleep(3)
	except
