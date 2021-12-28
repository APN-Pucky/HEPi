from typing import List
import subprocess
from string import Template
import numpy as np
import pkgutil
from .. import Input, Result, LD2DL, get_output_dir, get_input_dir, get_pre
import re
from uncertainties import ufloat_fromstr
import os.path
from pathlib import Path
from .result import ResumminoResult, parse_single
import enlighten
import time
import difflib
from smpl.parallel import *
import hashlib

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


def run(params: List[Input], noskip=False, bar=True, no_parse=False):
    rps = _queue(params, noskip)
    _run(rps, bar, no_parse)
    if not no_parse:
        outs = LD2DL(rps)["out_path"]
        results = _parse(outs)
        rdl = LD2DL(results)
        pdl = LD2DL(params)
        return {**rdl, **pdl}
    return {}


def _parse(outputs: List[str]) -> List[ResumminoResult]:
    rsl = []
    for r in par(parse_single, outputs):
        rsl.append(r)
    return rsl


def namehash(n):
    m = hashlib.sha256()
    m.update(str(n).encode('utf-8'))
    return str(m.digest())


def _queue(params: List[Input], noskip=False) -> List[RunParams]:
    Path("output").mkdir(parents=True, exist_ok=True)
    Path("input").mkdir(parents=True, exist_ok=True)
    ret = []
    for p in params:
        d = p.__dict__
        d["code"] = "RS"
        # TODO insert defautl if missing in d!
        name = namehash("_".join("".join(str(_[0]) + "_" + str(_[1]))
                        for _ in d.items()).replace("/", "-"))
        skip = False
        if not noskip and os.path.isfile(get_output_dir() + name + ".out"):
            print("skip", end='')
            skip = True
        if not skip:
            data = pkgutil.get_data(__name__, "plot_template.in").decode(
                'utf-8')

            src = Template(data)
            result = src.substitute(d)
            open(get_input_dir() + name + ".in", "w").write(result)
            open(get_output_dir() + name + ".out", "w").write(result + "\n\n")

            sname = d['slha']
            with open(get_input_dir() + sname, 'r') as f:
                #src = Template(f.read())
                #result = src.substitute(d)
                #open(get_input_dir() + sname + ".in", "w").write(result)
                open(get_output_dir() + name + ".out",
                     "a").write(f.read() + "\n\n")

        ret.append(RunParams(["--lo", "--nlo", "--nll"]
                             [p.order], get_input_dir()+name + ".in", get_output_dir()+name + ".out", skip))

    return ret


def _run(rps: List[RunParams], bar=True, no_parse=False):
    # TODO clean up on exit emergency
    global resummino_path
    # TODO RS build path checks?!?!
    template = get_pre() + " " + resummino_path + 'build/bin/resummino {} {} >> {}'

    # Run commands in parallel
    processes = []
    processesrpo = {}
    processesbar = {}
    manager = enlighten.get_manager()
    status_format = '{program}{fill} Stage: {stage}{fill} Status {status}:{fill}{lastline}'
    main_format = '{program}'
    mp = ""
    if bar:
        mp = rps[0].out_path
        main_bar = manager.status_bar(status_format=main_format,
                                      program=mp)
        mp = rps[1].out_path

    for rp in rps:
        if not rp.skip:
            command = template.format(rp.in_path, rp.flags, rp.out_path)
            process = subprocess.Popen(command, shell=True)
            processes.append(process)
            processesrpo[process] = rp.out_path
            if bar:
                nnn = ""
                nn = ""
                ch = False
                for i, s in enumerate(difflib.ndiff(mp+"_", rp.out_path+"_")):
                    if s[-1] == "_":
                        if ch:
                            nnn = nnn + " ... " + nn
                        ch = False
                        nn = ""
                    if s[0] == '+':
                        ch = True
                    if (s[0] == '+' or s[0] == ' ') and s[-1] != "_":
                        nn = nn + s[-1]
                processesbar[process] = manager.status_bar(status_format=status_format,
                                                           program=nnn,
                                                           stage='INIT',
                                                           status='OKAY',
                                                           lastline="0")
        mp = rps[0].out_path
    if bar:
        c = True
        while c:
            if len(processes) > 0:
                time.sleep(10)
            c = False
            for p in processes:
                if p.poll() is None:
                    c = True
                    pat = re.compile(r'^\* (.*) \*')
                    n = ""
                    cl = 0
                    with open(processesrpo[p], mode="r") as f:
                        for l in f:
                            tmp = pat.search(l)
                            if(tmp is not None):
                                n = tmp.group(1)
                                cl = 0
                            cl = cl+1

                    processesbar[p].update(
                        stage=n, status=cl, lastline=l[int(len(l)/2)::])
                else:
                    processesbar[p].update(
                        stage="DONE", status='DONE', lastline="")
        for p in processes:
            processesbar[p].close()
        main_bar.close()

    if not no_parse:
        # Collect statuses
        output = [p.wait() for p in processes]
        return output
    return []
