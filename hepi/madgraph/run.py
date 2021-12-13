from typing import List
import subprocess
from string import Template
import numpy as np
import pkgutil
from .. import Input, Result, LD2DL, get_output_dir, get_input_dir
import re
from uncertainties import ufloat_fromstr
import os.path
from pathlib import Path
from .result import MadgraphResult, parse_single
import enlighten
import time
import difflib
import pyslha

madgraph_path = "/opt/MG5_aMC_v2_7_0/"


def set_path(p):
    global madgraph_path
    madgraph_path = p


def get_path():
    global madgraph_path
    return madgraph_path


class RunParams:
    def __init__(self, dic,  skip=False):
        self.dic = dic
        self.skip = skip


def run(params: List[Input], noskip=False):
    rps = _queue(params, noskip)
    _run(rps)
    outs = LD2DL(rps)["dic"]
    results = _parse(outs)
    rdl = LD2DL(results)
    pdl = LD2DL(params)
    return {**rdl, **pdl}


def _parse(outputs: List[str]) -> List[MadgraphResult]:
    rsl = []
    for f in outputs:
        res = parse_single(f["out"])
        rsl.append(res)
    return rsl


def _queue(params: List[Input], noskip=False) -> List[RunParams]:
    Path("output").mkdir(parents=True, exist_ok=True)
    Path("input").mkdir(parents=True, exist_ok=True)
    ret = []
    for p in params:
        d = p.__dict__
        d["code"] = "MG"
        # TODO insert defautl if missing in d!
        name = "_".join("".join(str(_[0]) + "_" + str(_[1]))
                        for _ in d.items()).replace("/", "-")
        skip = False
        if not noskip and os.path.isfile(get_output_dir() + name + ".out"):
            print("skip", end='')
            skip = True

        d["dir"] = get_output_dir() + name + ".dir"
        d["bdir"] = get_output_dir() + name + ".bdir"
        d["energyhalf"] = d["energy"]/2.
        b = pyslha.read(d["slha"])
        d["mu"] = (b.blocks["MASS"][d["particle1"]] +
                   b.blocks["MASS"][d["particle2"]])/2.

        data = pkgutil.get_data(__name__, ["lo.mg", "nlo.mg"][p.order]).decode(
            'utf-8')
        src = Template(data)
        result = src.substitute(d)
        open(get_input_dir() + name + ".mg", "w").write(result)
        if not skip:
            open(get_output_dir() + name + ".out", "w").write(result + "\n\n")

        data = pkgutil.get_data(__name__, ["run_card_lo.dat", "run_card_nlo.dat"][p.order]).decode(
            'utf-8')
        src = Template(data)
        result = src.substitute(d)
        open(get_input_dir() + name + ".dat", "w").write(result)
        if not skip:
            open(get_output_dir() + name + ".out", "a").write(result + "\n\n")

        sname = d['slha']
        with open(get_input_dir() + sname, 'r') as f:
            #src = Template(f.read())
            #result = src.substitute(d)
            #open(get_input_dir() + sname + ".in", "w").write(result)
            if not skip:
                open(get_output_dir() + name + ".out",
                     "a").write(f.read() + "\n\n")

        ret.append(RunParams({'in': get_input_dir()+name + ".mg",
                              'dir': d["dir"],
                              'bdir': d["bdir"],
                              'run': get_input_dir() + name + ".dat",
                              'slha': get_input_dir() + sname,
                              'out': get_output_dir()+name + ".out"}, skip))

    return ret


def _run(rps: List[RunParams]):
    # TODO clean up on exit emergency
    global madgraph_path
    # TODO RS build path checks?!?!
    template =  \
        'rm -rf {dir} && cp -r ' + rps[0].dic["bdir"] + \
        ' {dir}  && cp {slha} {dir}/Cards/param_card.dat && cp {run} {dir}/Cards/run_card.dat && {dir}/bin/calculate_xsect -f >> {out}'
    print(rps[0].dic["out"])
    if not rps[0].skip:
        pp = subprocess.Popen(madgraph_path +
                          'bin/mg5_aMC --mode="MadSTR" --file {in} >> {out}'.format(**rps[0].dic), shell=True)
        pp.wait()
    # Run commands in parallel
    processes = []

    for rp in rps:
        if not rp.skip:
            command = template.format(**rp.dic)
            #print(command)
            process = subprocess.Popen(command, shell=True)
            processes.append(process)

    # Collect statuses
    output = [p.wait() for p in processes]
    return output


# print(sp)
# names = queue(sp)
# run(names)
