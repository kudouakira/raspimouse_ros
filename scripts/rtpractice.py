#!/usr/bin/env python

import time,sys,threading
import rospy
from std_msgs.msg import *
from raspimouse_ros.msg import *
from raspimouse_ros.srv import *
from check_driver_io import *

class RP(object):
    def __init__(self):
	self.__lightsensor_sub = rospy.Subscriber('/raspimouse/lightsensors', LightSensorValues, self.lightsensor_callback)
	self.__lv = LightSensorValues()
	self.p = rospy.get_param('~p_gain', 0.1)
	rospy.on_shutdown(self.shutdown_hook)

    def lightsensor_callback(self, data):
	self.__lv = data

    def get_left_lightsensor(self):
        return(self.__lv.left_side)

    def get_right_lightsensor(self):
        return(self.__lv.right_side)

    def get_forward_lightsensor(self):
	return(self.__lv.left_forward + self.__lv.right_forward) * 0.5

    def shutdown_hook(self):
	print pos_control(0, 0, 0)
	print switch_motors(False)


if __name__=='__main__':
    rospy.init_node("raspimouse")

    rp = RP()
    print switch_motors(True)
    print rp.p
    target = 850
    moter = 500
    raw_control(moter, moter)

    while not rospy.is_shutdown():
		try:
		#thread
       	t=threading.Timer(0.15,LightSensorValues)
       		t.start()
       		time.sleep(0.15)
       		t.cancel()

       	#lightsensors data
	   		data_l = rp.get_left_lightsensor()
	   		data_r = rp.get_right_lightsensor()
       		data_f = rp.get_forward_lightsensor()

       	#turn right
       		if data_f >= 2200:  
				motor_r=-300
           		motor_l=300
           		raw_control(motor_l,motor_r)
	   			time.sleep(0.5)
           		continue

	   		if data_l <= 90:
	   			break

       	#trace left wall
	   		e = rp.p*(data_l - target) #- (data_r - target)
	   		moter_r = moter - e
	   		moter_l = moter + e
	   		raw_control(moter_l, moter_r)
	   	#rp.r.sleep()
		except rospy.ROSInterruptException:
	    	pass
    raw_control(0,0)
    print "stop now : raw_control(0,0)"
