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

def nearest_stand_visual ():
	############# Data Visualization for Taxi stands and initial starting point ###############
	m = pd.read_csv('vivi.csv', header=0, usecols=['trip_id','nearest_stand','destination'])
	#print len(m.nearest_stand.unique())
	m = m.groupby('nearest_stand')['destination'].apply(', '.join).reset_index()

	# for index in m.index: 
	# 	array = []
	# 	prev = ""
	# 	count = 0
	# 	curMax = 0
		# for dest in m.iloc[index]['destination']: 
	# 		if (dest == prev):
	# 			count = count + 1
	# 		else:
	# 			curMax = max(count, curMax)
	# 			count = 0
	# 		prev = dest
	# 	array.append(curMax) 
	# 	#print curMax
	# 	curMax = 0

	# print array
	print "0"
	print " "
	print " "	
	print m.iloc[0]['destination']
	print "1"
	print " "
	print " "
	print " "
	print " "	
	print m.iloc[1]['destination']
	print "2"
	print " "
	print " "
	print " "	
	print m.iloc[2]['destination']
	print "3"
	print " "
	print " "
	print " "	
	print m.iloc[3]['destination']
#############################################################################################

def convert_time ():
	############# Convert timestamp to hours ###############
	m = pd.read_csv('train.csv', header=0, usecols=['TIMESTAMP'])
	# for index, t in enumerate(m['TIMESTAMP']):
	# 	newt = t 
	# 	m.set_value(index, 'TIMESTAMP', newt)
	m = m.sort_values(by=['TIMESTAMP'], ascending = True)
	m['TIMESTAMP'] = pd.to_datetime(m['TIMESTAMP'], unit = 's')
	print m[0:50]['TIMESTAMP']

#############################################################################################
def main(): 
	#count_waiting()
	#nearest_stand_visual()
	convert_time()

if __name__ == "__main__": main()