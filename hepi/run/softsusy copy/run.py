import os
import subprocess
import warnings
from typing import List

from hepi.input import Input, update_slha
from hepi.run import Runner


class SPhenoRunner(Runner):
    def _check_path(self) -> bool:
        if os.path.exists(os.path.expanduser(self.get_path() + "/bin/softpoint.x")):
            self.set_path(self.get_path() + "/bin/softpoint.x")
            return True
        if self.get_path().endswith("softpoint.x"):
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
        for s in slhas:
            # Remove Creation time for hash-/caching
            comm = (
                "cp "
                + self.get_output_dir()
                + s.slha
                + " softsusy_tmp.in && "
                + get_path()
                + " leshouches < softsusy_tmp.in > Softsusy.spc"
                + " && mv "
                + "Softsusy.spc "
                + self.get_output_dir()
                + s.slha
#                + " && sed -i '/Created/d' "
#                + self.get_output_dir()
#                + s.slha
            )
            #print(comm)
            proc = subprocess.Popen(
                comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            proc.wait()
            # get proc return code
            if proc.returncode != 0:
                warnings.warn("softsusy failed")
            update_slha(s)
        return slhas


# Backward compatibility
spheno_default_runner = SPhenoRunner("softpoint.x")
"""Default SoftSusy Runner to provide backward compatibility"""
run = spheno_default_runner.run
set_path = spheno_default_runner.set_path
get_path = spheno_default_runner.get_path
