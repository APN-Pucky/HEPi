from typing import List
import warnings
from hepi import get_input_dir
import subprocess
import os
from hepi.input import Input, update_slha

spheno_path = "~/git/SPheno-3.3.8/"
"""spheno folder containing the binary in './bin'."""


def set_path(p:str):
    """
    Set the path to the SPheno folder containing the binary in './bin'.

    Args:
        p (str): new path.
    """
    global spheno_path
    spheno_path = p + ("/" if p[-1]!="/" else "")


def get_path() ->str:
    """
    Get the SPheno path.

    Returns:
        str: current SPheno path.
    """
    global spheno_path
    return spheno_path


def run(slhas : List[Input]) -> List[Input]:
    """
    Run the passed list of parameters for SPheno.
    """
    if os.path.exists("Messages.out"):
        os.remove("Messages.out")
    for s in slhas:
        #print(s.slha)
        comm= "cp " +  get_input_dir() + s.slha  + " spheno_tmp.in && " +get_path() + "bin/SPheno spheno_tmp.in && mv "  + "SPheno.spc " + get_input_dir() + s.slha  + " && sed -i '/Created/d' " + get_input_dir() + s.slha
        proc = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        update_slha(s)
    if os.path.exists("Messages.out"):
        with open("Messages.out",'r') as r:
            t = r.read()
            if t != "":
                warnings.warn(r.read())
    return slhas
