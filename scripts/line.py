import rospy
from check_driver_io.py import *
import sys, time
from raspimouse_ros.srv import *
from raspimouse_ros.msg import *
from std_msgs.msg import UInt16

def lightsensor_callback(data):
	ls.left_side = data.left_side
	ls.left_forward = data.left_forward
	ls.right_side = data.right_side
	ls.right_foeward = data.right_forward

if __name__ == "__main__":
	rospy.init_node('line trase')
	sensors()
	
	while rospy.is_shutdown():
