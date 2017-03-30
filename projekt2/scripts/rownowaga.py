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



pygame.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()



with Morse() as simu:

  motion = simu.robot.motion
  pose = simu.robot.pose
  velocity=simu.robot.velocity


  v = 0.0
  w = 0.0
  alfa=0.0;
  reset=False

  while True:
      

              pygame.event.get()
              if js.get_button(0):
                  alfa+=0.1
                  print('w')
              if js.get_button(2):
                  alfa-=0.1
                  print('s')
              if js.get_button(1):
                  w+=0.01
                  print('a')
              if js.get_button(3):
                  w-=0.01
                  print('d')
              if js.get_button(4):
                  print('reset')
                  reset=True
                  v=0
                  w=0
                  alfa=0
              if js.get_button(6):
                  print('reset')
                  reset=False
              if js.get_button(5):
                  print('\n\n\n')
                  print ('alfa:',alfa)
                  print('w:',w,'\n')
                  print ('v:',v)
                  print ('x1:',pose.get()['x'])
                  print ('x2:',velocity.get()['linear_velocity'][0])
                  print ('x2:',pose.get()['pitch'])
                  print ('x2:',velocity.get()['angular_velocity'][0])
              if js.get_button(7):
                  alfa=0
                  w=0
                  print('stop')

        
              K=[0,-1,-2.7,-0.26]
              if (not reset):
                   v=-(alfa+K[0]*pose.get()['x']+K[1]*velocity.get()['linear_velocity'][0]+K[2]*(pose.get()['pitch'])+K[3]*velocity.get()['angular_velocity'][0])

      
#      print(pygame.key.get_pressed()[pygame.K_UP])
#      if( pygame.key.get_pressed()[pygame.K_UP] != 0 ):
#          alfa+=0.1
#          
#      if( pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
#          alfa-=0.1
#      if( pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
#          w-=0.1
#      if( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
#          w+=0.1
#      key = getch.getch()
#
#      if key.lower() == "w":
#          v += 0.1
#      elif key.lower() == "s":
#          v -= 0.1
#      elif key.lower() == "a":
#          w += 0.1
#      elif key.lower() == "d":
#          w -= 0.1
#      elif key.lower() == "j":
#          w =0
#          v=0
#          alfa=0
      

      
#      v=-(-3*velocity.get()['linear_velocity'][0]+ alfa-5.47*pose.get()['pitch']-0.56*velocity.get()['angular_velocity'][0])
      
#      v= 20*(pose.get()['pitch']-alfa)

     

      # here, we call 'get' on the pose sensor: this is a blocking
      # call. Check pymorse documentation for alternatives, including
      # asynchronous stream subscription.
#      print("The robot is currently at: %s" % pose.get())

#     motion.publish({"v": v, "w": velocity.get()['angular_velocity'][2]})     
     
              motion.publish({"v": v, "w": w})

