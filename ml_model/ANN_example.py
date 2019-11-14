# ANN_example.py

from genres import classes
from ANN_parameter import Parameter
from ANN_result import Result
from ANN_class import ANN

# paramterize if you want
# see ANN_parameters.py
net = ANN(p=Parameter(
	num_input=2,
	num_hidden_layers=2,
	nodes_per_hidden=3,
	num_output=len(classes),
	hidden_activation='sigmoid',
	output_activation='softmax',
	initialize=False,
	learning_rate=10,
	loss_function='mean_squared_error'
))

# TODO make this a general function for showin n layers or a specific layer
net.show_weights()

for i in range(0, net.num_hidden_layers + 1):
	print('\n\n****')
	print(net.model.layers[i].get_weights())

net.save_to_disk('test_0')

# The data after removing outliers
# data = outlier_method(RawData)

# Test and train split using encoded Y labels (vector of 0s with one 1)
# trainx, testx, trainy, testy = train_test_split(
# 	data.drop(columns=[dep]),
#	encode(data), # one hot encoder, see ANN_encode.py
#	test_size=0.34,
#	random_state=EXPERIMENT_SEED
#)

# Ordered pair for validating the ANN
# test_set = (testx, np.array(testy))

# Train the network
# returns history of training process, and a callback object that can extract information about the model at the end of events
# history, callback = net.train(
#	trainx,
#	trainy,
#	num_iter=NUM_EPOCHS,
#	testing=test_set
#)
# sample = pd.DataFrame(data=[
# 	[feat_1, feat_2, ... ]
# ], cols=data.cols)

# res = net.predict(sample)
# print(res['title'])
# print(res['artist'])
# for genre in res['prediction']:
# 	print("{0}: {1}".format(genre, res['prediction'][genre]))
