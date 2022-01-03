import os
import re
from datetime import datetime, timedelta, date

# inpath = r"C:\workspace\work\aishub\August_2020_AISHub_Boundary_Pass"
inpath = r"C:\workspace\work\aishub\Nov_2020_AISHub_Boundary_Pass"

outpath = r"C:\workspace\work\aishub"


# Zero if starting with mmsi, 1 if starting with an identifier
offset = 0


def main():
	global inpath, outpath, offset
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
				if not (is_int(split[0 + offset]) and len(split) >= 9):
					skipped += 1
					continue

				dt = split[1 + offset].split(' ')[0].split('-')
				y, m, d = dt
				if d.startswith('0'):
					d = d[1:]
				if m.startswith('0'):
					m = m[1:]
				newCurrDate = date(int(y), int(m), int(d))

				mmsi = split[0 + offset]
				datetimeStr = split[1 + offset].replace(' ', '_')
				datetimeStr = datetimeStr.replace(':', '-')
				lat = split[6 + offset]
				lon = split[5 + offset]
				aisClass = split[2 + offset]
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
