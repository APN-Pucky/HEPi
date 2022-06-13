"""Runs MadGraph."""
from typing import List
import subprocess
from string import Template
from hepi.input import Order
from hepi.run import RunParam, Runner
import pkgutil
from .. import Input, Result, get_output_dir
from .result import is_valid, parse_single
import time
import os


class MadGraphRunParams(RunParam):
    """Parameters for MadGraph."""

    def __init__(self, dic, skip=False, madstr=True):
        super().__init__(skip)
        self.dic = dic
        # self.skip = skip
        self.madstr = madstr


class MadGraphRunner(Runner):

    def orders(self) -> List[Order]:
        return [Order.LO, Order.NLO]

    def _check_path(self) -> bool:
        if os.path.exists(os.path.expanduser(self.get_path() +
                                             "/bin/mg5_aMC")):
            self.set_path(self.get_path() + "/bin/mg5_aMC")
            return True
        if self.get_path().endswith("mg5_aMC"):
            return True
        return False

    def _check_input(self, param: Input, **kwargs) -> bool:
        """Checks input parameter for compatibility with Prospino"""
        return True

    def _is_valid(self, file: str, p: Input, d) -> bool:
        if not super()._is_valid(file, p, d):
            return False
        return is_valid(file, p, d)

    def _parse_file(self, file: str) -> Result:
        return parse_single(file)

    def _run(self,
             rps: List[RunParam],
             wait=True,
             parallel=True,
             sleep=0,
             **kwargs):
        # TODO clean up on exit emergency
        skipall = True
        for rp in rps:
            if not rp.skip:
                skipall = False
        template = ""
        if not skipall:
            lo = "&& nice -n 5 {dir}/bin/calculate_xsect LO -f >> {out} " if rps[
                0].dic["order"] == Order.NLO else ""
            template =  \
                'rm -rf {dir} && cp -r ' + rps[0].dic["bdir"] + \
                ' {dir}  && cp {slha} {dir}/Cards/param_card.dat && cp {run} {dir}/Cards/run_card.dat && echo "nb_core = 1" >> {dir}/Cards/amcatnlo_configuration.txt ' + lo+ '&& nice -n 5 {dir}/bin/calculate_xsect -f >> {out}  && rm -rf {dir}'
            print(rps[0].dic["out"])
        if not rps[0].skip:
            mgcom = ''
            if rps[0].madstr:
                mgcom = ' --mode="MadSTR"'
            com = self.get_path() + mgcom + \
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
                if not parallel:
                    process.wait()
                # Forced delay to prevent overloading clusters when registering jobs
                time.sleep(sleep)
        if wait:
            # Collect statuses
            output = [p.wait() for p in processes]
            return output
        return []

    def _prepare(self, p: Input, **kwargs) -> RunParam:
        rp = super()._prepare(p, **kwargs)
        name = rp.name
        if not rp.skip:
            d = p.__dict__
            d["dir"] = get_output_dir() + name + ".dir"
            d["bdir"] = get_output_dir() + name + ".bdir"

            infile = ""
            if p.order is Order.LO:
                infile = "lo.mg"
            elif p.order is Order.NLO:
                infile = "nlo.mg"
            else:
                raise ValueError("Madgraph only supported for LO/NLO.")

            data = pkgutil.get_data(__name__, infile).decode('utf-8')
            src = Template(data)
            result = src.substitute(d)
            open(get_output_dir() + name + ".mg", "w").write(result)
            if not rp.skip:
                open(get_output_dir() + name + ".out",
                     "w").write(result + "\n\n")

            if p.order == Order.LO:
                mgfile = "run_card_no_madstr.dat"
            elif p.order == Order.NLO:
                mgfile = "run_card_with_madstr.dat"
            else:
                raise ValueError("Order must be one of LO/NLO in MadGraph.")

            if "madstr" in kwargs and not kwargs["madstr"]:
                mgfile = "run_card_no_madstr.dat"
                rp.madstr = False
            else:
                rp.madstr = True
            data = pkgutil.get_data(__name__, mgfile).decode('utf-8')

            src = Template(data)
            result = src.substitute(d)
            open(get_output_dir() + name + ".dat", "w").write(result)
            if not rp.skip:
                open(get_output_dir() + name + ".out",
                     "a").write(result + "\n\n")

            sname = d['slha']
            with open(get_output_dir() + sname, 'r') as f:
                #src = Template(f.read())
                #result = src.substitute(d)
                #open(get_input_dir() + sname + ".in", "w").write(result)
                if not rp.skip:
                    open(get_output_dir() + name + ".out",
                         "a").write(f.read() + "\n\n")
            rp.dic = {
                'in': get_output_dir() + name + ".mg",
                'dir': d["dir"],
                'bdir': d["bdir"],
                'run': get_output_dir() + name + ".dat",
                'slha': get_output_dir() + sname,
                'out': get_output_dir() + name + ".out",
                'order': p.order
            }
            rp.out_file = rp.dic['out']
        return rp


# Legacy
default_madgraph_runner = MadGraphRunner("/opt/MG5_aMC_v2_7_0/")
"""Default MadGraph Runner to provide backward compatibility"""
run = default_madgraph_runner.run
set_path = default_madgraph_runner.set_path
get_path = default_madgraph_runner.get_path

# print(sp)
# names = queue(sp)
# run(names)
