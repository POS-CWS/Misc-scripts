import os
import re
from datetime import datetime, timedelta, date

# inpath = r"C:\workspace\work\aishub\May_2020_AISHub_Boundary_Pass"
# inpath = r"C:\workspace\work\aishub\June_2020_AISHub_Boundary_Pass"
# inpath = r"C:\workspace\work\aishub\July_2020_AISHub_Boundary_Pass"
inpath = r"C:\Users\CORAL\Downloads\June2021_AISHub_BoundaryPass\new"
outpath = r"C:\Users\CORAL\Downloads\June2021_AISHub_BoundaryPass\new"

# inpath = r"C:\Users\CORAL\Downloads\June2021_AISHub_BoundaryPass\new"
# outpath = r"C:\Users\CORAL\Downloads\June2021_AISHub_BoundaryPass\new"


def main():
	global inpath, outpath
	currfile = None
	currDate = date(2000, 1, 1)
	skipped = 0
	countA = 0
	countB = 0
	for filename in os.listdir(inpath):
		if not filename.endswith('.csv'):
			continue
		filepath = os.path.join(inpath, filename)
		with open(filepath, 'r') as infile:
			for line in infile.readlines():
				split = line.split(',')
				if not (is_int(split[0]) and len(split) >= 9):
					skipped += 1
					continue

				rawdt = split[1]
				# strip off quotation marks sometimes present in .csv files
				rawdt = rawdt.replace('"', '').replace("'", '')

				dt = rawdt.split(' ')[0].split('-')
				y, m, d = dt
				if d.startswith('0'):
					d = d[1:]
				if m.startswith('0'):
					m = m[1:]
				newCurrDate = date(int(y), int(m), int(d))

				mmsi = split[0]
				datetimeStr = rawdt.replace(' ', '_')
				datetimeStr = datetimeStr.replace(':', '-')
				lat = split[6]
				lon = split[5]
				aisClass = split[2]
				# Skip 14 and 24 as they can be class A or B
				if aisClass in ('14', '24'):
					skipped += 1
					continue
				else:
					if aisClass in ('18', '19'):
						aisClass = "B"
						countB += 1
					else:
						aisClass = "A"
						countA += 1


				if not (is_float(lat) and is_float(lon) and is_int(mmsi)):
					skipped += 1
					continue

				# Seek correct file/directory
				if not currDate == newCurrDate:
					targetPath = os.path.join(outpath, y, m, d)
					if not os.path.exists(targetPath):
						os.makedirs(targetPath)
						if currfile:
							currfile.close()
						currfile = open(os.path.join(targetPath, 'condensed_ais.txt'), 'w+')
					else:
						if currfile:
							currfile.close()
						currfile = open(os.path.join(targetPath, 'condensed_ais.txt'), 'a')

				currDate = newCurrDate
				currfile.write(','.join([datetimeStr, mmsi, aisClass, lat, lon]))
				currfile.write('\n')

	currfile.close()
	print("Skipped: {0}".format(skipped))
	print("A class: {0}".format(countA))
	print("B class: {0}".format(countB))




def is_int(str):
	try:
		int(str)
		return True
	except ValueError:
		return False


def is_float(str):
	try:
		float(str)
		return True
	except ValueError:
		return False


if __name__ == '__main__':
	main()
