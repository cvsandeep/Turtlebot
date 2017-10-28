from motion_app import *

def Task1():
    print "Task #1: Stage with Mobile Arm in the back wall. Arm works, robot moves, and it assembles something."
    #os.system(" roslaunch turtlebot2i_block_manipulation block_sorting_demo.launch ")
    Introduction()

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
    build_animals(30)
    build_animals(70)
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

