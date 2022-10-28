import os
import importlib.resources

def list_files():
	"""
	List all files in the data directory

	Returns
	-------
	list
		List of files in the data directory

	"""
	return  [os.path.basename(b) for b in importlib.resources.files('.'.join(__name__.split(".")[:-1])).joinpath("json").iterdir()]

def get_file(filename):
	"""
	Get the content of a file in the data directory

	Parameters
	----------
	filename : str
		Name of the file

	Returns
	-------
	str
		Content of the file

	"""
	return importlib.resources.files('.'.join(__name__.split(".")[:-1])).joinpath("json").joinpath( filename)