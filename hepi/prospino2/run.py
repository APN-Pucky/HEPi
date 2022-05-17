import os
import pkgutil
import shutil
import stat
from string import Template
import subprocess
import warnings
from hepi.input import Input, Order, is_gluino, is_slepton, is_squark, is_weakino
from hepi.results import Result
from hepi.run import RunParam, Runner
from uncertainties import ufloat


class ProspinoResult(Result):
    """
    Prospino Result Data.
    """


class ProspinoRunner(Runner):
    # TODO add leptoqaurk, stop and sbottom cases
    weakino_map = {
        1000022: 1,
        1000023: 2,
        1000025: 3,
        1000035: 4,
        1000024: 5,
        1000037: 6,
        -1000024: 7,
        -1000037: 8,
    }
    squark_map = {
        1000005: -5,
        1000004: -4,
        1000003: -3,
        1000001: -2,
        1000002: -1,
        2000002: 1,
        2000001: 2,
        2000003: 3,
        2000004: 4,
        2000005: 5,
    }
    slepton_map = {
        (1000011, 1000011): 1,
        (2000011, 2000011): 2,
        (1000012, 1000012): 3,
        (-1000011, 1000012): 4,
        (1000011, 1000012): 5,
        (1000015, 1000015): 6,
        (2000015, 2000015): 7,
        (1000015, 2000015): 8,
        (1000016, 1000016): 9,
        (-1000015, 1000016): 10,
        (1000015, 1000016): 11,
        (-2000015, 1000016): 12,
        (2000015, 1000016): 13,
    }

    def _get_ps_proc(self, p: Input):
        if p.has_squark() and p.has_weakino():
            sq = p.particle1 if is_squark(p.particle1) else p.particle2
            weakino = p.particle2 if is_squark(p.particle1) else p.particle1
            return 'ns', self.weakino_map[weakino], 1, self.squark_map[abs(
                sq)], 1
        if p.has_gluino() and p.has_weakino():
            return 'ng', self.weakino_map[p.particle1 if is_gluino(p.particle2
                                                                   ) else p.
                                          particle2], 1, 1, 1
        if p.has_gluino() and p.has_squark():
            return 'sg', 1, 1, self.squark_map[abs(
                p.particle1 if is_gluino(p.particle2) else p.particle2)], 1
        if is_weakino(p.particle1) and is_weakino(p.particle2):
            return 'nn', self.weakino_map[p.particle1], self.weakino_map[
                p.particle2], 1, 1
        if is_slepton(p.particle1) and is_slepton(p.particle2):
            return 'll', self.slepton_map[(p.particle1, p.particle2)], 1, 1, 1
        if is_gluino(p.particle1) and is_gluino(p.particle2):
            return 'gg', 1, 1, 1, 1
        if is_squark(p.particle1) and is_squark(p.particle2):
            if p.particle1 > 0 and p.particle2 > 0:
                return 'ss', 1, 1, self.squark_map[abs(
                    p.particle1)], self.squark_map[abs(p.particle2)]
            elif (p.particle1 > 0
                  and p.particle2 < 0) or (p.particle1 < 0
                                           and p.particle2 > 0):
                s = p.particle1 if p.particle1 > p.particle2 else p.particle2
                b = p.particle2 if p.particle1 > p.particle2 else p.particle1
                return 'sb', 1, 1, self.squark_map[abs(s)], self.squark_map[
                    abs(b)]
        return "UNKNOWN_PROCESS_OR_UNIMPLEMENTED_PROCESS"

    def _get_ps_input(self, p: Input) -> dict:
        d = {}
        d["ps_inlo"] = int(p.order)
        d["ps_final_state_in"], d["ps_ipart1_in"], d["ps_ipart2_in"], d[
            "ps_isquark1_in"], d["ps_isquark2_in"] = self._get_ps_proc(p)
        return d

    def orders(self) -> Order:
        return [Order.LO, Order.NLO]

    def _check_input(self, p: Input, **kwargs) -> bool:
        """Checks input parameter for compatibility with Prospino"""
        if p.mu_f != 1. or p.mu_r != 1.:
            warnings.warn(
                "Prospino2 does not support varying the scales manually.")
            return False
        if p.pdf_lo != "cteq6l1" or p.pdf_nlo != "cteq66":
            warnings.warn(
                "Prospino2 does not support all pdfs (CTEQ6L1 and CTEQ66 allowed defaults)."
            )
            return False
        return True

    def _is_valid(self, file: str, p: Input, d) -> bool:
        return super()._is_valid(file, p, d)

    def _parse_file(self, file: str) -> Result:
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
        return ProspinoResult(
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
            d["ps_inlo"] = int(p.order)
            for k, v in self._get_ps_input(p).items():
                d[k] = v
            result = src.substitute(d)
            #open(rp.in_file, "w").write(result)
            open(rp.out_file, "w").write(result + "\n\n")
            rdir = self.get_output_dir() + rp.name + ".rdir"
            if os.path.exists(rdir) and os.path.isdir(rdir):
                shutil.rmtree(rdir)
            shutil.copytree(self.get_path(), rdir)
            open(rdir + "/prospino_main.f90", "w").write(result)
            # compile
            subprocess.Popen("cd " + rdir + " && make",
                             shell=True,
                             stdout=subprocess.DEVNULL).wait()

            open(rp.execute, "w").write(
                "#!/bin/sh\n" +
                "H=$PWD && cd {rdir}&& ./prospino_2.run > tmp.out && cd $H  && cat {rdir}/tmp.out  >> {out} && cat {rdir}/prospino.dat>> {out} && rm -rf {rdir}"
                .format(rdir=rdir, out=rp.out_file))
            st = os.stat(rp.execute)
            os.chmod(rp.execute, st.st_mode | stat.S_IEXEC)

            sname = d['slha']
            shutil.copy(self.get_output_dir() + sname,
                        rdir + "/prospino.in.les_houches")
            with open(self.get_output_dir() + sname, 'r') as f:
                open(rp.out_file, "a").write(f.read() + "\n\n")
        return rp


# Legacy
default_prospino_runner = ProspinoRunner("~/git/Prospino2/")
"""Default Prospino Runner to provide backward compatibility"""
run = default_prospino_runner.run
set_path = default_prospino_runner.set_path
get_path = default_prospino_runner.get_path