

import sys
import time
from PIL import Image
import numpy as np
import os
import math
import cost_graph
import astar




def v_calc(K, alfa,X):                                                                               # calculating linear velocity based on controller matrix and required pitch angle
    v = -(alfa
          + K[0] *X[0]     # pose.get()['x']
          + K[1] * X[1]    # velocity.get()['linear_velocity'][0]
          + K[2] * X[2]    # (pose.get()['pitch'])
          + K[3] * X[3])   #velocity.get()['angular_velocity'][0])
    return v


def save_route():                                       # saving your route to the new .png file
    global map1
    map1.save("output2.png")


def controll(motion,pose,velocity,pose_main):

    # initializing global variables
    global controller_enable
    global v
    global w
    global alfa
    global K

    doAStar = False
    next_target=True
    target_idx=0

    while True:

        if(doAStar):
                if next_target:
                    (x2,y2)=resultMap[target_idx]
                    y2=y2-35
                    x2 *= 96 / gs
                    y2 *= 96 / gs

                    target_idx+=1
                    next_target=False
                    print("cel:", x2, y2)

                # get information from segway sensors
                pitch = pose.get()['pitch']
                yaw = pose.get()['yaw']
                X = [pose.get()['x'], velocity.get()['linear_velocity'][0], (pose.get()['pitch']),
                     velocity.get()['angular_velocity'][0]]
                y = pose.get()['y']

                # calculate angle to next target
                angle_to_target=math.atan2(y2-y,x2-X[0])
                angle_to_target=angle_to_target-yaw

                # calculate distance to next target
                dist = math.hypot(x2 - X[0], y2 - y)

                # check distance to target
                if dist>0 and math.fabs(angle_to_target)<0.2:
                    alfa=0.3
                elif dist<0 and math.fabs(angle_to_target)<0.2 :
                    alfa=-0.3
                elif math.fabs(dist)<2:
                    if target_idx==len(resultMap)-1:
                        doAStar = False
                        target_idx=0
                    else:
                        next_target=True
                else:
                    alfa=0

                # rotate to target direction
                if angle_to_target>0.1:
                    w=-1
                elif angle_to_target<-0.1:
                    w=1
                else:
                    w=-angle_to_target/10

                v = v_calc(K, alfa,X)       # calculating velocity                                            # calculating velocity

                if controller_enable and math.fabs(pitch) < math.pi / 3:

                    # calculating wheels position based on center of mass, pitch and yaw
                    d = l * math.sin(pitch)
                    x_left = X[0] - d * math.cos(yaw) - axis_width / 2 * math.sin(yaw)
                    y_left = y - d * math.sin(yaw) + axis_width / 2 * math.cos(yaw)
                    x_right = X[0] - d * math.cos(yaw) + axis_width / 2 * math.sin(yaw)
                    y_right = y - d * math.sin(yaw) - axis_width / 2 * math.cos(yaw)

                    # calculating position in friction matrix basen on wheels position
                    x_left = int(x_left / (96/np.size(mi, 0)))
                    x_right = int(x_right / (96/np.size(mi, 0)))
                    y_right = -int(y_right / (96 / np.size(mi, 1)))
                    y_left = -int(y_left / (96 / np.size(mi, 1)))

                    # creating new map with route colored on black
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            map1.putpixel((x_left+dx, y_left+dy), (0, 0, 0))
                            map1.putpixel((x_right+dx, y_right+dy), (0, 0, 0))

                    # calculating new omega considering friction
                    # uncomment if you want to have a friction force on the chase segway
                    # w = w-0.02*(mi[x_left][y_left]-mi[x_right][y_right])*v

                    motion.publish({"v": v, "w": w})                # sending information about velocity and rotation to segway

                elif controller_enable:

                    save_route()  # save route to the png file
                    controller_enable = False  # turn off controller
                    motion.publish(
                        {"v": 0, "w": 0})  # sending information about velocity and rotation to segway to stop moving


        else:

            # get information from chase segway sensors
            X = [pose.get()['x'],
                 velocity.get()['linear_velocity'][0],
                 pose.get()['pitch'],
                 velocity.get()['angular_velocity'][0]]
            y = pose.get()['y']

            # get information from main segway sensors
            x2 = pose_main.get()['x']
            y2 = pose_main.get()['y']

            xp = int(X[0] / 96 * gs)
            yp = int((96+y)/ 96 * 35)

            xk = int(x2/ 96 * 35)
            yk = int((96+y2) / 96* 35)
            print("mapa dla:",xp, yp, xk, yk)
            resultMap = astar.a_star(graph, (xp, yp), (xk, yk))
            print(resultMap)


            doAStar = True
            next_target=True



try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)

try:
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                        # getting friction map directory to make friction matrix
    map1 = Image.open(dir_path+"/data/segwaysim/mi.png")

except:
    print("can't open the image")
    sys.exit(1)

x, y = map1.size                                                                                  # getting map size

mi = np.zeros((x,y))                                                                              # initializing friction matrix

gs = 35                                                                                           # grid Size

resultMap = []
costs = cost_graph.makeGraph()
graph = astar.SquareGrid(gs, gs)
graph.weights = {(x, y): costs[x][y] for x in range(gs) for y in range(gs)}

for i in range(0, y):
    for p in range(0, x):

        r, g, b = map1.getpixel((p,i))
        if (r == 185 and g == 122 and b == 87):
            mi[p, i] = 5                                                                          # sand friction = 5
        if (r == 34 and g == 177 and b == 76):
            mi[p, i] = 2                                                                          # grass friction = 2
        if (r == 127 and g == 127 and b == 127):
            mi[p, i] = 1                                                                          # sidewalk friction = 1


v = 0.0                                                                                           # linear speed
w = 0.0                                                                                           # rotation speed
alfa = 0.0                                                                                        # required pitch angle
K = [0, -1, -4, -0.26]                                                                            # controller matrix
controller_enable=True;
l = 1.8
axis_width = 1.17

for i in range(100):
    print(i)
    try:                                        # trying to connect with Morse

        with Morse() as simu:
            motion = simu.chase.motion          # connection to motion controller
            pose = simu.chase.pose              # connection to pose sensor
            velocity = simu.chase.velocity      # connection to velocity sensor

            pose_main = simu.robot.pose

            print('Connected')
                                  # using different joystick to move segway
            controll(motion,pose,velocity,pose_main)


    except:                     # couldn't connect to Morse
        time.sleep(1)
        continue
