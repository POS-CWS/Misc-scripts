# Short utility with copy/pasted code from the file copy sort tool.
# Recreates as much of the original folder structure as needed to copy
# all 'condensed_ais.txt' files
# This copies the part that the clicky type tools needs

import re
import sys
import os
import time
from datetime import date, timedelta
import shutil

from PyQt4 import QtCore
from PyQt4.QtGui import *

from functools import partial

# Used in the copy_file method. This (and copy_file method) is based on code by Michael Burns:
# https://stackoverflow.com/questions/22078621/python-how-to-copy-files-fast
try:
	O_BINARY = os.O_BINARY
except:
	O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
BUFFER_SIZE = 128 * 1024

# Determine which version of python we are working with, for the copy method.
# Print warning if using 3
py2 = True
if sys.version_info > (3, 0):
	py2 = False
	print("Warning: this script is designed for python 2, but is currently running on python 3")
	print("This will cause it to run much slower (roughly 1/3 to 1/4 of the python 2 speed)")


def main():
	inpath = "C:/Workspace/Work/AIS_linker/Processed_ais/raw/2018"
	outpath = "C:/Workspace/Work/AIS_linker/Processed_ais/2018"
	search_folder(inpath, outpath)


def search_folder(inpathBase, outpathBase, subfolder='', recurse=True):
	print("Searching folder: " + os.path.join(inpathBase, subfolder))
	print("Found " + str(len(os.listdir(os.path.join(inpathBase,subfolder)))) + " items")
	for filename in os.listdir(os.path.join(inpathBase, subfolder)):
		# recurse if needed
		if os.path.isdir(os.path.join(inpathBase, subfolder, filename)) and recurse:
			search_folder(inpathBase, outpathBase, os.path.join(subfolder, filename), recurse)
		# copy only this text file
		elif re.search('^condensed_ais.txt$', filename):
			# recreate original folder structure if needed
			dstFolder = os.path.join(outpathBase, subfolder)
			if not os.path.exists(dstFolder):
				os.makedirs(dstFolder)
			copyfile(os.path.join(os.path.join(inpathBase, subfolder), filename),
					 os.path.join(dstFolder, filename))


# Copies a file. Works quickly in Python 2.
# Based on code by Michael Burns:
# https://stackoverflow.com/questions/22078621/python-how-to-copy-files-fast
def copyfile(src, dst):
	global py2
	if py2:
		try:
			fin = os.open(src, READ_FLAGS)
			stat = os.fstat(fin)
			fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
			for x in iter(lambda: os.read(fin, BUFFER_SIZE), ""):
				os.write(fout, x)
		finally:
			try:
				os.close(fin)
			except:
				pass
			try:
				os.close(fout)
			except:
				pass
	# This version allows for python 3 compatibility, but is MUCH slower
	else:
		shutil.copy2(src, dst)

if __name__ == '__main__':
	main()
