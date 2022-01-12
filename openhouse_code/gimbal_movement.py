from robomaster import robot
from time import sleep


def sub_data_handler(angle_info):
    pitch_angle, yaw_angle, pitch_ground_angle, yaw_ground_angle = angle_info
    print("gimbal angle: pitch_angle:{0}, yaw_angle:{1}, pitch_ground_angle:{2}, yaw_ground_angle:{3}".format(
        pitch_angle, yaw_angle, pitch_ground_angle, yaw_ground_angle))

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta",sn="3JKDH6U0019784")
    # ep_robot.initialize(conn_type="sta",sn="3JKDH2T0018UHQ")
    ep_gimbal = ep_robot.gimbal

    ep_gimbal.sub_angle(freq=5, callback=sub_data_handler)

    ep_gimbal.recenter(pitch_speed=100, yaw_speed=100).wait_for_completed()
    sleep(1)
    ep_gimbal.moveto(pitch=0,yaw=5,pitch_speed=50,yaw_speed=50).wait_for_completed()
    sleep(1)
    ep_gimbal.moveto(pitch=0,yaw=10,pitch_speed=50,yaw_speed=50).wait_for_completed()
    sleep(1)
    ep_gimbal.moveto(pitch=0,yaw=-5,pitch_speed=50,yaw_speed=50).wait_for_completed()
    sleep(1)
    ep_gimbal.moveto(pitch=0,yaw=-10,pitch_speed=50,yaw_speed=50).wait_for_completed()
    sleep(1)
    # ep_gimbal.recenter(pitch_speed=100, yaw_speed=100).wait_for_completed()
    ep_gimbal.unsub_angle()

    ep_robot.close()


