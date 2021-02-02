import os
import re
from datetime import datetime, timedelta

# Get this via "pip install Pillow"
from PIL import Image


targetPath = "C:/Workspace/Work/vessels-may_1st-san-juan"

# how often to print timestamps to the output file
# "1" means every image, while "100" means every hundredth image (any integer is okay)
skip = 1

def main():
	global targetPath
	# each item in datepairs will be a tuple: (file time, image time, filename)
	# All info ends up in datePairs
	datePairs = []
	scan_folder(targetPath, datePairs)
	print_results(datePairs)


# recursively searches a folder for images
def scan_folder(path, datePairs):
	for filename in os.listdir(path):
		filepath = os.path.join(path, filename)

		# Recurse on all folders
		if os.path.isdir(filepath):
			scan_folder(filepath, datePairs)
			continue

		fileTime = get_file_time(filepath)
		if fileTime:
			imageTime = get_image_time(filepath)
			if imageTime:
				datePairs.append((fileTime, imageTime, filename))


def print_results(datePairs):
	global skip
	# Start by sorting our data
	datePairs.sort()
	# Write to a file
	with open("report.csv", "w+") as outfile:
		outfile.write("file time,image time,difference (seconds),file time (seconds),image time (seconds)\n")
		for i, line in enumerate(datePairs):
			if i % skip != 0:
				continue

			# Write human readable first 3 columns
			outfile.write(date_to_string(line[0]) + ",")
			outfile.write(date_to_string(line[1]) + ",")
			outfile.write(str(line[0] - line[1]) + ",")
			# Write both dates as decimal seconds
			outfile.write(str(line[0].timestamp()) + "," + str(line[1].timestamp()) + "\n")


# Gets the CAMERA timestamp of the image
# Returns a datetime object, accurate to the seconds place
def get_image_time(filePath):
	timeStr = ""
	try:
		timeStr = Image.open(filePath)._getexif()[36867]
	except:
		return None
	return datetime(int(timeStr[0:4]), int(timeStr[5:7]), int(timeStr[8:10]),
			int(timeStr[11:13]), int(timeStr[14:16]), int(timeStr[17:19]))

# Gets the PI timestamp of the image
# Returns a datetime object, accurate to the seconds place
def get_file_time(filePath):
	m = re.search(r'(\d\d\d\d).*(\d\d).*(\d\d).*(\d\d).*(\d\d).*(\d\d)', filePath)
	if not m:
		return None
	return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
				 int(m.group(4)), int(m.group(5)), int(m.group(6)))


def date_to_string(date):
	return date.strftime("%m_%d_%Y %H:%M:%S")


if __name__ == '__main__':
	main()
