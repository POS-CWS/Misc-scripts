import re
import os


def main():
	# process("Z:/vol01/AIS_linker/Processed_ais/2017/12", True)
	process("C:/workspace/work/ais/onc2019saturna_decoded/2019", True)


def process(path, recurse=False):
	outFile = None
	print("working in folder: " + path)
	for f in os.listdir(path):
		if os.path.isdir(os.path.join(path, f)):
			if recurse:
				process(os.path.join(path, f), recurse)
		# 18: position report (B)
		# 1, 3: position report (A)
		elif f.endswith("msg18.txt") or f.endswith("msg1.txt") or f.endswith("msg3.txt"):
			with open(os.path.join(path, f), 'r') as inFile:
				for line in inFile:
					split = line.split(",", 20)
					mmsi = 0
					isA = True
					time = None
					lat = 0
					lon = 0
					for s in split:
						# Get date and time from the timestamp
						if s.startswith('{"date":'):
							m = re.search(r"(\d\d\d\d)(\d\d)(\d\d)T(\d\d)(\d\d)(\d\d)", s)
							if m:
								time = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6))]
						# Determine A or B from the message types
						# Note: only messages 1 and 18 are processed right now
						elif s.startswith('"msgtype":'):
							if s.endswith('18'):
								isA = False
						# Note: leading '0's on mmsi's are missing (hence the variable length)
						elif s.startswith('"mmsi":'):
							m = re.search(r"\d\d\d+", s)
							if m:
								mmsi = m.group(0)
						elif s.startswith('"lon":'):
							try:
								lon = float(s[7:-1])
							except ValueError:
								pass
						elif s.startswith('"lat":'):
							try:
								lat = float(s[7:-1])
							except ValueError:
								pass
					# check that we've gotten everything (protection from malformed lines)
					if not (mmsi and time and lat and lon):
						continue

					# build time string with constant length, then add other information
					# output lines look like: 'time,mmsi,<A/B>,lat,lon'
					outStr = str(time[0]) + "-"
					if time[1] < 10:
						outStr += "0"
					outStr += str(time[1]) + "-"
					if time[2] < 10:
						outStr += "0"
					outStr += str(time[2]) + "_"
					if time[3] < 10:
						outStr += "0"
					outStr += str(time[3]) + "-"
					if time[4] < 10:
						outStr += "0"
					outStr += str(time[4]) + "-"
					if time[5] < 10:
						outStr += "0"
					outStr += str(time[5]) + ","
					outStr += str(mmsi) + ","
					if isA:
						outStr += "A,"
					else:
						outStr += "B,"
					outStr += str(lat) + ","
					outStr += str(lon)

					if outFile is None:
						outFile = open(os.path.join(path, "condensed_ais.txt"), "w+")
					outFile.write(outStr + "\n")

	if outFile:
		outFile.close()


if __name__ == "__main__":
	main()
