from distutils import command
from typing import List
import warnings
import pyslha
from hepi import get_input_dir, get_output_dir
#from hepi.input import slha_scan
import subprocess
import os

from hepi.input import Input

spheno_path = "~/git/SPheno-3.3.8/"


def set_path(p):
    global spheno_path
    spheno_path = p


def get_path():
    global spheno_path
    return spheno_path


def run(slhas : List[Input]) -> List[Input]:
	if os.path.exists("Messages.out"):
		os.remove("Messages.out")
	for s in slhas:
		comm= get_path() + "bin/SPheno " + get_input_dir() + s.slha + " && mv "  + "SPheno.spc " + get_input_dir() + s.slha
		proc = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
		proc.wait()
	if os.path.exists("Messages.out"):
		with open("Messages.out",'r') as r:
			t = r.read()
			if t != "":
				warnings.warn(r.read())
	return slhas
