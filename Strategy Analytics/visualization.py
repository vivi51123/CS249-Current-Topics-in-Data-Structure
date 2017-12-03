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
	
	#For convert lat lon string to float tuple
	m['destination'] = [literal_eval(x) for x in m['destination']]
	
	m['lat'] = ""
	m['lon'] = ""

	for index, cord in enumerate(m['destination']): 
		m.set_value(index, 'lat', round(cord[0], 3))
		m.set_value(index, 'lon', round(cord[1], 3))

	m = m.drop('destination', axis=1)
	
	m['coordinate'] = m['lat'].map(str)+m['lon'].map(str)
	m['coordinate'] = m['coordinate'].str.replace('.', '')

	m['destination'] = m['destination'].apply(lambda x: ', '.join([str(i) for i in x]))
	
	#m = m.groupby('nearest_stand')['lat'].apply(lambda x: ','.join(x.astype(str))).reset_index()
	#m = m.groupby('nearest_stand').apply(lambda x: pd.Series({'lat': ','.join(x['lat'].astype(str)), 'lon': ','.join(x['lon'].astype(str))})).reset_index()
	m = m.groupby('nearest_stand')['coordinate'].apply(lambda x: ','.join(x.astype(str))).reset_index()

	#print m[0:1]['destination']
	#m['destination'] = [literal_eval(x) for x in m['destination']]
	
	# Convert to tuple again
	m['coordinate'] = [literal_eval(x) for x in m['coordinate']]
	
	#print Counter(m.iloc[0]['destination'])
	for index in range(0,63): 
		print Counter(m.iloc[index]['coordinate']).most_common(10)

#############################################################################################

def main(): 
	nearest_stand_visual()

if __name__ == "__main__": main()
