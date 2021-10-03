# import to set current working directory
from os import path, chdir
from glob import glob

# set current working directory
cwd = path.dirname(path.abspath(__file__))
chdir(cwd)

# file path helper
def file_path(file_name):
	"""This function return full absolute path of given file_name, but it works correctly only when the filename is unique in all folders and subfolders!!!"""
	file_abs_path = path.abspath(glob(f"**/{file_name}", recursive=True)[0])
	return file_abs_path
