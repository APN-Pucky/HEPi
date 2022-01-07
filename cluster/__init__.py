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
from smpl import plot

user = "a_neuw01"

def get_job_name() -> str:
    return os.path.basename(sys.argv[0])

def wait():
    output = "\n\n\n"
    while(len(output.split('\n')) > 2):
        bashCommand = "squeue -u " + user + " --name=" + get_job_name() 
        if output != "\n\n\n":
            #print(bashCommand , " -> ", output)
            time.sleep(60)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output=output.decode()


rs.set_path("/home/a/"+user+"/git/resummino/")
input.set_output_dir("/scratch/tmp/"+user+"/hepi/")
input.set_input_dir("/home/a/"+user+"/git/hepi/tests/input/")
input.set_pre("while [[ $(squeue -u " + user+ " | wc -l) -gt 1998 ]]; do sleep 60; done && sbatch --job-name=" +get_job_name() +
" --ntasks-per-node 1 --cpus-per-task 1  --time=24:00:00 --mem=100M --partition normal" +
" --mail-type=ALL --mail-user="+user+"@uni-muenster.de")
print(rs.get_path())



