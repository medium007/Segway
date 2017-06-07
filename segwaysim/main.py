import subprocess
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))                          # getting main.py directory


cmd = ['morse','import', '-f', dir_path,'segwaysim']                            # creating morse project
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
process.wait()
for line in process.stdout:
        print(line)

cmd=['morse','run','segwaysim']                                                 # running morse project
cmd2=['python3',dir_path+'/scripts/rownowaga.py']                               # running script which controls segaway
cmd3=['python3',dir_path+'/scripts/chase_controller.py']
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)

process3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE)


process.wait()
process2.kill()   # exiting rownowaga.py when you close blender
process3.kill()   # exiting ruch_chase.py when you close blender



