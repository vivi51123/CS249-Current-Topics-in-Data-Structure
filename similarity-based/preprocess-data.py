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




def get_nearest_stop(element_list,coor_list,stop_dict):
	nearest_stop = -1
	if element_list[1] == "B" and element_list[3] != "":
		nearest_stop = int(element_list[3])
	else:
		#calculate the nearest bus stop from the starting point
		if len(coor_list) > 0:
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
	for index in range(len(coor_list)-interval):
		coor = coor_list[index]
		if last_x == coor[0] and last_y == coor[1]:
			still+=1
		else:
			last_x = coor[0]
			last_y = coor[1]
			still = 0

		if still >= interval:
			start = index + 1
	new_coor_list = coor_list[start:,]
	return new_coor_list






#keep three decimals and remove the duplicates#
def remove_dup(old_coor_list):
	old_coor_list = np.around(old_coor_list,3)
	new_coor_list = np.array([[0,0]])
	last_coor = [0,0]
	for coor in old_coor_list:
		if coor[0] != last_coor[0] or coor[1] != last_coor[1]:
			new_coor_list = np.append(new_coor_list,coor)
		last_coor = coor
	return new_coor_list.reshape(-1,2)[1:,]




def preprocessed_line(element_list,coor_list,stop_dict):
	# 5 decimal point ~ 1m
	# if we do not move at least 1m within 30s, then this is a new journey
	new_coor_list = get_last_journey(np.around(coor_list,5),2)
	# get the nearest taxi stand for last starting point
	nearest_stop = get_nearest_stop(element_list,new_coor_list,stop_dict)

	new_coor_list = remove_dup(new_coor_list)
	return nearest_stop,new_coor_list




def preprocess_train_data(meta_folder,preprocessed_folder):
	content = open(meta_folder+"/train.csv",'r')
	result = open(preprocessed_folder+"/train.csv",'w+')
	stop_dict = get_stop_dict(meta_folder+"/metaData_taxistandsID_name_GPSlocation.csv")

	#skip the header line
	header = content.readline()
	result.write("\"TRIP_ID\",\"TIMESTAMP\",\"DAY_TYPE\",\"NEAREST_STOP\",\"POLYLINE\"\n")

	count = 0

	for line in content.readlines():
		count += 1
		element_list = line.split('"')[1::2]
		trip_id,timestamp,day_type,coor_list = element_list[0],element_list[5],element_list[6],np.array(ast.literal_eval(element_list[8]))
		#if there is missing data, we ignore this training sample
		if element_list[7] == "True" or len(coor_list) == 0:
			continue

		nearest_stop,new_coor_list = preprocessed_line(element_list,coor_list,stop_dict)
		result.write("\""+str(trip_id)+"\",\""+str(timestamp)+"\",\""+str(day_type)+"\",\""+str(nearest_stop)
			+"\",\""+str(new_coor_list.tolist())+"\"\n")

		if count%10000 == 0:
			print(count)
	content.close()
	result.close()



def preprocess_test_data(meta_folder,preprocessed_folder):
	content = open(meta_folder+"/test.csv",'r')
	result = open(preprocessed_folder+"/test.csv",'w+')
	stop_dict = get_stop_dict(meta_folder+"/metaData_taxistandsID_name_GPSlocation.csv")

	#skip the header line
	header = content.readline()
	result.write("\"TRIP_ID\",\"TIMESTAMP\",\"DAY_TYPE\",\"NEAREST_STOP\",\"POLYLINE\"\n")

	for line in content.readlines():
		element_list = line.split('"')[1::2]
		trip_id,timestamp,day_type,coor_list = element_list[0],element_list[5],element_list[6],np.array(ast.literal_eval(element_list[8]))

		nearest_stop,new_coor_list = preprocessed_line(element_list,coor_list,stop_dict)
		result.write("\""+str(trip_id)+"\",\""+str(timestamp)+"\",\""+str(day_type)+"\",\""+str(nearest_stop)
			+"\",\""+str(new_coor_list.tolist())+"\"\n")
	content.close()
	result.close()











def main():
	preprocess_test_data("../data/meta","../data/preprocessed")
	preprocess_train_data("../data/meta","../data/preprocessed")




if __name__ == "__main__":
	main()



