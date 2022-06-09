from typing import List
import warnings
import subprocess
import os
from hepi.input import Input, update_slha
from hepi.run import Runner


class SPhenoRunner(Runner):

    def _check_path(self) -> bool:
        if os.path.exists(os.path.expanduser(self.get_path() + "/bin/SPheno")):
            self.set_path(self.get_path() + "/bin/SPheno")
            return True
        if self.get_path().endswith("SPheno"):
            return True
        return False

    def run(self, slhas: List[Input], **kwargs) -> List[Input]:
        """
        Run the passed list of parameters for SPheno.
    
        Args:
            slhas (:obj:`list` of :class:`Input`): Input parameters with a SLHA file that can be processed by SPheno.
        Returns:
            :obj:`list` of :class:`Input`
        """
        if not self._check_path():
            warnings.warn("The path is not valid for " + self.get_name())
        if os.path.exists("Messages.out"):
            os.remove("Messages.out")
        for s in slhas:
            # Remove Creation time for hash-/caching
            comm = "cp " + self.get_output_dir(
            ) + s.slha + " spheno_tmp.in && " + get_path(
            ) + " spheno_tmp.in && mv " + "SPheno.spc " + self.get_output_dir(
            ) + s.slha + " && sed -i '/Created/d' " + self.get_output_dir(
            ) + s.slha
            proc = subprocess.Popen(comm,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            proc.wait()
            update_slha(s)
        if os.path.exists("Messages.out"):
            with open("Messages.out", 'r') as r:
                t = r.read()
                if t != "":
                    warnings.warn(r.read())
        return slhas


# Backward compatibility
spheno_default_runner = SPhenoRunner("~/git/SPheno-3.3.8/")
"""Default SPheno Runner to provide backward compatibility"""
run = spheno_default_runner.run
set_path = spheno_default_runner.set_path
get_path = spheno_default_runner.get_path
