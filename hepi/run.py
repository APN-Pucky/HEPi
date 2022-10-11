from concurrent.futures import ThreadPoolExecutor
from logging import warning
import os
import subprocess
from subprocess import Popen, PIPE
from typing import List
import warnings

import numpy as np
from hepi.input import Input, Order, get_input_dir, get_output_dir, get_pre
from hepi.results import Result
from hepi.util import DL2DF, LD2DL, DictData, namehash
from smpl.parallel import par
import time
import tqdm
from pqdm.threads import pqdm as tpqdm
from pqdm.processes import pqdm as ppqdm
import multiprocessing as mp
#from pqdm.processes import pqdm


def my_parallel(f, arr, n_jobs=None, desc=None):
    """
    Parallel execution of f on each element of args

    Examples
    --------
    >>> my_parallel(lambda x : x**2, range(0,5))
    [0, 1, 4, 9, 16]

    """
    n_jobs = n_jobs or mp.cpu_count()
    sa = np.array_split(np.array(arr), len(arr) / n_jobs)
    res = []
    for i in tqdm.tqdm(range(len(sa)), desc=desc):
        res += par(f, sa[i])
    return res


class RunParam(DictData):
    """Abstract class that is similar to a dictionary but with fixed keys."""

    def __init__(self,
                 skip: bool = False,
                 in_file: str = None,
                 out_file: str = None,
                 execute: str = None,
                 name: str = None):
        self.name = name
        self.skip = skip
        self.in_file = in_file
        self.out_file = out_file
        self.execute = execute


class Runner:

    def __init__(self,
                 path: str,
                 in_dir: str = None,
                 out_dir: str = None,
                 pre=None):
        self.path = path
        if in_dir is None:
            self.in_dir = get_input_dir()
        else:
            self.in_dir = in_dir
        if out_dir is None:
            self.out_dir = get_output_dir()
        else:
            self.out_dir = out_dir
        if pre is None:
            self.pre = get_pre()
        else:
            self.pre = pre

    def orders(self) -> List[Order]:
        """List of supported Orders in this runner."""
        return [e.value for e in Order]

    def get_name(self) -> str:
        """Returns the name of the runner."""
        return type(self).__name__

    def get_version(self) -> str:
        return "?"

    def _sub_run(self, coms: List[str]) -> str:
        process = Popen(coms, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        if exit_code != 0:
            return err.decode()
        else:
            return output.decode()

    def _check_path(self) -> bool:
        """Checks if the passed path is valid."""
        return True

    def _prepare(self, p: Input, skip=False, assume_valid = False, **kwargs) -> RunParam:
        skip_ = skip
        d = p.__dict__
        d["runner"] = str(type(self).__name__) + "-" + self.get_version(
        )  # TODO re add version, but removed for reusable hashing!
        name = namehash("_".join("".join(str(_[0]) + "_" + str(_[1]))
                                 for _ in d.items()).replace("/", "-"))
        #print(name)
        skip = False
        if skip_ and os.path.isfile(self.get_output_dir() + name +
                                    ".out") and (assume_valid or self._is_valid(
                                        self.get_output_dir() + name + ".out",
                                        p,
                                        d,
                                        skip=skip_,
                                        **kwargs)):
            #print(".", end='')
            skip = True
        else:
            #print('|', end='')
            pass
        return RunParam(execute=self.get_output_dir() + name + ".sh",
                        in_file=self.get_output_dir() + name + ".in",
                        out_file=self.get_output_dir() + name + ".out",
                        skip=skip,
                        name=name)

    def _check_input(self, param: Input, **kwargs) -> bool:
        if param.order not in self.orders():
            warnings.warn("Order " + str(param.order) + " not supported in " +
                          type(self).__name__)
            return False
        return True

    def _prepare_all(self,
                     params: List[Input],
                     skip=True,
                     n_jobs = None,
                     **kwargs) -> List[RunParam]:
        """
        Prepares all parameters for execution.

        Args:
            params (List[:class:`hepi.Input`]): List of input parameters.
            skip (bool, optional): If True, the runner will check if the output file already exists and skip the execution if it does. Defaults to True.
            n_jobs (int): Number of parallel jobs. If None, use all available cores.
        """
        ret = []

        #ret = my_parallel(self._check_input,params,desc="Checking input")
        ret = tpqdm(params,
                    self._check_input,
                    n_jobs=n_jobs if n_jobs is not None else mp.cpu_count(),
                    desc="Checking input")
        if not np.alltrue(ret):
            warnings.warn("Check input failed.")
            return []
        #ret = my_parallel(
        #    lambda p: self._prepare(p, skip=skip, **kwargs),
        #    params,
        #    #n_jobs=mp.cpu_count(),
        #    desc="Preparing")
        args = [{'p': p, 'skip': skip, **kwargs} for p in params]
        ret = ppqdm(args,
                    self._prepare,
                    n_jobs=n_jobs if n_jobs is not None else mp.cpu_count(),
                    argument_type='kwargs',
                    desc="Preparing")
        skipped = 0
        not_skipped = 0
        for r in ret:
            if r.skip:
                skipped += 1
            else:
                not_skipped += 1
        print("Skipped: " + str(skipped) + " Not skipped: " + str(not_skipped))
        #for p in params:
        #    if not self._check_input(p):
        #        warnings.warn("Check input failed.")
        #        return []
        #    ret.append(self._prepare(p, skip=skip, **kwargs))
        return ret

    def run(self,
            params: List[Input],
            skip=True,
            parse=True,
            parallel=True,
            sleep=0,
            run=True,
            ignore_error=False,
            n_jobs = None,
            **kwargs):
        """
		Run the passed list of parameters.

		Args:
		    params (:obj:`list` of :class:`hepi.Input`): All parameters that should be executed/queued.
		    skip (bool): True means stored runs will be skipped. Else the are overwritten.
		    parse (bool): Parse the results. 
		        This is not the prefered cluster/parallel mode, as there the function only queues the job.
		    parallel (bool): Run jobs in parallel.
		    sleep (int): Sleep seconds after starting job.
            run (bool): Actually start/queue runner.
            ignore_error (bool): Continue instead of raising Exceptions. Also ignores hash collisions.
            n_jobs (int): Number of parallel jobs. If None, use all available cores.

		Returns:
		    :obj:`pd.DataFrame` : combined dataframe of results and parameters. The dataframe is empty if `parse` is set to False.

		"""
        if not self._check_path():
            warnings.warn("The path is not valid for " + self.get_name())
            if not ignore_error:
                raise RuntimeError("The path is not valid for " +
                                   self.get_name())
        rps = self._prepare_all(params,
                                parse=parse,
                                skip=skip,
                                ignore_error=ignore_error,
                                n_jobs=n_jobs,
                                **kwargs)
        #print("= " + str(len(params)) + " jobs")
        if sleep is None:
            sleep = 0 if parse else 5
        if run:
            self._run(rps,
                      wait=parse,
                      parallel=parallel,
                      sleep=sleep,
                      n_jobs = n_jobs,
                      **kwargs)
        if parse:
            outs = LD2DL(rps)["out_file"]
            results = self.parse(outs,n_jobs=n_jobs)
            rdl = LD2DL(results)
            pdl = LD2DL(params)
            return DL2DF({**rdl, **pdl})
        return DL2DF({})

    def _run(self,
             rps: List[RunParam],
             wait=True,
             parallel=True,
             sleep=0,
             n_jobs = None,
             **kwargs):
        """
		Runs Runner per :class:`RunParams`.
	
		Args:
		    rps (:obj:`list` of :class:`RunParams`): Extended run parameters.
		    bar (bool): Enable info bar.
		    wait (bool): Wait for parallel runs to finish.
		    sleep (int): Sleep seconds after starting subprocess.
		    parallel (bool): Run jobs in parallel.
            n_jobs (int): Number of parallel jobs. If None, use all available cores.
	
		Returns:
		    :obj:`list` of int: return codes from jobs if `no_parse` is False.
		"""
        # get cluster or niceness prefix
        template = self.get_pre() + " " + "{}"

        # Run commands in parallel
        processes = []
        cmds = []

        for rp in rps:
            if not rp.skip:
                command = template.format(rp.execute)
                cmds.append(command)

        if wait and parallel:
            return tpqdm(cmds,
                  lambda c: subprocess.call(c,shell=True),
                  n_jobs=n_jobs if n_jobs is not None else mp.cpu_count(),
                  desc="Running")
            #with ThreadPoolExecutor(max_workers=n_jobs if n_jobs is not None else mp.cpu_count()) as executor:
            #    for cmd in cmds:
            #        processes.append(executor.submit(subprocess.call, cmd, shell=True))
            #        time.sleep(sleep)
            #    return [p.result() for p in processes]

        for command in cmds:
            command = template.format(rp.execute)
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

    def _is_valid(self, file: str, p: Input, d, **kwargs) -> bool:
        """
		Verifies that a file is a complete output.
	
		Args:
		    file (str): File path to be parsed.
		    p (:class:`hepi.Input`): Onput parameters.
		    d (:obj:`dict`): Param dictionary.
	
		Returns:
		    bool : True if `file` could be parsed.
		"""
        res = self._parse_file(file)
        if res.LO is None and p.order is Order.LO:
            return False
        if res.NLO is None and p.order is Order.NLO:
            return False
        if res.NLO_PLUS_NLL is None and p.order is Order.NLO_PLUS_NLL:
            return False
        if res.aNNLO_PLUS_NNLL is None and p.order is Order.aNNLO_PLUS_NNLL:
            return False
        return True

    def parse(self, outputs: List[str],n_jobs=None) -> List[Result]:
        """
		Parses Resummino output files and returns List of Results.
	
		Args:
		    outputs (:obj:`list` of `str`): List of the filenames to be parsed.
            n_jobs (int): Number of parallel jobs. If None, use all available cores.
	
		Returns:
		    :obj:`list` of :class:`hepi.resummino.result.ResumminoResult`
	
		"""
        rsl = []
        #for r in parallel(self._parse_file, outputs):
        #    rsl.append(r)

        # parallelized opens to many files at times
        #rsl = my_parallel(self._parse_file, outputs, desc="Parsing")
        rsl = tpqdm(outputs,
                   self._parse_file,
                   n_jobs=n_jobs if n_jobs is not None else mp.cpu_count(),
                   desc="Parsing")
        return rsl
        #for o in tqdm.tqdm(outputs):
        #    rsl.append(self._parse_file(o))
        #return rsl

    def _parse_file(self, file: str) -> Result:
        """
		Extracts results from an output file.

		Args:
		    file (str): File path to be parsed.

		Returns:
		    :class:`Result` : If a value is not found in the file None is used.

		"""
        return None

    def get_path(self) -> str:
        """
		Get the Runner path.

		Returns:
		    str: current Runner path.
		"""
        return self.path

    def get_input_dir(self) -> str:
        """
		Get the input directory.

		Returns:
		    str: :attr:`in_dir`
		"""
        return self.in_dir

    def get_output_dir(self) -> str:
        """
		Get the input directory.

		Returns:
		    str: :attr:`out_dir`
		"""
        return self.out_dir

    def get_pre(self) -> str:
        """
		Gets the command prefix.

		Returns:
		    str: :attr:`pre`
		"""
        return self.pre

    def set_path(self, p: str):
        """
		Set the path to the Runner folder containing the binary in './bin' or './build/bin'.

		Args:
		    p (str): new path.
		"""
        if os.path.isdir(p):
            self.path = p + ("/" if p[-1] != "/" else "")
        self.path = p

    def set_input_dir(self, indir: str):
        """
		Sets the input directory.

		Args:
		    indir (str): new input directory.
		"""
        self.in_dir = indir

    def set_output_dir(self, outdir: str, create: bool = True):
        """
		Sets the output directory.

		Args:
		    outdir (str): new output directory.
			create (bool): create directory if not existing.
		"""
        if create:
            os.makedirs(outdir, exist_ok=True)
        self.out_dir = outdir

    def set_pre(self, ppre: str):
        """
		Sets the command prefix.

		Args:
		    ppre (str): new command prefix.
		"""
        self.pre = ppre
