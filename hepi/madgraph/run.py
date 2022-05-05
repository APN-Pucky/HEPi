"""Runs MadGraph"""
import shutil
from typing import List
import subprocess
from string import Template
from hepi.input import Order
from hepi.run import RunParam
import numpy as np
import pkgutil
from .. import Input, Result, LD2DL, get_output_dir, get_input_dir
import re
import os.path
from pathlib import Path
from .result import MadgraphResult, is_valid, parse_single
import time
import difflib
from smpl.parallel import par
import hashlib

madgraph_path = "/opt/MG5_aMC_v2_7_0/"
"""madgraph folder"""


def set_path(p:str):
    """
    Set the path to the MadGraph folder containing the binary in './bin'.

    Args:
        p (str): New MadGraph path.
    """
    global madgraph_path
    madgraph_path = p+ ("/" if p[-1]!="/" else "")


def get_path():
    """
    Get the current MadGraph path.

    Returns:
        str: current MadGraph path.
    """
    global madgraph_path
    return madgraph_path


class MadGraphRunParams(RunParam):    
    """
    Parameters for MadGraph.
    """
    def __init__(self, dic,  skip=False,madstr=True):
        super().__init__(skip)
        self.dic = dic
        # self.skip = skip
        self.madstr = madstr


def run(params: List[Input], noskip=False,madstr=True,para=True):
    rps = _queue(params, noskip,madstr)
    _run(rps,para)
    outs = LD2DL(rps)["dic"]
    results = _parse(outs)
    rdl = LD2DL(results)
    pdl = LD2DL(params)
    return {**rdl, **pdl}


def _parse(outputs: List[str]) -> List[MadgraphResult]:
    rsl = []
    for r in par(lambda f: parse_single(f["out"]), outputs):
        rsl.append(r)
    return rsl

def namehash(n):
    m = hashlib.sha256()
    m.update(str(n).encode('utf-8'))
    return m.hexdigest()

def _queue(params: List[Input], noskip=False,madstr=True,para=True) -> List[MadGraphRunParams]:
    Path("output").mkdir(parents=True, exist_ok=True)
    Path("input").mkdir(parents=True, exist_ok=True)
    ret = []
    for p in params:
        d = p.__dict__
        d["code"] = "MG"
        # TODO insert defautl if missing in d!
        name = namehash("_".join("".join(str(_[0]) + "_" + str(_[1]))
                        for _ in d.items()).replace("/", "-"))
        skip = False
        if not noskip and os.path.isfile(get_output_dir() + name + ".out") and is_valid(get_output_dir() + name + ".out",p,d):
            print("skip", end='')
            skip = True

        d["dir"] = get_output_dir() + name + ".dir"
        d["bdir"] = get_output_dir() + name + ".bdir"

        data = pkgutil.get_data(__name__, ["lo.mg", "nlo.mg"][p.order]).decode( 'utf-8')
        src = Template(data)
        result = src.substitute(d)
        open(get_output_dir() + name + ".mg", "w").write(result)
        if not skip:
            open(get_output_dir() + name + ".out", "w").write(result + "\n\n")

        if p.order == Order.LO:
            mgfile = "run_card_no_madstr.dat"
        elif p.order == Order.NLO:
            mgfile = "run_card_with_madstr.dat"
        else:
            raise ValueError("Order must be one of LO/NLO in MadGraph.")


        if not madstr:
            mgfile = "run_card_no_madstr.dat"
        data = pkgutil.get_data(__name__, mgfile).decode( 'utf-8')

        src = Template(data)
        result = src.substitute(d)
        open(get_output_dir() + name + ".dat", "w").write(result)
        if not skip:
            open(get_output_dir() + name + ".out", "a").write(result + "\n\n")

        sname = d['slha']
        with open(get_output_dir() + sname, 'r') as f:
            #src = Template(f.read())
            #result = src.substitute(d)
            #open(get_input_dir() + sname + ".in", "w").write(result)
            if not skip:
                open(get_output_dir() + name + ".out",
                     "a").write(f.read() + "\n\n")

        ret.append(MadGraphRunParams({'in': get_output_dir()+name + ".mg",
                              'dir': d["dir"],
                              'bdir': d["bdir"],
                              'run': get_output_dir() + name + ".dat",
                              'slha': get_output_dir() + sname,
                              'out': get_output_dir()+name + ".out",
                              'order' : p.order}, skip,madstr))

    return ret


def _run(rps: List[MadGraphRunParams],para=True):
    # TODO clean up on exit emergency
    global madgraph_path
    lo = "&& nice -n 5 {dir}/bin/calculate_xsect LO -f >> {out} " if rps[0].dic["order"] == Order.NLO else ""
    template =  \
        'rm -rf {dir} && cp -r ' + rps[0].dic["bdir"] + \
        ' {dir}  && cp {slha} {dir}/Cards/param_card.dat && cp {run} {dir}/Cards/run_card.dat && echo "nb_core = 1" >> {dir}/Cards/amcatnlo_configuration.txt ' + lo+ '&& nice -n 5 {dir}/bin/calculate_xsect -f >> {out}  && rm -rf {dir}'
    print(rps[0].dic["out"])
    if not rps[0].skip:
        mgcom = 'bin/mg5_aMC'
        if rps[0].madstr:
            mgcom = 'bin/mg5_aMC --mode="MadSTR"'
        com = madgraph_path + mgcom + \
            ' --file {in} >> {out} && cp {slha} {bdir}/Cards/param_card.dat && cp {run} {bdir}/Cards/run_card.dat && sed -i \'s/.*= req_acc_FO/ 1 = req_acc_FO/g\' {bdir}/Cards/run_card.dat && echo "automatic_html_opening = False" >> {bdir}/Cards/amcatnlo_configuration.txt && nice -n 5 {bdir}/bin/calculate_xsect -f'
        pp = subprocess.Popen(com.format(**rps[0].dic), shell=True)
        pp.wait()
    # Run commands in parallel
    processes = []

    for rp in rps:
        if not rp.skip:
            command = template.format(**rp.dic)
            # print(command)
            process = subprocess.Popen(command, shell=True)
            processes.append(process)
            if not para:
                process.wait()

    # Collect statuses
    output = [p.wait() for p in processes]
    return output


# print(sp)
# names = queue(sp)
# run(names)
