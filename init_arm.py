import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import PlanningScene, ObjectColor
from moveit_commander import MoveGroupCommander, PlanningSceneInterface

GROUP_NAME_GRIPPER = 'gripper'

GRIPPER_FRAME = 'gripper_link'
GRIPPER_JOINT_NAMES = ['gripper_joint']
GRIPPER_EFFORT = [1.0]
GRIPPER_PARAM = '/gripper_controller'

arm = moveit_commander.MoveGroupCommander("arm")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=10)
gripper_pose_pub = rospy.Publisher('target_pose', PoseStamped, queue_size=10)
scene_pub = rospy.Publisher('planning_scene', PlanningScene, queue_size=10)
scene = moveit_commander.PlanningSceneInterface()
robot = moveit_commander.RobotCommander()
gripper = MoveGroupCommander(GROUP_NAME_GRIPPER)

gripper_opened = [rospy.get_param(GRIPPER_PARAM + "/max_opening") ]
gripper_closed = [rospy.get_param(GRIPPER_PARAM + "/min_opening") + 0.01]
gripper_neutral = [rospy.get_param(GRIPPER_PARAM + "/neutral", (gripper_opened[0] + gripper_closed[0])/2.0) ]
gripper_tighten = rospy.get_param(GRIPPER_PARAM + "/tighten", 0.0) 

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
        print "Moving to desired location"
        arm.set_joint_value_target(group_variable_values)

        plan = arm.plan()

        arm.go(wait=True)

def reset_arm():
    print "Moving the arm to reset position"
    position_creater(-1.55, -1.60, -1.58, 1.50, 0.0)
    #position_creater(1.70, -1.61, -1.58, -0.48, 0.0)

def display():
	print "============ Reference frame: %s" % arm.get_planning_frame()
	print "============ Reference frame: %s" % arm.get_planning_frame()
	print "============ Reference frame: %s" % arm.get_end_effector_link()
	print "============ Robot Groups:"
	print robot.get_group_names()
	print "============ Printing robot state"
	print robot.get_current_state()
	print "============"

def set_gripper(state):
    if state == "opened":
              rospy.loginfo("Set Gripper: Open " +  str(gripper_opened))
              gripper.set_joint_value_target(gripper_opened)
              gripper.go() 
    if state == "close":
              rospy.loginfo("Set Gripper: close " +  str(gripper_closed))
              gripper.set_joint_value_target(gripper_closed)
              gripper.go() 
    elif state == "neutral":
              rospy.loginfo("Set Gripper: neutral " +  str(gripper_neutral))
              gripper.set_joint_value_target(gripper_neutral)
              gripper.go()
    elif state == "tighten":
              rospy.loginfo("Set Gripper: tighten " +  str(gripper_tighten))
              gripper.set_joint_value_target(gripper_tighten)
              gripper.go()
                          	
def rotation_percentage(percentage):

	#Initialize the arm
	#Clear pose target
	arm.clear_pose_targets()
	#Get the current set of joint values
	group_variable_values = arm.get_current_joint_values()
	
	#Declare variables
	output = 0
	
	#Initialize the arm to the starting position
	#
	#
	#------------------------------------------

	#If the percentage is between 0 and 49	
	if 0 <= percentage and percentage <= 49:
		#Convert to servo value
  		output = -1.55 - (percentage * 0.021)
  		print ("The output is:", output)
		group_variable_values[0] = output

	#If the percentage is equal to 50
	elif percentage == 50:
		#Convert to servo value
  		print ("The output is:", output)
		group_variable_values[0] = output

	#If the percentage is between 51 and 100
	elif 51 <= percentage and percentage <= 100:
		#Convert to servo value
  		output = 2.61 - ((percentage - 51) * 0.021)
  		print ("The output is:", output)
		group_variable_values[0] = output

	#Otherwise the percentage is out of bounds
	else:
    		print ("This is an invalid state")
	
	#Rotate the arm to the desired location
	arm.set_joint_value_target(group_variable_values)
	plan = arm.plan()
	arm.go(wait=True)
