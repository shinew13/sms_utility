######################sms_utility_spark.py######################
import re
import os
import random
from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

from sms_utility_re import *

try:
	sc = SparkContext("local", "sms_utility_spark")
	sqlContext_local = SparkSession.builder.getOrCreate()
	print('created sqlContext_local')
except:
	pass

'''
load entities/indicators from a csv file

usage

rm entities.csv
vi entities.csv
i wang
jingyan
456 ewn

you can also put arabic in to the csv file

hadoop fs -rm -r entities.csv
hadoop fs -put entities.csv ./

from sms_utility_spark import *

load_entities('indicator.csv',\
	return_format = 'df')\
	.show()

print load_entities('entities.csv',\
	return_format = 'list',\
	ignore_space_at_start_and_end = True)

usage:

rm entities.json
vi entities.json
i{"entity":"wang"}
{"entity":"\u0627\u0628\u0646\u064a"}

hadoop fs -rm -r entities.json
hadoop fs -put entities.json ./

from sms_utility_spark import *

load_entities(\
	entity_file = 'entities.json',\
	return_format = 'df')\
	.show()

print load_entities('entities.json',\
	return_format = 'list',\
	ignore_space_at_start_and_end = True)
'''
def load_entities(entity_file = None,\
	return_format = 'df',\
	ignore_space_at_start_and_end = False,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if entity_file.split('.')[-1] == 'csv':
		print('loading the entities from '+entity_file)
		customSchema = StructType([\
			StructField("entity", StringType(), True)])
		sqlContext.read.format("csv")\
			.option("header", "false")\
			.schema(customSchema)\
			.load(entity_file)\
			.withColumn('entity',\
			udf(lambda input: indicator_preprocess(input,\
			ignore_space_at_start_and_end = \
			ignore_space_at_start_and_end),\
			StringType())\
			('entity'))\
			.registerTempTable('entities')
	if entity_file.split('.')[-1] == 'json':
		print('loading the entities from '+entity_file)
		entity_df_json = sqlContext.read.json(entity_file)
		entity_df_json.withColumn('entity',\
			udf(lambda input: indicator_preprocess(input,\
			ignore_space_at_start_and_end = \
			ignore_space_at_start_and_end),\
			StringType())\
			(entity_df_json.columns[0]))\
			.registerTempTable('entities')
	df_entity = sqlContext.sql(u"""
		SELECT DISTINCT entity
		FROM entities
		WHERE entity IS NOT NULL
		""")
	number_entity = df_entity.count()
	print('loaded '+str(number_entity)+' entities')
	if return_format == 'df':
		return df_entity
	if return_format == 'list':
		return [row['entity'] \
		for row \
		in df_entity.select('entity').collect()]

'''
updating entities from a csv file of adding/deleting

usage:

rm entity.csv
vi entity.csv
i
jim
wang
yan

rm entity_to_delete.csv
vi entity_to_delete.csv
i
yan

rm entity_to_add.csv
vi entity_to_add.csv
i
liang

hadoop fs -rm -r /data/jim/entity.csv
hadoop fs -put /data/jim/entity.csv /data/jim/

hadoop fs -rm -r /data/jim/entity_to_delete.csv
hadoop fs -put /data/jim/entity_to_delete.csv /data/jim/

hadoop fs -rm -r /data/jim/entity_to_add.csv
hadoop fs -put /data/jim/entity_to_add.csv /data/jim/

from sms_utility_spark import * 

entity_csv_update(\
	entity_file_input = '/data/jim/entity.csv',
	entity_file_to_delete = '/data/jim/entity_to_delete.csv',
	entity_file_to_add = '/data/jim/entity_to_add.csv',
	output_file_csv = '/data/jim/entity_new.csv',
	sqlContext = sqlContext)

entity_csv_update(
	entity_file_input = '/data/jim/entity.csv',
	entity_file_to_delete = '/data/jim/entity_to_delete.csv',
	output_file_csv = '/data/jim/entity_new.csv',
	sqlContext = sqlContext)

entity_csv_update(
	entity_file_input = '/data/jim/entity.csv',
	entity_file_to_add = '/data/jim/entity_to_add.csv',
	output_file_csv = '/data/jim/entity_new.csv',
	sqlContext = sqlContext)
'''
def entity_csv_update(entity_file_input,
	entity_file_to_delete = None,
	entity_file_to_add = None,
	output_file_csv = None,
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	###
	entity_df = load_entities(
		entity_file = entity_file_input,
		return_format = 'df',
		ignore_space_at_start_and_end = True,
		sqlContext = sqlContext)
	entity_df.cache()
	entity_df.registerTempTable('entity_df')
	###
	if entity_file_to_add is not None:
		entity_df_to_add = load_entities(
			entity_file = entity_file_to_add,\
			return_format = 'df',
			ignore_space_at_start_and_end = True,
			sqlContext = sqlContext)
		entity_df_to_add.cache()
		entity_df_to_add.registerTempTable('entity_df_to_add')
		###
		entity_temp = sqlContext.sql(u"""
			SELECT DISTINCT * FROM (
			SELECT * FROM entity_df
			UNION ALL
			SELECT * FROM entity_df_to_add
			) AS temp
			""")		
	else:
		entity_temp = sqlContext.sql(u"""
			SELECT * FROM entity_df
			""")	
	entity_temp.registerTempTable('entity_temp')
	entity_temp.cache()
	###
	if entity_file_to_delete is not None:
		entity_df_to_delete = load_entities(
			entity_file = entity_file_to_delete,\
			return_format = 'df',
			ignore_space_at_start_and_end = True,
			sqlContext = sqlContext)
		entity_df_to_delete.cache()
		entity_df_to_delete.registerTempTable('entity_df_to_delete')
		###
		output_df = sqlContext.sql(u"""
			SELECT entity_temp.*
			FROM entity_temp
			LEFT JOIN entity_df_to_delete
			ON entity_df_to_delete.entity = 
			entity_temp.entity
			WHERE entity_df_to_delete.entity IS NULL
			""")
	else:
		output_df = sqlContext.sql(u"""
			SELECT entity_temp.*
			FROM entity_temp
			""")
	output_df.cache()
	####
	if output_file_csv is not None:
		print(u"saving results to "+output_file_csv)
		output_df_temp = 'temp'+str(random.randint(0, 10000000000))\
			.zfill(10)
		os.system(u"hadoop fs -rm -r "+output_df_temp)
		os.system(u"rm -r "+output_df_temp)
		output_df.write.format('csv').save(output_df_temp)
		os.system(u"hadoop fs -get "+output_df_temp+" ./")
		os.system(u"cat "+output_df_temp+"/* > "+output_file_csv)
		os.system(u"hadoop fs -rm -r "+output_file_csv)
		os.system(u"hadoop fs -cp -f "+output_df_temp+u" "+output_file_csv)
		os.system(u"hadoop fs -rm -r "+output_df_temp)
		os.system(u"rm -r "+output_df_temp)
	return output_df

'''
map a title csv tile to a relation datatframe

rm titles.csv
vi titles.csv
ifather
dada
daddy

title_relation_df = title_csv2title_relation_df(\
	'titles.csv',\
	'father_of',\
	relation_reverse_type = 'child_of')
'''
def title_csv2title_relation_df(input_file,\
	relation_type,\
	relation_reverse_type = None,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if input_file.split('.')[-1] == 'csv':
		customSchema = StructType([\
			StructField("title", StringType(), True)])
		sqlContext.read.format("csv").option("header", "false")\
			.schema(customSchema)\
			.load(input_file)\
			.withColumn('title',\
			udf(lambda input: indicator_preprocess(\
			input, ignore_space_at_start_and_end = True),\
			StringType())\
			('title'))\
			.registerTempTable('temp')
	if input_file.split('.')[-1] == 'json':
		sqlContext.read.json(input_file)\
			.registerTempTable('temp')
	if relation_reverse_type is not None:
		return sqlContext.sql(u"""
			SELECT DISTINCT *, 
			'"""+relation_type+u"""' AS relation,
			'"""+relation_reverse_type+u"""' AS relation_reverse
			FROM temp
			""")
	else:
		return sqlContext.sql(u"""
			SELECT DISTINCT *, 
			'"""+relation_type+u"""' AS relation,
			NULL AS relation_reverse
			FROM temp
			""")

'''
convert text to text with wild patterns of re
usage:

sudo rm input.json
sudo vi input.json
i{'text':' this ia an email jingx@gmgn.com 24r&234 P00 '}

hadoop fs -rm -r input.json
hadoop fs -put input.json ./

from sms_utility_spark import *

text_json2text_entity_wildcard_re_json(
	input_json = 'input.json',
	output_json = 'output.json',
	entity_fun_res = [text2text_email, extract_number],
	enitty_names = ['email', 'number'],
	sqlContext = sqlContext)
'''
def text_json2text_entity_wildcard_re_json(input_json,
	output_json,
	entity_fun_res,
	enitty_names,
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	print('loading data from '+input_json)
	output_df = sqlContext.read.json(input_json)
	output_df = output_df.withColumn('text_entity', udf(lambda input: input, \
		StringType())('text'))
	for entity_fun_re, entity_name \
		in zip(entity_fun_res, enitty_names):
		print('extracting entities by '+str(entity_fun_re))
		output_df = output_df.withColumn('text_entity',
			udf(entity_fun_re, StringType())('text_entity'))
		output_df = output_df.withColumn(entity_name,
			udf(text_entity2entities, ArrayType(StringType()))('text_entity'))
		output_df = output_df.withColumn('text_entity',
			udf(lambda input: \
			text_entity2text_entity_wildcard(input, entity_name), \
			StringType())('text_entity'))
	output_df = output_df.withColumn('text_entity',
		udf(text_preprocess, StringType())('text_entity'))
	output_df.cache()
	print('saving results to '+output_json)
	os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
	output_df.write.json('temp')
	os.system(u"""
		hadoop fs -get temp ./
		cat temp/* > """+output_json)
	os.system(u'hadoop fs -rm -r '+output_json)
	os.system(u'hadoop fs -mv temp '+output_json)

'''
usage: 

text_json2entity_re_json(\
	input_json = '/data/jim/sms_business.json',\
	output_json = '/data/jim/clinic_dr_name.json',\
	entity_extract_re_funcs = [extract_dr_name],\
	enitty_names = ['dr_name'])
'''
def text_json2entity_re_json(input_json,\
	output_json,\
	entity_extract_re_funcs,\
	enitty_names,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	print('loading data from '+input_json)
	output_df = sqlContext.read.json(input_json)
	print('extracging entities from sms')
	for func, entity_name \
		in zip(entity_extract_re_funcs, enitty_names):
		print('extracting entities by '+str(func))
		output_df = output_df.withColumn(entity_name,\
			udf(func, StringType())('text'))
		output_df.cache()
	print('saving results to '+output_json)
	os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
	output_df.write.json('temp')
	os.system(u"""
		hadoop fs -get temp ./
		cat temp/* > """+output_json)
	os.system(u'hadoop fs -rm -r '+output_json)
	os.system(u'hadoop fs -mv temp '+output_json)

'''
extract entities from a dataframe of text
by using a extraction function

rm input.json
vi input.json
i{"text":"it is 10:10 am now","sender":"1"}
{"text":"this is a test","sender":"2"}
{"sender":"1"}

usage: 

from sms_utility_spark import *
sqlContext = sqlContext_local

entity_extract_fun = lambda input: \
	extract_entity_by_re(input, \
	re_arabic_number)

input_df = sqlContext.read.json('input.json')

text_df2text_entity_df_by_func(input_df,\
	entity_extract_fun = entity_extract_fun,\
	entity_type = 'number',
	extract_entity_from_original_text = True,\
	nearby_entity_merge = False)\
	.show(100, False)
'''
def text_df2text_entity_df_by_func(input_df,\
	entity_extract_fun,\
	entity_type = 'entity',
	extract_entity_from_original_text = False,\
	nearby_entity_merge = False,\
	entity_type_repalce_by_wildcard = False,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	'''
	extract entities from text by extraction function
	'''
	print('extracting entities by using functin '\
		+str(entity_extract_fun))
	if extract_entity_from_original_text is True:
		output_df = input_df.withColumn('text_entity',\
			udf(entity_extract_fun, StringType())\
			('text'))
	else:
		output_df = input_df.withColumn('text_entity',\
			udf(entity_extract_fun, StringType())\
			('text_entity'))
	if nearby_entity_merge is True:
		output_df = output_df.withColumn('text_entity', \
		udf(lambda input: re.sub('\]\s+\[', ' ', input) \
		if input is not None else None, \
		StringType())\
		('text_entity'))
	output_df = output_df.withColumn(entity_type, \
		udf(text_entity2entities, ArrayType(StringType()))\
		('text_entity'))
	'''
	replace the entities by wildcard so that in the 
	text_preprocessing fucntion they will not be effected
	'''
	output_df = output_df.withColumn('text_entity', \
		udf(lambda input:\
		text_entity2text_entity_wildcard(\
		input, entity_type), StringType())\
		('text_entity'))
	if extract_entity_from_original_text is True:
		output_df = output_df.withColumn('text_entity', \
			udf(text_preprocess, StringType())\
			('text_entity'))
	if entity_type_repalce_by_wildcard is False:
		output_df = output_df.withColumn('text_entity',\
			udf(lambda input, entities: \
			text_wildcard_entity_recovery(input, \
			entities, entity_type,\
			with_bracket = True), StringType())\
			('text_entity', entity_type))
	return output_df

'''
sudo rm input.json
sudo vi input.json
i{"text":"this is wang and you?","sender":"1"}
{"text":" but it is wang, jingyan haha","sender":"2"}
{"text":" but it is wang, jingyan wang haha","sender":"3"}
{"text":" i will cost 131 cloud haha","sender":"4"}
{"text":" i will cost 131 cloud haha","sender":"5"}
{"text":"a test","sender":"5"}

sudo rm entities.csv
sudo vi entities.csv
iwang
"wang, jingyan"
331 cloud
mr

hadoop fs -rm -r input.json
hadoop fs -rm -r entities.csv
hadoop fs -put input.json ./
hadoop fs -put entities.json ./

from sms_utility_spark import *
sqlContext = sqlContext_local

input_df = sqlContext.read.json('input.json')

text_df2text_entity_df_by_entity_match(\
	input_df,\
	'entities.csv',\
	entity_type = 'name',\
	sqlContext = sqlContext)\
	.show(100, False)

text_df2text_entity_df_by_entity_match(\
	input_df,\
	'entities.csv',\
	entity_type = 'name',\
	mathc_entity_by_word = True)\
	.show(100, False)
'''
def text_df2text_entity_df_by_entity_match(\
	input_df,\
	entity_file,\
	mathc_entity_by_word = False,\
	entity_type = None,\
	nearby_entity_merge = False,\
	entity_type_repalce_by_wildcard = False,\
	ignoare_entity = True,\
	sqlContext  = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if entity_type is None:
		entity_type = 'entity'
	if 'text_entity' not in input_df.columns:
		print('preprocessing text')
		input_df = input_df.withColumn(\
			'text_entity',\
			udf(text_preprocess, StringType())\
			('text'))
		input_df.cache()
	###	match the entities by a fucntion	
	if mathc_entity_by_word is False:
		entities = load_entities(entity_file,\
			return_format = 'list',\
			ignore_space_at_start_and_end = False,\
			sqlContext = sqlContext)
		entity_extract_fun = lambda input: \
			marge_entity2preprocessed_text(\
			input,\
			entities, \
			nearby_entity_merge = nearby_entity_merge)
		output_entity = text_df2text_entity_df_by_func(\
			input_df,\
			entity_extract_fun,\
			entity_type = entity_type,
			extract_entity_from_original_text = False,\
			nearby_entity_merge = nearby_entity_merge,\
			entity_type_repalce_by_wildcard = \
			entity_type_repalce_by_wildcard,\
			sqlContext = sqlContext)
		output_entity.cache()
	if mathc_entity_by_word is True:
		df_entity = load_entities(entity_file,\
			return_format = 'df',\
			sqlContext = sqlContext)
		'''
		load the texts from the input json file
		'''
		input_df.registerTempTable('input')
		df_input = sqlContext.sql(u"""
			SELECT DISTINCT text_entity
			FROM input
			WHERE text_entity IS NOT NULL
			""")
		'''
		match words of preprocessed text and the entity
		to find the candidate text-entity paires
		'''
		print('spliting input texts and entities to words')
		'''
		split the input text to words
		'''
		df_input.withColumn('word',\
			udf(lambda input: process_text2words(input, \
			ignore_start_and_end = True,\
			irgnore_puntuation = True,\
			ignoare_entity = ignoare_entity),\
			ArrayType(StringType()))\
			('text_entity'))\
			.withColumn('word', explode('word'))\
			.registerTempTable('temp1')
		input_word = sqlContext.sql(u"""
			SELECT DISTINCT text_entity, word
			FROM temp1
			WHERE word IS NOT NULL
			""")
		input_word.cache()
		input_word.registerTempTable('input_word')
		'''
		split the entities to words
		'''
		df_entity.withColumn('word',\
			udf(lambda input: process_text2words(input, \
			irgnore_puntuation = True,\
			ignoare_entity = ignoare_entity),\
			ArrayType(StringType()))\
			('entity'))\
			.withColumn('word',\
			explode('word'))\
			.registerTempTable('temp2')
		entity_word = sqlContext.sql(u"""
			SELECT DISTINCT entity, word
			FROM temp2
			WHERE word IS NOT NULL
			""")
		entity_word.cache()
		entity_word.registerTempTable('entity_word')
		'''
		join by words and the entity to texts
		'''
		print('matching entities to texts by joining words')
		input_entity_candidate2 = sqlContext.sql(u"""
			SELECT DISTINCT 
			input_word.text_entity,
			entity_word.entity
			FROM input_word
			JOIN entity_word
			ON input_word.word = entity_word.word
			""").groupby('text_entity')\
			.agg(collect_set('entity').alias('entity'))
		input_entity_candidate2.cache()
		input_entity_candidate2.registerTempTable(\
			'text_entity_indicator_candidate')
		output_entity = sqlContext.sql(u"""
			SELECT input.*,
			text_entity_indicator_candidate.entity
			AS candidate_entities
			FROM input
			LEFT JOIN text_entity_indicator_candidate
			ON text_entity_indicator_candidate.text_entity
			= input.text_entity
			""")
		output_entity.cache()
		'''
		there is another way to generate entity by matching 
		text to entity by hashing and set intersation
		the input must have text_entity and candidate_entities
		but this method needs regex
		'''
		'''
		entities = load_entities(entity_file,\
			return_format = 'list',\
			ignore_space_at_start_and_end = True,\
			sqlContext = sqlContext)
		try:
			print('matching enities by set intersection')
			entities_set = set(entities)
			entiteis_not = [e for e in entities_set if '_not_' in e]
			find_candidate_entities_by_set = \
				lambda input: list(entities_set.intersection(\
				set(text_entity2text_entity_subset(input))))+\
				entiteis_not
			output_entity = input_df.withColumn('candidate_entities',\
				udf(find_candidate_entities_by_set, \
				ArrayType(StringType()))\
				('text_entity'))
		except:
			output_entity = input_df.withColumn(\
				'candidate_entities',\
				udf(lambda input: entities, \
				ArrayType(StringType()))\
				('text_entity'))
		'''
		'''
		merge the candidate entiteis to the text_entity
		'''
		print('merging matched entities to text_entity')
		output_entity = output_entity.withColumn('text_entity',\
			udf(lambda input, entities: \
			marge_entity2preprocessed_text(input, \
			entities, nearby_entity_merge = nearby_entity_merge), \
			StringType())\
			('text_entity', 'candidate_entities'))\
			.drop('candidate_entities')\
			.withColumn(entity_type,\
			udf(text_entity2entities, ArrayType(StringType()))\
			('text_entity'))
		output_entity.cache()
	if entity_type_repalce_by_wildcard is True:
		output_entity = output_entity\
			.withColumn('text_entity',\
			udf(lambda input: \
			text_entity2text_entity_wildcard(\
			input, entity_type), \
			StringType())\
			('text_entity'))
	return output_entity

'''
rm input.json
vi input.json
i{"text":"i have 100 aed and you give me usd 100.00 "}

rm currency.csv
vi currency.csv
iaed
usd

rm money_indicator.csv
vi money_indicator.csv
i_number_ _currency_
_currency_ _number_

text_entity_json2text_entity_comb_json(\
	comb_entity_indicator_csv = 'money_indicator.csv',\
	comb_entity = 'money',\
	sub_entity_files_funcs = [extract_number,\
	'currency.csv'],\
	sub_entity_types = ['number',\
	'currency'],\
	input_json = 'input.json',\
	output_json = 'output.json',\
	sqlContext = sqlContext)
'''

def text_entity_json2text_entity_comb_json(\
	comb_entity_indicator_csv,\
	comb_entity = 'entity',\
	sub_entity_files_funcs = None,\
	sub_entity_types = None,\
	sub_entity_indicator_match_by_word = None,\
	sub_entity_type_repalce_by_wildcard = False,\
	input_json = None,\
	input_df = None,\
	output_json = None,\
	comb_entity_indicator_match_by_word = False,\
	comb_entity_type_repalce_by_wildcard = False,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if input_json is not None:
		print('loading data from '+input_json)
		input_df = sqlContext.read.json(input_json)
	'''
	1. replace the sub entities by function/indicators
	'''
	if sub_entity_indicator_match_by_word is None:
		sub_entity_indicator_match_by_word = [False]*len(sub_entity_files_funcs)
	print('replace the sub entties')
	output_df = input_df
	extract_entity_from_original_text = True
	for entity_indicator, entity_type, entity_match_by_word \
		in zip(sub_entity_files_funcs,\
			sub_entity_types,\
			sub_entity_indicator_match_by_word):
		if entity_type not in output_df.columns:
			print('extracting '+entity_type)
			if type(entity_indicator) is str:
				output_df = text_df2text_entity_df_by_entity_match(\
					output_df,\
					entity_file = entity_indicator,\
					entity_type = entity_type,\
					entity_type_repalce_by_wildcard = True,\
					nearby_entity_merge = True,\
					mathc_entity_by_word = entity_match_by_word,\
					sqlContext  = sqlContext)
			else:
				output_df = text_df2text_entity_df_by_func(\
					output_df,\
					entity_extract_fun = entity_indicator,\
					entity_type = entity_type,
					extract_entity_from_original_text =\
					extract_entity_from_original_text,\
					nearby_entity_merge = True,\
					entity_type_repalce_by_wildcard = True,\
					sqlContext = sqlContext)
				if extract_entity_from_original_text is True:
					extract_entity_from_original_text = False
	'''
	2. match to the comb entity indicators
	'''
	print('matching to comb entity indicators')
	output_df = text_df2text_entity_df_by_entity_match(\
		output_df,\
		entity_file = comb_entity_indicator_csv,\
		entity_type = comb_entity,\
		mathc_entity_by_word =\
		comb_entity_indicator_match_by_word, \
		nearby_entity_merge = True,\
		sqlContext  = sqlContext)
	'''
	3. recover the sub entities
	'''
	if sub_entity_type_repalce_by_wildcard is not True:
		print('recover the sub entities in the comb entity')
		for entity_type in sub_entity_types:
			output_df = output_df.withColumn('text_entity',\
				udf(lambda input, entities:\
				text_entity_wildcard_subentity_recovery(input, \
				entities, \
				entity_type))('text_entity', entity_type))
	'''
	4. recover the comb_entities
	'''
	print('extracting the comb entities')
	output_df = output_df.withColumn(comb_entity,\
		udf(text_entity2entities, ArrayType(StringType()))\
		('text_entity'))
	'''
	5. replace the comb entities by wild card
	'''
	if comb_entity_type_repalce_by_wildcard is True:
		print('')
		output_df = output_df.withColumn('text_entity',\
			udf(lambda input: text_entity2text_entity_wildcard(\
			input, comb_entity), \
			StringType())('text_entity'))
	###
	if output_json is not None:
		print('saving results to '+output_json)
		os.system(u"""
			hadoop fs -rm -r temp
			rm -r temp
			""")
		output_df.write.json('temp')
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_json)
		os.system('hadoop fs -rm -r '+output_json)
		os.system('hadoop fs -cp -f temp '+output_json)
		print('results saved to '+output_json)
	else:
		return output_df

'''
conver a json file of text to texts with entities
by mathcing to a csv file of entities

usage:

rm input.json
vi input.json
i{"text":"this is wang and you?","sender":"1"}
{"text":" but it is wang, jingyan haha","sender":"2"}
{"text":" but it is wang, jingyan wang haha","sender":"3"}
{"text":" i will cost 131 cloud haha","sender":"4"}
{"text":" i will cost 131 cloud haha","sender":"5"}
{"text":"a test","sender":"5"}

rm entities.csv
vi entities.csv
iwang
"wang, jingyan"
331 cloud
mr

from sms_utility_spark import *

import time
start_time = time.time()
text_json2text_entity_json('input.json',
	'output1.json',\
	entity_file = 'entities.csv',\
	entity_type = 'name',\
	nearby_entity_merge = True)
print(time.time() - start_time)
#1.59361386299

import time
start_time = time.time()
text_json2text_entity_json('input.json',
	'output1.json',\
	entity_file = 'entities.csv',\
	mathc_entity_by_word = True,\
	entity_type = 'name',\
	nearby_entity_merge = True)
print(time.time() - start_time)
#22.5578608513

usage:

from sms_utility_spark import *

extract_number = lambda input: \
	extract_entity_by_re(input, \
	re_arabic_number)

text_json2text_entity_json(\
	'input.json',
	'output.json',\
	entity_extract_fun = extract_number,\
	entity_type = 'number',\
	entity_type_repalce_by_wildcard = True)

usage:

rm input.json
vi input.json
i{"text":"my wife will come"}
{"text":"my son will come"}
{"sender":"123"}

rm indicator.csv
vi indicator.csv
imy wife

from sms_utility_spark import *

text_json2text_entity_json(\
	input_json = 'input.json',
	output_json = 'output.json',\
	entity_file = 'indicator.csv',\
	entity_type = 'male_indicator',\
	entity_surrounded_by_brackets = False)
'''
def text_json2text_entity_json(input_json = None,
	input_df = None,\
	output_json = None,\
	entity_extract_fun = None,\
	entity_file = None,\
	mathc_entity_by_word = False,\
	entity_type = None,\
	nearby_entity_merge = False,\
	entity_type_repalce_by_wildcard = False,\
	entity_surrounded_by_brackets = True,\
	ignoare_entity = True,\
	sqlContext  = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if input_json is not None:
		print('loading the input date from '+input_json)
		input_df_original = sqlContext.read.json(input_json)
	else:
		input_df_original = input_df
	'''
	matching to short entity list by fucntion
	'''
	if entity_extract_fun is not None:
		print('extracting entities from text by fucntion '\
			+str(entity_extract_fun))
		if 'text_entity' in input_df_original.columns:
			extract_entity_from_original_text = False
		else:
			extract_entity_from_original_text = True
		output_entity = text_df2text_entity_df_by_func(\
			input_df_original,\
			entity_extract_fun,\
			entity_type = entity_type,
			extract_entity_from_original_text \
			= extract_entity_from_original_text,\
			nearby_entity_merge = nearby_entity_merge,\
			entity_type_repalce_by_wildcard = \
			entity_type_repalce_by_wildcard,\
			sqlContext = sqlContext)
	'''
	matching to a entity csv file by word matching to 
	reduce search space
	'''
	if entity_file is not None:
		print('extracting entities from text by matching to '\
			+entity_file)
		output_entity = text_df2text_entity_df_by_entity_match(\
			input_df_original,\
			entity_file,\
			mathc_entity_by_word = mathc_entity_by_word,\
			entity_type = entity_type,\
			nearby_entity_merge = nearby_entity_merge,\
			entity_type_repalce_by_wildcard = \
			entity_type_repalce_by_wildcard,\
			ignoare_entity = ignoare_entity,\
			sqlContext  = sqlContext)
	if entity_surrounded_by_brackets is False:
		output_entity = output_entity.withColumn(\
			'text_entity',\
			udf(lambda input: re.sub('\[|\]', '', input) \
			if input is not None else None,\
			StringType())('text_entity'))
	if output_json is not None:
		print('saving the result to '+output_json)
		os.system(u"""
			hadoop fs -rm -r temp
			rm -r temp
			""")
		output_entity.write.json('temp')
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_json)
		os.system('hadoop fs -rm -r '+output_json)
		os.system('hadoop fs -cp -f temp '+output_json)
	else:
		return output_entity

'''
replace the entities in a context of entity by wildcards

usage:

rm input.json
vi input.json
i{"text_entity":" _start_ this is mr jim i am from [China] _end_ ","location":["china"]}
{"text_entity":" _start_ are you in [Dubai] dr jim _end_ ","location":["dubai"]}

rm names.csv
vi names.csv
ijim
yan
smith

rm title.csv
vi title.csv
imr
dr

from sms_utility_spark import *

text_context_json2text_context_entity_wildcard_json(\
	input_json = 'input.json',\
	output_json = 'output.json',\
	target_entity = 'location',\
	entity_files = ['names.csv', 'title.csv'],\
	entities =  ['name', 'title'],\
	sqlContext = sqlContext)
'''
def text_context_json2text_context_entity_wildcard_json(\
	entity_files,\
	entities,\
	input_json = None,\
	input_df = None,\
	output_json = None,\
	target_entity = None,\
	entity_nearby_merge = None,\
	mathc_entity_by_word = None,\
	sqlContext  = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	###
	if input_json is not None:
		print('loading the input texts from '+input_json)
		input_df = sqlContext.read.json(input_json)
	'''
	before replace the entities in the context, firstly 
	replace the target entity, so that the target entiteis
	are not effected.
	The target entities will be recoevered later
	'''
	output_df = input_df
	if target_entity is not None:
		print('replace the target entity by wildcard')
		output_df = output_df.withColumn(\
			'text_entity',\
			udf(lambda input: text_entity2text_entity_wildcard(\
			input, target_entity), \
			StringType())('text_entity'))
	else:
		if 'text_entity' not in input_df.columns:
			output_df = output_df.withColumn(\
			'text_entity',\
			udf(text_preprocess, StringType())('text'))
	###
	print('replace the entities in context by wildcards')
	if entity_nearby_merge is None:
		entity_nearby_merge = [False]*len(entity_files)
	if mathc_entity_by_word is None:
		mathc_entity_by_word = [False]*len(entity_files)
	for entity_csv, entity_type, nearby_entity_merge, \
		match_entity_by_word \
		in zip(entity_files, entities,\
			entity_nearby_merge,\
			mathc_entity_by_word):
		output_df = text_df2text_entity_df_by_entity_match(\
			output_df,\
			entity_csv,\
			mathc_entity_by_word = match_entity_by_word,\
			entity_type = entity_type,\
			nearby_entity_merge = nearby_entity_merge,\
			entity_type_repalce_by_wildcard = True,\
			sqlContext  = sqlContext)
	output_df.cache()
	###
	if target_entity is not None:
		print('receovering the '+target_entity+' entities')
		output_df = output_df.withColumn('text_entity', \
			udf(lambda input, entities: \
			text_wildcard_entity_recovery(input, \
			entities, entity_type = target_entity, \
			with_bracket = True),\
			StringType())('text_entity', target_entity))
	output_df.cache()
	if output_json is not None:
		print('saving the results to '+output_json)
		os.system(u"""
			hadoop fs -rm -r temp
			rm -r temp
			""")
		output_df.write.json('temp')
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_json)
		os.system(u"hadoop fs -rm -r "+output_json)
		os.system(u"hadoop fs -cp -f temp "+output_json)
		print('results saved to '+output_json)
	return output_df


'''
replace the entities in the context of indicators

usage:

sudo rm input.csv
sudo vi input.csv
i _start_ this is jim working for pegasus
_start_ this is [dr] working for pegasus my wife is jean

sudo rm name1.csv 
sudo vi name1.csv 
ijim
jean

sudo rm orgnization1.csv 
sudo vi orgnization1.csv 
ipegasus

input_csv = 'input.csv'
output_csv = 'output.csv'

entity_files = ['name1.csv', 'orgnization1.csv']
entities = ['name', 'orgnization']

indicator_csv2indicator_context_entity_wildcard_csv(\
	entity_files,\
	entities,\
	input_csv = input_csv,\
	output_csv = output_csv)
'''
def indicator_csv2indicator_context_entity_wildcard_csv(\
	entity_files,\
	entities,\
	input_csv = None,\
	input_df = None,\
	output_csv = None,\
	entity_nearby_merge = None,\
	mathc_entity_by_word = None,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if input_csv is not None:
		customSchema = StructType([\
			StructField("text_entity", StringType(), True)])
		input_df = sqlContext.read.format("csv")\
			.option("header", "false")\
			.schema(customSchema)\
			.load(input_csv)\
			.withColumn('text_entity',\
			udf(lambda input: indicator_preprocess(input,\
			ignore_space_at_start_and_end = \
			False),\
			StringType())\
			('text_entity'))
	input_df.cache()
	outut_df = text_context_json2text_context_entity_wildcard_json(\
		entity_files = entity_files,\
		entities = entities,\
		input_df = input_df,\
		entity_nearby_merge = entity_nearby_merge,\
		mathc_entity_by_word = mathc_entity_by_word,\
		sqlContext = sqlContext)
	outut_df = outut_df.withColumnRenamed('text_entity', 'indicator')\
		.select('indicator')
	outut_df.cache()
	if output_csv is not None:
		os.system(u"""
			hadoop fs -rm -r temp
			rm -r temp
			""")
		outut_df.write.format('csv')\
			.option("header", "false")\
			.save('temp')
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_csv)
		os.system(u"hadoop fs -rm -r "+output_csv)
		os.system(u"hadoop fs -cp -f temp "+output_csv)
	return outut_df

'''
convert a text_entity to df, where each text_entity has only one
single entity, while the other entites are neither replaced
by wildcard of as the original text

usage: 

rm input.json
vi input.json
i{"text_entity":" _start_ i am [jim] and you are [smith] _end_ "}
{"text_entity":" _start_ this is a test _end_ "}

from sms_utility_spark import *
sqlContext = sqlContext_local

input_df = sqlContext.read.json('input.json')
text_entity2text_single_entity(input_df,\
	target_entity_context_wildcard = 'name')\
	.show(100, False)

text_entity2text_single_entity(input_df,\
	target_entity_type = 'trigger',\
	replace_target_entity_by_wildcard = True)\
	.show(100, False)
'''
def text_entity2text_single_entity(input_df,\
	target_entity_type = 'entity',\
	target_entity_context_wildcard = None,\
	replace_target_entity_by_wildcard = False,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if target_entity_context_wildcard is not None:
		udf_text_entity2entity_context_list = \
		lambda input: text_entity2entity_context_list(\
		input,\
		entity_type = target_entity_context_wildcard,\
		context_entity_replacy_by_wildcard = True)
	else:
		udf_text_entity2entity_context_list = \
		text_entity2entity_context_list
	output_df = input_df.withColumn('text_entity',\
		udf(udf_text_entity2entity_context_list, \
		ArrayType(StringType()))\
		('text_entity'))\
		.withColumn('text_entity',\
		explode('text_entity'))\
		.withColumn(target_entity_type, \
		udf(text_entity2entity, StringType())\
		('text_entity'))
	if replace_target_entity_by_wildcard:
		output_df = output_df.withColumn('text_entity', \
			udf(lambda input: text_entity2text_entity_wildcard(\
			input, entity_wildcard = target_entity_type), \
			StringType())('text_entity'))
	return output_df

'''
extract triggers from text and 
generate candidate text_trigger texts
only the texts with one or more triggers will be kept

usage:

rm input.json
vi input.json
i{"text":"Today's meeting has been cancled. I will see you tomorrow."}
{"text":"He visit me today. He will visit Ahmed tomorrow."}
{"text":"this is a test"}
{"text":"it is good"}

rm triggers.csv
vi triggers.csv
imeeting
see
visit
go

from sms_utility_spark import *

text_json2text_trigger(input_json = 'input.json',\
	output_json = 'output.json',\
	trigger_file = 'triggers.csv',\
	trigger_type = 'meet')
'''
def text_json2text_trigger(trigger_file,\
	input_json = None,\
	input_df = None,\
	output_json = None,\
	mathc_entity_by_word = False,\
	trigger_type = 'trigger',\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if input_json is not None:
		print('loading data from '+input_json)
		input_df = sqlContext.read.json(input_json)
	print('extracting the triggers by matching to '\
		+trigger_file)
	text_trigger_df = text_df2text_entity_df_by_entity_match(\
		input_df,\
		entity_file = trigger_file,\
		entity_type = trigger_type,\
		sqlContext  = sqlContext)
	text_trigger_df.cache()
	print('generating record for each trigger textracted')
	text_trigger_df = text_entity2text_single_entity(\
		text_trigger_df,\
		target_entity_type = trigger_type,\
		replace_target_entity_by_wildcard = True,\
		sqlContext = sqlContext)
	text_trigger_df.cache()
	text_trigger_df.registerTempTable('text_trigger_df')
	output_df = sqlContext.sql(u"""
		SELECT *, 
		text_entity AS text_trigger
		FROM text_trigger_df
		""")
	print('saving results to '+output_json)
	os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
	output_df.write.json('temp')
	os.system(u"""
		hadoop fs -get temp ./
		cat temp/* > """+output_json)
	os.system(u"hadoop fs -rm -r "+output_json)
	os.system(u"hadoop fs -cp -f temp "+output_json)
	print('results saved to '+output_json)

'''
match a text to multi indicators for 
multi-class classifiation labeling

usage:

rm input.json
vi input.json
i{"text":"my wife is coming"}
{"text":"my husband is here"}
{"text":"this is a test"}
{"text":"Hi my son is here","sender":1}
{"text":"dear Mrs Wang, your child here","sender":2}
{"text":"a test","sender":3}

rm indicator1.csv
vi indicator1.csv
imy wife

rm indicator2.csv
vi indicator2.csv
imy husband

from sms_utility_spark import *

def positive_indicator_func1(input):
	try:
		return re.sub(' my son ', ' [my son] ', input)
	except:
		return input

def positive_indicator_func2(input):
	try:
		return re.sub(' your child ', ' [your child] ', input)
	except:
		return input

psoitive_indicators_files = ['indicator1.csv',\
	'indicator2.csv', None, None]

psoitive_indicators_funcs = [\
	None, None, 
	positive_indicator_func1,\
	positive_indicator_func2]

text_json2text_indicators_json(\
	input_json = 'input.json',\
	output_json_file = 'output.json',\
	psoitive_indicators_files = \
	psoitive_indicators_files,\
	psoitive_indicators_funcs = \
	psoitive_indicators_funcs)

usage:

from sms_utility_spark import *

text_json2text_indicators_json(input_json ='input.json',\
	output_json_file = 'output.json',\
	psoitive_indicators_funcs = [\
	None, None, 
	positive_indicator_func1,\
	positive_indicator_func2])
'''
def text_json2text_indicators_json(\
	input_json = None,\
	input_df = None,\
	output_json_file = None,\
	psoitive_indicators_files = None,\
	psoitive_indicators_funcs = None,\
	mathc_entity_by_word = False,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	'''
	loading data
	'''
	if input_json is not None:
		print('loading input texts from '+input_json)
		input_df = sqlContext.read.json(input_json)
	if 'text_entity' not in input_df.columns:
		input_df = input_df.withColumn('text_entity',\
			udf(text_preprocess, StringType())\
			('text'))
	'''
	match by indicators
	'''
	if psoitive_indicators_files is not None:
		'''
		build class database
		'''
		print('building indicator database for all classes')
		sqlContext.sql(u"""
			SELECT NULL AS entity, NULL AS label
			""").registerTempTable('indicators_class')
		for class_idx1, context_indicator_file in \
			zip(range(len(psoitive_indicators_files)),\
			psoitive_indicators_files):
			class_idx = class_idx1+1
			if context_indicator_file is not None:
				print('loading the indicators from '+context_indicator_file\
					+' as the '+str(class_idx)+'-th class indicator')
				df_indicator = load_entities(context_indicator_file,\
					return_format = 'df',\
					sqlContext = sqlContext)
				df_indicator = df_indicator.withColumn('label', lit(class_idx))
				df_indicator.registerTempTable('indicators_class_new')
				sqlContext.sql(u"""
					SELECT *
					FROM indicators_class_new
					UNION ALL
					SELECT *
					FROM indicators_class
					""").registerTempTable('indicators_class')
		sqlContext.sql(u"""
			SELECT DISTINCT entity, label
			FROM indicators_class
			WHERE entity IS NOT NULL 
			AND label IS NOT NULL
			""").registerTempTable('indicators_class')
		print('saving the indicator-class label database')
		os.system(u"""
			hadoop fs -rm -r indicators_class.json
			rm -r indicators_class.json
			""")
		sqlContext.sql(u"""
			SELECT DISTINCT entity
			FROM indicators_class
			""").write.json('indicators_class.json')
		'''
		match multi-class indicators
		'''
		print('matching indicctors to texts')
		input_indicator_df = text_json2text_entity_json(\
			input_df = input_df,\
			entity_file = 'indicators_class.json',\
			mathc_entity_by_word = mathc_entity_by_word,\
			entity_type = 'indicator',\
			entity_surrounded_by_brackets = False,\
			ignoare_entity = False,\
			sqlContext  = sqlContext)
		input_indicator_df.cache()
		print('matching indicators to class labels')
		input_indicator_df = input_indicator_df.withColumn('indicator', \
			explode('indicator'))\
			.withColumn('indicator', \
			udf(lambda input: ' '+input+' ' if input is not None \
			else None, StringType())\
			('indicator'))
		input_indicator_df.cache()
		input_indicator_df.registerTempTable('input_indicator_df')
		output_df_indicator = sqlContext.sql(u"""
			SELECT DISTINCT 
			input_indicator_df.text_entity,
			input_indicator_df.indicator,
			indicators_class.label
			FROM input_indicator_df
			JOIN indicators_class
			ON indicators_class.entity 
			= input_indicator_df.indicator
			""")
		output_df_indicator.cache()
		output_df_indicator.registerTempTable(\
			'text_entity_match_by_indicator')
	else:
		sqlContext.sql(u"""
			SELECT NULL AS text_entity, 
			NULL AS indicator,
			NULL AS label
			""").registerTempTable(\
			'text_entity_match_by_indicator')
	if psoitive_indicators_funcs is not None:
		input_df.registerTempTable('input_df')
		text_entity_df = sqlContext.sql(u"""
			SELECT DISTINCT text_entity
			FROM input_df
			WHERE text_entity IS NOT NULL
			""")
		sqlContext.sql(u"""
			SELECT NULL AS text_entity, 
			NULL AS indicator,
			NULL AS label
			""").registerTempTable(\
			'text_entity_match_by_func')
		for class_idx1, psoitive_indicators_func in \
			zip(range(len(psoitive_indicators_funcs)),\
			psoitive_indicators_funcs):
			if psoitive_indicators_func is not None:
				class_idx = class_idx1+1
				print('extracting the indicators by '\
					+str(psoitive_indicators_func)\
					+' as the '+str(class_idx)+'-th class indicator')
				text_indicator_current = text_json2text_entity_json(\
					input_df = text_entity_df,\
					entity_extract_fun = psoitive_indicators_func,\
					entity_type = 'indicator',\
					entity_surrounded_by_brackets = False,\
					sqlContext = sqlContext)\
					.withColumn('indicator', explode('indicator'))\
					.withColumn('label', lit(class_idx))
				text_indicator_current.cache()
				text_indicator_current.registerTempTable(\
					'text_indicator_current')
				sqlContext.sql(u"""
					SELECT text_entity, indicator, label
					FROM text_indicator_current
					UNION ALL 
					SELECT text_entity, indicator, label
					FROM text_entity_match_by_func
					""").registerTempTable(\
					'text_entity_match_by_func')
	else:
		sqlContext.sql(u"""
			SELECT NULL AS text_entity, 
			NULL AS indicator,
			NULL AS label
			""").registerTempTable(\
			'text_entity_match_by_func')
	sqlContext.sql(u"""
		SELECT * 
		FROM text_entity_match_by_indicator
		UNION ALL 
		SELECT * 
		FROM text_entity_match_by_func
		""").registerTempTable('text_entity_indicator_match')
	sqlContext.sql(u"""
		SELECT DISTINCT * 
		FROM text_entity_indicator_match
		WHERE text_entity IS NOT NULL
		AND indicator IS NOT NULL
		AND label IS NOT NULL
		""").withColumn('indicator', udf(\
		lambda input: input.strip(), StringType())\
		('indicator'))\
		.registerTempTable(\
		'text_entity_indicator_all')
	input_df.registerTempTable('input_df')
	output_df = sqlContext.sql(u"""
		SELECT input_df.*, 
		text_entity_indicator_all.indicator,
		CASE 
			WHEN text_entity_indicator_all.label
			IS NOT NULL
			THEN text_entity_indicator_all.label
			ELSE 0
		END AS label
		FROM input_df
		LEFT JOIN text_entity_indicator_all
		ON text_entity_indicator_all.text_entity = 
		input_df.text_entity
		""")
	if output_json_file is not None:
		os.system(u"""
			hadoop fs -rm -r temp
			rm -r temp
			""")
		output_df.write.json('temp')
		print('saving the results to '+output_json_file)
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_json_file)
		os.system('hadoop fs -rm -r '+output_json_file)
		os.system('hadoop fs -cp -f temp '+output_json_file)
	else:
		return output_df

'''
matching the context of entities to label the entities
in text_entity by matching to context indicator
or using a context matching function

usgae:

1. matching to indicator csv

rm input.json
vi input.json
i{"text_entity":" _start_ this is [jim] i am here _end_ "}
{"text_entity":" _start_ dear [zhou] how are you regards [wang] _end_ "}

rm indicator1.csv
vi indicator1.csv
ithis is [jim] i

rm indicator2.csv
vi indicator2.csv
i dear [zhou] how 

from sms_utility_spark import * 

context_indicator_files = ['indicator1.csv',\
	'indicator2.csv']

text_entity2text_entity_context_indicator(\
	input_json = 'input.json',\
	output_json = 'output.json',
	context_indicator_files = ['indicator1.csv',\
	'indicator2.csv'],\
	target_entity_context_wildcard = 'name',\
	sqlContext = None)

2. macth entities in a text_entity by a function

usage:

rm input.json
vi input.json
i{"text_entity":" _start_ my name is [jim] and you are [sayed] _end_ "}

from sms_utility_spark import *

def context_indicator_func(input):
	try:
		input = re.sub('\[[^\[\]]+\]', '_entity_', input)
		return re.sub(' my name is _entity_ and ', \
		' [my name is _entity_ and] ',\
		input)
	except: 
		return input

text_entity2text_entity_context_indicator(\
	input_json = 'input.json',\
	output_json = 'output.json',\
	context_indicator_funcs = [context_indicator_func])
'''
def text_entity2text_entity_context_indicator(\
	input_json,\
	output_json = None,
	context_indicator_files = None,\
	context_indicator_funcs = None,\
	mathc_entity_by_word = False,\
	target_entity_type = 'entity',\
	target_entity_context_wildcard = None,\
	replace_target_entity_by_wildcard = False,\
	ignoare_entity = True,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	'''
	explode text_entity to text_single_entity
	'''
	print('loading the input text_entity from '+input_json)	
	input_df = sqlContext.read.json(input_json)
	print('loaded '+str(input_df.count())+' sms from '+input_json)
	print('exploding the text_entity to text_single_entity')
	output_df = text_entity2text_single_entity(input_df,\
		target_entity_type = 'entity',\
		replace_target_entity_by_wildcard = True,\
		target_entity_context_wildcard = \
		target_entity_context_wildcard,\
		sqlContext = sqlContext)
	output_df.cache()
	print('detected '+str(output_df.count())+' entities')
	'''
	match to entity context indicator
	'''
	print('matching to entity context indicators')
	output_df = text_json2text_indicators_json(\
		input_df = output_df,\
		psoitive_indicators_files = \
		context_indicator_files,\
		psoitive_indicators_funcs = \
		context_indicator_funcs,\
		sqlContext = sqlContext)
	output_df.cache()
	if replace_target_entity_by_wildcard is False:
		print('recovering target entities to text_entity')
		output_df = output_df.withColumn('text_entity',\
			udf(lambda input, entities: \
			text_wildcard_entity_recovery(input, \
			entities, \
			'entity',\
			with_bracket = True))('text_entity', 'entity'))
	output_df.cache()
	if output_json is not None:		
		print('saving results to '+output_json)
		output_file_temp = 'temp'+str(random.randint(0, 10000000000))\
			.zfill(10)
		output_df.write.json(output_file_temp)
		os.system(u"hadoop fs -get "+output_file_temp+u" ./")
		os.system(u"cat "+output_file_temp+u"/*> "+output_json)
		os.system('hadoop fs -rm -r '+output_json)
		os.system('hadoop fs -cp -f '+output_file_temp+' '+output_json)
		print('results saved to '+output_json)
		os.system(u"hadoop fs -rm -r "+output_file_temp)
	else:
		return output_df

'''
extract data/time entities from texts

usage: 

rm input.json
vi input.json
i{"text":"Good morning \n\nThis is Walid We talked last week about residence in hungary. \n\nI am  travelling to Budapest  Friday 16 Dec 10:00 AM 12/21/2018. \nCan we meet to discuss the availabil options. @"}

rm time_indicator.csv
vi time_indicator.csv
i_weekday_ 16 _month_ 10:00 AM
12/21/2018
morning
tomorrow

from sms_utility_spark import *

text_json2text_datetime_json(input_json = 'input.json',\
	output_json = 'output.json',\
	week_day_csv = 'week_day.csv',\
	month_csv = 'month.csv',\
	data_time_indicator_csv = 'time_indicator.csv')
'''
def text_json2text_datetime_json(input_json = None,\
	input_df = None,\
	output_json = None,\
	week_day_csv = 'week_day.csv',\
	month_csv = 'month.csv',\
	data_time_indicator_csv = 'date_time_indicator.csv',\
	data_time_indicator_match_by_word = False,\
	data_time_indicator_funct = None,\
	sub_entity_type_repalce_by_wildcard = False,\
	entity_type_repalce_by_wildcard = False,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	if input_json is not None:
		print('loading data from '+input_json)
		input_df = sqlContext.read.json(input_json)
	#extract other number	
	if 'number' not in input_df.columns:
		print('extracting other number')
		output_df = text_df2text_entity_df_by_func(\
			input_df,\
			extract_number,\
			entity_type = 'number',
			extract_entity_from_original_text = True,\
			entity_type_repalce_by_wildcard = True,\
			sqlContext = sqlContext)
	else:
		output_df = input_df
	#extract weekday
	print('extracting the weekdays by matching to '\
		+week_day_csv)
	output_df = text_df2text_entity_df_by_entity_match(\
		output_df,\
		entity_file = week_day_csv,\
		entity_type = 'weekday',\
		entity_type_repalce_by_wildcard = True,\
		sqlContext  = sqlContext)
	#extract month
	print('extracting the months by matching to '\
		+month_csv)
	output_df = text_df2text_entity_df_by_entity_match(\
		output_df,\
		entity_file = month_csv,\
		entity_type = 'month',\
		entity_type_repalce_by_wildcard = True,\
		sqlContext  = sqlContext)
	#match to date time indicator
	print('extracing time by matching to')
	output_df = text_df2text_entity_df_by_entity_match(\
		output_df,\
		entity_file = data_time_indicator_csv,\
		entity_type = 'datetime',\
		mathc_entity_by_word =\
		data_time_indicator_match_by_word, \
		ignoare_entity = False,\
		nearby_entity_merge = True,\
		sqlContext  = sqlContext)
	#recover time
	if sub_entity_type_repalce_by_wildcard is False:
		print('recovering the time entities from number/weekday/month')
		if 'number' in output_df.columns:
			output_df = output_df.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'number'))('text_entity', 'number'))
		if 'weekday' in output_df.columns:
			output_df = output_df.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'weekday'))('text_entity', 'weekday'))
		if 'month' in output_df.columns:
			output_df = output_df.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'month'))('text_entity', 'month'))
		output_df = output_df.withColumn('datetime', \
			udf(text_entity2entities, ArrayType(StringType()))\
			('text_entity'))
	if entity_type_repalce_by_wildcard is True:
		output_df = output_df.withColumn('text_entity',\
			udf(lambda input: text_entity2text_entity_wildcard(\
			input, 'datetime'), \
			StringType())('text_entity'))
	if output_json is not None:
		print('saving results to '+output_json)
		os.system(u"""
			hadoop fs -rm -r temp
			rm -r temp
			""")
		output_df.write.json('temp')
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_json)
		os.system('hadoop fs -rm -r '+output_json)
		os.system('hadoop fs -cp -f temp '+output_json)
	else:
		return output_df

'''
convert a preprocessed text to a list of word indeces for 
dl training and prediction

usage:

rm input.json
vi input.json
i{"text":"a test","text_preprocessed":" _start_ a test _end_ "}
{"text":"dear Mrs Wang, Sayed here","text_preprocessed":" _start_ dear mrs _name_ _puntuation_ _name_ here _end_ ","indicator":" dear mrs _name_ _puntuation_ ","label":2}
{"text":"I am Halima's husband, howre are you","text_preprocessed":" _start_ i am _name_ _puntuation_ s husband _puntuation_ how are you _end_ ","indicator":" i am _name_ _puntuation_ s husband ","label":1}

from sms_utility_spark import *

prepare_multiclass_dl_input('input.json',\
	'output.json')

rm input.json
vi input.json
i{"text":"I am Halima's husband, howre are you"}
{"text":"dear Mrs Wang, Sayed here"}
{"text":"a test"}

prepare_multiclass_dl_input('input.json',\
	'output.json')
'''
def prepare_multiclass_dl_input(input_json_file,\
	output_json_file = None,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	print('loading text data from '+input_json_file)
	input_df = sqlContext.read.json(input_json_file)
	if 'text_entity' not in input_df.columns:
		print('convering the text to text_entity')
		input_df = input_df.withColumn('text_entity',\
			udf(lambda input: text_preprocess(input), \
			StringType())('text'))
	'''
	if 'label' in input_df.columns:
		print('labels detected')
		input_df = input_df.withColumn('label',\
			udf(lambda input: 0 if input is None else input,\
			IntegerType())('label'))
	else:
		print('labels not detected')
	'''		
	print('convering the text_entity to word indeces')
	output_df = input_df.withColumn('words',\
		udf(lambda input: process_text2words(input, \
		ignoare_entity = False), \
		ArrayType(StringType()))('text_entity'))\
		.withColumn('word_idx',\
		udf(word_list2word_idx, ArrayType(IntegerType()))\
		('words'))\
		.drop('words')
	output_df.cache()
	if output_json_file is not None:		
		print('saving the results to '+output_json_file)	
		os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
		output_df.write.json('temp')
		os.system(u"""
			hadoop fs -get temp ./
			cat temp/* > """+output_json_file)
		os.system('hadoop fs -rm -r '+output_json_file)
		os.system('hadoop fs -cp -f temp '+output_json_file)
	else:
		return output_df

'''
prepare_entity_dl_input

usage: 

rm input.json
vi input.json
i{"text":"this is a test","text_entity":" _start_ this is a test _end_ "}
{"text":"how are you, regards, jim smith","text_entity":" _start_ how are you _puntuation_ regards _puntuation_ [jim smith] _end_ ","entity":["jim smith"]}
{"text":"dear Jane, my name is jim","text_entity":" _start_ dear [jane] _puntuation_ my name is [jim] _end_ ","entity":["jane","jim"]}
{"text":"good morning, sayed here from Abu Dhabi","text_entity":" _start_ good morning _puntuation_ [sayed] here from [abu] dhabi _end_ ","entity":["sayed","abu"]}

from sms_utility_spark import * 

prepare_entity_dl_input('input.json',\
	output_file = 'output.json')

usage:

rm input.json
vi input.json
i{"text_entity":" _start_ this is [jim] how are you _end_ ","indicator":" this is _entity_ ","label":1}
{"text_entity":" _start_ it is [jim] _end_ ","label":0}

from sms_utility_spark import * 

prepare_entity_dl_input('input.json',\
	output_file = 'output.json')
'''
def prepare_entity_dl_input(input_file,\
	output_file = None,\
	negative_number = None,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	print('loading input data from '+input_file)
	input_df = sqlContext.read.json(input_file)
	print('loaed '+str(input_df.count())+' records from '+input_file)
	if 'label' in input_df.columns:
		print('prepare the input for dl entity model training')
		output_df = input_df
		if negative_number is not None:
			output_df.registerTempTable('output_df')
			output_df = sqlContext.sql(u"""
				SELECT * FROM output_df
				WHERE label != 0
				UNION ALL 
				SELECT * FROM output_df
				WHERE label = 0
				LIMIT """+str(negative_number))
			output_df.cache()
	else:
		print('prepare the input for dl entity model prediction')
		output_df = text_entity2text_single_entity(input_df,\
			target_entity_type = 'entity',\
			sqlContext = sqlContext)
	output_df.cache()
	output_df.registerTempTable('output_df')
	output_df = sqlContext.sql(u"""
		SELECT *
		FROM output_df
		WHERE text_entity IS NOT NULL
		AND entity IS NOT NULL
		""").withColumn('context_word_idx',\
		udf(lambda input: \
		preprocessed_text_entity2context_idx(input),\
		MapType(StringType(), ArrayType(IntegerType()))\
		)('text_entity'))
	output_df_temp = 'temp'+str(random.randint(0, 10000000000))\
		.zfill(10)
	output_df.write.json(output_df_temp)
	sqlContext.read.json(output_df_temp)\
		.registerTempTable('temp')
	output_df = sqlContext.sql(u"""
			SELECT *,
			context_word_idx.left_word_idx,
			context_word_idx.entity_word_idx,
			context_word_idx.right_word_idx
			FROM temp
			WHERE text_entity IS NOT NULL  
			AND entity IS NOT NULL
			""").drop('context_word_idx')
	if output_file is not None:
		print('saving results to '+output_file)
		output_file_temp = 'temp'+str(random.randint(0, 10000000000))\
			.zfill(10)
		output_df.write.json(output_file_temp)
		os.system(u"hadoop fs -get "+output_file_temp+u" ./")
		os.system(u"cat "+output_file_temp+u"/*> "+output_file)
		os.system('hadoop fs -rm -r '+output_file)
		os.system('hadoop fs -cp -f '+output_file_temp+' '+output_file)
		print('results saved to '+output_file)
		os.system(u"hadoop fs -rm -r "+output_file_temp)
	os.system(u"hadoop fs -rm -r "+output_df_temp)
	return output_df

######################sms_utility_spark.py######################	
