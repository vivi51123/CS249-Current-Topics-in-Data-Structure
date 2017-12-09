import sklearn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter 
from ast import literal_eval

#############################################################################################
def convert_time ():
############# Convert timestamp to hours ###############
	m = pd.read_csv('train.csv', header=0, usecols=['TRIP_ID','TIMESTAMP','POLYLINE'])
	
	# m = m[0:1]
	#For convert lat lon string to float tuple
	# m['POLYLINE'] = [literal_eval(x) for x in m['POLYLINE']]

	#print type(m['POLYLINE'])
	#print m['POLYLINE'][0]
	# array = []
	#array = m['POLYLINE'].tolist()
	# #array = array[-2:]

	# print array[-2:]

	#m = m.sort_values(by=['TIMESTAMP'], ascending = True)

	#m['TIMESTAMP'] = pd.to_datetime(m['TIMESTAMP'], unit = 's')
	#print m[0:49]['TIMESTAMP']
	#min(m['TIMESTAMP']) = 1372636853 = July 1, 2013 @ 12:00:53 am Monday

	#July 1, 2013 @ 7:00:00 am = 1372662000
	#July 2, 2013 @ 7:00:00 am = 1372748400

	#July 1, 2013 @ 8:00:00 am = 1372665600
	#July 2, 2013 @ 8:00:00 am = 1372752000

	#July 1, 2013 @ 7:00:00 am = 1372662000
	#July 1, 2013 @ 8:00:00 am = 1372665600
	#July 1, 2013 @ 9:00:00 am = 1372669200

	#July 1, 2013 @ 11:00:00 am = 1372676400
	#July 1, 2013 @ 12:00:00 pm = 1372680000
	#July 1, 2013 @ 1:00:00 pm = 1372683600

	#July 1, 2013 @ 5:00:00 pm = 1372698000
	#July 1, 2013 @ 6:00:00 pm = 1372701600
	#July 1, 2013 @ 7:00:00 pm = 1372705200

	# m_7 = ((m['TIMESTAMP'] - 1372662000) % (24*3600)) #gives the hours elaspe from 7am 7/1
	# m_8 = ((m['TIMESTAMP'] - 1372665600) % (24*3600)) #gives the hours elaspe from 8am 7/1

	# for index, t in enumerate(m['TIMESTAMP']): 
	# 	if (((t - 1372662000) % (24*3600) >= 0) and ((t - 1372662000) % (24*3600)  <= 3600)):  # day elaspe from 7/1 7am must all be 0 and 8am must be 3600
			#m.iloc[index][POLYLINE] <- need the destination instead of polyline
			# print m.iloc[index]['TIMESTAMP']
			# print m.iloc[index]['TRIP_ID']
			# print "------------"	

	m = m.drop(m[((m.TIMESTAMP - 1372662000) % (24*3600)) > 3600].index)

	print len(m.index)

	# # assume we have the destination or lat long 
	# m['destination'] = [literal_eval(x) for x in m['destination']]

	# m['lat'] = ""
	# m['lon'] = ""

	# for index, cord in enumerate(m['destination']): 
	# 	m.set_value(index, 'lat', cord[0])
	# 	m.set_value(index, 'lon', cord[1])

	# m = m.drop('destination', axis=1)

	# m['coordinate'] = m['lat'].map(str)+m['lon'].map(str)
	# m['coordinate'] = m['coordinate'].str.replace('.', '')

	# #m = m.groupby('nearest_stand')['coordinate'].apply(lambda x: ','.join(x.astype(str))).reset_index()

	# #m['coordinate'] = [literal_eval(x) for x in m['coordinate']]	

	# coordList = []
	# countList = []

	# c = Counter(m['coordinate']).most_common(20)
	# for pair in c: 
	# 		coordList.append(pair[0])
	# 		countList.append(pair[1])

	# plt.title('7~8am vs Destination Count')
	# plt.plot(list(range(len(countList))), countList, color='r')
	# plt.xlabel('Time Interval')
	# plt.ylabel('Destination Count')
	# plt.show()

#############################################################################################
def main(): 
	convert_time()

if __name__ == "__main__": main()
