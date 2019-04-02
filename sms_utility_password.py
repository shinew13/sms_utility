from sms_utility_nlp_conll import *
from sms_utility_spark import *


'''
extract potential passwords from text

usage: 

rm input.json
vi input.json
i{"text":"the password is 32#4wed "}

from sms_utility_spark import *
from sms_utility_nlp_conll import *

detect_possible_passwords_from_json(\
	'input.json',\
	'output.json')
'''
def detect_possible_passwords_from_json(input_json,\
	output_json,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	print('load the text from ' + input_json)
	sqlContext.read.json(input_json)\
		.registerTempTable('input')
	sqlContext.sql(u"""
		SELECT *
		FROM input
		WHERE text IS NOT NULL
		""").withColumn('output',\
		udf(extract_password_candidate, \
		MapType(StringType(),ArrayType(StringType())))\
		('text'))\
		.registerTempTable('temp')
	print('saving results to '+output_json)
	os.system(u"""
		hadoop fs -rm -r temp
		rm -r temp
		""")
	sqlContext.sql(u"""
		SELECT temp.*, 
		output.text_entity,
		output.password
		FROM temp
		WHERE output IS NOT NULL
		""").drop('output')\
		.withColumn('text_entity',\
		explode('text_entity'))\
		.withColumn('password',\
		udf(lambda input, entities: \
		text_wildcard_entity_recovery(input, entities, 'password'),\
		StringType())\
		('text_entity', 'password'))\
		.withColumn('password', \
		udf(text_entity2entity, StringType())\
		('password'))\
		.write.json('temp')
	os.system(u"""
		hadoop fs -get temp ./
		cat temp/* > """+output_json)
	os.system(u"hadoop fs -rm -r "+output_json)
	os.system(u"hadoop fs -cp -f temp "+output_json)