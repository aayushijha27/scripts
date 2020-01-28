import glob
import os

path = os.getcwd()
filenames = glob.glob('/home/aayushi/Documents/files (2)' + "/*.csv")
for filename in filenames:
	flag = False
	with open(filename,'r') as f:
		for line in f:
			if 'Haryana Election' in line:
				flag = True
	print(filename,' : ',flag)
	if flag is True:
		print(filename,' : Removed')
		os.remove(filename)
	

