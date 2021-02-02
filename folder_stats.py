from __future__ import print_function
import os


def main():
	folder_stats("Z:/vol03/Haro_Strait_Raw")
	print("Done")


# Looks through a folder and counts files of size 0 (these are 'bad' files)
def folder_stats(inpath, showMasterStats=True, recurse=True):
	subfolders = []
	totalSize = 0
	numGoodFiles = 0
	numBadFiles = 0
	print(inpath, end=':  ')
	for f in os.listdir(inpath):
		fullPath = os.path.join(inpath, f)

		# Track folders, but do not include them in the rest of the stats
		if os.path.isdir(fullPath):
			subfolders.append(fullPath)
			continue

		size = os.stat(fullPath).st_size

		# if the size is 0, the file is bad
		if not size > 0:
			numBadFiles += 1
			continue

		numGoodFiles += 1
		totalSize += size

	# print out stats
	print(str(numGoodFiles) + " good files, " + str(numBadFiles) + " bad files.")

	# recurse if requested
	if recurse:
		for f in subfolders:
			g, b, t = folder_stats(f, False, recurse)
			numGoodFiles += g
			numBadFiles += b
			totalSize += t

	# Print out final stats:
	if showMasterStats:
		print("\nMaster Stats:")
		print("Number of good files: " + str(numGoodFiles))
		print("Number of bad files: " + str(numBadFiles))
		print("Total size (MB): " + str(totalSize / 1048576.0))
		print("Average size (MB): " + str(totalSize / 1048576.0 / numGoodFiles))

	return numGoodFiles, numBadFiles, totalSize


if __name__ == '__main__':
	main()
