from pymorse import Morse
import time
import getch


print("Use WASD to control the Ranger")

with Morse() as simu:

  motion = simu.segway.motion
  orientation=simu.segway.orientation
  wheels = simu.segway.wheels

  v = 0.0
  w = 0.0
  
  r = 0.0
  f = 0.0

  left = 0.0
  right = 0.0
  reset=False
  debug=False;

  while True:
      key = getch.getch()
      reset=False
      print((key.lower()))
      print('\x1b[a')
     
      if key.lower() == 'w':
          f -= 1
      elif key.lower() == "s":
          f += 1
      elif key.lower() == "o":
          f += 10.3
          
      elif key.lower() == "k":
          f -= 10.3
      elif key.lower() == "d":
          r -= 0.001
      elif key.lower() == "a":
          r +=0.001
      elif key.lower() == "j":
          reset=True
          f =0
          r=0
      elif key=="h":
           debug=(~debug)




      
      



      motion.publish({"Ux": f,"Uy":r,"Reset": reset,"Debug":debug})
     # wheels.publish({"v": v, "w": w})
      #motion.publish({"v": v, "w": w})
      

