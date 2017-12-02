'''
implement the similarity based model for prediction
'''



def judge_stand_start_time_similarity(train_line):
	return True


def get_journey_similarity(test_coor_list,train_coor_list):
	return 0



def predict_single_case(line,train_file):
	element_list = line.split('"')[1::2]
	trip_id,start_time,day_type,nearest_stop = element_list[0],int(element_list[1]),element_list[2],int(element_list[3])
	coor_list = np.array(ast.literal_eval(element_list[4]))

	train_content = open(train_file,'r')
	train_content.readline()
	for train_line in train_content.readlines():
		train_element_list = line.split('"')[1:2]
		






def predict_test(test_file,train_file):
	test_content = open(test_file,'r')
	test_content.readline()
	for line in test_content.readlines():
		result = predict_single_case(line,train_file)


		




def main():




if __name__ == "__main__":
	main()


