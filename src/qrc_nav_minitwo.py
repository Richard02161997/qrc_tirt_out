#!/usr/bin/env python
import rospy
import actionlib
import time
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from std_msgs.msg import String

###### Code infomation ######
# Version V1.0.0            #
# Date    Aug.25 2021       #
# Note    *From Yuntech     #
#         *Fix bugs         #
#############################

class map_navigation():
    def __init__(self):
        #set point
        #Table 1
        self.xTable1 = -0.026
        self.yTable1 = 0.266
        #Table 2
        self.xTable2 = -0.026
        self.yTable2 = 0.266
        #Table 3
        self.xTable3 = -0.026
        self.yTable3 = 0.266
        #Table 4
        self.xTable4 = -0.026
        self.yTable4 = 0.266
        
        #Others
        self.goalReached = False
        self.datatemp = '' #Check info from zbar
        self.times = 0 #Times for callback
        
        #make a node and ready
        rospy.init_node('qr_code_py', anonymous=True)
        rospy.loginfo("qr_code ready")

        rospy.loginfo("Wait for zbar_opencv")
        rospy.Subscriber('zbar_opencv_code', String, self.callback)

        rospy.spin()

        rospy.loginfo("exit")    


    #Check data from zbar and do something
    def callback(self,data):
        if data.data != self.datatemp:
            if data.data == '1':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xTable1, self.yTable1)
                self.check(self.goalReached)

            elif data.data == '2':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xTable2, self.yTable2)
                self.check(self.goalReached)

            elif data.data == '3':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xTable3, self.yTable3)
                self.check(self.goalReached)

            elif data.data == '4':
                rospy.loginfo( '%s', data.data)
                self.goalReached = self.moveToGoal(self.xTable3, self.yTable3)
                self.check(self.goalReached)
        
            rospy.loginfo("   ")
            self.datatemp = data.data
            rospy.loginfo("Waiting...")
            time.sleep(1)
            rospy.loginfo("Wait for zbar_opencv")


    #Send point to move_base node 
    def moveToGoal(self,xGoal,yGoal):
        #define a client for to send goal requests to the move_base server through a SimpleActionClient
        ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        #wait for the action server to come up
        while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
            rospy.loginfo("Waiting for the move_base action server to come up")

        goal = MoveBaseGoal()

        #set up the frame parameters
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # moving towards the goal*/
        goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0

        rospy.loginfo("Sending goal location ...")
        ac.send_goal(goal)

        #for x in range(30):
        ac.wait_for_result(rospy.Duration(60))
            #rospy.sleep(1.0)
            #rospy.loginfo("%d",ac.get_state())

        if(ac.get_state() ==  GoalStatus.SUCCEEDED):
            rospy.loginfo("You have reached the destination")
            return True

        else:
            rospy.loginfo("The robot failed to reach the destination")
            return False


    #Check for robot 
    def check(self,goalReached):
        if (self.goalReached):
            rospy.loginfo("Congratulations!")
            
        else:
            rospy.loginfo("Hard Luck!")

        return 0


if __name__ == '__main__':
        map_navigation()
        rospy.spin()       
