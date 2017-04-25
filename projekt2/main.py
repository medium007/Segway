import subprocess
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))


cmd = ['morse','import', '-f', dir_path,'segwaysim']
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
process.wait()
for line in process.stdout:
        print(line)

cmd=['morse','run','segwaysim']
cmd2=['python3',dir_path+'/scripts/rownowaga.py']
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)


process.wait()
process2.kill()



