#!/usr/bin/env python

import rospy
import actionlib
import pandas as pd
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client(num):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal_data = pd.read_csv('/home/gear-patt/catkin_ws/src/simple_navigation_goals/scripts/goals.csv')
    goal.target_pose.pose.position.x = float(goal_data['goal'+str(num)+'_x'][0])
    goal.target_pose.pose.position.y = float(goal_data['goal'+str(num)+'_y'][0])
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        num = int(pd.read_csv('/home/gear-patt/catkin_ws/src/simple_navigation_goals/scripts/number.csv')['number'][0])
        result = movebase_client(num)
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

