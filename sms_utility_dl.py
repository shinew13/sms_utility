################sms_utility_dl.py###############
from keras.losses import *
from keras.metrics import *
from keras.models import *
from keras.layers import *
from keras.utils import *
from keras.preprocessing.text import *
from keras.preprocessing.sequence import *
import h5py

from sms_utility_re import *
from sms_utility_conll import *
from sms_utility_spark import * 

'''
multi-class models
'''
def build_multiclass_model(positive_class_num = 1):
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
	return model

def train_multiclass_model(x_train, y_train, \
	positive_class_num = None,\
	positive_weight = 1, \
	model_file = 'temp_model.h5py', \
	batch_size=500, \
	epochs=3):
	if positive_class_num is None:
		positive_class_num = y_train.shape[1]-1
	model = build_multiclass_model(positive_class_num)
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
	return model

'''
entity models
'''
def build_entity_model(\
	num_max_context_len = num_max_context_len,\
	num_max_entity_len = num_max_name_len,\
	include_entity_input = False):
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
	return model

def train_entity_model(x_train, y_train, \
	positive_weight = 1, \
	model_file = 'temp_model.h5py', \
	batch_size=500, \
	num_max_context_len = num_max_context_len,\
	epochs=3):
	model = build_entity_model(num_max_context_len \
		= num_max_context_len)
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
	return model

'''
train a deep learning model from a input json file
the input json file should have text, word_indx, label feilds

usage:

rm input.json
vi input.json
i{"text":"This is a positive case","label":1}
{"text":"This is anohter positive case","label":1}
{"text":"This is the third positive case","label":0}
{"text":"but it is negative","label":0}
{"text":"ok another negative","label":0}
{"text":"the last negative case","label":0}

from sms_utility_spark import *
from sms_utility_dl import *

prepare_multiclass_dl_input(\
	'input.json',\
	'input1.json')

dl_model_multiclass_train_from_json(
	'input1.json',\
	num_train = 5,\
	positive_weight_factor = 1,\
	model_file= 'model.h5py', \
	recommend_positive_file_json = 'positive_recommend.json',\
	prediction_text = 'positive_predict.json',\
	epochs=2)
'''
def dl_model_multiclass_train_from_json(
	input_file,\
	num_train = 100000,\
	positive_weight_factor = 2,\
	model_file= 'temp_model.h5py', \
	recommend_positive_file_json = None,\
	recommend_positive_file_conll = None,\
	prediction_text = None,\
	recommend_positive_num = 1000,\
	epochs=3,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	'''
	PREPARE THE DATA
	'''
	print('load the data and count the number of text')
	sqlContext.read.json(input_file)\
		.registerTempTable('input')
	data = sqlContext.sql(u"""
		SELECT word_idx, label
		FROM input
		WHERE word_idx IS NOT NULL
		AND label IS NOT NULL
		""")
	num_text = data.count()
	print('Number of texts: '+str(num_text))
	print('prepare the input')
	data_text_idx1 = np.array(\
		data.select('word_idx')\
		.collect())\
		.reshape((num_text,))
	x = pad_sequences(data_text_idx1, \
		maxlen = num_max_text_len)
	print('prepare the label')
	label = np.array(\
		data.select('label')\
		.collect())\
		.reshape((num_text,))
	y = to_categorical(label)
	'''
	TRAIN THE MODEL
	'''
	#load the training data
	print('number of total samples of each class')
	print(np.sum(y,0))
	idx_negative = np.where(y[:,0] == 1)[0]
	idx_positive = np.where(y[:,0] != 1)[0]
	num_train = num_text if num_text <= num_train else num_train
	np.random.shuffle(idx_negative)
	idx_train = np.concatenate((idx_positive, \
		idx_negative[0:num_train-len(idx_positive)]), \
		axis=0)
	x_train = x[idx_train]
	y_train = y[idx_train]
	#calculate the weights of the positive 
	num_sample_per_class = np.sum(y_train, 0)
	weight_1 = (num_sample_per_class[0]/np.sum(num_sample_per_class[1:]))\
		*positive_weight_factor
	print 'weight of non-negative class:\t', weight_1
	#train the model
	model = train_multiclass_model(x_train, y_train, \
		positive_weight = weight_1, \
		model_file = model_file,\
		epochs=epochs)
	'''
	SHOW THE PREDICTION RESULT
	'''
	#perform prediction and save the prediction results
	y_score = model.predict(x)
	df = sqlContext.createDataFrame(\
		[[int(label1), \
		int(preidction), \
		score, word_idx] \
		for label1, preidction, score, word_idx in \
		zip(label,\
		np.argmax(y_score, axis=1).tolist(),\
		np.max(y_score, axis=1).tolist(),\
		data_text_idx1.tolist())],\
		schema=\
		StructType([StructField("label", LongType()),\
		StructField('prediction', LongType()),\
		StructField('score', DoubleType()),\
		StructField('word_idx', ArrayType(LongType()))])\
		)
	df.cache()
	df.registerTempTable('prediction')
	sqlContext.sql(u"""
		SELECT label, prediction, COUNT(*)
		FROM prediction
		GROUP BY label, prediction
		""").show()
	df.dropDuplicates().registerTempTable('prediction')
	'''
	output the prediction results of the input file
	'''
	if prediction_text is not None:
		print('saving prediction results of original input to '\
			+ prediction_text)
		sqlContext.sql(u"""
			SELECT DISTINCT * FROM prediction
			""").registerTempTable('prediction1')
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.*,
			prediction1.prediction,
			prediction1.score
			FROM input
			JOIN prediction1
			ON prediction1.word_idx = input.word_idx
			""").write.json('temp')
		os.system('cat temp/* > '+prediction_text)
	'''
	output the negatives predicted as positives
	'''
	if recommend_positive_file_json is not None:
		print('saving the recommended positives to '+recommend_positive_file_json)
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.text,
			input.text_entity,
			prediction.prediction
			FROM input
			JOIN prediction
			ON prediction.word_idx = input.word_idx
			WHERE prediction.prediction != 0
			AND prediction.label = 0
			ORDER BY score DESC
			LIMIT """+str(recommend_positive_num))\
		.write.json('temp')
		os.system('cat temp/* > '+recommend_positive_file_json)
	'''
	output the negatives predicted as positives
	'''
	if recommend_positive_file_conll is not None:
		print('saving the recommended positives to conll for annotation')
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.text_entity,
			prediction.prediction
			FROM input
			JOIN prediction
			ON prediction.word_idx = input.word_idx
			WHERE prediction.prediction != 0
			AND prediction.label = 0
			ORDER BY score DESC
			LIMIT """+str(recommend_positive_num))\
		.withColumn('conll',\
			udf(text_entity2conll,\
			StringType())('text_entity'))\
			.registerTempTable('temp')
		sqlContext.sql(u"""
			SELECT DISTINCT CONCAT(conll, '\n') AS conll
			FROM temp 
			LIMIT """)\
		.write.format("text")\
		.options(header="false",sep="\n\n")\
		.mode("append").save("temp")
		os.system('cat temp/* > '+recommend_positive_file_conll)

'''
predcition of multicalss model given a input json file with text word_idx field

usage:

rm input.json
vi input.json 
i{"text":"Goodmorning sir this is Jim can we send our driver now for the mulkiya?"}
{"text":"Hapy birthday to my own lovely sister.  I miss you sis and I pray the good God leads us through this new year of yours"}
{"text":"Dear sir, I want to come today"}
{"text":"your husband is here"}
{"text":"this is a negative example"}

from sms_spark_utility import *
from sms_dl_utility import *

prepare_multiclass_dl_input(\
	'input.json',\
	'input1.json')

dl_model_multiclass_predict_from_json(\
	'input1.json',\
	'model.h5py',\
	positive_class_num = 1,\
	output_text_file = 'output.json')
'''
def dl_model_multiclass_predict_from_json(\
	input_file,\
	model_file,\
	positive_class_num = 1,
	output_text_file = 'text_prediciton.json', 
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	#load the binary model
	model = load_multiclass_model(model_file, \
		positive_class_num = positive_class_num)
	#laod the input data
	sqlContext.read.json(input_file)\
		.registerTempTable('input')
	data = sqlContext.sql(u"""
		SELECT DISTINCT word_idx
		FROM input
		""")
	num_text = data.count()
	print('Number of texts: '+str(num_text))
	##prepare the input
	'''
	this is a bug: if there is two texts with the same 
	numbers of words, an error of 
	'ValueError: cannot reshape array of size 44 into shape (2,)'
	'''
	if num_text > 1:
		try:
			data_text_idx1 = np.array(\
				data.select('word_idx')\
				.collect())\
				.reshape((num_text,))
		except:
			data_text_idx1 = np.array(\
				data.select('word_idx')\
				.collect())
			data_text_idx1 = data_text_idx1.reshape(\
				(num_text,data_text_idx1.shape[2]))
	else:
		data_text_idx1 = np.array(\
			data.select('word_idx')\
			.collect())[0]
	x = pad_sequences(data_text_idx1, \
		maxlen = num_max_text_len)
	#do the prediction
	y_score = model.predict(x)
	###
	df = sqlContext.createDataFrame(\
		[[int(preidction), \
		score, word_idx] \
		for preidction, score, word_idx in \
		zip(np.argmax(y_score, axis=1).tolist(),\
		np.max(y_score, axis=1).tolist(),\
		data_text_idx1.tolist())],\
		schema=\
		StructType([StructField('prediction', LongType()),\
		StructField('score', DoubleType()),\
		StructField('word_idx1', ArrayType(LongType()))])\
		)
	df.cache()
	df.registerTempTable('prediction1')
	sqlContext.sql(u"""
		SELECT prediction, COUNT(*)
		FROM prediction1
		GROUP BY prediction
		""").show()
	#join the prediction to the orignal file
	if output_text_file is not None:
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.*,
			prediction1.prediction,
			prediction1.score
			FROM input
			LEFT JOIN prediction1
			ON prediction1.word_idx1 = input.word_idx
			""").write.json('temp')
		print('saving the prediction results to '+output_text_file)
		os.system('cat temp/* > '+output_text_file)

'''
train a model to predicte if an entity in a text is positive 
according to the contexts

usage:

rm input.json
vi input.json
i{"text":"my name is jim","text_entity":" _start_ my name is [jim] how are you _end_ ","label":1}
{"text":"my name is sayed and you","text_entity":" _start_ my name [sayed] and you _end_ ","label":1}
{"text":"negative name sayed","text_entity":" _start_ negative name [sayed] _end_ ","label":0}
{"text":"another negative name sayed","text_entity":" _start_ another negative name [sayed] _end_ ","label":0}
{"text":"another negative sayed","text_entity":" _start_ negative [sayed] _end_ ","label":0}
{"text":"another negative sayed test","text_entity":" _start_ negative name [sayed] test _end_ ","label":0}

from sms_spark_utility import *
from sms_dl_utility import *

prepare_entity_dl_input(\
	'input.json',\
	'input1.json')

dl_model_entity_train_from_json(\
	'input1.json',\
	num_train = 100000,\
	positive_weight_factor = 1,\
	model_file= 'model.h5py', \
	recommend_positive_json_file\
	= 'positive_recommend.json',\
	prediction_text_file = 'positive_predict.json')
'''
def dl_model_entity_train_from_json(\
	input_file,\
	num_train = 100000,\
	positive_weight_factor = 1,\
	model_file= 'temp_model.h5py', \
	prediction_text_file = None,\
	recommend_positive_json_file = None,\
	recommend_positive_conll_file = None,\
	epochs = 3,\
	num_max_context_len = num_max_context_len,\
	recommend_positive_num = 1000,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	print('load the input training data')
	sqlContext.read.json(input_file)\
		.registerTempTable('input')
	data = sqlContext.sql(u"""
		SELECT left_word_idx,
		entity_word_idx,
		right_word_idx,
		label
		FROM input
		WHERE left_word_idx IS NOT NULL
		OR right_word_idx IS NOT NULL
		""")
	num_text = data.count()
	print('Number of texts: '+str(num_text))
	##prepare the input
	print('prepare the left context word index')
	data_left_word_idx = np.array(\
		data.select('left_word_idx')\
		.collect())\
		.reshape((num_text,))
	x_left = pad_sequences(data_left_word_idx, \
		maxlen = num_max_context_len,\
		truncating = 'pre',\
		padding='pre')
	##
	print('prepare the right context word index')
	data_right_word_idx = np.array(\
		data.select('right_word_idx')\
		.collect())\
		.reshape((num_text,))
	x_right = pad_sequences(data_right_word_idx, \
		maxlen = num_max_context_len,\
		truncating = 'post',\
		padding='post')
	'''
	x_entity = pad_sequences(data_entity, \
		maxlen = num_max_name_len)
	'''
	print('prepare the label')
	data_label = np.array(\
		data.select('label')\
		.collect())\
		.reshape((num_text,))
	##
	x = [x_left, x_right]
	y = to_categorical(data_label)
	###
	idx_positive = np.where(y[:,1] == 1)[0]
	idx_negative = np.where(y[:,0] == 1)[0]
	np.random.shuffle(idx_negative)
	num_negative = num_train-len(idx_positive) \
		if num_train < len(y)\
		else len(idx_negative)
	idx_train = np.concatenate((idx_positive, \
		idx_negative[0:num_negative]))
	print('Number of trianing texts: '+str(len(idx_train)))
	x_train = [x_left[idx_train], \
		x_right[idx_train]]
	y_train = y[idx_train]
	#calculate the weights of the positive 
	num_0, num_1 = np.sum(y_train, 0)
	weight_1 = (num_0/num_1)*positive_weight_factor
	print 'negative training text number:\t', num_0
	print 'positive training text number:\t', num_1
	print 'weight of positive class:\t', weight_1
	#train the model
	print('train the model')
	model = train_entity_model(x_train, y_train, \
		positive_weight = weight_1, \
		model_file = model_file,\
		num_max_context_len = num_max_context_len,\
		epochs=epochs)
	y_score = model.predict(x)
	###
	df = sqlContext.createDataFrame(\
		[[int(label1),\
		int(preidction), \
		score, \
		left_word_idx,\
		right_word_idx] \
		for label1, preidction, score, \
		left_word_idx, right_word_idx in \
		zip(np.argmax(y, axis=1).tolist(),\
		np.argmax(y_score, axis=1).tolist(),\
		np.max(y_score, axis=1).tolist(),\
		data_left_word_idx.tolist(),\
		data_right_word_idx.tolist())],\
		schema=\
		StructType([StructField('label', LongType()),\
		StructField('prediction', LongType()),\
		StructField('score', DoubleType()),\
		StructField('left_word_idx', ArrayType(LongType())),\
		StructField('right_word_idx', ArrayType(LongType()))])\
		)
	df.cache()
	df.registerTempTable('prediction1')
	sqlContext.sql(u"""
		SELECT label, prediction, COUNT(*)
		FROM prediction1
		GROUP BY label, prediction
		""").show()
	df.dropDuplicates().registerTempTable('prediction1')
	'''
	join the prediction to the orignal file
	'''
	if prediction_text_file is not None:
		print('join the prediction to the orignal file and save to '\
			+prediction_text_file)
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.*,
			prediction1.prediction,
			prediction1.score
			FROM input
			JOIN prediction1
			ON prediction1.left_word_idx = input.left_word_idx
			AND prediction1.right_word_idx = input.right_word_idx
			""").write.json('temp')
		os.system('cat temp/* > '+prediction_text_file)
	'''
	output the negatives predicted as positives
	'''
	print('recommend potential positives')
	if recommend_positive_json_file is not None:
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.text_entity, input.text
			FROM input
			JOIN prediction1
			ON prediction1.left_word_idx = input.left_word_idx
			AND prediction1.right_word_idx = input.right_word_idx
			WHERE prediction1.prediction = 1 
			AND prediction1.label = 0
			ORDER BY prediction1.score DESC
			""").write.json('temp')
		os.system('cat temp/* > '+recommend_positive_json_file)
	'''
	save to conll
	'''
	print('recommend potential positives')
	if recommend_positive_conll_file is not None:
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT input.text_entity
			FROM input
			JOIN prediction1
			ON prediction1.left_word_idx = input.left_word_idx
			AND prediction1.right_word_idx = input.right_word_idx
			WHERE prediction1.prediction = 1 
			AND prediction1.label = 0
			ORDER BY prediction1.score DESC
			LIMIT """+str(recommend_positive_num))\
		.withColumn('conll',\
			udf(text_entity2conll,\
			StringType())('text_entity'))\
			.registerTempTable('temp')
		sqlContext.sql(u"""
			SELECT DISTINCT CONCAT(conll, '\n') AS conll
			FROM temp 
			LIMIT """)\
		.write.format("text")\
		.options(header="false",sep="\n\n")\
		.mode("append").save("temp")
		os.system('cat temp/* > '+recommend_positive_conll_file)

'''
predict the category of entities in the text_entity

usage:

rm input.json
vi input.json
i{"text":"my name is jim","text_entity":" _start_ my name is [jim] how are you _end_ ","label":1}
{"text":"my name is sayed and you","text_entity":" _start_ my name [sayed] and you _end_ ","label":1}
{"text":"negative name sayed","text_entity":" _start_ negative name [sayed] _end_ ","label":0}
{"text":"another negative name sayed","text_entity":" _start_ another negative name [sayed] _end_ ","label":0}
{"text":"another negative sayed","text_entity":" _start_ negative [sayed] _end_ ","label":0}
{"text":"another negative sayed test","text_entity":" _start_ negative name [sayed] test _end_ ","label":0}

from sms_utility_spark import *
from sms_utility_dl import *

prepare_entity_dl_input(\
	'input.json',\
	'input1.json')

dl_model_entity_predict_from_json(\
	input_file = 'input1.json',\
	model_file  = 'model.h5py',\
	output_text_file = 'output.json',\
	sqlContext = None)

bug: if all the left/right context has the same number
of words, it will report the 
error of cannot reshape 10 to number_text
'''
def dl_model_entity_predict_from_json(\
	input_file,\
	model_file,\
	output_text_file,\
	num_max_context_len = num_max_context_len,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	#load the binary model
	print('laoding the model from '+model_file)
	model = load_entity_model(model_file,\
		num_max_context_len = num_max_context_len)
	#laod the input data
	print('load the input data from '+input_file)
	sqlContext.read.json(input_file)\
		.registerTempTable('input')
	print('prepare the dl input')
	data = sqlContext.sql(u"""
		SELECT DISTINCT left_word_idx,
		right_word_idx
		FROM input
		""")
	num_text = data.count()
	print('Number of texts: '+str(num_text))
	##prepare the input
	print('prepare the input data')
	print('prepare left context words inputs')
	data_left_word_idx = np.array(\
		data.select('left_word_idx')\
		.collect())
	if num_text > 1:
		try:
			data_left_word_idx = data_left_word_idx\
				.reshape((num_text,))
		except:
			data_left_word_idx = np.squeeze(\
				data_left_word_idx, axis=1)
	else:
		data_left_word_idx = data_left_word_idx[0]
	x_left = pad_sequences(data_left_word_idx, \
		maxlen = num_max_context_len,\
		truncating = 'pre',\
		padding='pre')
	###
	print('prepare right context words inputs')
	data_right_word_idx = np.array(\
		data.select('right_word_idx')\
		.collect())
	if num_text > 1:
		try:
			data_right_word_idx = data_right_word_idx\
				.reshape((num_text,))
		except:
			data_right_word_idx = np.squeeze(\
				data_right_word_idx, axis=1)
	else:
		data_right_word_idx = data_right_word_idx[0]
	x_right = pad_sequences(data_right_word_idx, \
		maxlen = num_max_context_len,\
		truncating = 'post',\
		padding='post')
	##
	x = [x_left, x_right]
	print('predicting the entity type according to the contexts')
	#do the prediction
	y_score = model.predict(x)
	##
	df = sqlContext.createDataFrame(\
		[[int(preidction), \
		score, \
		left_word_idx,\
		right_word_idx] \
		for preidction, score, \
		left_word_idx, right_word_idx in \
		zip(np.argmax(y_score, axis=1).tolist(),\
		np.max(y_score, axis=1).tolist(),\
		data_left_word_idx.tolist(),\
		data_right_word_idx.tolist())],\
		schema=\
		StructType([StructField('prediction', LongType()),\
		StructField('score', DoubleType()),\
		StructField('left_word_idx', ArrayType(LongType())),\
		StructField('right_word_idx', ArrayType(LongType()))])\
		)
	df.cache()
	df.registerTempTable('prediction')
	sqlContext.sql(u"""
		SELECT prediction, COUNT(*)
		FROM prediction
		GROUP BY prediction
		""").show()
	#join the prediction to the orignal file
	if output_text_file is not None:
		print('saving the prediction results and corresponding sms data to '\
		+output_text_file)
		os.system('rm -r temp')
		sqlContext.sql(u"""
			SELECT DISTINCT input.*,
			prediction.prediction,
			prediction.score
			FROM input
			JOIN prediction
			ON prediction.left_word_idx = input.left_word_idx
			AND prediction.right_word_idx = input.right_word_idx
			""").write.json('temp')
		os.system('cat temp/* > '+output_text_file)
################sms_dl_utility.py###############