#########sms_utility_conll.py#########
import os
import re

'''
from sms_utility_conll import *

text_entity2conll(' _start_ this is a _name_ _end_ ')

target_entity = 'name'
input = u" _start_ this is [jim yan wang] how are you [yan] _end_ "
print text_entity2conll(input,\
	target_entity = target_entity)
'''
def text_entity2conll(input,\
	target_entity = None):	
	try:
		words = input.strip().split(' ')
		if target_entity is None:			
			entity_tag_list = ['O']*len(words)
			return '\n'.join([w+' '+e for w, e \
				in zip(words, entity_tag_list)\
				if len(w.strip())>0])
		else:
			output = []
			next_status = 'O'
			for word in words:
				if len(word.strip())>0:
					current_status = next_status
					if bool(re.search(r'\]$', word)):
						current_status = 'I-'+target_entity
					if bool(re.search(r'^\[', word)):
						current_status = 'B-'+target_entity
						next_status = 'I-'+target_entity
					if bool(re.search(r'\]$', word)):
						next_status = 'O'
					output.append(re.sub(r'[\[\]]', '', word).strip()\
					+' '+current_status)
			return '\n'.join(output)
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


'''
three cases

1. both left and right context

2. only left context

3. only right context
'''

def conll2context_indicator_conll(input, \
	context_indicator_type, \
	target_entity):
	input = u'\n\n'+input.strip()+u'\n\n'
	try:
		re_context_left_and_right = \
			r'\n'\
			+r'[^\n ]{1,} B\-'+context_indicator_type+r'\n'\
			+r'([^\n ]{1,} I\-'+context_indicator_type+r'\n)*'\
			+r'[^\n ]{1,} B\-'+target_entity+r'\n'\
			+r'([^\n ]{1,} I\-'+target_entity+r'\n)*'\
			+r'([^\n ]{1,} I\-'+context_indicator_type+r'\n)+'
		return re.search(re_context_left_and_right, input)\
			.group().strip()
	except:
		pass
	try:
		re_context_left_and_right = \
			r'\n'\
			+r'[^\n ]{1,} B\-'+target_entity+r'\n'\
			+r'([^\n ]{1,} I\-'+target_entity+r'\n)*'\
			+r'([^\n ]{1,} I\-'+context_indicator_type+r'\n)+'
		return re.search(re_context_left_and_right, input)\
			.group().strip()
	except:
		pass
	try:
		re_context_left_and_right = \
			r'\n'\
			+r'[^\n ]{1,} B\-'+context_indicator_type+r'\n'\
			+r'([^\n ]{1,} I\-'+context_indicator_type+r'\n)*'\
			+r'[^\n ]{1,} B\-'+target_entity+r'\n'\
			+r'([^\n ]{1,} I\-'+target_entity+r'\n)*'
		return re.search(re_context_left_and_right, input)\
			.group().strip()
	except:
		pass
	return None

def context_indicator_conll2context_indicator(input, \
	context_indicator_type, \
	target_entity):
	try:
		input = u'\n'+input.strip()+u'\n'
		re_target_entity = r'\n'\
			+r'[^\n ]{1,} B\-'+target_entity+r'\n'\
			+r'([^\n ]{1,} I\-'+target_entity+r'\n)*'
		target_entity_conll = re.search(re_target_entity,\
			input).group()
		target_entity_text = re.sub(r' (B|I)\-'+target_entity+r'\n',\
			' ', target_entity_conll).strip()
		#####
		context_conll = re.split(target_entity_conll, input)
		left_context_conll = '\n'+context_conll[0].strip()+'\n'
		left_context_text = re.sub(r' (B|I)\-'+context_indicator_type+r'\n',\
			' ', left_context_conll).strip()
		#####
		right_context_conll = '\n'+context_conll[1].strip()+'\n'
		right_context_text = re.sub(r' (B|I)\-'+context_indicator_type+r'\n',\
			' ', right_context_conll).strip()
		########
		output = left_context_text + u' ['+target_entity_text+u'] '\
			+right_context_text
		return output.strip()
	except:
		return None

'''
convert a entity context indicator annotated conll file
to csv files of indicators

usage:

rm input.conll
vi input.conll
i
hi O
my B-sender_name_context_indicator
name I-sender_name_context_indicator
is I-sender_name_context_indicator
jim B-name
how I-sender_name_context_indicator
are O
you O

my B-sender_name_context_indicator
name I-sender_name_context_indicator
is I-sender_name_context_indicator
jim B-name
wang I-name
and I-sender_name_context_indicator

my B-sender_name_context_indicator
name I-sender_name_context_indicator
yan B-name

my B-sender_name_context_indicator
name I-sender_name_context_indicator
yan B-name
hi O

my B-sender_name_context_indicator
name I-sender_name_context_indicator
yan B-name
hi B-someother

hi B-somethoer
jim B-name
is I-sender_name_context_indicator
name I-sender_name_context_indicator
haha O

hi O
jim B-name
is I-sender_name_context_indicator
name I-sender_name_context_indicator
haha O

jim B-name
is I-sender_name_context_indicator
name I-sender_name_context_indicator
haha O

yan B-name
is I-sender_name_context_indicator
name I-sender_name_context_indicator


from sms_utility_conll import *

indicator_cvs = 'output.csv'
annotat_conll = 'input.conll'
context_indicator_type = 'sender_name_context_indicator'
target_entity = 'name'

conll_file2entity_context_indicator_csv(\
	'/Users/Jim/Downloads/ar_relation_receiver_is_senders_role_ar_recommend_anno.conll',\
	indicator_cvs = 'context_indicator.csv',\
	context_indicator_type = 'receiver_is_senders_role_context_indicator',\
	target_entity = 'role')
'''

def conll_file2entity_context_indicator_csv(\
	annotat_conll,\
	indicator_cvs,\
	context_indicator_type,\
	target_entity):
	output = []
	input = open(annotat_conll)\
		.read().decode('utf-8')
	for setence in input.strip().split('\n\n'):
		context_indicator_conll = conll2context_indicator_conll(\
			setence, \
			context_indicator_type,\
			target_entity)
		indicator  = context_indicator_conll2context_indicator(\
			context_indicator_conll, \
			context_indicator_type,\
			target_entity)
		if indicator is not None:
			output.append(indicator)
	if len(output)>0:
		output = list(set(output))
		output = '\n'.join(output)
		open(indicator_cvs, 'w+').write(output.encode('utf-8'))
	else:
		print('no indicator detected')
#########sms_utility_conll.py#########
