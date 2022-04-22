import abc
import os
import subprocess
from typing import List
import warnings
from hepi.input import Input, get_input_dir, get_output_dir, get_pre
from hepi.results import Result
from hepi.util import LD2DL, DictData, namehash
from smpl.parallel import par
from smpl import debug
import time
import shutil




class RunParam(DictData):
	"""Abstract class that is similar to a dictionary but with fixed keys."""
	def __init__(self,skip:bool=False,in_file:str=None,out_file:str=None,execute:str=None,name:str=None):
		self.name = name
		self.skip = skip
		self.in_file = in_file
		self.out_file = out_file
		self.execute= execute

class Runner:
	def __init__(self,path:str, in_dir:str=None,out_dir:str=None,pre=None):
		self.path = path
		if in_dir is None:
			self.in_dir = get_input_dir()
		else:
			self.in_dir= in_dir
		if out_dir is None:
			self.out_dir = get_output_dir()
		else:
			self.out_dir= out_dir
		if pre is None:
			self.pre= get_pre()
		else:
			self.pre = pre

	def _prepare(self,p: Input,skip=True,**kwargs) -> RunParam:
		skip_ = skip
		d = p.__dict__
		d["runner"] = type(self).__name__
		name = namehash("_".join("".join(str(_[0]) + "_" + str(_[1]))
			for _ in d.items()).replace("/", "-"))
		#print(name)
		skip = False
		if skip_ and os.path.isfile(self.get_output_dir() + name + ".out") and self._is_valid(self.get_output_dir() + name + ".out",p,d):
			print("skip", end='')
			skip = True
		return RunParam(execute=self.get_output_dir()+name + ".sh",in_file=self.get_output_dir()+name + ".in", out_file=self.get_output_dir()+name + ".out",skip= skip,name=name)

	def _check_input(self,param: Input,**kwargs) -> bool:
		return True


	def _prepare_all(self,params: List[Input],**kwargs) -> List[RunParam]:
		ret = []
		for p in params:
			if not self._check_input(p):
				warnings.warn("Check input failed.")
				return []
			ret.append(self._prepare(p,**kwargs))
		return ret

	def run(self,params: List[Input], parse=True,parallel=True,sleep=0,**kwargs):
		"""
		Run the passed list of parameters.

		Args:
		    params (:obj:`list` of :class:`hepi.Input`): All parameters that should be executed/queued.
		    skip (bool): True means stored runs will be skipped. Else the are overwritten.
		    parse (bool): Parse the results. 
		        This is not the prefered cluster/parallel mode, as there the function only queues the job.
		    parallel (bool): Run jobs in parallel.
		    sleep (int): Sleep seconds after starting job.

		Returns:
		    :obj:`dict` : combined dictionary of results and parameters. Each member therein is a list.
		        The dictionary is empty if `parse` is set to False.

		"""
		print("Running: " + str(len(params))  +" jobs" )
		rps = self._prepare_all(params,parse=parse,**kwargs )
		if sleep is None:
			sleep = 0 if parse else 5
		self._run(rps, wait=parse,parallel=parallel,sleep=sleep,**kwargs)
		if parse:
			outs = LD2DL(rps)["out_file"]
			results = self.parse(outs)
			rdl = LD2DL(results)
			pdl = LD2DL(params)
			return {**rdl, **pdl}
		return {}

	def _run(self,rps: List[RunParam], wait=True,parallel=True,sleep=0,**kwargs):
		"""
		Runs Runner per :class:`RunParams`.
	
		Args:
		    rps (:obj:`list` of :class:`RunParams`): Extended run parameters.
		    bar (bool): Enable info bar.
		    wait (bool): Wait for parallel runs to finish.
		    sleep (int): Sleep seconds after starting subprocess.
		    parallel (bool): Run jobs in parallel.
	
		Returns:
		    :obj:`list` of int: return codes from jobs if `no_parse` is False.
		"""
		# get cluster or niceness prefix
		template = self.get_pre() + " " +  "{}"
	
		# Run commands in parallel
		processes = []
	
		for rp in rps:
			if not rp.skip:
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

	def _is_valid(self,file:str,p:Input,d) -> bool:
		"""
		Verifies that a file is a complete output.
	
		Args:
		    file (str): File path to be parsed.
		    p (:class:`hepi.Input`): Onput parameters.
		    d (:obj:`dict`): Param dictionary.
	
		Returns:
		    bool : True if `file` could be parsed.
		"""
		return True

	def parse(self,outputs: List[str]) -> List[Result]:
		"""
		Parses Resummino output files and returns List of Results.
	
		Args:
		    outputs (:obj:`list` of `str`): List of the filenames to be parsed.
	
		Returns:
		    :obj:`list` of :class:`hepi.resummino.result.ResumminoResult`
	
		"""
		rsl = []
		for r in par(self._parse_file, outputs):
			rsl.append(r)
		return rsl

	def _parse_file(self,file : str) -> Result:
		"""
		Extracts results from an output file.

		Args:
		    file (str): File path to be parsed.

		Returns:
		    :class:`Result` : If a value is not found in the file None is used.

		"""
		return None

	def get_path(self) ->str:
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

	def set_path(self,p:str):
		"""
		Set the path to the Runner folder containing the binary in './bin'.

		Args:
		    p (str): new path.
		"""
		self.path = p + ("/" if p[-1]!="/" else "")

	def set_input_dir(self,ind:str):
		"""
		Sets the input directory.

		Args:
		    ind (str): new input directory.
		"""
		self.in_dir = ind


	def set_output_dir(self,outd:str):
		"""
		Sets the output directory.

		Args:
		    outd (str): new output directory.
		"""
		self.out_dir = outd


	def set_pre(self,ppre:str):
		"""
		Sets the command prefix. 

		Args:
		    ppre (str): new command prefix.
		"""
		self.pre = ppre

