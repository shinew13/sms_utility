##############sms_utility_rest_api.py##############
from sms_utility_re import * 
from sms_utility_spark import * 

'''
name
'''
entity_csv_update(\
	entity_file_input = 'name_combine.csv',
	entity_file_to_delete = 'names_to_delete.csv',
	output_file_csv = 'name_en_all.csv')

name_en_all = load_entities(\
	entity_file = 'name_en_all.csv',\
	return_format = 'list')

name_en_all = set(name_en_all)
name_max_word = sorted([len(w.strip().split(' ')) \
	for w in name_en_all], \
	reverse = True)[0]

'''
location
'''
entity_csv_update(\
	entity_file_input = 'location_combine.csv',
	entity_file_to_delete = 'location_to_delete.csv',
	output_file_csv = 'location_en_all.csv')

location_en_all = load_entities(\
	entity_file = 'location_en_all.csv',\
	return_format = 'list')

location_en_all = set(location_en_all)
location_max_word = sorted([len(w.strip().split(' ')) \
	for w in location_en_all], \
	reverse = True)[0]

'''
title
'''
entity_csv_update(\
	entity_file_input = 'title_combine.csv',
	entity_file_to_delete = 'title_to_delete_fun_all.csv',
	output_file_csv = 'title_fun_all.csv')

title_fun_all = load_entities(\
	entity_file = 'title_fun_all.csv',\
	return_format = 'list')

title_fun_all = set(title_fun_all)
title_max_word = sorted([len(w.strip().split(' ')) \
	for w in title_fun_all], \
	reverse = True)[0]

'''
role
'''
entity_csv_update(\
	entity_file_input = 'role_combine.csv',
	entity_file_to_delete = 'title_to_delete.csv',
	output_file_csv = 'role_all.csv')

role_all = load_entities(\
	entity_file = 'role_all.csv',\
	return_format = 'list')

role_all = set(role_all)
role_max_word = sorted([len(w.strip().split(' ')) \
	for w in role_all], \
	reverse = True)[0]

'''
orgnization
'''
orgnization_en_all = load_entities(\
	entity_file = 'orgnization_en_all.csv',\
	return_format = 'list')

orgnization_en_all = set(orgnization_en_all)
orgnization_max_word = sorted([len(w.strip().split(' ')) \
	for w in orgnization_en_all], \
	reverse = True)[0]

'''
currency
'''
entity_csv_update(\
	entity_file_input = 'currency.csv',
	entity_file_to_delete = 'currency_to_delete.csv',
	output_file_csv = 'currency_all.csv')
currency_all = load_entities(\
	entity_file = 'currency_all.csv',\
	return_format = 'list')
currency_all = set(currency_all)

'''
week_day
'''
week_day = load_entities(\
	entity_file = 'week_day.csv',\
	return_format = 'list')
week_day = set(week_day)

'''
month
'''
month = load_entities(\
	entity_file = 'month.csv',\
	return_format = 'list')
month = set(month)

'''
orgnization_type
'''
orgnization_type = load_entities(\
	entity_file = 'orgnization_type.csv',\
	return_format = 'list')
orgnization_type = set(orgnization_type)

'''
orgnization_type
'''
place_type = load_entities(\
	entity_file = 'place_type.csv',\
	return_format = 'list')
place_type = set(place_type)

'''
document_format
'''
document_format = load_entities(\
	entity_file = 'document_format.csv',\
	return_format = 'list')
document_format = set(document_format)

'''
document_type
'''
document_type = load_entities(\
	entity_file = 'document_type.csv',\
	return_format = 'list')
document_type = set(document_type)

max_word_indicator = numpy.max([
	name_max_word,
	title_max_word,
	location_max_word,
	orgnization_max_word,
	role_max_word])

'''
usage:

from pami_entity_matching import * 

input = u"will go to the sayed road, then to the school, feb 2015, See you next monday. it costs 100 cny. I work in Bank of Ajman.  This is mr. Jim Wang how are you sayed, i am in dubai uae now seeing my brother "
entity_matching(input)
'''
def entity_matching(input):
	try:
		text_entity = text_preprocess(input)
		text_entity_set = text_entity2text_entity_subset(\
			text_entity, \
			max_number_word = max_word_indicator)
		text_entity_set = set(text_entity_set)
		###
		output = {}
		numbers = text_entity2entities(extract_number(input))
		output['number'] = numbers if numbers is not None else []
		emails = text_entity2entities(extract_email(input))
		output['email'] = emails if emails is not None else []
		output['name'] = [w.strip() for w in list(name_en_all & text_entity_set)]
		output['location'] = [w.strip() for w in list(location_en_all & text_entity_set)]
		output['orgnization'] = [w.strip() for w in list(orgnization_en_all & text_entity_set)]
		###
		output['title'] = [w.strip() for w in list(title_fun_all & text_entity_set)]
		output['role'] = [w.strip() for w in list(role_all & text_entity_set)]
		###
		output['currency'] = [w.strip() for w in list(currency_all & text_entity_set)]
		output['weekday'] = [w.strip() for w in list(week_day & text_entity_set)]
		output['month'] = [w.strip() for w in list(month & text_entity_set)]
		output['placetype'] = [w.strip() for w in list(place_type & text_entity_set)]
		output['orgnizationtype'] = [w.strip() for w in list(orgnization_type & text_entity_set)]
		output['documenttype'] = [w.strip() for w in list(document_type & text_entity_set)]
		output['documentformat'] = [w.strip() for w in list(document_format & text_entity_set)]
		return output		
	except:
		return None

'''
usage:

input = u"i will see you on monday march 3th 2019, this month morning is also ok"
entities = {'month':['march'],\
	'weekday':['monday'],\
	'number':['3', '2019']}
text2text_comb_entity(input, \
	entities,\
	sub_entities = ['number', 'month', 'weekday'],\
	comb_entity_indicator = date_time_indicator)

input = u"this is dr wang and my sister miss yan will come my email is wang@xx.com"
entities = {'number': [], 'email': ['wang@xx.com'], 'name': ['wang', 'yan'], 'location': [], 'orgnization': [], 'title': ['dr', 'sister'], 'role': ['sister'], 'currency': [], 'weekday': [], 'month': [], 'placetype': [], 'orgnizationtype': [], 'documenttype': [], 'documentformat': []}
text2text_comb_entity(input, \
	entities,\
	sub_entities = ['name', 'title'],\
	comb_entity_indicator = person_indicator)
'''
def text2text_comb_entity(input, \
	entities,\
	sub_entities,\
	comb_entity_indicator):
	try:
		text_entity = text_preprocess(input)
		ordered_entities = {}
		'''
		matching the sub_entities
		'''
		for sub_entity in sub_entities:
			if sub_entity in ['number', 'email']:
				ordered_entities[sub_entity] = entities[sub_entity]
			else:
				text_entity = marge_entity2preprocessed_text(\
					text_entity, \
					entities[sub_entity])
				ordered_entities[sub_entity] = text_entity2entities(\
					text_entity)
				text_entity = text_entity2text_entity_wildcard(\
					text_entity,\
					entity_wildcard = sub_entity)
		'''
		merge number, weekday and month to the text entity
		'''
		text_entity = marge_entity2preprocessed_text(\
			text_entity, comb_entity_indicator, \
			nearby_entity_merge = True)
		for sub_entity in sub_entities:
			###recover the sub-entities
			text_entity = text_entity_wildcard_subentity_recovery(text_entity, \
				ordered_entities[sub_entity], \
				sub_entity)
		return text_entity
	except:
		return None
##############sms_utility_rest_api.py##############
