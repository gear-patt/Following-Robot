#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from subprocess import call
import pandas as pd
import time

def callback(data):
	print(data.data)
	data = data.data
	data = int(data)
	if data in [1,2]:
		df = pd.read_csv('/home/mustar/catkin_ws/src/simple_navigation_goals/scripts/number.csv')
		df['number'] = data
		df.to_csv('/home/mustar/catkin_ws/src/simple_navigation_goals/scripts/goals.csv', index=False)
		call(["rosrun", "simple_navigation_goals", "send_goal.py"])

def listener():
	rospy.init_node('listener', anonymous=True)
  	rospy.Subscriber("take_me_to", String, callback)
  	rospy.spin()
if __name__ == '__main__':
	listener()
