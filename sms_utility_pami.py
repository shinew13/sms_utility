#############sms_utility_pami.py#################
from sms_utility_re import *
from sms_utility_dl_model import *

'''
'''
def text_entity_list_categorization_rest_api(\
	input,
	indicator_func = None, 
	indicator_list = None,
	model = None,\
	num_max_context_len = num_max_context_len):
	output = []
	for text_entity in input:
		indicator = text_entity_categorization(text_entity,
			indicator_func = indicator_func,\
			indicator_list = indicator_list)
		if model is not None:
			prediction, score = text_entity_categorization_dl(\
				text_entity, model,\
				num_max_context_len = num_max_context_len)
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

#############sms_utility_pami.py#################
