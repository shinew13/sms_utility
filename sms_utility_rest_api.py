##############sms_utility_rest_api.py##############
from flask import *
from flask_restplus import *

from sms_utility_re import *
from sms_utility_dl_model import *

text_entities_struct = {\
	'text': fields.String,\
	'number': fields.List(fields.String),\
	'email': fields.List(fields.String),\
	'url': fields.List(fields.String),\
	'name': fields.List(fields.String),\
	'location': fields.List(fields.String),\
	'orgnization': fields.List(fields.String),\
	'title': fields.List(fields.String),\
	'role': fields.List(fields.String),\
	'currency': fields.List(fields.String),\
	'weekday': fields.List(fields.String),\
	'month': fields.List(fields.String),\
	'placetype': fields.List(fields.String),\
	'orgnizationtype': fields.List(fields.String),
	'documenttype': fields.List(fields.String),\
	'documentformat': fields.List(fields.String),\
	'running_time':fields.Float,\
	'error':fields.String\
	}

text_entities_struct_comb = {\
	'time': fields.List(fields.String),\
	'person': fields.List(fields.String),\
	'place': fields.List(fields.String),\
	'document': fields.List(fields.String),\
	'money': fields.List(fields.String)\
	}

text_entities_struct_full = text_entities_struct.copy()
text_entities_struct_full.update(text_entities_struct_comb)

'''
'''
def text_entity_list_categorization_rest_api(\
	input,
	indicator_func = None, 
	indicator_list = None,
	model = None):
	output = []
	for text_entity in input:
		indicator = text_entity_categorization(text_entity,
			indicator_func = indicator_func,\
			indicator_list = indicator_list)
		if model is not None:
			prediction, score = text_entity_categorization_dl(\
				text_entity, model)
		if model is not None:
			if indicator is not None or prediction > 0:
				output.append({\
					'entity': text_entity2entity(text_entity),\
					'indicator': indicator,\
					'score':score})
		else:
			if indicator is not None:
				output.append({\
					'entity': text_entity2entity(text_entity),\
					'indicator': indicator})
	return output

##############sms_utility_rest_api.py##############
