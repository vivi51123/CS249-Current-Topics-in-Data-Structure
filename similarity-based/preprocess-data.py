'''
preprocessed the meta data, including:
	(1) keep only 41~42 -8.8~-7 coordinates in the training set
	(2) keep only the last journey
	(3) keep 3 decimal, remove duplicates
	(4) calculate nearest taxi stop
'''

import numpy as np
import ast
import sys
import math

def get_stop_dict(taxi_meta_file):
	stop_dict = {}
	content = open(taxi_meta_file,'r')
	header = content.readline()
	for line in content.readlines():
		element_list = line.strip('\n').strip().split(',')
		taxi_id,lat,lon= int(element_list[0]),float(element_list[2]),float(element_list[3])
		stop_dict[taxi_id] = [lat,lon]
	content.close()
	return stop_dict



def valid_start(x_start,y_start):
	if y_start >= 41 and y_start <= 42 and x_start >= -8.8 and x_start <= -7:
		return True
	else:
		return False




def get_nearest_stop(element_list,stop_dict):
	nearest_stop = -1
	if element_list[1] == "B" and element_list[3] != "":
		nearest_stop = int(element_list[3])
	else:
		#calculate the nearest bus stop from the starting point
		coor_list = np.array(ast.literal_eval(element_list[8]))
		x_start = float(coor_list[0,0])
		y_start = float(coor_list[0,1])
		if valid_start(x_start,y_start):
			min_dis = sys.float_info.max
			for stop_id in stop_dict.keys():
				x_stop, y_stop = float(stop_dict[stop_id][1]), float(stop_dict[stop_id][0])
				tmp_dis = math.sqrt((x_start - x_stop)**2 + (y_start - y_stop)**2)
				if tmp_dis < min_dis:
					min_dis = tmp_dis
					nearest_stop = stop_id 
	return nearest_stop




def get_last_journey(coor_list,interval):
	last_x = -1
	last_y = -1
	still = 0
	start = 0
	index = 0
	for coor in coor_list:
		print(coor[0])
		print(coor[1])

		if last_x == coor[0] and last_y == coor[1]:
			still+=1
		else:
			last_x = coor[0]
			last_y = coor[1]
			still = 0

		if still >= 4:
			start = index
	new_coor_list = coor_list[start:,]




def calculate_new_coor_list(coor_list,interval):
	#getting the last trip
	new_coor_list = get_last_journey(coor_list,interval)

	#keep three decimal and throw away the duplicates


	return new_coor_list















def preprocessed_data(meta_folder,preprocessed_folder):
	content = open(meta_folder + "/train.csv",'r')
	result = open(preprocessed_folder + "/train.csv",'w+')
	stop_dict = get_stop_dict(meta_folder+"/metaData_taxistandsID_name_GPSlocation.csv")


	#skip the header line
	header = content.readline()
	result.write("\"TRIP_ID\",\"TIMESTAMP\",\"DAY_TYPE\",\"NEAREST_STOP\",\"POLYLINE\"")
	print(header)

	count = 0

	for line in content.readlines():
		element_list = line.split('"')[1::2]
		trip_id,timestamp,day_type,coor_list = element_list[0],element_list[5],element_list[6],np.array(ast.literal_eval(element_list[8]))
		#if there is missing data, we ignore this training sample
		if element_list[7] == "True" or len(coor_list) == 0:
			continue
		#if the start point excceed the defined limit, we ignore this training sample
		nearest_stop = get_nearest_stop(element_list,stop_dict)
		if nearest_stop == -1:
			continue



		
		new_coor_list = calculate_new_coor_list(coor_list,4)
		



















def main():
	preprocessed_data("../data/meta","../data/preprocessed")



if __name__ == "__main__":
	main()



