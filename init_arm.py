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

def position_creater(joint0,joint1,joint2,joint3,joint4):
        #Clear pose target
        arm.clear_pose_targets()

        #Get the create set of joint values
        group_variable_values = arm.get_current_joint_values()

        group_variable_values[0] = joint0
        group_variable_values[1] = joint1
        group_variable_values[2] = joint2
        group_variable_values[3] = joint3
        group_variable_values[4] = joint4

        arm.set_joint_value_target(group_variable_values)

        plan = arm.plan()

        arm.go(wait=True)

def reset_arm():
	set.position_creater(1.66, -1.61, -1.58, -0.48, 0.0)

def display()
	print "============ Reference frame: %s" % arm.get_planning_frame()
	print "============ Reference frame: %s" % arm.get_planning_frame()
	print "============ Reference frame: %s" % arm.get_end_effector_link()
	print "============ Robot Groups:"
	print robot.get_group_names()
	print "============ Printing robot state"
	print robot.get_current_state()
	print "============"
