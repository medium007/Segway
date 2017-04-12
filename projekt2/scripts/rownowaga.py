

import sys
import pygame

try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)


def v_calc(K,alfa):   # calculating linear velocity based on controller matrix and required pitch angle
    v = -(alfa
          + K[0] * pose.get()['x']
          + K[1] * velocity.get()['linear_velocity'][0]
          + K[2] * (pose.get()['pitch'])
          + K[3] * velocity.get()['angular_velocity'][0])
    return v


# initializing joystick
pygame.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()
name=js.get_name()

with Morse() as simu:
    motion = simu.robot.motion   # connection to motion controller
    pose = simu.robot.pose       # connection to pose sensor
    velocity = simu.robot.velocity     # connection to velocity sensor

    v = 0.0      # linear speed
    w = 0.0      # rotation speed
    alfa = 0.0   # required pitch angle
    controller_enable = True  # controller enable
    K = [0, -1, -3.7, -0.26]  # controller matrix

    # using different joystick to move segway
    if 'Microntek' in name:

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

            if not js.get_button(1) and not js.get_button(3): # stop rotation
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
                print ('alfa:', alfa)
                print('w:', w)
                print ('v:', v,'\n')
                print ('x1:', pose.get()['x'])                           #position
                print ('x2:', velocity.get()['linear_velocity'][0])      #linear velocity
                print ('x3:', pose.get()['pitch'])                       #inclination
                print ('x4:', velocity.get()['angular_velocity'][0])     #angular velocity

            if js.get_button(7):  # stopping segway
                alfa = 0
                w = 0
                print('stop')

            if controller_enable:
                v = v_calc(K,alfa)  # calculating velocity
            else:
                v = 0

            if not 'Microntek' in name:
                if js.get_button(0):
                    v *= 2
                    print('turbo')
            else:
                if js.get_button(5):
                    v *= 2
                    print('turbo')

            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway


    else:                        # using controller we are supposed to use
        while True:

            alfa = -1* js.get_axis(1)                # moving forward and backward
            w = 0.5* joystick.get_axis(0)            # rotation left and right

            if controller_enable and js.get_button(2):   # turning segway controller off
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

            if controller_enable:  # calculating velocity
                v = v_calc(K,alfa)
            else:
                v = 0

            if not 'Microntek' in name:
                if js.get_button(0):
                    v *= 2
                    print('turbo')
            else:
                if js.get_button(5):
                    v *= 2
                    print('turbo')

            motion.publish({"v": v, "w": w})  # sending information about velocity and rotation to segway


