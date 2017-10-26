import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import PlanningScene, ObjectColor
from moveit_msgs.msg import CollisionObject, AttachedCollisionObject
from moveit_msgs.msg import Grasp, GripperTranslation
from moveit_msgs.msg import MoveItErrorCodes
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from moveit_commander import MoveGroupCommander, PlanningSceneInterface, RobotCommander

GROUP_NAME_ARM = 'arm'
GROUP_NAME_GRIPPER = 'gripper'

GRIPPER_FRAME = 'gripper_link'
GRIPPER_JOINT_NAMES = ['gripper_joint']
GRIPPER_EFFORT = [1.0]
GRIPPER_PARAM = '/gripper_controller'

REFERENCE_FRAME = 'base_link'
ARM_BASE_FRAME = 'arm_base_link'

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=10)


class tb_arm:
    arm = 0
    robot = 0
    griper = 0
    def __init__(self):
        print "Intializing moveit commander"
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('TurtleBot_ARM', anonymous=True)

        self.gripper_opened = [rospy.get_param(GRIPPER_PARAM + "/max_opening")]
        self.gripper_closed = [rospy.get_param(GRIPPER_PARAM + "/min_opening") + 0.01]
        self.gripper_neutral = [
            rospy.get_param(GRIPPER_PARAM + "/neutral", (self.gripper_opened[0] + self.gripper_closed[0]) / 2.0)]
        self.gripper_tighten = rospy.get_param(GRIPPER_PARAM + "/tighten", 0.0)

        # Use the planning scene object to add or remove objects
        self.scene = PlanningSceneInterface()

        # Create a scene publisher to push changes to the scene
        self.scene_pub = rospy.Publisher('planning_scene', PlanningScene, queue_size=10)

        # Create a publisher for displaying gripper poses
        self.gripper_pose_pub = rospy.Publisher('target_pose', PoseStamped, queue_size=10)

        # Create a dictionary to hold object colors
        self.colors = dict()

        # Initialize the move group for the right arm
        tb_arm.arm = MoveGroupCommander(GROUP_NAME_ARM)
        tb_arm.robot = RobotCommander()

        # Initialize the move group for the right gripper
        tb_arm.gripper = MoveGroupCommander(GROUP_NAME_GRIPPER)

        # Get the name of the end-effector link
        end_effector_link = tb_arm.arm.get_end_effector_link()

        # Allow some leeway in position (meters) and orientation (radians)
        tb_arm.arm.set_goal_position_tolerance(0.04)
        tb_arm.arm.set_goal_orientation_tolerance(0.01)

        # Allow replanning to increase the odds of a solution
        tb_arm.arm.allow_replanning(True)

        # Set the right arm reference frame
        tb_arm.arm.set_pose_reference_frame(REFERENCE_FRAME)

        # Allow 5 seconds per planning attempt
        tb_arm.arm.set_planning_time(5)

        # Remove any attached objects from a previous session
        #self.scene.remove_attached_object(GRIPPER_FRAME, target_id)

        # Give the scene a chance to catch up
        rospy.sleep(1)

        # Start the arm in the "arm_up" pose stored in the SRDF file
        print "Set Arm: right_up"
        tb_arm.arm.set_named_target('right_up')
        if tb_arm.arm.go() != True:
            print "  Go failed for right up"

        # Move the gripper to the open position
        print "Set Gripper: Open " + str(self.gripper_opened)
        tb_arm.gripper.set_joint_value_target(self.gripper_opened)
        if tb_arm.gripper.go() != True:
            print "  Go failed for gripper open"

    def position_creater(self, joint0, joint1, joint2, joint3, joint4):
        # Clear pose target
        tb_arm.arm.clear_pose_targets()

        # Get the create set of joint values
        group_variable_values = tb_arm.arm.get_current_joint_values()

        group_variable_values[0] = joint0
        group_variable_values[1] = joint1
        group_variable_values[2] = joint2
        group_variable_values[3] = joint3
        group_variable_values[4] = joint4
        print "Moving to desired location"
        tb_arm.arm.set_joint_value_target(group_variable_values)

        plan = tb_arm.arm.plan()

        tb_arm.arm.go(wait=True)

    def reset_arm(self):
        print "Moving the arm to reset position"
        # self.position_creater(-1.55, -1.60, -1.58, 1.50, 0.0)
	self. position_creater(1.70, -1.61, -1.58, -0.48, 0.0)

    def display(self):
        print "============ Reference frame: %s" % tb_arm.arm.get_planning_frame()
        print "============ Reference frame: %s" % tb_arm.arm.get_planning_frame()
        print "============ Reference frame: %s" % tb_arm.arm.get_end_effector_link()
        print "============ Robot Groups:"
        print tb_arm.robot.get_group_names()
        print "============ Printing robot state"
        print tb_arm.robot.get_current_state()
        print "============"

    def set_gripper(self, state):
        self.gripper_opened = [rospy.get_param(GRIPPER_PARAM + "/max_opening")]
        self.gripper_closed = [rospy.get_param(GRIPPER_PARAM + "/min_opening") + 0.01]
        self.gripper_neutral = [
            rospy.get_param(GRIPPER_PARAM + "/neutral", (self.gripper_opened[0] + self.gripper_closed[0]) / 2.0)]
        self.gripper_tighten = rospy.get_param(GRIPPER_PARAM + "/tighten", 0.0)

        if state == "opened":
            rospy.loginfo("Set Gripper: Open " + str(self.gripper_opened))
            tb_arm.gripper.set_joint_value_target(self.gripper_opened)
            tb_arm.gripper.go()
        elif state == "close":
            rospy.loginfo("Set Gripper: close " + str(self.gripper_closed))
            tb_arm.gripper.set_joint_value_target(self.gripper_closed)
            tb_arm.gripper.go()
        elif state == "neutral":
            rospy.loginfo("Set Gripper: neutral " + str(self.gripper_neutral))
            tb_arm.gripper.set_joint_value_target(self.gripper_neutral)
            tb_arm.gripper.go()
        elif state == "tighten":
            rospy.loginfo("Set Gripper: tighten " + str(self.gripper_tighten))
            tb_arm.gripper.set_joint_value_target(self.gripper_tighten)
            tb_arm.gripper.go()

    def rotation_percentage(self, percentage):
        # Initialize the arm
        # Clear pose target
        tb_arm.arm.clear_pose_targets()
        # Get the current set of joint values
        group_variable_values = tb_arm.arm.get_current_joint_values()

        # Declare variables
        output = 0

        # Initialize the arm to the starting position
        #
        #
        # ------------------------------------------

        # If the percentage is between 0 and 49
        if 0 <= percentage and percentage <= 49:
            # Convert to servo value
            output = -1.55 - (percentage * 0.021)
            print ("The output is:", output)
            group_variable_values[0] = output

        # If the percentage is equal to 50
        elif percentage == 50:
            # Convert to servo value
            print ("The output is:", output)
            group_variable_values[0] = output

        # If the percentage is between 51 and 100
        elif 51 <= percentage and percentage <= 100:
            # Convert to servo value
            output = 2.61 - ((percentage - 51) * 0.022)
            print ("The output is:", output)
            group_variable_values[0] = output

        # Otherwise the percentage is out of bounds
        else:
            print ("This is an invalid state")

        # Rotate the arm to the desired location
        tb_arm.arm.set_joint_value_target(group_variable_values)
        plan = tb_arm.arm.plan()
        tb_arm.arm.go(wait=True)

    def lift_percentage(self,percentage):
	# Initialize the arm
        # Clear pose target
        tb_arm.arm.clear_pose_targets()
        # Get the current set of joint values
        group_variable_values = tb_arm.arm.get_current_joint_values() 

	# Declare variables 
	output = 0

	# If percentage is between 0 and 49
	if 0 <= percentage and percentage <= 49:
		
		# Convert to servo value
    		output = -1.13 + (percentage * 0.022)
   	 	print ("The output is:", output)
		group_variable_values[2] = output

	#If percentage is between 50 and 100
  	elif 50 <= percentage and percentage <= 100:
		
		# Convert to servo value
    		output = ((percentage - 50) * 0.011)
    		print ("The output is:", output)
		group_variable_values[2] = output

	#Otherwise the percentage is invalid
  	else:
		# Display percentage error
    		print ("This is an invalid state")

	# Rotate the arm to the desired location
        tb_arm.arm.set_joint_value_target(group_variable_values)
        plan = tb_arm.arm.plan()
        tb_arm.arm.go(wait=True)
