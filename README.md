# UCLA Fall 2017 CS249: Big Data Analytics (Wei Wang)

## Introduction
The goal of this project is to predict the taxi trip destination in Porto, Portugal based on some given initial partial trajectories. Kaggle contest details can be found [here](https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i).

## Members
- Junheng Hao (jhao@cs.ucla.edu)
- Xue Sun (cynosure@ucla.edu)
- Yunsheng Bai (yba@ucla.edu)
- Tzu-Wei Chuang (twc@g.ucla.edu)

## Code Explanation
- `Strategy Analytics` folder gives intuition on how we decided to do some preprocessing to eliminate useless information. 
  - `count_waiting.py`: counts the number of waiting instances in a taxi trip. 
  - `timeSelection.py`: showed a good reason why -3~+1 minutes are meaningful to our trajectory. 
  - `visualization.py`: generates the Snip20171203_2.png.
  - `Snip20171203_2.png`: a picture of nearest taxi stand vs the destination count, this provides a good reason that users are likely to visit certain destinations starting from the same nearest taxi stands.
- `data` folder contains the necessary files used for training and testing our algorithm.
- `similarity-based` folder contains the code for our similarity-based baseline model. 
- `adbreds-taxi` folder contains the code for neural network based model. Explanation on code and models can be found in `README.md` inside this folder.

## Link
For brief review of our motivation and methods, please see the [slides](https://github.com/vivi51123/CS249-Current-Topics-in-Data-Structure/blob/master/doc/Taxi%20Project%20Presentation-VWXYJ.pdf). For more detail in implementation, training process and results, please see the [project report](https://github.com/vivi51123/CS249-Current-Topics-in-Data-Structure/blob/master/doc/cs249-project-report-VWXYJ.pdf).
