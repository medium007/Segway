
import sys
import getch

try:
    from pymorse import Morse
except ImportError:
    print("you need first to install pymorse, the Python bindings for MORSE!")
    sys.exit(1)

print("Use WASD to control the robot")

with Morse() as simu:

  motion = simu.robot.motion
  pose = simu.robot.pose
  przechylenie=simu.robot.przechylenie
  velocity=simu.robot.velocity


  v = 0.0
  w = 0.0
  alfa=0;

  while True:
      key = getch.getch()

      if key.lower() == "w":
          alfa += 1
      elif key.lower() == "s":
          alfa -= 1
      elif key.lower() == "a":
          w += 0.1
      elif key.lower() == "d":
          w -= 0.1
      elif key.lower() == "j":
          w =0
          v=0
          alfa=0
      
      
#      v= 10*(pose.get()['pitch']-alfa)

     

      # here, we call 'get' on the pose sensor: this is a blocking
      # call. Check pymorse documentation for alternatives, including
      # asynchronous stream subscription.
#      print("The robot is currently at: %s" % pose.get())

  
      przechylenie.publish({"force": [0,0,0],"torque":[alfa,0,0]})

      
      motion.publish({"w":w,"v": velocity.get()['linear_velocity'][0]})
