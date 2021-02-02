# This script copies AIS data from one of the AIS_linker's databases into a single file
# for any sort of additional processing. Please set the following variables before using:
# 	startDate, endDate, path, outpath

from datetime import datetime, timedelta
import os

# -----------------------------------------------------------------------

# Edit information in this block to change the database and date range

# Start and end dates (year, month, day, hour, minute, second):
startDate = datetime(2018, 1, 1, 0, 0, 0)
endDate = datetime(2018, 1, 2, 0, 0, 0)

# -----------------------------------------------------------------------

# The root path you want to search. The yearly folders should be present at this location
# Remember that python paths always use forward slashes ("/"), not back slashes ("\")
path = "Z:/vol06/AIS_Linker/Processed_ais"

# The name (and path) of the file to create. All of the found data will be copied into this
# single, potentially massive file (depends on database, but potentially ~100MB per month).
# Note: This will overwrite a file if one already exists with the given name, so make sure it
# points somewhere safe. Also make sure it ends in ".txt" (or ".csv", or another convenient
# format)
outpath = "C:/Workspace/ball of AIS.txt"

# -----------------------------------------------------------------------


def main():
	global outpath, path, startDate, endDate
	pointsCopied = 0
	validPathFound = False

	# zero our time of day when determining which files to open
	currentDate = datetime(startDate.year, startDate.month, startDate.day, 0, 0, 0)

	with open(outpath, "w+") as outfile:
		while currentDate < endDate:
			inpath = get_file(path, currentDate)

			if os.path.exists(inpath):
				validPathFound = True

				with open(inpath, 'r') as infile:
					for line in infile:
						lineDate = get_dt(line)

						if startDate < lineDate < endDate:
							outfile.write(line)
							pointsCopied += 1
							if pointsCopied % 10000 == 0:
								print('Working... copied {0} AIS points so far'.format(pointsCopied))

			currentDate += timedelta(days=1)

	print('Done. Copied {0} AIS points in total'.format(pointsCopied))
	if not validPathFound:
		print("Warning: no AIS data was found at the given path over the given date range.", end=' ')
		print("You may wish to check that this information is correct")


def get_file(basePath, dt):
	return os.path.join(basePath, str(dt.year), str(dt.month), str(dt.day), "condensed_ais.txt")


def get_dt(s):
	try:
		return datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]),
						int(s[11:13]), int(s[14:16]), int(s[17:19]))
	except (ValueError, IndexError):
		return datetime.max


if __name__ == '__main__':
	main()
