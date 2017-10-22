#Import libraries
from init_arm import *

#Wait for RVIZ to initialize
print "============ Waiting for RVIZ..."
rospy.sleep(10)
print "============ Starting tutorial "

#Clear target goal that was previously set
arm.clear_pose_targets()

#Get the create set of joint values
group_variable_values = group.get_current_joint_values()
print "============ Joint values: ", group_variable_values

#Reset position
group_variable_values[0] = 1.66
group_variable_values[1] = -1.61
group_variable_values[2] = -1.58
group_variable_values[3] = -0.48
group_variable_values[4] = 0.0
arm.set_joint_value_target(group_variable_values)

#Initialize the planned reset
plan_reset = arm.plan()

#Display the planned reset
print "============ Waiting while RVIZ displays plan reset..."
rospy.sleep(5)

#Run the planned reset
arm.go(wait=True)
