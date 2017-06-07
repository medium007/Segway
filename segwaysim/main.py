import subprocess
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))                          # getting main.py directory


cmd = ['morse','import', '-f', dir_path,'segwaysim']                            # creating morse project
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
process.wait()
for line in process.stdout:
        print(line)

cmd=['morse','run','segwaysim']                                                              # running morse project
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)


cmd2=['python3',dir_path+'/scripts/main_segway_controller.py']                               # running script which controls main segaway
process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)

cmd3=['python3',dir_path+'/scripts/chase_controller.py']                                     # running script which controls chase segaway
process3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE)


process.wait()    # wait for main window close
process2.kill()   # exiting main_segway_controller.py when you close blender
process3.kill()   # exiting ruch_chase.py when you close blender

for line in process.stdout and process2.stdout and process3.stdout:
        print(line)


