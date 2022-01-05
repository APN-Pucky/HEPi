import hepi
import smpl
import hepi.resummino as rs
import hepi.input as input
#import hepi
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time
import os
import sys

user = "a_neuw01"

rs.set_path("/home/a/"+user+"/git/resummino/")
input.set_output_dir("/scratch/tmp/"+user+"/hepi/")
input.set_input_dir("/home/a/"+user+"/git/hepi/tests/input/")
input.set_pre("sbatch --job-name=" +os.path.basename(sys.argv[0]) +
" --ntasks-per-node 1 --cpus-per-task 1  --time=06:00:00 --mem=100M --partition normal" +
" --mail-type=ALL --mail-user="+user+"@uni-muenster.de")
print(rs.get_path())


def wait():
    output = "\n\n\n"
    while(len(output.split('\n')) > 1):
        bashCommand = "squeue -u " + user
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output=output.decode()
        time.sleep(60)
