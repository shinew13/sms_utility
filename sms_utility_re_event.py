#############sms_event_utility.py#############

from sms_re_utility import *
from sms_nlp_conll_utility import *
from sms_dl_utility import *

'''
usage: 

rm input.json
vi input.json
i{"text":"Good morning \n\nThis is Walid We talked last week about residence in hungary. \n\nI am  travelling to Budapest  Friday 16 Dec 10:00 AM 12/21/2018. \nCan we meet to discuss the availabil options. @"}

hadoop fs -rm -r input.json
hadoop fs -put input.json ./

text_json2text_datetime('input.json',\
	'output.json',\
	week_day_csv = '/data/jim/week_day.csv',\
	month_csv = '/data/jim/month.csv',\
	locations_en_csv = '/data/jim/locations_en.csv',\
	data_time_indicator_csv = '/data/jim/data_time_indicator.csv',\
	entity_type_repalce_by_wildcard = False)

head output.json
'''
def text_json2text_datetime(input_json,\
	output_json,\
	sqlContext,\
	week_day_csv = '/data/jim/week_day.csv',\
	month_csv = '/data/jim/month.csv',\
	locations_en_csv = '/data/jim/locations_en.csv',\
	names_en_csv = '/data/jim/names_en.csv',\
	data_time_indicator_csv = '/data/jim/data_time_indicator.csv',\
	entity_type_repalce_by_wildcard = True):
	#defin the time data and number extraction func
	#extract date
	extract_date_number = lambda input: \
		extract_entity_by_re(input, \
		r'\d{1,4}((\s+)?[\\\/\-\.](\s+)?\d{1,4}){1,2}')
	text_json2text_entity_json(input_json,
		'temp1.json',\
		sqlContext = sqlContext,\
		entity_type = 'date',\
		entity_extract_fun = extract_date_number,\
		entity_type_repalce_by_wildcard = True)
	#extract time
	extract_time_number = lambda input: \
		extract_entity_by_re(input, \
		r'\d{1,2}((\s+)?[\:\.](\s+)?\d{1,2}){1,2}')
	text_json2text_entity_json('temp1.json',
		'temp2.json',\
		sqlContext = sqlContext,\
		entity_type = 'time',\
		entity_extract_fun = extract_time_number,\
		entity_type_repalce_by_wildcard = True)
	#extract other number
	extract_number = lambda input: \
		extract_entity_by_re(input, \
		r'\d+((([\.\,]+)?\d+)+)?')
	text_json2text_entity_json('temp2.json',
		'temp3.json',\
		sqlContext = sqlContext,\
		entity_type = 'number',\
		entity_extract_fun = extract_number,\
		entity_type_repalce_by_wildcard = True)
	#preprocess the text
	os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
	sqlContext.read.json('temp3.json')\
		.withColumn('text_entity', \
		udf(text_preprocess, StringType())\
		('text_entity'))\
		.write.json('temp')
	os.system(u"""
		hadoop fs -get temp ./
		cat temp/* > temp4.json
		hadoop fs -rm -r temp4.json
		hadoop fs -cp -f temp temp4.json
		""")
	#extract weekday
	text_json2text_entity_json(\
		'temp4.json',
		'temp5.json',\
		sqlContext = sqlContext,\
		entity_csv_file = week_day_csv,\
		entity_type = 'weekday',\
		entity_type_repalce_by_wildcard = True)
	#extract month
	text_json2text_entity_json(\
		'temp5.json',
		'temp6.json',\
		sqlContext = sqlContext,\
		entity_csv_file = month_csv,\
		entity_type = 'month',\
		entity_type_repalce_by_wildcard = True)
	#extract locations
	text_json2text_entity_json(\
		'temp6.json',
		'temp7.json',\
		sqlContext = sqlContext,\
		entity_csv_file = locations_en_csv,\
		entity_type = 'location',\
		entity_type_repalce_by_wildcard = True)
	#extract names
	text_json2text_entity_json(\
		'temp7.json',
		'temp8.json',\
		sqlContext = sqlContext,\
		entity_csv_file = names_en_csv,\
		entity_type = 'name',\
		entity_type_repalce_by_wildcard = True)
	#match to date time indicator
	text_json2text_entity_json(\
		'temp8.json',
		'temp9.json',\
		sqlContext = sqlContext,\
		entity_csv_file = data_time_indicator_csv,\
		entity_type = 'datetime',\
		ignoare_entity = False,\
		nearby_entity_merge = True)
	#explode the entities
	os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
	sqlContext.read.json('temp9.json')\
		.withColumn('text_entity',\
		udf(text_entity2entity_context_list, ArrayType(StringType()))\
		('text_entity'))\
		.withColumn('text_entity',\
		explode('text_entity'))\
		.write.json('temp')
	os.system(u"""
		hadoop fs -get temp ./
		cat temp/* > temp10.json
		hadoop fs -rm -r temp10.json
		hadoop fs -cp -f temp temp10.json
		""")
	#recover time
	if entity_type_repalce_by_wildcard is False:
		output_df = sqlContext.read.json('temp10.json')\
			.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'time'))('text_entity', 'time'))\
			.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'date'))('text_entity', 'date'))\
			.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'number'))('text_entity', 'number'))\
			.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'weekday'))('text_entity', 'weekday'))\
			.withColumn('text_entity',\
			udf(lambda input, entities:\
			text_wildcard_entity_recovery(input, \
			entities, \
			'month'))('text_entity', 'month'))
	else:
		output_df = sqlContext.read.json('temp10.json')
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

#############sms_event_utility.py#############
