from typing import List
import subprocess
from string import Template
import numpy as np
import pkgutil
from .. import Input, Result, LD2DL
import re
from uncertainties import ufloat_fromstr
import os.path
from pathlib import Path


resummino_path = "~/resummino/"


def set_path(p):
    global resummino_path
    resummino_path = p


def get_path():
    global resummino_path
    return resummino_path


class RunParams:
    def __init__(self, flags: str, in_path: str, out_path: str, skip=False):
        self.skip = skip
        self.flags = flags
        self.in_path = in_path
        self.out_path = out_path


def run(params: List[Input]):
    rps = _queue(params)
    _run(rps)
    outs = LD2DL(rps)["out_path"]
    results = _parse(outs)
    rdl = LD2DL(results)
    pdl = LD2DL(params)
    return {**rdl, **pdl}


def _parse(outputs: List[str]) -> List[Result]:
    rsl = []
    for f in outputs:
        res = _parse_single(f)
        rsl.append(res)
    return rsl


def _parse_single(file) -> Result:
    lo_pattern = re.compile(r'^LO = \((.*)\) pb')
    nlo_pattern = re.compile(r'^NLO = \((.*)\) pb')
    nll_pattern = re.compile(r'^NLO\+NLL = \((.*)\) pb')

    lo_result = None
    nlo_result = None
    nll_result = None
    with open(file) as output:
        for line in output:
            tmp = lo_pattern.search(line)
            if tmp is not None:
                lo_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = nlo_pattern.search(line)
            if tmp is not None:
                nlo_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))
            tmp = nll_pattern.search(line)
            if tmp is not None:
                nll_result = ufloat_fromstr(tmp.group(1).replace("+-", "+/-"))

    return Result(lo_result, nlo_result, nll_result)


def _queue(params: List[Input]) -> List[RunParams]:
    Path("output").mkdir(parents=True, exist_ok=True)
    Path("input").mkdir(parents=True, exist_ok=True)
    ret = []
    for p in params:
        d = p.__dict__
        # TODO insert defautl if missing in d!
        name = "_".join("".join(str(_[0]) + "_" + str(_[1]))
                        for _ in d.items())
        skip = False
        if os.path.isfile("output/" + name + ".out"):
            print("skip", end='')
            skip = True
        data = pkgutil.get_data(__name__, "plot_template.in").decode(
            'utf-8')

        src = Template(data)
        result = src.substitute(d)
        open("input/" + name, "w").write(result)
        if not skip:
            open("output/" + name + ".out", "w").write(result + "\n\n")

        sname = d['slha']
        with open('mastercode.in', 'r') as f:
            src = Template(f.read())
            result = src.substitute(d)
            open("input/" + sname, "w").write(result)
            if not skip:
                open("output/" + name + ".out", "a").write(result + "\n\n")

        ret.append(RunParams(["--lo", "--nlo", "--nll"]
                             [p.order], "./input/"+name, "./output/"+name + ".out", skip))

    return ret


def _run(rps: List[RunParams]):
    global resummino_path
    # TODO RS build path checks?!?!
    template = resummino_path + 'build/bin/resummino {} {} >> {}'

    # Run commands in parallel
    processes = []

    for rp in rps:
        if not rp.skip:
            command = template.format(rp.in_path, rp.flags, rp.out_path)
            process = subprocess.Popen(command, shell=True)
            processes.append(process)

    # Collect statuses
    output = [p.wait() for p in processes]
    return output


sp = []
p = {'energy': 13000, 'p1': 2000002, 'p2': 1000022,
     'slha': "mastercode.in", "mu_f": 1., "mu_r": 1.}
for mu_f in np.logspace(-1, 1, 3):
    for mu_r in np.logspace(-1, 1, 3):
        p['mu_r'] = mu_r
        p['mu_f'] = mu_f
        sp.append(p.copy())

# print(sp)
# names = queue(sp)
# run(names)
