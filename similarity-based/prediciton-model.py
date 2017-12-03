'''
implement the similarity based model for prediction
'''
import collections
import numpy as np
import sys


def get_destination(train_coor_list):
	train_len = len(train_coor_list)
	return train_coor_list[train_len-1,0],train_coor_list[train_start_time-1,1]


def judge_stand_similarity(test_stand,train_stand):
	return test_stand == train_stand


def judge_start_similarity(test_start,train_start):
	within_hour = (abs(test_start - train_start)%(24*3600)) <= 3600
	return within_hour


def calculate_journey_similarity(test_coor_list,train_coor_list):
	#for journey similarity,we are only keeping for final 10 points
	new_test_coor_list = test_coor_list
	test_len = len(test_coor_list)
	min_len = min(len(train_coor_list),10)
	if len(new_test_coor_list) > min_len:
		new_test_coor_list = new_test_coor_list[test_len - min_len:]

	min_dis = sys.float_info.max
	for first in range(len(train_coor_list) - len(new_test_coor_list) + 1):

		tmp_dis = 0
		for test_index in range(len(new_test_coor_list)):
			current_dis = ((train_coor_list[first+test_index,0] - test_coor_list[test_index,0])**2 +
			(train_coor_list[first+test_index,1] - test_coor_list[first+test_index,1])**2)
			**0.5

			#assign larger weight to the latter journey
			tmp_dis += current_dis * (2**first)

		min_dis = min(min_dis,tmp_dis)


	return min_dis/(2**len(test_coor_list)-1)



# the correlation 1:1:10
def predict_single_case(line,train_file):

	element_list = line.split('"')[1::2]
	trip_id,start_time,day_type,nearest_stop = element_list[0],int(element_list[1]),element_list[2],int(element_list[3])
	coor_list = np.array(ast.literal_eval(element_list[4]))

	similar_trip_nearest = []
	similar_trip_start = []
	similar_trip_journey = collections.defaultdict(list)#similar_trip_jou


	train_content = open(train_file,'r')
	train_content.readline()
	for train_line in train_content.readlines():

		train_element_list = line.split('"')[1:2]
		train_start_time,train_nearest_stop = int(train_element_list[1]),int(train_element_list[3])
		train_coor_list = np.array(ast.literal_eval(train_element_list[4]))
		train_destination_x,train_destination_y = get_destination(train_coor_list)

		#if this is a trip with the same nearset taxi stand
		if judge_stand_similarity(nearest_stop,train_nearest_stop):
			similar_trip_nearest.append([train_destination_x,train_destination_y])

		#if this is a trip with some near start time
		if judge_start_similarity(start_time,train_start_time):
			similar_trip_start.append([train_destination_x,train_destination_y])

		journey_similarity = calculate_journey_similarity(coor_list,train_coor_list)
		#only keep top 200 similar journeys
		similar_trip_journey[journey_similarity].append([train_destination_x,train_destination_y])


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
			if journey_match_count <= 100:
				total_x_journey += x
				total_y_journey += y
			else:
				break
		if end:
			break

	avg_x_journey = total_x_journey/journey_match_count
	avg_y_journey = total_y_journey/journey_match_count

	#assigning different weight to the different similarity
	#right now: 1:1:10
	final_x = (total_x_start + total_x_stand + total_x_journey * 10)/12
	final_y = (total_y_start + total_y_stand + total_y_journey * 10)/12

	train_content.close()
	return final_x, final_y


		
def predict_validation(test_file,test_answer,train_file):
	total_dis = 0
	test_content = open(test_file,'r')
	test_answer = open(train_file,'r')
	test_content.readline()
	for line in test_content.readlines():
		result_x,result_y = predict_single_case(line,train_file)
		answer_line = test_answer.readline()
		answer_x,answer_y = answer_line.split(',')[0],answer_line.split(',')[1]
		dis = ((answer_x -result_x)**2 + (answer_y - result_y)**2)**0.5
		total_dis += dis
	return total_dis



def predict_test()









def main():




if __name__ == "__main__":
	main()


