'''
implement the similarity based model for prediction
'''

def get_destination(train_coor_list):
	train_len = len(train_coor_list)
	return train_coor_list[train_len-1,0],train_coor_list[train_start_time-1,1]


def judge_stand_similarity(test_stand,train_stand):
	return test_stand == train_stand


def judge_start_similarity(test_start,train_start):
	within_hour = (abs(test_start - train_start)) <= 3600
	return within_hour


def get_journey_similarity(test_coor_list,train_coor_list):

	return 0




def predict_single_case(line,train_file):
	element_list = line.split('"')[1::2]
	trip_id,start_time,day_type,nearest_stop = element_list[0],int(element_list[1]),element_list[2],int(element_list[3])
	coor_list = np.array(ast.literal_eval(element_list[4]))

	similar_trip_nearest = []
	similar_trip_start = []
	similar_trip_journey = {}


	train_content = open(train_file,'r')
	train_content.readline()
	for train_line in train_content.readlines():

		train_element_list = line.split('"')[1:2]
		train_start_time,train_nearest_stop = int(train_element_list[1]),int(train_element_list[3])
		train_coor_list = np.array(ast.literal_eval(train_element_list[4]))

		#if this is a trip with the same nearset taxi stand
		if judge_stand_similarity(nearest_stop,train_nearest_stop):
			train_destination_x,train_destination_y = get_destination(train_coor_list)
			similar_trip_nearest.append([train_destination_x,train_destination_y])

		#if this is a trip with some near start time
		if judge_start_similarity(start_time,train_start_time):
			train_destination_x,train_destination_y = get_destination(train_coor_list)
			similar_trip_start.append([train_destination_x,train_destination_y])

		#if this is a trip with similar journey 
		if  get_journey_similarity(coor_list,train_coor_list):
			






	train_content.close()


		






def predict_test(test_file,train_file):
	test_content = open(test_file,'r')
	test_content.readline()
	for line in test_content.readlines():
		result = predict_single_case(line,train_file)



		




def main():




if __name__ == "__main__":
	main()


