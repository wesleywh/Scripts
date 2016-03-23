import glob
import os
drive = raw_input("Drive: ")
ext = raw_input("Extension (EX:txt): ")
string = raw_input("String: ")

print "Searching..."
os.chdir(drive)
for file in glob.glob('*.'+ext):
	with open(file) as f:
		contents = f.read()
	if string in contents:
		print file
