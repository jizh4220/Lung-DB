# basic structure: ['<command_to_run>', '<path_to_script>', 'arg1' , 'arg2', 'arg3', 'arg4']
# run_max.py
import subprocess
# Define command and arguments
command = 'Rscript'
path2script = 'path/to your script/max.R'
# Variable number of args in a list
args = ['11', '3', '9', '42']
# Build subprocess command
cmd = [command, path2script] + args
# check_output will run the command and store to result
x = subprocess.check_output(cmd, universal_newlines=True)
print('The maximum of the numbers is:', x)