import os
import datetime
import sqlite3
from pyproj import Transformer

destination = "C:/workspace/work/0 coral-cws github/AIS-linker/processed_ais_kirk"

countPoints = 0
countSkipped = 0
countNotParsed = 0
countA = 0
countB = 0


def main():
	global countPoints, countA, countB, countSkipped, countNotParsed
	process(r"C:\Users\grego\Downloads\OneDrive from kirk\AIS Files\ais_receiver.db")

	print("points read:", countPoints)
	print("points skipped:", countSkipped)
	print("points not parsed:", countNotParsed)
	print("class A count:", countA)
	print("class B count:", countB)


def process(filename):
	global countPoints, countA, countB, countSkipped
	# bc algers to lat/lon
	transformer = Transformer.from_crs("EPSG:3005", "EPSG:4326")
	# This object will automatically seek the correct file when we write to it
	rightFile = file_writer(destination)

	with sqlite3.connect(filename) as conn:
		c = conn.cursor()

		print("Table sizes:")
		for statement in ["SELECT count(*) FROM static_data_class_a",
						  "SELECT count(*) FROM static_data_message",
						  "SELECT count(*) FROM position_class_a",
						  "SELECT count(*) FROM position_class_b",
						  "SELECT count(*) FROM position_message",
						  ]:
			c.execute(statement)
			print(statement.split()[-1], c.fetchall())


		c.execute("SELECT datetime, message_class, mmsi, lat, lon FROM position_message")

		while True:
			point = c.fetchone()
			if not point:
				break
			countPoints += 1
			# Parse each piece of information
			dt = datetime.datetime.strptime(point[0][:19], "%Y-%m-%d %H:%M:%S")
			isA = True if point[1] == "position_a" else False
			mmsi = point[2]
			lat = int(point[3]) / 600000
			lon = int(point[4]) / 600000

			if not (dt and mmsi and lat and lon):
				countNotParsed += 1
				print(point)
				continue

			dateTuple = (dt.year, dt.month, dt.day)
			datetimeString = dt.strftime("%Y-%m-%d_%H-%M-%S")

			rightFile.write(dateTuple, datetimeString, str(mmsi), isA, str(lat), str(lon))

			if isA:
				countA += 1
			else:
				countB += 1

	rightFile.close()


# Writes a point to the correct file. Creates folders as needed.
# Note: MUST CLOSE after done writing (using method file_writer.close())
class file_writer:
	def __init__(self, rootFolder=""):
		self.currFile = None
		self.currTime = (0, 0, 0)
		self.rootFolder = rootFolder

	# All of these strings except for dateTuple, which should be of form (year, month, day), and isA, which should be a boolean
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
