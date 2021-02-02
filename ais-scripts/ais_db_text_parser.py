import re
import os
from time import sleep

# This script parses AIS data from the NEMES AIS antennae.
# Author - Gregory O'Hagan (2019)

# NORMA - change this to the top level destination folder desired
# Note that this should be a new folder, or it will simply append to
# files that already exist here
destination = "C:/Users/grego/Desktop/sooke"


# Some global variables for logging
badLines = 0
goodLines = 0
skipLines = 0


def main():
	global badLines, goodLines, skipLines
	# NORMA - change this file path to whatever you want processed
	# If you have multiple files, you can add extra "process" lines
	# Debug should usually be false - it is for helping debug lots of "bad lines"
	# Setting debug to true prints out each line and what is missing in it
	process("D:/ais_receiver_Sooke_July2019.db", debug=False)
	# process("C:/Users/grego/Desktop/unsorted/ais_receiver.db2")
	print("AIS points successfully parsed:", goodLines)
	print("points unsuccessfully parsed (if this is big, double check script):", badLines)
	print("Other lines (database structure sort of thing):", skipLines)


# ----- Everything below here is internal, and shouldn't need editing unless the AIS format changes -----


def process(filename, debug=False):
	global badLines, goodLines, skipLines, destination
	# This object will automatically seek the correct file when we write to it
	rightFile = file_writer(destination)

	with open(filename, "r", encoding="latin-1") as infile:
		line = infile.readline()
		while(line):
			# Look for each piece of required information
			timeM = re.search(r"position_([ab])(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)", line)
			mmsiM = re.search(r'"mmsi": (\d+)(\D)', line)
			latM = re.search(r'"lat": ([-\d\.]+),', line)
			lonM = re.search(r'"lon": ([-\d\.]+),', line)

			# Increment appropriate debug counters depending on matches
			if timeM or mmsiM or latM or lonM:
				if timeM and mmsiM and latM and lonM:
					goodLines += 1

					# Parse all our needed data, plus a file date
					isA = timeM.group(1).startswith("a")
					date = (int(timeM.group(2)), int(timeM.group(3)), int(timeM.group(4)))
					timeStr = timeM.group(2) + "-" + timeM.group(3) + "-" + timeM.group(4) + "_"
					timeStr += timeM.group(5) + "-" + timeM.group(6) + "-" + timeM.group(7)
					lat = str(float(latM.group(1)) / 600000)
					lon = str(float(lonM.group(1)) / 600000)
					mmsi = mmsiM.group(1)

					# Write the data to the correct file. The object handles switching files
					rightFile.write(date, timeStr, mmsi, isA, lat, lon)
				# we found some information, but not all.
				# log
				else:
					badLines += 1
					if debug:
						print(line)
						print("not found:")
						if not timeM:
							print("time")
						if not mmsiM:
							print("mmsi")
						if not latM:
							print("lat")
						if not lonM:
							print("lon")
						print()
						sleep(5)
			else:
				skipLines += 1
			line = infile.readline()


# Writes a point to the correct file. Creates folders as needed.
# Note: MUST CLOSE after done writing (using method file_writer.close())
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
