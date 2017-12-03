import sklearn
#import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
#import csv
from collections import Counter 
from ast import literal_eval

#############################################################################################
def convert_time ():
	############# Convert timestamp to hours ###############
	m = pd.read_csv('train.csv', header=0, usecols=['TIMESTAMP'])

	# for index, t in enumerate(m['TIMESTAMP']):
	# 	newt = some computation
	# 	m.set_value(index, 'TIMESTAMP', newt)

	#m = m.sort_values(by=['TIMESTAMP'], ascending = True)
	#m['TIMESTAMP'] = pd.to_datetime(m['TIMESTAMP'], unit = 's')
	#print m[0:49]['TIMESTAMP']
	#min(m['TIMESTAMP']) = 1372636853 = July 1, 2013 @ 12:00:53 am Monday

	#July 1, 2013 @ 7:00:00 am = 1372662000
	#July 1, 2013 @ 9:00:00 am = 1372669200

	#July 1, 2013 @ 11:00:00 am = 1372676400
	#July 1, 2013 @ 1:00:00 pm = 1372683600

	#July 1, 2013 @ 5:00:00 pm = 1372698000
	#July 1, 2013 @ 7:00:00 pm = 1372662000

	#print m[0:49]['TIMESTAMP']

#############################################################################################
def main(): 
	convert_time()

if __name__ == "__main__": main()
