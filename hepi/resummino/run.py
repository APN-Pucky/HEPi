"""Runs Resummino"""
from typing import List
import subprocess
from string import Template
import numpy as np
import pkgutil

from hepi.util import namehash
from .. import Input, Result, LD2DL, get_output_dir, get_input_dir, get_pre
import re
from uncertainties import ufloat_fromstr
import os.path
from pathlib import Path
from .result import ResumminoResult, is_valid, parse_single
import enlighten
import time
import difflib
from smpl.parallel import par
import hashlib
import os 
import stat


resummino_path = "~/resummino/"
"""resummino folder containing the binary in './build/bin'."""



def set_path(p: str):
    """
    Set the path to the resummino folder containing the binary in './build/bin'.

    Args:
        str: new Resummino path.
    """
    global resummino_path
    resummino_path = p+ ("/" if p[-1]!="/" else "")


def get_path():
    """
    Get Resummino path.

    Returns: 
        str: current Resummino path
    """
    global resummino_path
    return resummino_path


class RunParams:
    """
    Parameters for running Resummino.

    Attributes:
        skip (bool): Skip already performed and stored runs.
        flags (str): Additional resummino flags. E.g. '--nlo'.
        in_path (str): File path of the input file.
        out_path (str): File path of the output file.
    """
    def __init__(self, flags: str, in_path: str, out_path: str, skip=False):
        self.skip = skip
        self.flags = flags
        self.in_path = in_path
        self.out_path = out_path


def run(params: List[Input], noskip=False, bar=True, no_parse=False,para=True):
    """
    Run the passed list of parameters.

    Args:
        params (:obj:`list` of :class:`hepi.Input`): All parameters that should be executed/queued.
        noskip (bool): False means stored runs will be skipped. Else the are overwritten.
        bar (bool): Display a progressbar.
        no_parse (bool): Skip parsing the results. 
            This is the prefered cluster mode, as this function only queues the job.
        para (bool): Run jobs in parallel.

    Returns:
        :obj:`dict` : combined dictionary of results and parameters. Each member therein is a list.
            The dictionary is empty if `no_parse` is set.

    """
    print("Running: " + str(len(params))  +" jobs" )
    rps = _queue(params, noskip)
    _run(rps, bar, no_parse,para)
    if not no_parse:
        outs = LD2DL(rps)["out_path"]
        results = _parse(outs)
        rdl = LD2DL(results)
        pdl = LD2DL(params)
        return {**rdl, **pdl}
    return {}


def _parse(outputs: List[str]) -> List[ResumminoResult]:
    """
    Parses Resummino output files and returns List of Results.

    Args:
        outputs (:obj:`list` of `str`): List of the filenames to be parsed.

    Returns:
        :obj:`list` of :class:`hepi.resummino.result.ResumminoResult`

    """
    rsl = []
    for r in par(parse_single, outputs):
        rsl.append(r)
    return rsl



def _queue(params: List[Input], noskip=False) -> List[RunParams]:
    """
    Queues and generates Resummino run files.

    Extends params by input and output files.

    Args:
        params (:obj:`list` of :class:`hepi.Input`): input parameters
        noskip (bool): False means stored runs will be skipped. Else the are overwritten.

    Returns:
        :obj:`list` of :class:`hepi.RunParams`: Run paramters for usage with :meth:`_run`.

    """
    global resummino_path
    Path("output").mkdir(parents=True, exist_ok=True)
    Path("input").mkdir(parents=True, exist_ok=True)
    ret = []
    for p in params:
        d = p.__dict__
        d["code"] = "RS"
        # TODO insert defautl if missing in d!
        name = namehash("_".join("".join(str(_[0]) + "_" + str(_[1]))
                        for _ in d.items()).replace("/", "-"))
        print(name)
        skip = False
        if not noskip and os.path.isfile(get_output_dir() + name + ".out") and is_valid(get_output_dir() + name + ".out",p,d):
            print("skip", end='')
            skip = True
        if not skip:
            data = pkgutil.get_data(__name__, "plot_template.in").decode(
                'utf-8')

            src = Template(data)
            result = src.substitute(d)
            open(get_input_dir() + name + ".in", "w").write(result)
            open(get_input_dir() + name + ".sh", "w").write("#!/bin/sh\n"+
                resummino_path + 'build/bin/resummino {} {} >> {}'.format(
                    get_input_dir()+name + ".in",["--lo", "--nlo", "--nll"][p.order],get_output_dir()+name + ".out"
                ))
            st = os.stat(get_input_dir() + name + ".sh")
            os.chmod(get_input_dir() + name + ".sh", st.st_mode | stat.S_IEXEC)
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


def _run(rps: List[RunParams], bar=True, no_parse=False,para=True):
    """
    Runs Resummino per :class:`RunParams`.

    Args:
        rps (:obj:`list` of :class:`RunParams`):  Extended run parameters.
        bar (bool): Enable info bar.
        no_parse (bool): Do not wait for parallel runs to finish.
        para (bool): Run jobs in parallel.

    Returns:
        :obj:`list` of int: return codes from jobs if `no_parse` is False.
    """
    # TODO clean up on exit emergency
    global resummino_path
    # TODO RS build path checks?!?!
    template = get_pre() + " " +  "{}"

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
            command = template.format(rp.in_path.replace(".in",".sh"))
            process = subprocess.Popen(command, shell=True)
            processes.append(process)
            processesrpo[process] = rp.out_path
            if not para:
                process.wait()
            if no_parse:
                time.sleep(5)
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
