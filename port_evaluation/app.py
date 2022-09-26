import subprocess
res = subprocess.call(['open', 'port_evaluation/src/run_src.r'])
print(res)

# run_max.py
import subprocess

# Define command and arguments
command ='Rscript'
path2script ='port_evaluation/src/run_src.r'

# Variable number of args in a list
# args = ['11','3','9','42']

# Build subprocess command
cmd = [command, path2script] #+ args

# check_output will run the command and store to result
x = subprocess.check_output(cmd, universal_newlines=True)

print('The R subscript returns:', x)