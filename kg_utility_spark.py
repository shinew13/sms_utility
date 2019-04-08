#####################kg_utility_spark.py#####################
import os
import random
from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

try:
	sc = SparkContext("local")
	sqlContext_local = SparkSession.builder.getOrCreate()
except:
	pass

'''
building a enity profile attribut from knowledge graph json file

usage: 

knowledge_graph_json2entity_profile_json(\
	input_json = "/raid/jim/knowledge_graph_fb.json",\
	output_json = "/raid/jim/upload_location_contain.json",\
	subject_name = 'location',\
	object_name = 'contained_location',\
	relation = '/location/location/contains')
'''
def knowledge_graph_json2entity_profile_json(\
	input_json,\
	output_json,\
	subject_name,\
	object_name,\
	relation = None,\
	sqlContext = None):
	if sqlContext is None:
		sqlContext = sqlContext_local
	sqlContext.read\
		.json(input_json)\
		.registerTempTable("knowledge_graph_fb")
	output_df_temp = 'temp'+str(random.randint(0, 10000000000))\
		.zfill(10)
	if relation is not None:
		output_df = sqlContext.sql(u"""
			SELECT subject AS """+subject_name+u""",
			object AS  """+object_name+u"""
			FROM knowledge_graph_fb
			WHERE relation = '"""+relation+u"""'
			""")
	else:
		output_df = sqlContext.sql(u"""
			SELECT subject AS """+subject_name+u""",
			object AS  """+object_name+u"""
			FROM knowledge_graph_fb
			""")
	output_df = output_df.groupby(subject_name)\
		.agg(\
		collect_list(object_name).alias(object_name)
		).write.json(output_df_temp)
	os.system('cat '+output_df_temp+'/* > '+output_json)
	os.system('rm -r '+output_df_temp)
#####################kg_utility_spark.py#####################
