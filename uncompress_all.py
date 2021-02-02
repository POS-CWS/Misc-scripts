import re
import os
import gzip
import shutil


def main():
	process("Z:/vol01/AIS_ONC_BoundaryPass_Raw")
	# process("C:/Workspace/Work/AIS_linker/Processed_ais/2018")


def process(path):
	for filename in os.listdir(path):
		filepath = os.path.join(path, filename)
		if os.path.isdir(filepath):
			process(filepath)
		elif filepath.endswith(".gz"):
			outpath = filepath[:-3] + ".txt"
			if os.path.exists(outpath):
				continue
			with gzip.open(filepath, 'rb') as f_in:
				with open(outpath, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
	main()
