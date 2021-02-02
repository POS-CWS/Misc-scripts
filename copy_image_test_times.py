# A script for copying a file across a bunch of times to attempt to home in on linking with
# AIS info
# Places copied files in the same path as the input file
# Author: Gregory O'Hagan


import re
import os
from datetime import datetime, timedelta
from shutil import copyfile


def copy_image_across_times(inpath, searchRange=24):
	split = os.path.split(inpath)
	path = os.path.join(*list(split[:-1]))
	filename = str(split[-1:])
	m = re.search(r"capture_(\d\d\d\d).(\d\d).(\d\d).(\d\d).(\d\d).(\d\d).*\.jpg", filename)
	if not m:
		print("Usage: could not parse time from filename")
		return

	origTime = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))

	for hoursChange in range(0 - searchRange, searchRange + 1, 1):
		if hoursChange == 0:
			continue
		newname = datetime_to_filename(origTime - timedelta(hours=hoursChange))
		copyfile(inpath, os.path.join(path, newname))


# Creates a filename formatted for the clicky tool out of a datetime object
def datetime_to_filename(date):
	filename = "capture_" + str(date.year) + "-"
	if date.month < 10:
		filename += "0"
	filename += str(date.month) + "-"
	if date.day < 10:
		filename += "0"
	filename += str(date.day) + "_"
	if date.hour < 10:
		filename += "0"
	filename += str(date.hour) + "-"
	if date.minute < 10:
		filename += "0"
	filename += str(date.minute) + "-"
	if date.second < 10:
		filename += "0"
	filename += str(date.second) + ".jpg"
	return filename


if __name__ == '__main__':
	copy_image_across_times("Z:/vol03/Haro_Strait_Raw/2018/6_June_Processed/28/Contacts/Vessels/time_test/capture_2018-06-28_16-06-02.jpg")
