#Stage1 "The Creation of Adam", Mini-script:2"
from init_arm import *

intialize()
reset_arm()
position_creater(1.66, -1.61, -1.58, -0.48, 0.0)
set_gripper("opened")
position_creater(-0.04,0.44,-0.77,1.15,0)
position_creater(-0.04,1.39,-0.3,1.55,0.0)
set_gripper("neutral")
