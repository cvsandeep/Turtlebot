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

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=10)




class tb_arm:
    def __init__(self):
        print "Intializing moveit commander"
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
		rospy.init_node('TurtleBot_ARM',anonymous=True)

        self.gripper_opened = [rospy.get_param(GRIPPER_PARAM + "/max_opening") ]
		self.gripper_closed = [rospy.get_param(GRIPPER_PARAM + "/min_opening") + 0.01]
		self.gripper_neutral = [rospy.get_param(GRIPPER_PARAM + "/neutral", (gripper_opened[0] + gripper_closed[0])/2.0) ]
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
        arm = MoveGroupCommander(GROUP_NAME_ARM)
		robot = RobotCommander()

        # Initialize the move group for the right gripper
        gripper = MoveGroupCommander(GROUP_NAME_GRIPPER)

        # Get the name of the end-effector link
        end_effector_link = arm.get_end_effector_link()
		
		# Allow some leeway in position (meters) and orientation (radians)
        arm.set_goal_position_tolerance(0.04)
        arm.set_goal_orientation_tolerance(0.01)

        # Allow replanning to increase the odds of a solution
        arm.allow_replanning(True)

        # Set the right arm reference frame
        arm.set_pose_reference_frame(REFERENCE_FRAME)

        # Allow 5 seconds per planning attempt
        arm.set_planning_time(5)

        # Remove any attached objects from a previous session
        self.scene.remove_attached_object(GRIPPER_FRAME, target_id)

        # Give the scene a chance to catch up
        rospy.sleep(1)
		
		# Start the arm in the "arm_up" pose stored in the SRDF file
        print "Set Arm: right_up"
        arm.set_named_target('right_up')
        if arm.go() != True:
            print "  Go failed for right up"

        # Move the gripper to the open position
        print "Set Gripper: Open " +  str(self.gripper_opened)
        gripper.set_joint_value_target(self.gripper_opened)
        if gripper.go() != True:
            print "  Go failed for gripper open"
 
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
                          	
	def rotation_motion(degree):
		#Declare variable to store degree that's converted  to servo value
		conversion = 0

		#Initialize the arm
		arm.clear_pose_targets()
		group_variable_values = arm.get_current_joint_values
		
		#Case for degrees between 0 and 89
		if 0 < degree < 89:
			#Display information about movement
			rospy.loginfo("Rotation is between 0 and 89 degrees")
			
			#Convert degrees to servo values
			conversion = (-1.55 - (degree * 0.01177))

			#Initialize the servos
			group_variable_values[0] = conversion
			group_variable_values[1] = -1.60
			
		#Case for a degree of 90
		elif degree == 90:
			#Display information about movement
			rospy.loginfo("Rotation is 90 degrees")

			#Initialize the servos
			group_variable_values[0] = conversion
			group_variable_values[1] = -1.60
			
		#Case for degrees between 91 and 180
		elif 91 < degree < 180:
			#Display information about movement
			rospy.loginfo("Rotation is between 91 and 180 degrees")
			
			#Convert degrees to servo values
			conversion = (2.61 - (degree * 0.01191))

			#Initialize the servos
			group_variable_values[0] = conversion
			group_variable_values[1] = -1.60

		#Case for degrees that are out of bounds
		else:
			#Display information about movement
			rospy.loginfo("Error: Rotation is out of bounds")

		#Move arm to the desired position(degree)
		arm.set_joint_value_target(group_variable_values)
		plan = arm.plan()
		arm.go()
