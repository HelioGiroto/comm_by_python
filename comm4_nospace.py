#!/usr/bin/python
# compatible with both Python 3 and Python 2
# fix algorithm for finding the same lines in both files

import sys, locale
from optparse import OptionParser

class readfile:
	def __init__(self, filename):
		f = open(filename, 'r')
		self.lines = f.readlines()
		f.close()

	def outputLine(self, num):
		return self.lines[num]

	def lineCount(self):
		return len(self.lines)


def printColumn1(line, options):
	if options.column1 == True:
		sys.stdout.write(line)


def printColumn2(line, options):
	if options.column2 == True:
		if options.column1 == True:
			out = "        " + line
			sys.stdout.write(out)
		else:
			out = line
			sys.stdout.write(out)


def printColumn3(line, options):
	if options.column3 == True:
		if options.column2 == True and options.column1 == True:
			out = "                " + line
			sys.stdout.write(out)
		elif options.column2 == False and options.column1 == False:
			out = line
			sys.stdout.write(out)
		else:
			out = "        " + line
			sys.stdout.write(out)


def main():
	version_msg = "%prog 1.0 by Yingbo Wang"
	usage_msg = """%prog [OPTION]... FILE1 FILE2

A Python script to compare two files and output the differences. """

# initialize the parser
	parser = OptionParser(version=version_msg, usage=usage_msg)
	parser.add_option("-1", action="store_false", dest="column1", default=True)
	parser.add_option("-2", action="store_false", dest="column2", default=True)
	parser.add_option("-3", action="store_false", dest="column3", default=True)
		
	parser.add_option("-u", action="store_true", dest="ignoreSort", default=False)

	options, args = parser.parse_args(sys.argv[1:])

	if len(args) != 2:
		parser.error("Wrong number of operands: there should be two files for comparison. ")

	input_file1 = args[0]
	input_file2 = args[1]

# reading file1 and file2 into the program
	try:
		reader1 = readfile(input_file1)
		reader2 = readfile(input_file2)
	except IOError as error:
		parser.error("I/O error({0}): {1}".format(error.errno, error.strerror))

	lineNum1 = reader1.lineCount()
	lineNum2 = reader2.lineCount()

	file1 = {}
	file2 = {}

	for i in range(0, lineNum1):
		file1[i] = reader1.outputLine(i)

	for i in range(0, lineNum2):
		file2[i] = reader2.outputLine(i)

# checking if file1 and file2 are in sorted order
	file1Order = 0 # changed to 1 if in positive order, -1 if in reverse order
	file2Order = 0
	notSorted = False

	for i in range(len(file1)-1):
		if locale.strcoll(file1[i], file1[i+1]) < 0:
			if file1Order == 0:
				file1Order = -1
			if file1Order == 1:
				sys.stdout.write("comm: FILE1 not in sorted order. \n")
				notSorted = True
				break

		if locale.strcoll(file1[i], file1[i+1]) > 0:
			if file1Order == 0:
				file1Order = 1
			if file1Order == -1:
				sys.stdout.write("comm: FILE1 not in sorted order. \n")
				notSorted = True
				break

	for i in range(len(file2)-1):
		if locale.strcoll(file2[i], file2[i+1]) < 0:
			if file2Order == 0:
				file2Order = -1
			if file2Order == 1:
				sys.stdout.write("comm: FILE2 not in sorted order. \n")
				notSorted = True
				break

		if locale.strcoll(file2[i], file2[i+1]) > 0:
			if file2Order == 0:
				file2Order = 1
			if file2Order == -1:
				sys.stdout.write("comm: FILE2 not in sorted order. \n")
				notSorted = True
				break

	if not options.ignoreSort and notSorted:
		sys.exit()

# comparing two files
	sameLinesInFile2 = []

	for i in range(0, len(file1)):
		inFile2 = False

		for j in range(0, len(file2)):
			if j in sameLinesInFile2:
				continue

			result = locale.strcoll(file1[i], file2[j])
			if result == 0:
				sameLinesInFile2.append(j)
				printColumn3(file1[i], options) # line in both file1 and file2
				inFile2 = True
				break
		
		if not inFile2:
			printColumn1(file1[i], options) # line only in file1
		
	for i in range(0, len(file2)):
		if i not in sameLinesInFile2:
			printColumn2(file2[i], options) # line only in file2
				

if __name__ == "__main__":
	main()

