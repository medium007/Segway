from pymorse import Morse
import time


print("Use WASD to control the Ranger")

with Morse() as simu:

  motion = simu.segway.motion
  orientation=simu.segway.orientation
  wheels = simu.segway.wheels

  v = 0.0
  w = 0.0
  
  t = 0.0
  f = 0.0

  left = 0.0
  right = 0.0
  reset=False
  debug=False;

  while True:
      key = input("WASD?")
      reset=False

     
      if key.lower() == "p":
          f += 0.05
      elif key.lower() == "l":
          f -= 0.05
      elif key.lower() == "o":
          f += 10.3
          
      elif key.lower() == "k":
          f -= 10.3
      elif key.lower() == "j":
          f =0
      elif key=="reset":
          reset=True
          f=0
      elif key=="debug":
           debug=!debug




      
      



      motion.publish({"F": f,"Reset": reset,"Debug":debug})
     # wheels.publish({"v": v, "w": w})
      #motion.publish({"v": v, "w": w})
      

