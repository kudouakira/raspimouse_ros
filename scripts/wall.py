#!/usr/bin/env python

import rospy 
import time, sys,threading 
from raspimouse_ros.srv import *
from raspimouse_ros.msg import *
from std_msgs.msg import UInt16
from check_driver_io import *

class RP(object):
    def __init__(self):
        self.__lightsensor_sub = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValues, self.lightsensor_callback)
        self.__lv = LightSensorValues()
        self.p = rospy.get_param('~p_gain', 0.2)

    def lightsensor_callback(self, data):
        self.__lv = data

    def get_left_lightsensor(self):
        return(self.__lv.left_side)

    def get_forward_lightsensor(self):
        return((self.__lv.left_forward)+(self.__lv.right_forward)) * 0.5

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

#def raw_control(left_hz,right_hz):
#	pub = rospy.Publisher('/raspimouse/motor_raw', LeftRightFreq, queue_size=10)
#	if not rospy.is_shutdown():
#		d = LeftRightFreq()
#		d.left = left_hz
#		d.right = right_hz
#		pub.publish(d)


if __name__ == '__main__':
	rospy.init_node("raspi")

rp = RP()
print switch_motors(True)
print rp.p
target = 700
motor = 500
raw_control(motor, motor)

while not rospy. is_shutdown():
	try:
       		t = threading.Timer(0.1,LightSensorValues)
       		t.start()
        	time.sleep(0.1)
        	t.cancel()

       		data_l = rp.get_left_lightsensor()
       		data_f = rp.get_forward_lightsensor()

        	e = rp.p * (data_l - target)
        	motor_r = motor - e
        	motor_l = motor + e
        	raw_control(motor_l, motor_r)

	        if data_l <= 20:
    	        raw_control(400,400)
        	    time.sleep(2)
       	    	raw_control(0,0)
            	time.sleep(0.1)
	            raw_control(-450, 450)
    	        time.sleep(0.3)
        	    continue

        	if data_f >= 300:
            	raw_control(0,0)
            	time.sleep(0.1)
            	raw_control(450, -450)
            	time.sleep(0.3)
            	continue

    except rospy.ROSInterruptException:
        pass
