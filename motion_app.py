import os, sys, time
import tb2i as TB

arm = TB.tb_arm()

def board_replace():
    arm.intial_pos()
    #Picking the board 
    arm.lift_percentage(75)
    arm.set_gripper("opened")
    arm.rotation_percentage(30)
    arm.upper_arm_bend(0)
    arm.lift_percentage(50)
    arm.set_gripper("close")
    arm.lift_percentage(75)

    #Placing the board
    arm.rotation_percentage(70)
    arm.lift_percentage(50)
    arm.set_gripper("opened")
    arm.reset_arm()

def build_animals(rotation):
    arm.intial_pos()
    arm.rotation_percentage(rotation)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.upper_arm_bend(40)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.upper_arm_bend(60)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.reset_arm()

 def guide():
    for num in range(1,3):
         arm.rotation_percentage(num*10)
    arm.reset_arm()

def press_enter():
    arm.intial_pos()

    #pick the screw
    
    arm.upper_arm_bend(0)
         
    # this may change according to placement of key board 
    arm.rotation_percentage(10)  
        
    #According to placment TWEAKKKKKKKKKKK
    arm.lift_percentage(70) 
    arm.lower_arm_bend(10)
    time.sleep(4)
    arm.reset_arm

def screw_motion():
    arm.intial_pos()
    
    #pick the screw
    
    arm.set_gripper("opened")
    arm.upper_arm_bend(0)
    
    # this may change according to placement of key board 
    arm.rotation_percentage(0)
    
    #According to placment TWEAKKKKKKKKKKK
    arm.lift_percentage(70)
    arm.lower_arm_bend(10)
    
    arm.set_gripper("close")
        
    #screw motion
    arm.intial_pos()
    arm.lift_percentage(10)
    time.sleep(1)
    for num in range(1,5):
    	arm.rotation_percentage(40)
    	arm.rotation_percentage(50)
    	arm.rotation_percentage(60)
	 
    # place the screw back
    arm.intial_pos()
    
    #Copied from above replace values
    arm.upper_arm_bend(0)
    
    # this may change according to placement of key board 
    arm.rotation_percentage(0)
    
    #According to placment TWEAKKKKKKKKKKK
    arm.lift_percentage(70)
    arm.lower_arm_bend(10)
    
    arm.set_gripper("opened")
    arm.reset_arm()
    
    
def wave():
    arm.intial_pos()
    arm.lower_arm_bend(0)
    arm.upper_arm_bend(100)
    for num in range(1,5):
        arm.rotation_percentage(40)
        time.sleep(1)
        arm.rotation_percentage(50)
        time.sleep(1)
        arm.rotation_percentage(60)
        time.sleep(1)
    arm.reset_arm()  

def bless():
    arm.intial_pos()
    for num in range(1,3):
        arm.lower_arm_bend(100)
	arm.upper_arm_bend(80)
	arm.upper_arm_bend(50)
    arm.rotation_percentage(100)
    for num in range(1,3):
	arm.lower_arm_bend(100)
        arm.upper_arm_bend(80)
        arm.upper_arm_bend(50)
    arm.rotation_percentage(0)
    for num in range(1,3):
        arm.lower_arm_bend(100)
        arm.upper_arm_bend(80)
        arm.upper_arm_bend(50)
    arm.reset_arm()
