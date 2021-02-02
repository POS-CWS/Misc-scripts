import re
import os
from time import sleep
import sqlite3

destination = "C:/Users/grego/Desktop/parsed_ais"

countPoints = 0
countSkipped = 0
countNotParsed = 0
countA = 0
countB = 0


def main():
	global countPoints, countA, countB, countSkipped, countNotParsed
	process("C:/Users/grego/Downloads/LKECHOsqlite20180714.sqlite3")

	print("points read:", countPoints)
	print("points skipped:", countSkipped)
	print("points not parsed:", countNotParsed)
	print("class A count:", countA)
	print("class B count:", countB)


def process(filename, debug=False):
	global countPoints, countA, countB, countSkipped, countNotParsed, destination
	# This object will automatically seek the correct file when we write to it
	rightFile = file_writer(destination)

	with sqlite3.connect(filename) as conn:
		c = conn.cursor()
		res = c.execute('SELECT UTC, shipType, imoNumber, latitude, longitude FROM AISData')
		while True:
			point = c.fetchone()
			if not point:
				break
			countPoints += 1

			# Parse each piece of information
			time = point[0]
			shipType = point[1]
			mmsi = point[2]
			lat = point[3]
			lon = point[4]

			if not (time and mmsi and lat and lon):
				countNotParsed += 1
				print(point)
				continue

			# print(type(time), type(shipType), type(mmsi), type(lat), type(lon))
			# Get class A or B ais
			# Override based on observation of data
			isA, isB = False, False
			if not (shipType):
				isB = True
			else:
				isA = shipType[:7] == 'Class A'
				isB = shipType[:7] == 'Class B'

			if isA:
				countA += 1
			elif isB:
				countB += 1

			# Override based on observation of data
			else:
				isA = True
				countA += 1

			date = (time[:4], time[5:7], time[8:10])
			# Reformat the time string like we want it:
			time = list(time)
			time[10], time[13], time[16] = '_', '-', '-'
			time = time[:19]
			time = "".join(time)

			rightFile.write(date, time, str(mmsi), isA, str(lat), str(lon))

	rightFile.close()


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
