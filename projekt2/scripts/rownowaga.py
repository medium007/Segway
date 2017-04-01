#! /usr/bin/env python3
"""
Test client for the <projekt2> simulation environment.

This simple program shows how to control a robot from Python.

For real applications, you may want to rely on a full middleware,
like ROS (www.ros.org).
"""

import sys
import getch
import pygame

try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)

# initializing joystick
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
name = joystick.get_name()

with Morse() as simu:
    motion = simu.robot.motion
    pose = simu.robot.pose
    velocity = simu.robot.velocity

    v = 0.0
    w = 0.0
    alfa = 0.0;
    reset = False

    while True:

        pygame.event.get()
        if 'Microntek' in name:  # using different joystick to move seagway

            if joystick.get_button(0):  # moving forward
                alfa += 0.1
                print('w')
            if joystick.get_button(2):  # moving backward
                alfa -= 0.1
                print('s')
            if joystick.get_button(1):  # moving left
                w += 0.03
                print('a')
            if joystick.get_button(3):  # moving right
                w -= 0.03
                print('d')
            if not joystick.get_button(1) and not joystick.get_button(3):  # stop rotating while button not pressed
                w = 0
            if joystick.get_button(4):  # turning seagway controller off
                print('reset')
                reset = True
                v = 0
                w = 0
                alfa = 0
            if joystick.get_button(6):  # turning seagway controller on
                print('reset')
                reset = False
            if joystick.get_button(8):  # printing states of seagway
                print('\n\n\n')
                print ('alfa:', alfa)
                print('w:', w, '\n')
                print ('v:', v)
                print ('x1:', pose.get()['x'])                           #position
                print ('x2:', velocity.get()['linear_velocity'][0])      #linear velocity
                print ('x2:', pose.get()['pitch'])                       #inclination
                print ('x2:', velocity.get()['angular_velocity'][0])     #angular velocity
            if joystick.get_button(7):           #reseting inclination
                alfa = 0



        else:  # using controller we are supposed to use
            axis = joystick.get_axis(1)  # getting value in X Axis

            alfa = -1 * axis  # moving forward and backward
            axis = joystick.get_axis(0)  # getting value in Y Axis
            w = 0.5 * axis  # rotation left and right
            if joystick.get_button(2):  # turning seagway controller off
                print('reset')
                reset = True
                v = 0
                w = 0
                alfa = 0
            if joystick.get_button(1):  # turning seagway controller on
                print('reset')
                reset = False
            if joystick.get_button(3):  # printing states of seagway
                print('\n\n\n')
                print ('alfa:', alfa)
                print('w:', w, '\n')
                print ('v:', v)
                print ('x1:', pose.get()['x'])
                print ('x2:', velocity.get()['linear_velocity'][0])
                print ('x2:', pose.get()['pitch'])
                print ('x2:', velocity.get()['angular_velocity'][0])

        K = [0, -1, -3.7, -0.26]  # controller matrix
        if (not reset):
            v = -(
            alfa + K[0] * pose.get()['x'] + K[1] * velocity.get()['linear_velocity'][0] + K[2] * (pose.get()['pitch']) +
            K[3] * velocity.get()['angular_velocity'][0])  # calculating velocity based on controller

        if not 'Microntek' in name:
            if joystick.get_button(0):  # increasing speed while holding button
                v *= 2
                print('turbo')
        else:
            if joystick.get_button(5):  # increasing speed while holding button
                print('turbo')

        motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to seagway

