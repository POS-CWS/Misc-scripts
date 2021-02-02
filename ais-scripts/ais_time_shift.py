import os
import datetime as dt

# This amount of time is SUBTRACTED to every time
timeShiftNeg = dt.timedelta(hours=0)
# This amount of time is ADDED to every time. The script doesn't care, but conceptually, make sure one of these is zero
timeShiftPos = dt.timedelta(hours=2)

def shift_time(filename):
	tempName = 'temp.txt'
	with open(filename, 'r+') as infile:
		with open(tempName, 'w+') as outfile:
			for line in infile:
				split = line.split(',', 2)

				# Parse and change time
				t = dt.datetime.strptime(split[0], '%Y-%m-%d_%H-%M-%S')
				t = t - timeShiftNeg + timeShiftPos
				split[0] = t.strftime('%Y-%m-%d_%H-%M-%S')
				# format and write result
				res = ','.join(split)
				outfile.write(res)
	os.remove(filename)
	os.rename(tempName, filename)

def iterate(folder):
	for filename in os.listdir(folder):
		filepath = os.path.join(folder, filename)
		if os.path.isdir(filepath):
			iterate(filepath)
		elif filepath.endswith('.txt'):
			shift_time(filepath)

if __name__ == "__main__":
	iterate('C:/Workspace/Work/AIS_linker/Processed_ais/2019/9/27')
	iterate('C:/Workspace/Work/AIS_linker/Processed_ais/2019/9/26')
	iterate('C:/Workspace/Work/AIS_linker/Processed_ais/2019/9/28')
