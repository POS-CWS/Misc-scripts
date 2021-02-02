import re
import os

targetDir = "C:/Workspace/Work/AIS_linker/calibration_db_Saturna camera1"
errorCount = 0


def main():
	folder_recurse(targetDir)


def folder_recurse(path):
	for filename in os.listdir(path):
		# if it's a folder, recurse
		if os.path.isdir(os.path.join(path, filename)):
			folder_recurse(os.path.join(path, filename))
			continue
		# ignore everything that isn't a .csv
		elif not filename.endswith('.csv'):
			continue
		# if it's a file, open it and remove duplicate lines
		# Start by reading the file
		lines = []
		with open(os.path.join(path, filename), 'r') as inFile:
			lines = inFile.readlines()
		# remove any duplicates. If we throw an error, doing this before opening the outfile
		# prevents us from overwriting anything
		dupesRemoved = 0
		timesStillEqual = 0
		i = 0
		while i < len(lines):
			j = i + 1
			while j < len(lines):
				if lines[j].startswith(lines[i]):
					lines.remove(lines[j])
					dupesRemoved += 1
				elif lines[j].split(',')[0] == lines[i].split(',')[0]:
					timesStillEqual += 1
				else:
					j += 1
			i += 1

		lines = order_by_sec_time(lines)

		# Ensure the lines are in order
		# This should never trigger the exit condition because of the sort right above
		times = []
		for line in lines:
			times.append(int(line.split(',')[0]))
		prevTime = -1
		for time in times:
			if time <= prevTime:
				global errorCount
				errorCount += 1
				print("ERROR: " + str(errorCount) + " times out of order in file " + os.path.join(path, filename))
				print("Exiting")
				exit(-1)
			prevTime = time

		# replace the file
		with open(os.path.join(path, filename), 'w+') as outFile:
			for line in lines:
				outFile.write(line)

		print("Processed file " + os.path.join(path, filename) +". " + str(dupesRemoved) + " duplicates removed. " + str(timesStillEqual) + " times still equal")


def sec_time_from_string(line):
	return int(line.split(',')[0])


def order_by_sec_time(lines):
	result = []
	while len(lines) > 0:
		minPos = 0
		minVal = sec_time_from_string(lines[0])
		for i, line in enumerate(lines):
			lineVal = sec_time_from_string(line)
			if lineVal < minVal:
				minPos = i
				minVal = lineVal
		result.append(lines[minPos])
		lines.remove(lines[minPos])
	return result


if __name__ == "__main__":
	main()
