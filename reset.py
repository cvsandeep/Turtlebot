#Import libraries
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

#Initialize moveit_commander and rospy
print "============ Starting tutorial setup"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

#Create the robot commander object
robot = moveit_commander.RobotCommander()

#Create the plan screen interface object
scene = moveit_commander.PlanningSceneInterface()

#Initialize the group
group = moveit_commander.MoveGroupCommander("arm")

#Create the display trajectory publisher
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

#Wait for RVIZ to initialize
print "============ Waiting for RVIZ..."
rospy.sleep(10)
print "============ Starting tutorial "

#Display basic turtlebot2i information
print "============ Reference frame: %s" % group.get_planning_frame()
print "============ Reference frame: %s" % group.get_end_effector_link()
print "============ Robot Groups:"
print robot.get_group_names()
print "============ Printing robot state"
print robot.get_current_state()
print "============"

#Clear target goal that was previously set
group.clear_pose_targets()

#Get the create set of joint values
group_variable_values = group.get_current_joint_values()
print "============ Joint values: ", group_variable_values

#Reset position
group_variable_values[0] = 1.66
group_variable_values[1] = -1.61
group_variable_values[2] = -1.58
group_variable_values[3] = -0.48
group_variable_values[4] = 0.0
group.set_joint_value_target(group_variable_values)

#Initialize the planned reset
plan_reset = group.plan()

#Display the planned reset
print "============ Waiting while RVIZ displays plan reset..."
rospy.sleep(5)

#Run the planned reset
group.go(wait=True)
