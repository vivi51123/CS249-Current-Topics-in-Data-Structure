import sklearn
#import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np
#import csv
from collections import Counter 
from ast import literal_eval

#m = pd.read_csv('train_m.csv', header=0, names=['ID','LAT','LON'])
# 'TRIP_ID','CALL_TYPE','ORIGIN_CALL','ORIGIN_STAND','TAXI_ID','TIMESTAMP','DAY_TYPE','MISSING_DATA','POLYLINE'

##############################################################################

def nearest_stand_visual ():
	############# Data Visualization for Taxi stands and initial starting point ###############
	m = pd.read_csv('vivi.csv', header=0, usecols=['trip_id','nearest_stand','destination'])
	#print len(m.nearest_stand.unique())
	
	m['destination'] = [literal_eval(x) for x in m['destination']]

	#type(m.iloc[0]['destination'][0]) = float
	#type(m.iloc[0]['destination']) = list of float 

	#print m[0:4]['destination']

	# print m.iloc[0]['destination'][0] 
	# print m.iloc[0]['destination'][1]

	for index in m[0:16999].index: 
		i = 0
		for cord in m.iloc[index]['destination']: 
			m.iloc[index]['destination'][i] = round(cord, 3)
			i = i + 1

			
	# print "------"
	# print m[15000:17000]['destination']

	#print Counter(m.iloc[0]['destination']) gives one for each float
	m['destination'] = m['destination'].apply(lambda x: ', '.join([str(i) for i in x]))
	#print type(m.iloc[0]['destination'])
	
	m = m.groupby('nearest_stand')['destination'].apply(', '.join).reset_index()
	# m = m.groupby('nearest_stand')['destination']
	# m = m.groupby('nearest_stand')

	print m[0:1]['destination']

	m['destination'] = [literal_eval(x) for x in m['destination']]

	#print m[0:4]['destination']
	
	print Counter(m.iloc[0]['destination'])
	
	#for index in m[0:4].index:
		#print Counter(m.iloc[index]['destination'])
	#print m.iloc[0]['destination']

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
	# print "0"
	# print " "
	# print " "	
	# print m.iloc[0]['destination']
	# print "1"
	# print " "
	# print " "
	# print " "
	# print " "	
	# print m.iloc[1]['destination']
	# print "2"
	# print " "
	# print " "
	# print " "	
	# print m.iloc[2]['destination']
	# print "3"
	# print " "
	# print " "
	# print " "	
	# print m.iloc[3]['destination']
#############################################################################################

def main(): 
	nearest_stand_visual()

if __name__ == "__main__": main()
