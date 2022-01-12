import threading
import cv2
from time import sleep
from robomaster import robot
import keyboard

class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info

markers = []
info_target = [[0, '1'], [0,'2'], [0,'3'], [0,'4'], [0,'5']]


def takeFirst(elem):
    return elem[0]
def takeSecond(elem):
    return elem[1]

def on_detect_marker(marker_info):
    global x, y, w, h, info
   
    number = len(marker_info)
    # This Thread lock makes it so this will not continuously update
    value_lock.acquire()
    # print(number)
    # print("markers", markers)
    markers.clear()
    # print("markers",markers)
    for i in range(0, number):
        x, y, w, h, info = marker_info[i] # Info is Marker Num
        markers.append(MarkerInfo(x, y, w, h, info))
        # print(type(markers))
        # print("x",x)
        # print("y",y)
        # print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
        # print("markerinfo",marker_info)

        # ===================================================================
        if i+1 == 1:
            info_target[0][0] = marker_info[i][0]
            info_target[0][1] = marker_info[i][4]
        elif i+1 == 2:
            info_target[1][0] = marker_info[i][0]
            info_target[1][1] = marker_info[i][4]
        elif i+1 == 3:
            info_target[2][0] = marker_info[i][0]
            info_target[2][1] = marker_info[i][4]
        elif i+1 == 4:
            info_target[3][0] = marker_info[i][0]
            info_target[3][1] = marker_info[i][4]
        elif i+1 == 5:
            info_target[4][0] = marker_info[i][0]
            info_target[4][1] = marker_info[i][4]
        # ===================================================================

    # print()
    return markers
    value_lock.release()

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap") # Robot 1
    # ep_robot.initialize(conn_type="sta",sn="3JKDH7G001KHP5") # Robot 2
    # ep_robot.initialize(conn_type="sta",sn="3JKDH2T001R12J") # Robot 3
    print("RUNNING")
    ep_gimbal = ep_robot.gimbal
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_blaster = ep_robot.blaster
    #ep_gimbal.moveto(pitch=0,yaw=0,pitch_speed=50).wait_for_completed() # recentering
    # ep_gimbal.moveto(pitch=27.5,yaw=0,yaw_speed=100,pitch_speed=50).wait_for_completed() # recentering
    ep_gimbal.moveto(pitch=24,yaw=0,yaw_speed=100,pitch_speed=50).wait_for_completed() # recentering
    sleep(0.1)
    value_lock = threading.Lock()  
    
    print("PRESS SPACE")
    while True:
        if keyboard.is_pressed(" "):     
            print("Pressed")
            break     

    # 控制云台航向轴速度100度每秒，俯仰轴速度100度每秒回中
    # ep_gimbal.recenter(pitch_speed=200, yaw_speed=200).wait_for_completed()

    ep_camera.start_video_stream(display=False)
    sleep(0.1)
    result = ep_vision.sub_detect_info(name="marker", color="blue", callback=on_detect_marker)

    img = ep_camera.read_cv2_image(strategy="newest")
    # cv2.imwrite('C:/temp/OpenHouse2022/image.png',img)
    sleep(0.1)
    # Can comment out all these, just for show (except for targetSortedToXPos, targetSortedToNumber)
    # ===================================================================
    cv2.imshow("Markers", img)
    cv2.waitKey(1)
    targetSortedToXPos = sorted(info_target,key=takeFirst)
    targetSortedToNumber = sorted(info_target,key=takeSecond)
    print('Original:', info_target) 
    print("XPos: "+str(targetSortedToXPos))
    print("TarNumb: "+str(targetSortedToNumber)+"\n")
    # ===================================================================

    # Dictionary of Xpos to angle
    dict1={ 
        tuple(targetSortedToXPos[0][1]): -16,
        tuple(targetSortedToXPos[1][1]): -7.5 ,
        tuple(targetSortedToXPos[2][1]): 0,
        tuple(targetSortedToXPos[3][1]): 7.5,
        tuple(targetSortedToXPos[4][1]): 16

        # tuple(targetSortedToXPos[0][1]): -30,
        # tuple(targetSortedToXPos[1][1]): -15,
        # tuple(targetSortedToXPos[2][1]): 0,
        # tuple(targetSortedToXPos[3][1]): 15,
        # tuple(targetSortedToXPos[4][1]): 30 
    }


    # Loops thru all 5 elements to find the '1' target, then shoot from 1 to 5
    for i in range(len(targetSortedToXPos)):
        if targetSortedToXPos[i][1] == '1':
            ep_gimbal.moveto(pitch=26,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            #ep_gimbal.moveto(pitch=0,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            print("Going to 1!")
            print("i: "+str(i))
            print("Yaw: "+str(dict1[tuple(targetSortedToXPos[i][1])])+"\n")
            ep_blaster.fire(times=1)
            # sleep(0.1)
            sleep(0.05)
            break
    for i in range(len(targetSortedToXPos)):
        if targetSortedToXPos[i][1] == '2':
            ep_gimbal.moveto(pitch=26,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            #ep_gimbal.moveto(pitch=0,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            print("Going to 2!")
            print("i: "+str(i))
            print("Yaw: "+str(dict1[tuple(targetSortedToXPos[i][1])])+"\n")
            ep_blaster.fire(times=1)
            # sleep(0.1)
            sleep(0.05)
            break 
    for i in range(len(targetSortedToXPos)):
        if targetSortedToXPos[i][1] == '3':
            ep_gimbal.moveto(pitch=26,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            #ep_gimbal.moveto(pitch=0,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            print("Going to 3!")
            print("i: "+str(i))
            print("Yaw: "+str(dict1[tuple(targetSortedToXPos[i][1])])+"\n")
            ep_blaster.fire(times=1)
            # sleep(0.1)
            sleep(0.05)
            break
    for i in range(len(targetSortedToXPos)):
        if targetSortedToXPos[i][1] == '4':
            ep_gimbal.moveto(pitch=26,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            #ep_gimbal.moveto(pitch=0,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            print("Going to 4!")
            print("i: "+str(i))
            print("Yaw: "+str(dict1[tuple(targetSortedToXPos[i][1])])+"\n")
            ep_blaster.fire(times=1)
            # sleep(0.1)
            sleep(0.05)
            break
    for i in range(len(targetSortedToXPos)):
        if targetSortedToXPos[i][1] == '5':
            ep_gimbal.moveto(pitch=26  ,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            #ep_gimbal.moveto(pitch=0,yaw=dict1[tuple(targetSortedToXPos[i][1])],yaw_speed=100).wait_for_completed()
            print("Going to 5!")
            print("i: "+str(i))
            print("Yaw: "+str(dict1[tuple(targetSortedToXPos[i][1])])+"\n")
            ep_blaster.fire(times=1)
            # sleep(0.1)
            sleep(0.05)
            break




ep_gimbal.moveto(pitch=0,yaw=0,yaw_speed=100  ,pitch_speed=50).wait_for_completed() # recentering
result = ep_vision.unsub_detect_info  (name=" marker")
cv2.destroyAllWindows()
ep_camera.stop_video_stream()

ep_robot.close()
