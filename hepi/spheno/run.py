from typing import List
import warnings
from hepi import get_input_dir
import subprocess
import os
from hepi.input import Input, update_slha
from hepi.run import Runner


class SPhenoRunner(Runner):

    def run(self, slhas: List[Input], **kwargs) -> List[Input]:
        """
        Run the passed list of parameters for SPheno.
    
        Args:
            slhas (:obj:`list` of :class:`Input`): Input parameters with a SLHA file that can be processed by SPheno.
        Returns:
            :obj:`list` of :class:`Input`
        """
        if os.path.exists("Messages.out"):
            os.remove("Messages.out")
        for s in slhas:
            # Remove Creation time for hash-/caching
            comm = "cp " + self.get_output_dir(
            ) + s.slha + " spheno_tmp.in && " + get_path(
            ) + "bin/SPheno spheno_tmp.in && mv " + "SPheno.spc " + self.get_output_dir(
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
