from robomaster import robot
from time import sleep

pitch_val = 27.5
yaw_val = 30
count=0

def gimbal_movement():
    global count
    if count==0:
        ep_gimbal.moveto(pitch=pitch_val, yaw=20).wait_for_completed()
    elif count==1:
        ep_gimbal.moveto(pitch=pitch_val, yaw=17.50).wait_for_completed()
    elif count==2:
        ep_gimbal.moveto(pitch=pitch_val, yaw=15).wait_for_completed()

    # else:
    #     ep_gimbal.moveto(pitch=pitch_val, yaw=-yaw_val).wait_for_completed()

def gimbal_shoot():
    ep_blaster.fire(times=1)
    # sleep(0.5)
    # ep_blaster.fire(fire_type=blaster.INFRARED_FIRE)
    # sleep(0.5)


# gimbal_movement()

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta",sn="3JKDH6U0019784")
    ep_gimbal = ep_robot.gimbal
    ep_blaster = ep_robot.blaster


while count < 3:
    gimbal_movement()
    gimbal_shoot()
    count+=1

ep_gimbal.recenter(pitch_speed=100, yaw_speed=100).wait_for_completed()
ep_robot.close()
