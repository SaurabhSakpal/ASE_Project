import numpy as np
import sys
file = sys.argv[1]

f = open(file, 'r')

for line in f:
	algo = line.split(' ')[0]
	line = map(float,line.split(' ')[1:])
	print algo, np.mean(line)