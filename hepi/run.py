from hepi.util import DictData


class RunParam(DictData):
	def __init__(self,skip:bool=False):
		self.skip = skip
