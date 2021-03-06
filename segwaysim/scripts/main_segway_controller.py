import sys
import pygame
import time
import math
import ctypes as ct
from ctypes.util import find_library
from PIL import Image
import numpy as np
import os



def v_calc(K, alfa):  # calculating linear velocity based on controller matrix and required pitch angle
    v = -(alfa
          + K[0] * pose.get()['x']
          + K[1] * velocity.get()['linear_velocity'][0]
          + K[2] * (pose.get()['pitch'])
          + K[3] * velocity.get()['angular_velocity'][0])
    return v


def v_calc(K, alfa, X):  # calculating linear velocity based on controller matrix and required pitch angle
    v = -(alfa
          + K[0] * X[0]  # pose.get()['x']
          + K[1] * X[1]  # velocity.get()['linear_velocity'][0]
          + K[2] * X[2]  # (pose.get()['pitch'])
          + K[3] * X[3])  # velocity.get()['angular_velocity'][0])
    return v


def save_route():  # saving your route to the new .png file
    global map1
    map1.save("output_main.png")


def joy1_control(motion, pose, velocity):

    # initializing global variables
    global controller_enable
    global joystick_exists
    global v
    global w
    global alfa
    global K

    while True:

        pygame.event.get()  # get event from joystick

        # get information from segway sensors
        pitch = pose.get()['pitch']
        yaw = pose.get()['yaw']
        X = [pose.get()['x'],
             velocity.get()['linear_velocity'][0],
             pose.get()['pitch'],
             velocity.get()['angular_velocity'][0]]
        y = pose.get()['y']

        #   event handling
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
            print('alfa:', alfa)
            print('w:', w)
            print('v:', v, '\n')
            print('x1:', X[0])  # position
            print('x2:', velocity.get()['linear_velocity'][0])  # linear velocity
            print('x3:', pitch)  # inclination
            print('x4:', velocity.get()['angular_velocity'][0])  # angular velocity

        if js.get_button(7):  # stopping segway
            alfa = 0
            w = 0
            print('stop')

        v = v_calc(K, alfa, X)  # calculating velocity

        if controller_enable and math.fabs(pitch) < math.pi / 3:

            # calculating wheels position based on center of mass, pitch and yaw
            d = l * math.sin(pitch)
            x_left = X[0] - d * math.cos(yaw) - axis_width / 2 * math.sin(yaw)
            y_left = y - d * math.sin(yaw) + axis_width / 2 * math.cos(yaw)
            x_right = X[0] - d * math.cos(yaw) + axis_width / 2 * math.sin(yaw)
            y_right = y - d * math.sin(yaw) - axis_width / 2 * math.cos(yaw)

            # calculating position in friction matrix basen on wheels position
            x_left = int(x_left / (96 / np.size(mi, 0)))
            x_right = int(x_right / (96 / np.size(mi, 0)))
            y_right = -int(y_right / (96 / np.size(mi, 1)))
            y_left = -int(y_left / (96 / np.size(mi, 1)))

            # creating new map with route colored on black
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    map1.putpixel((x_left + dx, y_left + dy), (0, 0, 0))
                    map1.putpixel((x_right + dx, y_right + dy), (0, 0, 0))

            w -= 0.02 * (mi[x_left][y_left] - mi[x_right][y_right]) * v  # calculating new omega considering friction

            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway

            save_route()  # save route to the png file

        elif controller_enable:
            save_route()    # save route to the png file
            controller_enable = False   # turn off controller
            motion.publish({"v": 0, "w": 0})  # sending information about velocity and rotation to segway to stop moving


def joy2_control(motion, pose, velocity):

    # initializing global variables
    global controller_enable
    global joystick_exists
    global v
    global w
    global alfa
    global K

    while True:

        # joystick handling
        pygame.event.get()
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
            print('alfa:', alfa)
            print('w:', w)
            print('v:', v, '\n')
            print('x1:', pose.get()['x'])
            print('x2:', velocity.get()['linear_velocity'][0])
            print('x3:', pose.get()['pitch'])
            print('x4:', velocity.get()['angular_velocity'][0])

        # get information from segway sensors
        pitch = pose.get()['pitch']
        yaw = pose.get()['yaw']
        X = [pose.get()['x'], velocity.get()['linear_velocity'][0], (pose.get()['pitch']),
             velocity.get()['angular_velocity'][0]]
        y = pose.get()['y']

        v = v_calc(K, alfa, X)  # calculating velocity


        if controller_enable and math.fabs(pitch) < math.pi / 3:

            # calculating wheels position based on center of mass, pitch and yaw
            d = l * math.sin(pitch)
            x_left = X[0] - d * math.cos(yaw) - axis_width / 2 * math.sin(yaw)
            y_left = y - d * math.sin(yaw) + axis_width / 2 * math.cos(yaw)
            x_right = X[0] - d * math.cos(yaw) + axis_width / 2 * math.sin(yaw)
            y_right = y - d * math.sin(yaw) - axis_width / 2 * math.cos(yaw)

            # calculating position in friction matrix basen on wheels position
            x_left = int(x_left / (96 / np.size(mi, 0)))
            x_right = int(x_right / (96 / np.size(mi, 0)))
            y_right = -int(y_right / (96 / np.size(mi, 1)))
            y_left = -int(y_left / (96 / np.size(mi, 1)))

            # creating new map with route colored on black
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    map1.putpixel((x_left + dx, y_left + dy), (0, 0, 0))
                    map1.putpixel((x_right + dx, y_right + dy), (0, 0, 0))

            w-=0.02 * (mi[x_left][y_left] - mi[x_right][y_right]) * v  # calculating new omega considering friction

            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway

            save_route()  # save route to the png file

        elif controller_enable:

            save_route()  # save route to the png file
            controller_enable = False  # turn off controller
            motion.publish({"v": 0, "w": 0})  # sending information about velocity and rotation to segway to stop moving


def alternative_control(motion, pose, velocity):

    # initializing global variables
    global v
    global w
    global alfa
    global K
    global controller_enable
    global l
    global axis_width

    while True:
        x11.XQueryKeymap(display, keyboard)  # puting keys state to keyboard matrix
        keys = bin(keyboard[:][13])[2:].zfill(8) +\
               bin(keyboard[:][14])[2:].zfill(8) + \
               bin(keyboard[:][8])[2:].zfill(8)  # checking if any key is pressed

        if keys[0] == '1':  # UP
            alfa += 0.05
        if keys[11] == '1': # DOWN
            alfa -= 0.05
        if keys[14] == '1': # LEFT
            w -= 0.05
        if keys[13] == '1': # RIGHT
            w += 0.05
        if keys[14] == '0' and keys[13] == '0':
            w = 0
        if keys[22] == '1':
            alfa = 0
        if keys[3] == '1' and keys[6] == '1':  # alt+ctr
            save_route()

        # get information from segway sensors
        pitch = pose.get()['pitch']
        yaw = pose.get()['yaw']
        X = [pose.get()['x'], velocity.get()['linear_velocity'][0], (pose.get()['pitch']),
             velocity.get()['angular_velocity'][0]]
        y = pose.get()['y']

        v = v_calc(K, alfa, X)  # calculating velocity

        if controller_enable and math.fabs(pitch) < math.pi / 3:

            # calculating wheels position based on center of mass, pitch and yaw
            d = l * math.sin(pitch)
            x_left = X[0] - d * math.cos(yaw) - axis_width / 2 * math.sin(yaw)
            y_left = y - d * math.sin(yaw) + axis_width / 2 * math.cos(yaw)
            x_right = X[0] - d * math.cos(yaw) + axis_width / 2 * math.sin(yaw)
            y_right = y - d * math.sin(yaw) - axis_width / 2 * math.cos(yaw)

            # calculating position in friction matrix basen on wheels position
            x_left = int(x_left / (96 / np.size(mi, 0)))
            x_right = int(x_right / (96 / np.size(mi, 0)))
            y_right = -int(y_right / (96 / np.size(mi, 1)))
            y_left = -int(y_left / (96 / np.size(mi, 1)))

            # creating new map with route colored on black
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    map1.putpixel((x_left + dx, y_left + dy), (0, 0, 0))
                    map1.putpixel((x_right + dx, y_right + dy), (0, 0, 0))

            w = w - 0.02 * (mi[x_left][y_left] - mi[x_right][y_right]) * v  # calculating new omega considering friction

            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway

            save_route()  # save route to the png file

        elif controller_enable:

            save_route()    # save route to the png file
            controller_enable = False   # turn off controller
            motion.publish({"v": 0, "w": 0})  # sending information about velocity and rotation to segway to stop moving






keyboard = (ct.c_char * 32)()  # matrix containing all keys
x11 = ct.cdll.LoadLibrary(find_library("X11"))  # need to use keyboard
display = x11.XOpenDisplay(None)

try:
    from pymorse import Morse  # try to import morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)

try:
    dir_path = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))  # getting friction map directory to make friction matrix
    map1 = Image.open(dir_path + "/data/segwaysim/mi.png")

except:
    print("can't open the image")
    sys.exit(1)

x, y = map1.size  # getting map size

mi = np.zeros((x, y))  # initializing friction matrix

for i in range(0, y):
    for p in range(0, x):

        r, g, b = map1.getpixel((p, i))
        if (r == 185 and g == 122 and b == 87):
            mi[p, i] = 5  # sand friction = 5
        if (r == 34 and g == 177 and b == 76):
            mi[p, i] = 2  # grass friction = 2
        if (r == 127 and g == 127 and b == 127):
            mi[p, i] = 1  # sidewalk friction = 1

controller_enable = True  # controller enable
joystick_exists = False
v = 0.0  # linear speed
w = 0.0  # rotation speed
alfa = 0.0  # required pitch angle
K = [0, -1, -4, -0.26]  # controller matrix

l = 1.8  # distance to the center of mass
axis_width = 1.17  # distance between wheels


try:  # initializing joystick
    pygame.init()
    pygame.joystick.init()

    js = pygame.joystick.Joystick(0)
    js.init()
    name = js.get_name()
    joystick_exists = True

except:
    joystick_exists = False




for i in range(100):
    print("Try to connect: ",i)
    try:  # trying to connect with Morse

        with Morse() as simu:
            motion = simu.robot.motion  # connection to motion controller
            pose = simu.robot.pose  # connection to pose sensor
            velocity = simu.robot.velocity  # connection to velocity sensor
            print('Connected')

            if joystick_exists:

                if 'Microntek' in name:  # using different joystick to move segway
                    joy1_control(motion, pose, velocity)

                elif 'USB Game Controllers' in name:  # using controller we are supposed to use
                    joy2_control(motion, pose, velocity)

                else:   # using alternate controller if no supported controller is connected
                    alternative_control(motion, pose, velocity)
            else:   # using alternate controller if no controller is connected
                alternative_control(motion, pose, velocity)

    except:  # couldn't connect to Morse
        time.sleep(1)
        continue


