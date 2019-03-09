#########sms_utility_conll.py#########
import os
import re

'''
text_entity2conll(' _start_ this is a _name_ _end_ ')
'''
def text_entity2conll(input):	
	try:
		words = input.strip().split(' ')
		entity_tag_list = ['O']*len(words)
		return '\n'.join([w+' '+e for w, e \
			in zip(words, entity_tag_list)\
			if len(w.strip())>0])
	except:
		return None

'''
extract a list of indicators from an annotated conll file
by a given indicator name

usage:

rm input.conll
vi input.conll
ihi O
I B-sender_employed_indicator
work I-sender_employed_indicator
now O

hi O
my B-sender_employed_indicator
work I-sender_employed_indicator
done O

from sms_nlp_conll_utility import *

extract_indicator_from_annot_conll(\
	'input.conll',\
	entity_type = 'sender_employed_indicator',\
	indicator_conll = 'indicators.conll',\
	indicator_cvs = 'indicators.cvs')

head indicators.conll
head indicators.cvs
'''
entity_conll2text = lambda input: \
	' '+(' '.join([w.split(' ')[0].lower() \
	for w in input.strip().split('\n')]))+' '

def extract_indicator_from_annot_conll(\
	annotat_conll,\
	entity_type,\
	indicator_conll = None,\
	indicator_cvs = None):
	temp = open(annotat_conll)\
		.read().decode('utf-8')
	content = ''
	for w in temp.strip().split('\n'):
		if 'B-'+entity_type in w:
			content += ('\n'+w+'\n')
		if 'I-'+entity_type in w:
			content += (w+'\n')
	content = list(set(content.strip().split('\n\n')))
	if len(content) > 0:
			if indicator_conll is not None:
				output = '\n\n'.join(content)+'\n\n'
				open(indicator_conll, 'w+')\
				.write(output.encode('utf-8'))
			if indicator_cvs is not None:
				output  = '\n'.join(entity_conll2text(entity)
				for entity in content)+'\n'
				open(indicator_cvs, 'w+')\
				.write(output.encode('utf-8'))
	else:
		print('detected no indicators')

'''
usage:

annotat_conll = '/data/sms_sender_male_180911_1.conll'
input_indicator_csv = '/data/sender_male_indicator.csv'
output_indicator_cvs = '/data/sender_male_indicator_180911.csv'
entity_type = 'sender_male_indicator'

merge_indicator_from_conll2indicator_csv(annotat_conll,\
	input_indicator_csv,\
	entity_type,\
	output_indicator_cvs)

wc -l /data/sender_male_indicator_180911.csv
wc -l /data/sender_male_indicator.csv
'''
def merge_indicator_from_conll2indicator_csv(\
	annotat_conll,\
	input_indicator_csv,\
	entity_type,\
	output_indicator_cvs = None):
	extract_indicator_from_annot_conll(\
		annotat_conll,\
		entity_type,\
		indicator_cvs = 'temp.cvs')
	content = open(input_indicator_csv).read().strip()+'\n'\
		+open('temp.cvs').read().strip()+'\n'
	if output_indicator_cvs == None:
		output_indicator_cvs = input_indicator_csv
	os.system('rm '+output_indicator_cvs)
	open(output_indicator_cvs, 'w+').write(content)

#########sms_utility_conll.py#########