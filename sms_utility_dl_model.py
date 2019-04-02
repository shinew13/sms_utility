################sms_utility_dl_model.py###############
'''
pip install --upgrade keras
'''
from keras.losses import *
from keras.metrics import *
from keras.models import *
from keras.layers import *
from keras.utils import *
from keras.utils.training_utils import *
from keras.preprocessing.text import *
from keras.preprocessing.sequence import *
import h5py
import time

from sms_utility_re import *

'''
multi-class models
'''
def build_multiclass_model(positive_class_num = 1,\
	gpus = None):
	model = Sequential()
	model.add(Embedding(input_dim = num_word_max,
		output_dim = 300,
		input_length=num_max_text_len))
	model.add(Dropout(0.1))
	model.add(Conv1D(filters = 500,
		kernel_size = 2, padding='valid',
		activation='relu', strides=1))
	model.add(Conv1D(filters = 500,
		kernel_size = 2, padding='valid',
		activation='relu', strides=1))
	model.add(MaxPooling1D(pool_size=2))
	model.add(Dropout(0.1))
	model.add(Conv1D(filters = 500,
		kernel_size = 3, padding='valid',
		activation='relu', strides=1))
	model.add(GlobalMaxPooling1D())
	model.add(Dropout(0.1))
	model.add(Dense(units = 500, 
		activation='relu'))
	model.add(Dense(positive_class_num+1, \
		activation='softmax'))
	if gpus is not None:
		model = multi_gpu_model(model, gpus = gpus)
	return model

def train_multiclass_model(x_train, y_train, \
	positive_class_num = None,\
	positive_weight = 1, \
	model_file = 'temp_model.h5py', \
	batch_size=500, \
	epochs=3,\
	gpus = None):
	if positive_class_num is None:
		positive_class_num = y_train.shape[1]-1
	model = build_multiclass_model(positive_class_num,\
		gpus = gpus)
	model.compile(loss='categorical_crossentropy',
		optimizer='adam', metrics=['accuracy'])
	class_weight =  {0: 1}
	for class_idx in range(1,positive_class_num+1):
		class_weight[class_idx] = positive_weight
	model.fit(x_train, y_train,
		class_weight = class_weight,
		batch_size=batch_size, epochs=epochs)
	model.save_weights(model_file)
	return model

def load_multiclass_model(model_file,\
	positive_class_num):		
	model = build_multiclass_model(positive_class_num)
	model.load_weights(model_file)
	model.compile(loss='categorical_crossentropy',
		optimizer='adam', metrics=['accuracy'])
	model._make_predict_function()
	return model

'''
entity models
'''
def build_entity_model(\
	num_max_context_len = num_max_context_len,\
	num_max_entity_len = num_max_name_len,\
	include_entity_input = False,\
	gpus = None):
	###left context
	input_left = Input(shape=(num_max_context_len, ))
	emb_word_left = Dropout(0.3)(\
		Embedding(
		input_dim = num_word_max,
		output_dim = 300,
		input_length=num_max_context_len)\
		(input_left))
	conv_left = Conv1D(filters = 500,
		kernel_size = 2, padding='valid',
		activation='relu', strides=1)(\
		emb_word_left)
	max_pooling_left = \
		Dropout(0.3)(\
		GlobalMaxPooling1D()(\
		conv_left))
	###name
	input_name = Input(shape=(num_max_entity_len, ))
	emb_name = Dropout(0.3)(\
		Embedding(
		input_dim = num_word_max,
		output_dim = 300,
		input_length=num_max_entity_len)\
		(input_name))
	conv_name = Conv1D(filters = 100,
		kernel_size = 1, padding='valid',
		activation='relu', strides=1)(\
		emb_name)
	max_pooling_name = \
		Dropout(0.3)(\
		GlobalMaxPooling1D()(\
		conv_name))
	###right context
	input_right = Input(shape=(num_max_context_len, ))
	emb_word_right = Dropout(0.3)(\
		Embedding(
		input_dim = num_word_max,
		output_dim = 300,
		input_length=num_max_context_len)\
		(input_right))
	conv_right = Conv1D(filters = 500,
		kernel_size = 2, padding='valid',
		activation='relu', strides=1)(\
		emb_word_right)
	max_pooling_right = \
		Dropout(0.3)(\
		GlobalMaxPooling1D()(\
		conv_right))
	###
	if include_entity_input:
		marge_layer = [max_pooling_left,\
			input_name,\
			max_pooling_right]
		input_layer = [input_left, input_name, input_right]

	else:
		marge_layer = [max_pooling_left,\
			max_pooling_right]
		input_layer = [input_left, input_right]
	merge_context = concatenate(marge_layer)
	dense = Dense(units = 1000, 
		activation='relu')(\
		merge_context)
	output = Dense(units = 2, 
		activation='softmax')(\
		dense)
	model = Model(\
		inputs=input_layer,\
		outputs=output)
	if gpus is not None:
		model = multi_gpu_model(model, gpus= gpus)
	return model

def train_entity_model(x_train, y_train, \
	positive_weight = 1, \
	model_file = 'temp_model.h5py', \
	batch_size=500, \
	num_max_context_len = num_max_context_len,\
	gpus = None,\
	epochs = 3):
	model = build_entity_model(num_max_context_len \
		= num_max_context_len,\
		gpus = gpus)
	model.compile(loss='categorical_crossentropy',
		optimizer='adam', metrics=['accuracy'])
	model.fit(x_train, y_train,
		class_weight = {0: 1, 1: positive_weight},
		batch_size=batch_size, epochs=epochs)
	model.save_weights(model_file)
	return model

def load_entity_model(model_file,\
	num_max_context_len = num_max_context_len):		
	model = build_entity_model(num_max_context_len \
		= num_max_context_len)
	model.load_weights(model_file)
	model.compile(loss='categorical_crossentropy',
		optimizer='adam', metrics=['accuracy'])
	model._make_predict_function()
	return model
################sms_utility_dl_model.py###############