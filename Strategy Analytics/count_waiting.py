import sklearn
#import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
#import csv
from collections import Counter 

#m = pd.read_csv('train_m.csv', header=0, names=['ID','LAT','LON'])
# 'TRIP_ID','CALL_TYPE','ORIGIN_CALL','ORIGIN_STAND','TAXI_ID','TIMESTAMP','DAY_TYPE','MISSING_DATA','POLYLINE'

def count_waiting ():
	############################ Count waiting instances #########################
	m = pd.read_csv('train.csv', header=0, usecols=['TRIP_ID','POLYLINE'])

	print "starting loop...."
	array = []
	prev = ""
	count = 0
	curMax = 0
	index = 0
	for index in m[0:170000].index: 
		for cord in m.iloc[index]['POLYLINE']: 
			if (cord == prev):
				count = count + 1
			else:
				curMax = max(count, curMax)
				count = 0
			prev = cord
		array.append(curMax) 
		#print curMax
		curMax = 0

	#print array
	print Counter(array)
##############################################################################

def main(): 
	count_waiting()
  
if __name__ == "__main__": main()
