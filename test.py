import tb2i as TB

arm = TB.tb_arm

arm.display()
arm.position_creater(0,-1.6,-1.59,1.5,0)
arm.display()
time.sleep(1)

#Test the gripper mechanisim
arm.set_gripper("close")
time.sleep(1)
arm.set_gripper("opened")
time.sleep(1)

#Test the rotation mechanisim
arm.rotation_motion(0)
time.sleep(1)
arm.rotation_motion(50)
time.sleep(1)
arm.rotation_motion(100)
time.sleep(1)

#Test the reset mechanisim
arm.reset_arm()
time.sleep(1)
