from subprocess import call
import os

def main():
	for year in range(2017, 2019):
		for month in range(1, 13):
			for day in range(1, 32):
				# Format:"C:\\Users\\grego\\Downloads\\ais\\DIGITALYACHTAISNET1302-0098-01_\y\y\y\y\m\m\d\dT000000.000Z.txt"
				# srcArg = "C:/Workspace/Work/ais_data/DIGITALYACHTAISNET1302-0097-01_" + str(year)
				# srcArg = "Z:/vol01/SIMRES_AIS_Data_2018/AIS_NormaSerra-20190320T182824Z-001/AIS_NormaSerra"
				srcArg = "Z:/vol01/AIS_ONC_BoundaryPass_Raw/2017/4_Apr"
				srcArg += "/DIGITALYACHTAISNET1302-0098-01_" + str(year)
				if month < 10:
					srcArg += "0"
				srcArg += str(month)
				if day < 10:
					srcArg += "0"
				srcArg += str(day) + "T000000.000Z.txt.txt"
				if not os.path.exists(srcArg):
					# print("Could not file", srcArg)
					continue

				dstArg = "Z:/vol01/AIS_ONC_BoundaryPass_Processing"
				if not os.path.exists(dstArg):
					os.mkdir(dstArg)
				dstArg = os.path.join(dstArg, str(year))
				if not os.path.exists(dstArg):
					os.mkdir(dstArg)
				dstArg = os.path.join(dstArg, str(month))
				if not os.path.exists(dstArg):
					os.mkdir(dstArg)
				dstArg = os.path.join(dstArg, str(day)) + ",ais"

				call(["C:\Python27-clean\python.exe", "C:/Workspace/Work/work_scripts/DMAS_TAIS_NM4_parsing.py", "-j", "-s", "-o", dstArg, srcArg])


if __name__ == "__main__":
	main()
