import subprocess
filename='test.py'
command='autopep8 --in-place --aggressive --aggressive '+filename
subprocess.call(command, shell=True)