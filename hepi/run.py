from hepi.util import DictData


class RunParam(DictData):
	"""Abstract class that is similar to a dictionary but with fixed keys."""
	def __init__(self,skip:bool=False):
		self.skip = skip
