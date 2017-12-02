'''
split the original data into train and validation set
when selecting the validation set: we use same method proposed in the kaggle competition
training set: validation set = 20 : 1
'''
import numpy as np
import ast
import random 


def substitute_parital_journey(line,cutoff_time):
	element_list = line.split('"')[1::2]
	start_time,coor_list = int(element_list[5]),np.array(ast.literal_eval(element_list[8]))
	coor_len = int((cutoff_time - start_time) / 15)
	new_coor_list = coor_list[:coor_len-1]

	new_line = ""
	for index in range(len(element_list)-1):
		new_line = new_line +"\""+element_list[index]+"\","
	new_line += "\"" + str(new_coor_list.tolist()) + "\"\n"
	return new_line




def split_train(train_file,output_train,output_validation,output_answer,timestamp_list):
	validation_count = 0
	train_count = 0
	content = open(train_file,'r')
	train_result = open(output_train,'w+')
	validation_result = open(output_validation,'w+')
	answer_result = open(output_answer,'w+')

	header = content.readline()
	print(header)
	train_result.write(header)
	validation_result.write(header)


	count = 0
	for line in content.readlines():
		count += 1
		element_list = line.split('"')[1::2]
		start_time,coor_list = int(element_list[5]),np.array(ast.literal_eval(element_list[8]))
		end_time = start_time + (len(coor_list) - 1) * 15
		flag = False
		for cutoff_time in timestamp_list:
			if cutoff_time <= end_time and cutoff_time > start_time:
				#then this journey is active
				validation_count += 1
				flag = True
				if validation_count <= 5000:
					new_line = substitute_parital_journey(line,cutoff_time)
					validation_result.write(new_line)
					dest_x = coor_list[len(coor_list)-1,0]
					dest_y = coor_list[len(coor_list)-1,1]
					answer_result.write(str(dest_x)+","+str(dest_y)+"\n")
				break
		if not flag:
			train_count += 1
			if train_count % 17 == 0:
				train_result.write(line)

		if count % 10000 == 0:
			print(count)

	print("final result")
	print(train_count)
	print(validation_count)

	content.close()
	train_result.close()
	validation_result.close()
	answer_result.close()







def main():
	'''
	the cutoff time for validation set:
	14/08/2013 18:00:00. => 1376503200
	30/09/2013 08:30:00  => 1380529800
	06/10/2013 17:45:00. => 1381081500
	01/11/2013 04:00:00  => 1383278400
	21/12/2013 14:30:00  => 1387636200
	'''

	random.seed(13)
	timestamp_list = random.sample(range(1372809600,1388361600),200)
	split_train("../data/meta/train.csv","../data/preprocessed/split-train.csv","../data/preprocessed/split-validation.csv","../data/preprocessed/validation-answer.csv",timestamp_list)


	

if __name__ == "__main__":
	main()
