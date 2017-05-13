

import sys
import pygame
import time
import math
import ctypes as ct
from ctypes.util import find_library


keyboard = (ct.c_char * 32)()
x11 = ct.cdll.LoadLibrary(find_library("X11"))
display = x11.XOpenDisplay(None)

try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)


controller_enable = True  # controller enable
joystick_exists = False
v = 0.0  # linear speed
w = 0.0  # rotation speed
alfa = 0.0  # required pitch angle
K = [0, -1, -3.7, -0.26]  # controller matrix

l = 1.8
axis_width = 1.17




def v_calc(K,alfa):   # calculating linear velocity based on controller matrix and required pitch angle
    v = -(alfa
          + K[0] * pose.get()['x']
          + K[1] * velocity.get()['linear_velocity'][0]
          + K[2] * (pose.get()['pitch'])
          + K[3] * velocity.get()['angular_velocity'][0])
    return v

def joy1_control(motion,pose,velocity):
    global controller_enable
    global joystick_exists
    global v
    global w
    global alfa
    global K
    global d

    while True:

        pygame.event.get()

        if js.get_button(0):  # moving forward
            alfa += 0.1
            print('w')

        if js.get_button(2):  # moving backward
            alfa -= 0.1
            print('s')

        if js.get_button(1):  # moving left
            w += 0.03
            print('a')

        if js.get_button(3):  # moving right
            w -= 0.03
            print('d')

        if not js.get_button(1) and not js.get_button(3):  # stop rotation
            w = 0
        print('joy1')
        if controller_enable and js.get_button(4):  # turning segway controller off
            print('controller off')
            controller_enable = False
            w = 0
            alfa = 0

        if not controller_enable and js.get_button(6):  # turning segway controller on
            print('controller on')
            controller_enable = True

        if js.get_button(8):  # printing states of segway
            print('\n\n\n')
            print ('alfa:', alfa)
            print('w:', w)
            print ('v:', v, '\n')
            print ('x1:', pose.get()['x'])  # position
            print ('x2:', velocity.get()['linear_velocity'][0])  # linear velocity
            print ('x3:', pose.get()['pitch'])  # inclination
            print ('x4:', velocity.get()['angular_velocity'][0])  # angular velocity

        if js.get_button(7):  # stopping segway
            alfa = 0
            w = 0
            print('stop')


        v = v_calc(K, alfa)  # calculating velocity


        if js.get_button(5):
                v *= 2
                print('turbo')

        if controller_enable and math.fabs(pose.get()['pitch'])<math.pi/3 :
            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway
        else:
            controller_enable=False
            motion.publish({"v": 0, "w": 0})  # sending information about velocity and rotation to segway




def joy2_control(motion,pose,velocity):
    global controller_enable
    global joystick_exists
    global v
    global w
    global alfa
    global K

    while True:

        alfa = -1 * js.get_axis(1)  # moving forward and backward
        w = 0.5 * js.get_axis(0)  # rotation left and right

        if controller_enable and js.get_button(2):  # turning segway controller off
            print('controller off')
            controller_enable = False
            v = 0

        if not controller_enable and js.get_button(1):  # turning segway controller on
            print('controller on')
            controller_enable = True

        if js.get_button(3):  # printing states of segway
            print('\n\n\n')
            print ('alfa:', alfa)
            print('w:', w)
            print ('v:', v, '\n')
            print ('x1:', pose.get()['x'])
            print ('x2:', velocity.get()['linear_velocity'][0])
            print ('x3:', pose.get()['pitch'])
            print ('x4:', velocity.get()['angular_velocity'][0])


        v = v_calc(K, alfa)     # calculating velocity

        if js.get_button(0):
                v *= 2
                print('turbo')

        if controller_enable and math.fabs(pose.get()['pitch'])<math.pi/3 :
            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway
        else:
            controller_enable=False
            motion.publish({"v": 0, "w": 0})  # sending information about velocity and rotation to segway


def alternative_control(motion,pose,velocity):
    global v
    global w
    global alfa
    global K
    global controller_enable
    global l
    global axis_width

    while True:
        x11.XQueryKeymap(display, keyboard)
        keys = bin(keyboard[:][13])[2:].zfill(8)+bin(keyboard[:][14])[2:].zfill(8)+bin(keyboard[:][8])[2:].zfill(8)
        if keys[0] == '1':
            alfa += 0.05
        if keys[11] == '1':
            alfa -= 0.05
        if keys[14] == '1':
            w -= 0.05
        if keys[13] == '1':
            w += 0.05
        if keys[14] == '0' and keys[13] == '0':
            w = 0
        if keys[22]=='1':
            alfa=0
        v = v_calc(K, alfa)

        if controller_enable and math.fabs(pose.get()['pitch'])<math.pi/3 :
            print('x: ',pose.get()['x'],'y: ',pose.get()['y'])
            d = l*math.sin(pose.get()['pitch'])
            x_left = pose.get()['x'] - d*math.cos(pose.get()['yaw']) - axis_width/2*math.sin(pose.get()['yaw'])
            y_left = pose.get()['y'] - d * math.sin(pose.get()['yaw']) + axis_width / 2 * math.cos(pose.get()['yaw'])
            x_right = pose.get()['x'] - d * math.cos(pose.get()['yaw']) + axis_width / 2 * math.sin(pose.get()['yaw'])
            y_right = pose.get()['y'] - d * math.sin(pose.get()['yaw']) - axis_width / 2 * math.cos(pose.get()['yaw'])

            print('left', x_left, ', ', y_left)
            print('right', x_right, ', ', y_right)


            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway
        else:
            controller_enable=False
            motion.publish({"v": 0, "w": 0})  # sending information about velocity and rotation to segway



try:  # initializing joystick
    pygame.init()
    pygame.joystick.init()

    js = pygame.joystick.Joystick(0)
    js.init()
    name = js.get_name()
    joystick_exists=True


except:
    joystick_exists=False



for i in range(100):
    print(i)
    try: # connect with Morse



        with Morse() as simu:
            motion = simu.robot.motion  # connection to motion controller
            pose = simu.robot.pose  # connection to pose sensor
            velocity = simu.robot.velocity  # connection to velocity sensor
            print('Connected')


            if joystick_exists:

                if 'Microntek' in name:                              # using different joystick to move segway
                    joy1_control(motion,pose,velocity)
                elif 'USB Game Controllers' in name :                                                # using controller we are supposed to use
                    joy2_control(motion, pose, velocity)
                else:
                    alternative_control(motion, pose, velocity)
            else:
                alternative_control(motion,pose,velocity)


    except:  # couldn't connect to Morse
        time.sleep(1)
        continue
