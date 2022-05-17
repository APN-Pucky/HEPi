"""Runs Resummino"""
from typing import List
import subprocess
from string import Template
import warnings
from hepi.input import Order
from hepi.results import Result
from hepi.run import RunParam, Runner
import pkgutil

from hepi.util import namehash
from .. import Input, LD2DL, get_output_dir, get_pre
import re
import os.path
from pathlib import Path
from .result import ResumminoResult, is_valid, parse_single
import enlighten
import time
import difflib
from smpl.parallel import par
import os
import stat
from smpl import debug


class ResumminoRunner(Runner):

    def orders(self) -> List[Order]:
        return [Order.LO, Order.NLO, Order.NLO_PLUS_NLL, Order.aNNLO_PLUS_NNLL]

    def _check_input(self, p: Input, **kwargs) -> bool:

        if p.order == Order.aNNLO_PLUS_NNLL and (
                p.has_gluino() and p.has_weakino()) or (p.has_squark()
                                                        and p.has_weakino()):
            warnings.warn(
                "Resummino does not support stong-weak mixed aNNLO+NNLL.")
            return False
        return True

    def _is_valid(self, file: str, p: Input, d) -> bool:
        if not super()._is_valid(file, p, d):
            return False
        return is_valid(file, p, d)

    def _parse_file(self, file: str) -> Result:
        return parse_single(file)

    def _prepare(self, p: Input, **kwargs) -> RunParam:
        rp = super()._prepare(p, **kwargs)
        if not rp.skip:
            data = pkgutil.get_data(__name__,
                                    "plot_template.in").decode('utf-8')
            flags = ""
            if p.order == Order.LO:
                flags = flags + "--lo"
            elif p.order == Order.NLO:
                flags = flags + "--nlo"
            elif p.order == Order.NLO_PLUS_NLL:
                flags = flags + "--nll"
            elif p.order == Order.aNNLO_PLUS_NNLL:
                flags = flags + "--nnll"
            else:
                raise ValueError(
                    "Order not supported by resummino. Must be one of LO/NLO/NLO+NLL/aNNLO+NNLL."
                )

            src = Template(data)
            result = src.substitute(p.__dict__)
            open(get_output_dir() + rp.name + ".in", "w").write(result)
            open(get_output_dir() + rp.name + ".sh",
                 "w").write("#!/bin/sh\n" + get_path() +
                            'build/bin/resummino {} {} >> {}'.format(
                                get_output_dir() + rp.name + ".in", flags,
                                get_output_dir() + rp.name + ".out"))
            st = os.stat(get_output_dir() + rp.name + ".sh")
            os.chmod(get_output_dir() + rp.name + ".sh",
                     st.st_mode | stat.S_IEXEC)
            open(get_output_dir() + rp.name + ".out",
                 "w").write(result + "\n\n")

            sname = p.slha
            with open(get_output_dir() + sname, 'r') as f:
                open(get_output_dir() + rp.name + ".out",
                     "a").write(f.read() + "\n\n")
        return rp


# Legacy
default_resummino_runner = ResumminoRunner("~/resummino/")
"""Default Resummino Runner to provide backward compatibility"""
run = default_resummino_runner.run
set_path = default_resummino_runner.set_path
get_path = default_resummino_runner.get_path