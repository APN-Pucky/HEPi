import os
import pkgutil
import stat
import warnings
from string import Template
from typing import List
from hepi.run.nllfast.result import NLLFastResult

import pyslha
from uncertainties import ufloat

from hepi.input import Input, Order, is_gluino, is_squark
from hepi.results import Result
from hepi.run import Runner, RunParam


class NLLfastRunner(Runner):
    def orders(self) -> List[Order]:
        return [Order.LO, Order.NLO, Order.NLO_PLUS_NLL]

    def _get_nf_proc(self, p: Input):
        d = pyslha.read(self.get_output_dir() + p.slha)
        mg = d.blocks["MASS"][1000021]
        ms = 0.0
        for r in range(1000001, 1000006):
            ms += d.blocks["MASS"][r]
        for r in range(2000001, 2000006):
            ms += d.blocks["MASS"][r]
        ms /= 10 # 10 flavors no (s)top
        if p.has_gluino() and p.has_squark():
            if is_squark(p.particle1):
                ms = d.blocks["MASS"][abs(p.particle1)]
            if is_squark(p.particle2):
                ms = d.blocks["MASS"][abs(p.particle2)]
            return "sg", "cteq", ms, mg, 10
        if is_gluino(p.particle1) and is_gluino(p.particle2):
            if ms > 2000: # go into decoupling limit
                return "gdcpl", "cteq","", mg, 1
            return "gg", "cteq", ms, mg, 1
        if is_squark(p.particle1) and is_squark(p.particle2):
            if mg > 2000: # go into decoupling limit
                return "sdcpl", "cteq", ms,"", 1
            ms =(d.blocks["MASS"][abs(p.particle1)] +d.blocks["MASS"][abs(p.particle2)])/2
            if p.particle1 > 0 and p.particle2 > 0:
                return "ss", "cteq", ms, mg,10*10
            elif (p.particle1 > 0 and p.particle2 < 0) or (
                p.particle1 < 0 and p.particle2 > 0
            ):
                s = p.particle1 if p.particle1 > p.particle2 else p.particle2
                b = p.particle2 if p.particle1 > p.particle2 else p.particle1
                return "sb", "cteq", ms, mg, 10
        return "UNKNOWN_PROCESS_OR_UNIMPLEMENTED_PROCESS"

    def _get_nf_input(self, p: Input) -> dict:
        d = {}
        # d["ps_inlo"] = int(p.order)
        (
            d["nf_final_state_in"],
            d["nf_pdf"],
            d["nf_squark_mass"],
            d["nf_gluino_mass"],
            d["nf_deg"],
        ) = self._get_nf_proc(p)
        return d

    def _check_input(self, p: Input, **kwargs) -> bool:
        """Checks input parameter for compatibility with Prospino"""
        if p.energy != 13000:
            warnings.warn("NLL-fast does not support other energies than 13 TeV.")
            return False
        if p.mu_f != 1.0 or p.mu_r != 1.0:
            warnings.warn("NLL-fast does not support varying the scales manually.")
            return False
        if p.pdf_lo != "cteq6l1" or p.pdf_nlo != "cteq66":
            warnings.warn(
                "NLL-fast does not support all pdfs (CTEQ6L1 and CTEQ66 allowed defaults)."
            )
            return False
        return True

    def _is_valid(self, file: str, p: Input, d,**kwargs) -> bool:
        return super()._is_valid(file, p, d)

    def _parse_file(self, file: str) -> Result:
        # TODO parse result
        ret = []
        with open(file) as output:
            for line in output:
                pass
            for s in line.split():
                ret.append(float(s))
        return NLLFastResult( # divide by 10 due to degeneracy, this is injeted into the result
            ufloat(ret[2]/ret[13], 0.0),
            ufloat(ret[3]/ret[13], 0.0),
            ufloat(ret[4]/ret[13], 0.0),
            ufloat(ret[6]/ret[13], 0.0),
            ufloat(ret[5]/ret[13], 0.0),
            ufloat((1-(ret[8]**2+ret[10]**2)**.5 )*ret[4]/ret[13] , 0.0),
            ufloat((1+(ret[7]**2+ret[9]**2)**.5)*ret[4]/ret[13], 0.0),
        )

    def _prepare(self, p: Input, **kwargs) -> RunParam:
        rp = super()._prepare(p, **kwargs)
        if not rp.skip:
            d = p.__dict__

            for k, v in self._get_nf_input(p).items():
                d[k] = v


            open(rp.execute, "w").write(
                "#!/bin/sh\n"
                + "pushd {path} > /dev/null\nR=\"$({exec} {proc} {pdf} {sq} {gl})\"\npopd > /dev/null\necho \"$R {deg}\">{out}".format(
                    exec=self.get_path(),
                    path=os.path.dirname(self.get_path()),
                    out=rp.out_file,
                    proc=d["nf_final_state_in"],
                    sq=d["nf_squark_mass"],
                    gl=d["nf_gluino_mass"],
                    pdf=d["nf_pdf"],
                    deg=d["nf_deg"],
                )
            )
            st = os.stat(rp.execute)
            os.chmod(rp.execute, st.st_mode | stat.S_IEXEC)

            sname = d["slha"]
            with open(self.get_output_dir() + sname, "r") as f:
                open(rp.out_file, "a").write(f.read() + "\n\n")
        return rp


# Legacy
default_nllfast_runner = NLLfastRunner("~/git/nll-fast/nll-fast")
"""Default Prospino Runner to provide backward compatibility"""
run = default_nllfast_runner.run
set_path = default_nllfast_runner.set_path
get_path = default_nllfast_runner.get_path
