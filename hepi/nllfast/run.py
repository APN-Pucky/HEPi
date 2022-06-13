import os
import pkgutil
import stat
from string import Template
from typing import List
import warnings
from hepi.input import Input, Order, is_gluino, is_squark
from hepi.results import Result
from hepi.run import RunParam, Runner
import pyslha
from uncertainties import ufloat


class NLLfastRunner(Runner):
    #TODO treat stop sbot separately
    #TODO separate nll and nnll

    def orders(self) -> List[Order]:
        return [Order.LO, Order.NLO, Order.NLO_PLUS_NLL]

    def _get_nf_proc(self, p: Input):
        d = pyslha.read(self.get_output_dir() + p.slha)
        mg = d.blocks["MASS"][1000021]
        ms = 0.
        for r in range(1000001, 1000007):
            ms += d.blocks["MASS"][r]
        for r in range(2000001, 2000007):
            ms += d.blocks["MASS"][r]
        ms /= 12
        if p.has_gluino() and p.has_squark():
            return 'sg', 'cteq', ms, mg
        if is_gluino(p.particle1) and is_gluino(p.particle2):
            return 'gg', 'cteq', ms, mg
        if is_squark(p.particle1) and is_squark(p.particle2):
            if p.particle1 > 0 and p.particle2 > 0:
                return 'ss', 'cteq', ms, mg
            elif (p.particle1 > 0
                  and p.particle2 < 0) or (p.particle1 < 0
                                           and p.particle2 > 0):
                s = p.particle1 if p.particle1 > p.particle2 else p.particle2
                b = p.particle2 if p.particle1 > p.particle2 else p.particle1
                return 'sb', 'cteq', s, b
        return "UNKNOWN_PROCESS_OR_UNIMPLEMENTED_PROCESS"

    def _get_nf_input(self, p: Input) -> dict:
        # TODO return masses of squark and gluino
        d = {}
        #d["ps_inlo"] = int(p.order)
        d["nf_final_state_in"], d["nf_pdf"], d["nf_squark_mass"], d[
            "nf_gluino_mass"] = self._get_ps_proc(p)
        return d

    def _check_input(self, p: Input, **kwargs) -> bool:
        """Checks input parameter for compatibility with Prospino"""
        if p.mu_f != 1. or p.mu_r != 1.:
            warnings.warn(
                "NLL-fast does not support varying the scales manually.")
            return False
        if p.pdf_lo != "cteq6l1" or p.pdf_nlo != "cteq66":
            warnings.warn(
                "NLL-fast does not support all pdfs (CTEQ6L1 and CTEQ66 allowed defaults)."
            )
            return False
        return True

    def _is_valid(self, file: str, p: Input, d) -> bool:
        return super()._is_valid(file, p, d)

    def _parse_file(self, file: str) -> Result:
        #TODO parse result
        ret = []
        with open(file) as output:
            for line in output:
                if line.startswith("nn") or line.startswith(
                        "ng") or line.startswith("ns") or line.startswith(
                            "sg") or line.startswith("ll") or line.startswith(
                                "gg") or line.startswith(
                                    "ss") or line.startswith(
                                        "sb"):  # TODO generalize
                    for s in line[2:].split():
                        ret.append(float(s))
        return Result(
            ufloat(ret[8], ret[8] * ret[9]),
            ufloat(ret[10], ret[10] * ret[11]) if ret[10] != 0. else None,
            None)

    def _prepare(self, p: Input, **kwargs) -> RunParam:
        rp = super()._prepare(p, **kwargs)
        if not rp.skip:
            d = p.__dict__
            data = pkgutil.get_data(
                __name__, "prospino_main.f90_template").decode('utf-8')
            src = Template(data)
            #compute dependent pieces for template
            for k, v in self._get_nf_input(p).items():
                d[k] = v
            result = src.substitute(d)
            #open(rp.in_file, "w").write(result)
            open(rp.out_file, "w").write(result + "\n\n")
            #rdir = self.get_output_dir() + rp.name + ".rdir"
            #if os.path.exists(rdir) and os.path.isdir(rdir):
            #	shutil.rmtree(rdir)
            #shutil.copytree(self.get_path(),rdir)
            #open(rdir  +"/prospino_main.f90", "w").write(result)
            ## compile
            #subprocess.Popen("cd " + rdir + " && make", shell=True,stdout=subprocess.DEVNULL).wait()

            open(rp.execute,
                 "w").write("#!/bin/sh\n" +
                            "{path}/nll-fast {proc} {pdf} {sq} {gl}> {out}".
                            format(path=self.get_path(),
                                   out=rp.out_file,
                                   proc=d["nf_final_state_in"],
                                   sq=d["nf_squark_mass"],
                                   gl=d["nf_gluino_mass"],
                                   pdf=d["nf_pdf"]))
            st = os.stat(rp.execute)
            os.chmod(rp.execute, st.st_mode | stat.S_IEXEC)

            sname = d['slha']
            with open(self.get_output_dir() + sname, 'r') as f:
                open(rp.out_file, "a").write(f.read() + "\n\n")
        return rp


# Legacy
default_nllfast_runner = NLLfastRunner("~/git/nll-fast/")
"""Default Prospino Runner to provide backward compatibility"""
run = default_nllfast_runner.run
set_path = default_nllfast_runner.set_path
get_path = default_nllfast_runner.get_path