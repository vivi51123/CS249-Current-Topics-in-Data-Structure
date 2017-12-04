'''
implement the similarity based model for prediction
'''
import collections
import numpy as np
import sys
import ast


def get_destination(train_coor_list):
	train_len = len(train_coor_list)
	return train_coor_list[train_len-1,0],train_coor_list[train_len-1,1]


def judge_stand_similarity(test_stand,train_stand):
	return test_stand == train_stand


def judge_start_similarity(test_start,train_start,hour):
	within_hour = (abs(test_start - train_start)%(24*3600)) <= 3600*hour
	return within_hour


def calculate_journey_similarity(test_coor_list,train_coor_list):
	#for journey similarity,we are only keeping for final 10 points
	'''
	print("enter calculate similarity")
	print("test coor list")
	print(test_coor_list)
	print("train_coor_list")
	print(train_coor_list)
	'''

	new_test_coor_list = test_coor_list
	test_len = len(test_coor_list)
	min_len = min(len(train_coor_list),10)
	if len(new_test_coor_list) > min_len:
		new_test_coor_list = new_test_coor_list[test_len - min_len:]

	min_dis = sys.float_info.max
	for first in range(len(train_coor_list) - len(new_test_coor_list) + 1):

		tmp_dis = 0
		for test_index in range(len(new_test_coor_list)):
			current_dis = ((train_coor_list[first+test_index,0] - new_test_coor_list[test_index,0])**2 +
			(train_coor_list[first+test_index,1] - new_test_coor_list[test_index,1])**2)**0.5

			#assign larger weight to the latter journey
			tmp_dis += current_dis * (3**test_index)
		min_dis = min(min_dis,tmp_dis)
		#print(str(first)+" "+str(tmp_dis)+" "+str(min_dis))

	#print(min_dis/(2**len(new_test_coor_list)-1))
	total_weight = 0
	for test_index in range(len(new_test_coor_list)):
		total_weight += 3**test_index

	return min_dis/total_weight




# the correlation 1:1:10
def predict_single_case(line,train_file,hour,neighour):

	element_list = line.split('"')[1::2]
	trip_id,start_time,day_type,nearest_stop = element_list[0],int(element_list[1]),element_list[2],int(element_list[3])
	coor_list = np.array(ast.literal_eval(element_list[4]))



	similar_trip_nearest = []
	similar_trip_start = []
	similar_trip_journey = collections.defaultdict(list)#similar_trip_jou

	train_content = open(train_file,'r')
	header = train_content.readline()
	count = 0
	for train_line in train_content.readlines():
		train_element_list = train_line.split('"')[1::2]
		#print(train_element_list)
		train_start_time,train_nearest_stop = int(train_element_list[1]),int(train_element_list[3])
		train_coor_list = np.array(ast.literal_eval(train_element_list[4]))
		train_destination_x,train_destination_y = get_destination(train_coor_list)

		#if this is a trip with the same nearset taxi stand and start from the similar time
		if judge_stand_similarity(nearest_stop,train_nearest_stop) and judge_start_similarity(start_time,train_start_time,hour):
			journey_similarity = calculate_journey_similarity(coor_list,train_coor_list)
			#only keep top 200 similar journeys
			similar_trip_journey[journey_similarity].append([train_destination_x,train_destination_y])
			count += 1
			#print(str(train_destination_x)+","+str(train_destination_y))
	train_content.close()

	if count == 0:
		train_content = open(train_file,'r')
		header = train_content.readline()
		count = 0
		for train_line in train_content.readlines():
			train_element_list = train_line.split('"')[1::2]
			#print(train_element_list)
			train_start_time,train_nearest_stop = int(train_element_list[1]),int(train_element_list[3])
			train_coor_list = np.array(ast.literal_eval(train_element_list[4]))
			train_destination_x,train_destination_y = get_destination(train_coor_list)

			#if this is a trip with the same nearset taxi stand and start from the similar time
			#if judge_stand_similarity(nearest_stop,train_nearest_stop) and judge_start_similarity(start_time,train_start_time,hour):
			journey_similarity = calculate_journey_similarity(coor_list,train_coor_list,weight)
			#only keep top 200 similar journeys
			similar_trip_journey[journey_similarity].append([train_destination_x,train_destination_y])
			count += 1
		train_content.close()

	'''
	total_x_start = 0
	total_y_start = 0
	start_match_count = 0


	for [x,y] in similar_trip_start:
		total_x_start += x
		total_y_start += y
		start_match_count += 1
	avg_x_start = total_x_start/start_match_count
	avg_y_start = total_y_start/start_match_count


	total_x_stand = 0
	total_y_stand = 0
	stand_match_count = 0

	for[x,y] in similar_trip_nearest:
		total_x_stand += x
		total_y_stand += y
		stand_match_count += 1
	avg_x_stand = total_x_stand/stand_match_count
	avg_y_stand = total_y_stand/stand_match_count
	'''

	#print("count:"+str(count))

	total_x_journey = 0
	total_y_journey = 0

	#only select the top 100 journeys
	key_list = sorted(similar_trip_journey)
	journey_match_count = 0
	end = False
	for key in key_list:
		match_coor_list = similar_trip_journey[key]
		for [x,y] in match_coor_list:
			journey_match_count += 1
			if journey_match_count <= min(int(count*0.3),neighour):
				total_x_journey += x
				total_y_journey += y
			else:
				journey_match_count -= 1
				end = True
				break
		if end:
			break

	avg_x_journey = total_x_journey/journey_match_count
	avg_y_journey = total_y_journey/journey_match_count

	#print(journey_match_count)
	#print(str(avg_x_journey)+","+str(avg_y_journey))
	return avg_x_journey,avg_y_journey



		
def predict_validation(test_file,test_answer_file,train_file,predict_result_file,new_answer_file,num,hour,neighour):
	test_content = open(test_file,'r')
	test_answer = open(test_answer_file,'r')
	test_predict = open(predict_result_file,'w+')
	new_test_answer = open(new_answer_file,'w+')
	test_predict.write("\"TRIP_ID\",\"LATITUDE\",\"LONGITUDE\"\n")
	new_test_answer.write("\"TRIP_ID\",\"LATITUDE\",\"LONGITUDE\"\n")

	test_content.readline()
	num_count = 0
	for line in test_content.readlines():
		element_list = line.split('"')[1::2]
		trip_id = element_list[0]
		result_x,result_y = predict_single_case(line,train_file,hour,neighour)

		answer_line = test_answer.readline().strip('\n')
		answer_x,answer_y = answer_line.split(',')[0],answer_line.split(',')[1]

		test_predict.write("\"T"+str(trip_id)+"\","+str(result_y)+","+str(result_x)+"\n")
		new_test_answer.write("\"T"+str(trip_id)+"\","+str(answer_y)+","+str(answer_x)+"\n")

		num_count += 1
		print(num_count)
		if num_count > num:
			break

	test_content.close()
	test_answer.close()
	new_test_answer.close()
	test_predict.close()


def predict_test(test_file,train_file,predict_result_file,hour,neighour):
	test_content = open(test_file,'r')
	test_predict = open(predict_result_file,'w+')
	test_predict.write("\"TRIP_ID\",\"LATITUDE\",\"LONGITUDE\"\n")

	test_content.readline()
	num_count = 0
	for line in test_content.readlines():
		element_list = line.split('"')[1::2]
		trip_id = element_list[0]
		result_x,result_y = predict_single_case(line,train_file,hour,neighour)

		test_predict.write("\""+str(trip_id)+"\","+str(result_y)+","+str(result_x)+"\n")
		num_count += 1
		print(num_count)

	test_content.close()
	test_predict.close()



def main():
	neighour_list = [20,50,100,150]
	for neighour in neighour_list:
		print("weight = 3, hour = 2,neighour = "+str(neighour))
		predict_test("../data/preprocessed/test.csv","../data/preprocessed/preprocessed-train.csv","../data/result/predict-test-weight-3-hour-2-nei-"+str(neighour)+".csv",2,neighour)





if __name__ == "__main__":
	main()

















