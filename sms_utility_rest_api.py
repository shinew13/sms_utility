##############sms_utility_rest_api.py##############
from flask import *
from flask_restplus import *

text_entities_struct = {\
	'text': fields.String,\
	'number': fields.List(fields.String),\
	'email': fields.List(fields.String),\
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

text_entities_struct_full = \
	text_entities_struct.update(text_entities_struct_comb)
##############sms_utility_rest_api.py##############
