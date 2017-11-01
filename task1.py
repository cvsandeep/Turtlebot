import time, sys
import tb2i as TB

arm = TB.tb_arm()

def introduction():
    print "----------------Introduction----------------"
    arm.intial_pos()
    arm.lift_percentage(75)
    arm.lift_percentage(25)
    arm.lift_percentage(50)
    arm.lift_percentage(75)
    arm.lift_percentage(50)
    arm.reset_arm()
    screw_motion()
    build_robot()

def build_robot():
    print "----------------build_robot----------------"
    arm.intial_pos()
    arm.upper_arm_bend(0)
    arm.lift_percentage(35)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.lift_percentage(50)
    arm.rotation_percentage(40)	
    arm.lift_percentage(35)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.lift_percentage(50)
    arm.rotation_percentage(5)
    arm.lift_percentage(35)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.lift_percentage(50)
    arm.intial_pos()
    arm.reset_arm()	
	
def board_replace():
    print "----------------board_replace----------------"
    arm.intial_pos()
    #Picking the board 
    arm.lift_percentage(75)
    arm.set_gripper("opened")
    arm.rotation_percentage(10)
    arm.upper_arm_bend(0)
    arm.lift_percentage(50)
    arm.lift_percentage(45)
    arm.set_gripper("close")
    arm.lift_percentage(85) 
    #Placing the board
    arm.rotation_percentage(60)
    arm.lift_percentage(50)
    arm.set_gripper("opened")
    arm.intial_pos()
    arm.reset_arm()

def build_animals(rotation):
    print "----------------build_animals----------------"
    arm.intial_pos()
    arm.rotation_percentage(rotation)
    arm.set_gripper("opened")
    arm.set_gripper("close")

    arm.upper_arm_bend(40)
    arm.lift_percentage(40)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.lift_percentage(70)
    arm.set_gripper("opened")
    arm.set_gripper("close")
    arm.intial_pos()

def guide():
    print "----------------guide----------------"
    arm.intial_pos()
    arm.set_gripper("opened")
    arm.lower_arm_bend(20)
    arm.upper_arm_bend(0) 
    arm.rotation_percentage(0)
    arm.set_gripper("close")
    for num in range(0,20):
         arm.rotation_percentage(num*3)
    arm.set_gripper("opened")
    arm.reset_arm()

def press_enter():
    print "----------------press_enter----------------"
    arm.intial_pos()

    #pick the screw
    
    arm.upper_arm_bend(0)
         
    # this may change according to placement of key board 
    arm.rotation_percentage(90)  
        
    #According to placment TWEAKKKKKKKKKKK
    arm.lift_percentage(70) 
    arm.lower_arm_bend(70)
    arm.set_gripper("close")
    time.sleep(2)
    arm.set_gripper("opened")
    arm.lower_arm_bend(50)
    arm.lift_percentage(50)
    arm.intial_pos()
    arm.reset_arm()

def screw_motion():
    print "----------------screw_mootion----------------"
    arm.intial_pos()
    
    #pick the screw
    
    arm.set_gripper("opened")
    arm.upper_arm_bend(0)
    
    # this may change according to placement of key board 
    arm.rotation_percentage(100)
    
    #According to placment TWEAKKKKKKKKKKK
    arm.upper_arm_bend(3)
    arm.lift_percentage(70)
    arm.lower_arm_bend(69)
    arm.set_gripper("close")
    for num in range(0,13):
    	arm.lift_percentage(71 - (num*2))
    	arm.lower_arm_bend(70 - (num*2))
	


    #screw motion
    arm.intial_pos()
    arm.lift_percentage(45)
    arm.upper_arm_bend(0)
    time.sleep(1)
    for num in range(1,5):
    	arm.rotation_percentage(40+(num*3))
    for num in range(1,5):
    	arm.rotation_percentage(55-(num*3))
    
	 
    
    # place the screw back
    arm.lift_percentage(50)
    arm.lower_arm_bend(45)
    time.sleep(1)

    #Copied from above replace values
    arm.upper_arm_bend(0)
    
    # this may change according to placement of key board 
    arm.rotation_percentage(100)
    
    #According to placment TWEAKKKKKKKKKKK
    arm.upper_arm_bend(3)
    for num in range(1,8):
    	arm.lift_percentage(55 + (num*2))
    	arm.lower_arm_bend(57 + (num*2))
    
    arm.set_gripper("opened")
    arm.reset_arm()
    
    
def wave():
    print "----------------wave----------------"
    arm.intial_pos()
    arm.lower_arm_bend(20)
    arm.upper_arm_bend(90)
    for num in range(1,5):
        arm.rotation_percentage(40)
        arm.rotation_percentage(60)
    arm.reset_arm()  

def bless():
    print "---------------bless----------------"
    arm.intial_pos()
    for num in range(1,3):
        arm.lower_arm_bend(20)
	arm.upper_arm_bend(80)
	arm.upper_arm_bend(30)
    arm.rotation_percentage(100)
    for num in range(1,3):
	arm.lower_arm_bend(20)
        arm.upper_arm_bend(80)
        arm.upper_arm_bend(30)
    arm.rotation_percentage(0)
    for num in range(1,3):
        arm.lower_arm_bend(20)
        arm.upper_arm_bend(80)
        arm.upper_arm_bend(30)
    arm.reset_arm()

def Task1():
    print "Task #1: Stage with Mobile Arm in the back wall. Arm works, robot moves, and it assembles something."
    #os.system(" roslaunch turtlebot2i_block_manipulation block_sorting_demo.launch ")
    introduction()

def Task2():
    print "Task #2:Adding a screw to Adam"
    screw_motion()

def Task3():
    print "Task #3:Mobile Arm punching the key ENTER"
    press_enter()
def Task4():
    print "Task #4: Mobile Arm guides the robot like a father walks a little child."
    guide()
def Task5():
    print "Task #5: Mobile arm builds animals."
    build_animals(10)
    build_animals(60)
    arm.reset_arm()
def Task6():
    print "Task #6: Achievements of god in creation."
    
def Task7():
    print "Task #7:arm to be blessed"
    bless()

def Task8():
    print "Task #8: Animals stop to parade"
    
def Task9():
    print "Task #9:Mobile Arm building another similar robot"
    build_robot()
def Task10():
    print "Task #10:Mobile Arm removes an electronic controller board"
    board_replace()
def Task11():
    print "Task #11: Adam and Eve are dressed in ancient Chinese costumes by God's hand."
    board_replace()
def Task12():
    print "Task #12: Arrive again as God in empty lab."
    bot_move()
def Task13():
    print "Task #13: Waves as trying to do something "
    wave()
def Task14():
    print "Task #14:we do not know if God is happy or not."
    
def Task15():
    print "Task #15: Few animals return to Paradise from outside of Paradise."
    print "Task #15: Few animals return to Paradise from outside of Paradise."

def main(argv):
    print "Starting the Scene"
    for arg in sys.argv[1:]:
        globals()[arg]()

if __name__ == "__main__":
    main(sys.argv[1:])

