import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

arm = moveit_commander.MoveGroupCommander("arm")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=10)
scene = moveit_commander.PlanningSceneInterface()
robot = moveit_commander.RobotCommander()

#rospy.sleep(10)
def intialize():
	print "Intializing moveit commander"
	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('TurtleBot_ARM',anonymous=True)
        
