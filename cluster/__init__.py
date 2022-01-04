import hepi
import smpl
import hepi.resummino as rs
import hepi.input as input
#import hepi
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time

user = "a_neuw01"

rs.set_path("/home/a/"+user+"/git/resummino/")
input.set_output_dir("/scratch/tmp/"+user+"/hepi/")
input.set_input_dir("/home/a/"+user+"/git/hepi/tests/input/")
input.set_pre(
    "srun --ntasks-per-node 1 --cpus-per-task 1 --partition normal --mem=100M --mail-type=ALL --time=04:00:00 --mail-user="+user+"@uni-muenster.de")
print(rs.get_path())


def wait():
    output = "\n\n\n"
    while(output.count('\n') > 1):
        bashCommand = "squeue -u " + user
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        time.sleep(60)
