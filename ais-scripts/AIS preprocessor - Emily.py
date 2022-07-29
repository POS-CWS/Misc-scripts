import re
import os
from time import sleep

# This script parses AIS data from the Scottish receivers
# Author - Gregory O'Hagan (2022)
# Based on this previous processing script:
# https://github.com/POS-CWS/Misc-scripts/blob/main/ais-scripts/ais_db_text_parser.py

# ***----------------------------------------------------------------------------------------------***
# *** Change just these variables ***

# The source folder will be (recursively) scanned for any files that start with "AISoutput_"
source = "C:/Users/grego/Downloads"
# The destination folder is the root
destination = "C:/workspace/work/test"
# ***----------------------------------------------------------------------------------------------***

# *** Everything below here is internal, and shouldn't need editing unless the AIS format changes ***

# Some global variables for logging
badLines = 0
goodLines = 0
skipLines = 0

def main():
	global badLines, goodLines, skipLines
	process()
	# process("C:/Users/grego/Desktop/unsorted/ais_receiver.db2")
	print("AIS points successfully parsed:", goodLines)
	print("points unsuccessfully parsed (if this is big, double check script):", badLines)
	print("points successfully parsed, but skipped due to duplicate mmsi/time:", skipLines)


def process():
	global badLines, goodLines, skipLines, source, destination

	# This object will automatically seek the correct file when we write to it
	rightFile = file_writer(destination)

	for filepath in get_file_list(source):
		with open(filepath, 'r') as infile:
			schema = infile.readline().split(',')

			mmsiIndex = schema.index("~MMSI")
			timeIndex = schema.index("Received Time UTC")
			latIndices = [i for i, x in enumerate(schema) if x == "Latitude"]
			lonIndices = [i for i, x in enumerate(schema) if x == "Longitude"]
			isAIndices = [i for i, x in enumerate(schema) if x == "Radio Channel"]

			# Checks on schema parsing. This is hardcoded, but useful as a warning flag if anything changes.
			if not 0 <= mmsiIndex: print("Error: mmsi index not found")
			if not 0 <= timeIndex: print("Error: time index not found")
			if not len(latIndices) == 5: print("Warning: found {} latitude indices".format(len(latIndices)))
			if not len(lonIndices) == 5: print("Warning: found {} longitude indices".format(len(lonIndices)))
			if not len(isAIndices) == 4: print("Warning: found {} ais class (a/b) indices".format(len(isAIndices)))

			for line in infile.readlines():
				splt = line.split(',')

				mmsi = splt[mmsiIndex]
				t = convert_time_string(splt[timeIndex])

				lat = None
				for i in latIndices:
					lat = interpret_lat_lon(splt[i])
					if lat:
						break

				lon = None
				for i in lonIndices:
					lon = interpret_lat_lon(splt[i])
					if lon:
						break

				isA = None
				for i in isAIndices:
					isA = parse_isA(splt[i])
					if isA:
						break

				if not mmsi or not t or not lat or not lon or isA is None:
					badLines += 1
					continue

				goodLines += 1
				timeStr = "{}-{}-{}_{}-{}-00".format(*t)
				dateTuple = t[:3]
				rightFile.write(dateTuple, timeStr, mmsi, isA, "{:6f}".format(lat), "{:6f}".format(lon))

	rightFile.close()


# Recursively finds all target files in a given root
def get_file_list(root):
	filelist = []
	for filename in os.listdir(root):
		filepath = os.path.join(root, filename)
		if os.path.isdir(filepath):
			filelist.extend(get_file_list(filepath))
		elif filename.startswith("AISoutput_"):
			filelist.append(filepath)
	return filelist


# Converts a string containing either a decimal or a degree/minute lat or lon into a float value
# Returns None if parsing isn't successful
def interpret_lat_lon(s):
	try:
		return float(s)
	except:
		m = re.match(r"(\d+)° (\d+\.\d*)' ([NSEW])", s)
		if not m:
			return None

		degrees, minutes, direction = m.groups()

		# Borrowed from:
		# https://stackoverflow.com/questions/33997361/how-to-convert-degree-minute-second-to-degree-decimal
		dd = float(degrees) + float(minutes)/60
		if direction == 'E' or direction == 'S':
			dd *= -1
		return dd


# Converts the time string from what's in the files to a (year, month, day, hour, minute, second) tuple of strings
# Returns None if parsing isn't successful
def convert_time_string(s):
	m = re.match(r"(\d\d)/(\d\d)/(\d\d\d\d) (\d\d):(\d\d)", s)
	if not m:
		return None

	day, month, year, hour, minute = m.groups()
	return year, month, day, hour, minute, "00"


# Returns "A" or "B", or None if parsing isn't successful
def parse_isA(s):
	if s.startswith("A"):
		return True
	elif s.startswith("B"):
		return False
	return None


# Writes a point to the correct file. Creates folders as needed.
# Note: MUST CLOSE after done writing (using method file_writer.close())
# Copied from ais_db_text_parser.py:
class file_writer:
	def __init__(self, rootFolder=""):
		self.currFile = None
		self.currTime = (0, 0, 0)
		self.rootFolder = rootFolder

	# All of these strings except for dateTuple, which should be of form (year, month, day)
	def write(self, dateTuple, timeStr, mmsi, isA, lat, lon):
		# Seek to correct file
		if dateTuple != self.currTime:
			self._switch_file(dateTuple)

		# write information to the file
		self.currFile.write(timeStr + "," + mmsi + ",")
		self.currFile.write("A,") if isA else self.currFile.write("B,")
		self.currFile.write(lat + "," + lon + "\n")

	# Internal method to change the open file.
	def _switch_file(self, dateTuple):
		# close old file
		if self.currFile:
			self.currFile.close()

		# ensure we have all the folder structure that we need
		outpath = os.path.join(self.rootFolder, str(dateTuple[0]), str(dateTuple[1]), str(dateTuple[2]))
		if not os.path.exists(outpath):
			os.makedirs(outpath)

		# open the new file and update what time it is for
		self.currFile = open(os.path.join(outpath, "condensed_ais.txt"), "a")
		self.currTime = dateTuple

	# closes the final file properly when finished
	def close(self):
		self.currTime = (0, 0, 0)
		self.currFile.close()
		self.currFile = None


if __name__ == '__main__':
	main()
