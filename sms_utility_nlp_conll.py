################sms_utility_nlp_conll.py####################
'''
pip install polyglot
polyglot download embeddings2.ar ner2.ar pos2.ar

!polyglot download LANG:en

polyglot download embeddings2.en ner2.en
'''

import os
import re
import sys
import argparse
import numpy as np
from hashlib import md5

from sms_utility_re import *

try:
	import pandas as pd
except:
	print('failed to import pandas')

try:
	from rippletagger.tagger import *
	tagger_en = Tagger(language="en")
	tagger_ar = Tagger(language="ar")
except:
	print('failed to import rippletagger')

try:
	import gender_guesser.detector as gender
	d = gender.Detector(case_sensitive=False)
except:
	print('failed to load gender_guesser')

try:
	from genderizer.genderizer import Genderizer
except:
	print('failed to load gender_guesser')

try:
	#!polyglot download LANG:ar
	#!polyglot download LANG:en
	from polyglot.text import *
	print('polyglot model loaded')
except:
	print('failed to load polyglot')

try:
	#python -m spacy download en
	import spacy
	nlp = spacy.load('en')
	print('spacy model loaded')
except:
	print('failed to load spacy')

try:
	import langid
	print('langid model loaded')
except:
	print('failed to load langid')


#re_filter = u'(\!|\"|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~|\t|\n|\s|\u0005|\u0000|\u0003|\u0000|\u0002|\u0001)+'

re_english_filter = u'[^\w]+'
re_arabic_filter = u'[^0-9\u0600-\u06FF\u0750-\u077F]+'

re_en_ar_filter = u'[^\u0020-\u007e\u0600-\u06ff]+'

re_tile = '(mr|mrs|dr|prof|miss|doctor|doc|uncle)'
re_none_name = '^(still|interested|with|sick|calling|how|cas|okay|due|save|sky|five|sib|tell|ming|ing|sing|cash|file|hat|take|lang|save|are|his|lucky|dot|way|one|babe|just|baby|the|sender|see|salik|here|adib|doctor|boss|dib|user|may|sad|free|happy|fine|prince|pls|plz|u|hope|sory|u|please|try|sorry|credit|love|lot|thank|guy|best|can|bcz|wit|will|min|rgds|ask|not|god|mr|sir|brother|bro|habibi|habib|dad|papa|pa|father|husband|boyfriend|son|boy|guy|man|men|buddy|male|uncle|prince|mrs|ms|miss|sister|sis|madam|mam|maam|habibty|ma\'am|aunty|mum|wife|girlfriend|mother|woman|women|female|princess|hello|hi|hey|hai|dear|salam|asalam|asalamoalekum|goodmorning|goodafternoon|assalamoalaikom|day|morning|afternoon|evening|night|birthday|alaikom|alikoum|good|happy|gud|alsalam|you)$'

'''
convert a text of english to a list of words

usage:

from sms_nlp_conll_utility import *

input = u"My name is Jim. ... How are you?????"
text2words(input)

text2words(input, package = 'spacy')
text2words(input, package = 'polyglot')

text2words(input, package = 'rippletagger')

print text2words(u"\u0647\u0630\u0627 \u0647\u0648 \u062c\u064a\u0645", \
	language_code = 'ar')
'''
def text2words(input, \
	language_code = 'ar',\
	package = 're'):
	if package == 're' and language_code == 'en':
		try:
			return re.sub(re_english_filter, ' ', input)\
			.strip().split(' ')
		except:
			return None
	if package == 're' and language_code == 'ar':
		try:
			return re.sub(re_arabic_filter, ' ', input)\
			.strip().split(' ')
		except:
			return None
	if package == 'polyglot':
		try:
			doc = Text(re.sub(u'[\u0000-\u0006]+', ' ', input), \
				hint_language_code = language_code)
			return [re.sub('\s+', '', w.string)\
				for w in doc.words]
		except:
			pass
	if package == 'spacy' and language_code == 'en':
		try:
			doc = nlp(input)
			return [w.text for w in doc]
		except:
			return None
	if package == 'rippletagger' and language_code == 'en':
		try:
			doc = tagger_en.tag(input)
			return [w[0] for w in doc]
		except:
			return None
	if package == 'rippletagger' and language_code == 'ar':
		try:
			doc = tagger_ar.tag(input)
			return [w[0] for w in doc]
		except:
			return None
	return None

'''
prepare dl input for entity classifcation from text
the text should be text_entity permit and only has one entity
surrended by []

input = ' good morning [dr] _name_ how are you'
text2words(input)
text_entity2context_idx(input)

{'left_word_idx': [74539L, 74092L], 'name': [74532L], 'right_word_idx': [28704L, 69903L, 198907L, 78722L, 29865L]}
'''
def text_entity2context_idx(input, language_code = 'en',\
	package = 're'):
	try:
		left_context = input.split('[')[0].strip()
		right_context = input.split(']')[-1].strip()
		name = re.search('\[.*\]', input).group()
		return {'left_word_idx': text2word_idx(left_context, \
			language_code = language_code,\
			package = package),\
			'right_word_idx': text2word_idx(right_context,\
			language_code = language_code,\
			package = package),\
			'entity_word_idx': text2word_idx(name,\
			language_code = language_code,\
			package = package)}
	except:
		return None

'''
for spark usage:

print text_entity2context_idx4spark('this is [jim] how are you')
'''
def text2word_idx4spark(input, language_code = 'en'):
	try:
		input = re.sub('[0-9]+', '0', input)
		if language_code == 'en':
			input = re.sub(re_english_filter, ' ', \
				input).strip().split(' ')
		if language_code == 'ar':
			input = re.sub(re_arabic_filter, ' ', \
				input).strip().split(' ')
		return [(int(md5(w.lower().encode('utf-16')).hexdigest(), 16)% \
			(num_word_max - 1) + 1) for w in input]
	except:
		return None

def text_entity2context_idx4spark(input):
	try:
		left_context = input.split('[')[0].strip()
		right_context = input.split(']')[-1].strip()
		name = re.search('\[.*\]', input).group()
		return {'left_word_idx': text2word_idx4spark(left_context),\
			'right_word_idx': text2word_idx4spark(right_context),\
			'entity_word_idx': text2word_idx4spark(name)}
	except:
		return None

'''
conver a trxt to conll

usage:

input = u"""
Hi Jim, This is Yan. How\u0005\u0000are you?
"""

print text2conll(input, language_code = 'en')

print text2conll(input, language_code = 'en' ,\
	package = 'spacy')

print text2conll(\
	u"\u0635\u0628\u0627\u062d \u0627\u0644\u062e\u064a\u0631 \u0633\u064a\u062f \u0642\u0627\u0626\u0644\u0627\u002e \u0647\u0630\u0627 \u0647\u0648 \u062c\u064a\u0645", \
	language_code = 'ar' ,\
	package = 're')

Hi O
Jim O
, O
This O
is O
Yan O
. O
How O
are O
you O
? O
'''
def text2conll(input, \
	language_code = 'en',\
	package = 're'):	
	try:
		words = text2words(input, \
			language_code = language_code,\
			package = package)
		entity_tag_list = ['O']*len(words)
		return '\n'.join([w+' '+e for w, e \
			in zip(words, entity_tag_list)\
			if len(w.strip())>0])
	except:
		return None

'''
conver the conll format of a sentence to 
a list of word index

usage:
input = u"""
Good O
morning O
, O
Noel B-name
Smith I-name
. O
This O
is O
Mr O
"""
print conll2words(input)

[u'Good', u'morning', u',', u'Noel', u'Smith', u'.', u'This', u'is', u'Mr']
'''
def conll2words(input):
	try:
		input = input.strip().split('\n')
		words = [w.split(' ')[0] for w in input]
		return words
	except:
		return None


'''
input = u"\u0005\u0000\u0003\u0000\u0002\u0001this is jim, how are you?"

conll = text2conll(input, package  = 're')

print conll2word_idx(conll)

words = conll2words(conll)

word_list2idx(words)
'''
def conll2word_idx(input):
	try:
		words = conll2words(input)
		return word_list2word_idx(words)
	except:
		return None

'''
detect if a word is a name, and return the gender of the name

usage:

print name_match('Raj')
'''
def name_match(input):
	#remove the last non-alphabet
	try:
		input = re.search('^([^\w]+)?[a-zA-Z]{3,}([^\w]+)?$',\
			input).group()
		input = re.sub('(^[^\w]+)|([^\w]+$)', '', input)
	except:
		return None
	#check if it is a none-name word
	if bool(re.search(re_none_name, \
		input.lower())):
		return None
	#check if it is a title
	if bool(re.search(re_tile, \
		input.lower())):
		return None
	input = input.title()
	try:
		output = d.get_gender(input)
		if output in [u'male', u'mostly_male']:
			return 'male'
		if output in [u'female', u'mostly_female']:
			return 'female'
		if output in [u'andy']:
			return 'unknown_gender'
	except:
		pass
	try:
		output = Genderizer.detect(firstName = input)
		if output in [u'male']:
			return 'male'
		if output in [u'female']:
			return 'female'
	except:
		pass
	return None

'''
extract names from a text

usage:

from sms_nlp_conll_ultility import *

input = "Sayed, this is jim wang, your sister John Smith, how are you liu"
input = "Hi Heidi, hope you good and family is good."
words, entity_idx  = extract_name(input)
for e in entity_idx:
	print ' '.join(words[e[0]:e[1]])

input = u"Hey Noel Smith. Congratulations on 1 with Ecocoast. Hope the shoulder has well and truly recovered!! Lach"
words, entity_idx  = extract_name(input, package = 'polyglot')
for e in entity_idx:
	print ' '.join(words[e[0]:e[1]])

words, entity_idx  = extract_name(input, package = 'spacy')
for e in entity_idx:
	print ' '.join(words[e[0]:e[1]])

Lach
Hey Noel Smith

ssh pegasus@10.1.129.12
source activate jimkeras
cd /home/pegasus/jim
python

from sms_nlp_conll_ultility import *

input = u"\u0000-\u0005\u0635\u0628\u0627\u062d \u0627\u0644\u062e\u064a\u0631 \u060c \u0647\u0630\u0627 \u0633\u0639\u064a\u062f\u002e \u0643\u064a\u0641 \u062d\u0627\u0644\u0643\u061f"
words, entity_idx  = extract_name(input, package = 'polyglot', language_code = 'ar')
for e in entity_idx:
	print ' '.join(words[e[0]:e[1]])

extract_name(u"My name is Jim",\
	package = 'spacy',\
	language_code = 'en')
'''
def extract_name(input, package = 're',\
	language_code = 'en'):
	input = re.sub(re_en_ar_filter, ' ', input)
	if package == 'polyglot':
		doc = Text(input, hint_language_code = language_code)
		words = [re.sub('\s+', '', w.string)\
			for w in doc.words]
		entity_idx = list(set([(ent.start, ent.end) \
			for ent in doc.entities\
			if ent.tag in ['I-PER']]))
		return words, entity_idx
	if package == 'spacy' and language_code == 'en':
		try:
			doc = nlp(input)
			words = [w.text for w in doc]
			entity_idx = [(e.start, e.end) for e in doc.ents\
				if e.label_ in [u'PERSON']]
			return words, entity_idx
		except:
			return None
	if package == 're' and language_code == 'en':
		try:
			input = re.sub('[^\w]+', ' ', input)
			input = re.sub('[0-9]+', '0', input)
			words1 = input.strip().split(' ')
			words =  [None]+words1+[None]
			name_gender = [None]+[name_match(word) for word in words1]+[None]
			starts = []
			ends = []
			for idx, gender, word in zip(range(len(name_gender)), \
				name_gender,\
				words):
				if gender is not None and name_gender[idx-1] is None:
					starts.append(idx-1)
				if gender is None and name_gender[idx-1] is not None:
					ends.append(idx-1)
			return words1, zip(starts, ends)
		except:
			return None
	return None

'''
extract orgnization entities from a text

usage:

input = u"My company is Bank of America"
extract_ornigzation(input)

([u'My', u'company', u'is', u'Bank', u'of', u'America'], [(3, 6)])
'''
def extract_ornigzation(input, package = 'spacy',\
	language_code = 'en',\
	return_format = 'word_indx'):
	input = re.sub(re_en_ar_filter, ' ', input)
	if package == 'spacy' and language_code == 'en':
		try:
			if return_format == 'word_indx':
				doc = nlp(input)
				words = [w.text for w in doc]
				entity_idx = [(e.start, e.end) for e in doc.ents\
					if e.label_ in [u'ORG', u'FAC']]
				if len(entity_idx) > 0:
					return words, entity_idx
			if return_format == 'text':
				doc = nlp(input)
				output = [ent.text for ent in doc.ents \
				if ent.label_ in [u'ORG', u'FAC']]
				if len(output) > 0:
					return output
		except:
			return None
	return None

'''
convert a text to a text with names within blackets

input = 'this is jim'
text2text_name(input)

input = u"\u0647\u0630\u0627 \u0645\u062d\u0645\u062f \u0633\u064a\u062f"
text2text_name(input, \
	language_code = 'ar',\
	package = 'polyglot')

input = "Sayed, hi this is Jim, how are you? mr wang"
text2text_name(input, \
	name_list = ['Jim', 'wang'])

text2text_name(u"My name is Jim",\
	package = 'spacy',\
	language_code = 'en') 
'''
def text2text_name(input, \
	language_code = 'en',\
	package = 're',\
	name_list = None):
	try:
		if name_list is not None:
			for name in name_list:
				name_context = re.search('(^|[^\w])'+name+'($|[^\w])',\
					input).group()
				name_context1 = name_context.split(name)[0] \
					+'['+name+']'\
					+name_context.split(name)[1]
				input = re.sub(name_context, name_context1, input)
			return input
	except:
		pass
	try:
		words, entity_idx = extract_name(input, \
			package = package,\
			language_code = language_code)
		for e in entity_idx:
				words[e[0]] = '['+words[e[0]]
				words[e[1]-1] = words[e[1]-1]+']'
		return ' '.join(words)
	except:
		pass
	return None

'''
conver a text to conll format with names

usage:

input = u"""
Good morning, Noel Smith. This is Mr Jim Wang. 
Hope the shoulder has well and truly recovered!! Lach
"""

print text2conll_name(input, 
	language_code = 'en', 
	package = 're')

Good O
morning O
, O
Noel B-name
Smith I-name
. O
This O
is O
Mr O
Jim B-name
Wang I-name
. O
Hope O
the O
shoulder O
has O
well O
and O
truly O
recovered O
! O
! O
Lach B-name


input = u"\u0000\u0005\u0635\u0628\u0627\u062d \u0627\u0644\u062e\u064a\u0631 \u060c \u0647\u0630\u0627 \u0633\u0639\u064a\u062f\u002e \u0643\u064a\u0641 \u062d\u0627\u0644\u0643\u061f"
print text2conll_name(input, 
	language_code = 'ar', 
	package = 'polyglot')

'''
def text2conll_name(input, 
	language_code = 'en', 
	package = 're'):	
	try:
		words, entity_idx = extract_name(input, \
			package = package,\
			language_code = language_code)
		if len(entity_idx) == 0:
			return None
		entity_tag_list = ['O']*len(words)
		for entity in entity_idx:
			start, end = entity[0], entity[1]
			entity_tag_list[start] = 'B-name'
			entity_tag_list[start+1:end] = ['I-name']*(end-start-1)
		return '\n'.join([w+' '+e for w, e \
			in zip(words, entity_tag_list)\
			if len(w.strip())>0])
	except:
		return None

'''
convert a conll entity to a text entity 

usage: 

input = u"""
I O
am O
Jim B-sender_name
Wang I-sender_name
and O
you O
are O
Smith B-name
OK O
Ruby B-sender_name
Wang I-sender_name
"""

print conll_entity2text_entity(input, entity_type = 'sender_name')
print conll_entity2text_entity(input, entity_type = 'address')
print conll_entity2text_entity(input)
'''

def conll_entity2text_entity(input, \
	entity_type = None):
	try:
		if entity_type is not None:
			if 'B-'+entity_type not in input:
				return None
			input1 = input.strip().split('\n')
			tags = [word.split(' ')[1] for word in input1]
			words = [word.split(' ')[0] for word in input1]
			for idx in range(len(words)):
				if bool(re.search('^B-'+entity_type, tags[idx])):
					words[idx] = '['+words[idx]
				if idx == len(words)-1:
					if bool(re.search('^I-'+entity_type, tags[idx])):
						words[idx] = words[idx]+']'
					if bool(re.search('^B-'+entity_type, tags[idx])):
						words[idx] = words[idx]+']'
				else:
					if bool(re.search('^I-'+entity_type, tags[idx]))\
						and not bool(re.search('^I-'+entity_type, tags[idx+1])):
						words[idx] = words[idx]+']'
					if bool(re.search('^B-'+entity_type, tags[idx]))\
						and not bool(re.search('^I-'+entity_type, tags[idx+1])):
						words[idx] = words[idx]+']'
			return ' '.join(words)
		else:
			if 'B-' not in input:
				return None
			input1 = input.strip().split('\n')
			tags = [word.split(' ')[1] for word in input1]
			words = [word.split(' ')[0] for word in input1]
			for idx in range(len(words)):
				if bool(re.search('^B-', tags[idx])):
					words[idx] = '['+words[idx]
				if idx == len(words)-1:
					if bool(re.search('^I-', tags[idx])):
						words[idx] = words[idx]+']'
					if bool(re.search('^B-', tags[idx])):
						words[idx] = words[idx]+']'
				else:
					if bool(re.search('^I-', tags[idx]))\
						and not bool(re.search('^I-', tags[idx+1])):
						words[idx] = words[idx]+']'
					if bool(re.search('^B-', tags[idx]))\
						and not bool(re.search('^I-', tags[idx+1])):
						words[idx] = words[idx]+']'
			return ' '.join(words)
	except:
		return None

'''
given a conll with entities
create a conll of mutiple sentences
each sentence contains only one entity

usage:

input = u"""
Good O
morning O
Smith B-name
, O
this O
is O
Jim B-sender_name
Wang I-sender_name
. O
"""

print conll_name2conll_name_list(input)

for e in conll_name2conll_name_list(input):
	print(e+'\n')

conll_name2conll_name_list("i O\n am O")
'''
def conll_name2conll_name_list(input):
	input = input.strip().split('\n')
	words = [w.split(' ')[0] for w in input]
	tags = [w.split(' ')[1] for w in input]
	starts = [idx for tag, idx in zip(tags, range(len(tags))) \
		if 'B-' in tag]
	if len(starts) == 0:
		return None
	entity_idx = []
	for start in starts:
		end = start+1
		for tag, idx in  zip(tags[start+1:], range(start+1, len(words))):
			if 'I-' in tag:
				end = idx+1
			else:
				break
		entity_idx.append((start, end))
	output_list = []
	for start, end in entity_idx:
		tag_entity = ['O']*len(tags)
		tag_entity[start:end] = tags[start:end]	
		conll = '\n'.join([w+' '+t \
			for w, t in  zip(words, tag_entity)])
		conll = conll.strip()
		output_list.append(conll)
	if len(output_list) > 0:
		return output_list
	return None

'''
extract the name from the conll of a single name context

usage:

input = u"""
My O
name O
is O
Jim B-name
Wang I-name
from O
China B-location
"""

print conll_single_name2name(input)

{'name': u'Jim Wang', 'name_type': u'name'}
'''
def conll_single_name2name(input,\
	entity_type = None):
	try:
		if entity_type == None:
			entity_type = re.search('B\-\w+\n', input).group()
			entity_type = re.sub('B\-', '', entity_type).strip()
		input = input.strip().split('\n')
		words = [w.split(' ')[0] for w in input]
		tags = [w.split(' ')[1] for w in input]
		start = np.where(np.array(tags) == 'B-'+entity_type)[0][0]
		end_idxs = np.where(np.array(tags) == 'I-'+entity_type)[0]
		end = start + 1 if len(end_idxs) == 0\
			else np.max(end_idxs)+1
		name = words[start:end]
		return {'name': ' '.join(name),\
			'name_type': entity_type}
	except:
		return None

'''
convert a conll of a single name and its context 
to the index of left, right contexts, and the name

usage:

input = u"""
Good O
morning O
Smith O
, O
this O
is O
Jim B-sender_name
. O
how O
are O
you O
. O
"""

print conll_single_name2context_idx(input)

{'entity_word_idx': [54106L], 'left_word_idx': [42357L, 108228L, 112244L, 150994L, 90949L, 89323L], 'right_word_idx': [64256L, 35450L, 130960L, 83482L, 64256L]}

'''
def conll_single_name2context_idx(input):
	try:
		entity_type = re.search('B\-\w+\n', input).group()
		entity_type = re.sub('B\-', '', entity_type).strip()
		input = input.strip().split('\n')
		words = [w.split(' ')[0] for w in input]
		tags = [w.split(' ')[1] for w in input]
		start = np.where(np.array(tags) == 'B-'+entity_type)[0][0]
		end_idxs = np.where(np.array(tags) == 'I-'+entity_type)[0]
		end = start + 1 if len(end_idxs) == 0 \
			else np.max(end_idxs)+1
		left_words = words[0:start]
		right_words = words[end:len(words)]
		name = words[start:end]
		return {'left_word_idx': word_list2word_idx(left_words),\
			'entity_word_idx': word_list2word_idx(name),\
			'right_word_idx': word_list2word_idx(right_words)}
	except:
		return None

'''
convert the annotation conll file to json
'''
def conll2json(conll_file, json_file):
	content = open(conll_file)\
		.read().strip()
	sentents = [sent.strip()\
		for sent \
		in content.split('\n\n')]
	df = pd.DataFrame.from_dict(\
		{'conll': sentents})
	df.to_json(json_file, \
		date_format = 'iso', orient = 'records', \
		lines = True)

'''
input_conll = 'employment_to_annot1.conll'
output_annotated_conll = 'employment_to_annot2.conll'
indicator_conll = 'indicators.conll'

annotate_conll_by_indicator_conll(\
	input_conll, \
	output_annotated_conll, \
	indicator_list)

cat employment_to_annot1.conll | grep sender_employed_indicator | wc -l 
cat employment_to_annot2.conll | grep sender_employed_indicator | wc -l 
'''
def annotate_conll_by_indicator_conll(\
	input_conll, \
	output_annotated_conll, \
	indicator_list):
	input = open(input_conll).read().decode('utf-8')
	input = '\n'+input.strip()+'\n'
	indicator_list = open(indicator_conll).read().decode('utf-8')
	indicator_list = indicator_list.strip().split('\n\n')
	for indicator in indicator_list:
		indicator = '\n'+indicator+'\n'
		indicator1 = re.sub(' (B|I)-'+entity_type+'\n',\
			' O\n', indicator)
		input = re.sub(indicator1,\
			indicator, input)
	open(output_annotated_conll, 'w+')\
		.write(input.encode('utf-8'))

'''
convert a text of indicator to a conll format
usage:

input = u"This is Jim's father"
entity_type = 'sender_name'
print indictor_text2conll(input, entity_type)
'''
def indictor_text2conll(input, entity_type):
	try:
		input = input.strip()
		input = re.sub(re_english_filter, ' ', input)
		words = input.split(' ')
		tags = ['I-'+entity_type]*len(words)
		tags[0] = 'B-'+entity_type
		return '\n'.join([word+' '+tag for word, tag in zip(words, tags)])
	except:
		return None

'''
convert a indcator text file to a conll file 
usage: 

input_indicator_file = '/data/sender_male_indicator.csv'
entity_type = 'sender_male_indicator'
output_conll_file = '/data/sender_male_indicator.conll'

indicator_text2conll_file(input_indicator_file,\
	output_conll_file,\
	entity_type)
'''
def indicator_text2conll_file(input_indicator_file,\
	output_conll_file,\
	entity_type):
	f = open(input_indicator_file)
	content = f.read()
	content = content.split('\n')
	content = '\n\n'.join([indictor_text2conll(line, entity_type) \
		for line in content\
		if line is not None])
	f1 = open(output_conll_file, 'w+')
	f1.write(content)
	f1.close()

'''
input = u"the entity is 2347*43678U]irt User name : Muthalib entity: maffu3538588 fevorate color: green"
extract_password_candidate(input)

input = u"this is a test"
extract_password_candidate(input)
'''
def extract_password_candidate(input):
	try:
		words_tags = tagger_en.tag(input)
		entitis = []
		words = []
		for w in words_tags:
			if w[1] in [u'NUM']:
				entitis.append(w[0])
				words.append(' _password_ ')
			else:
				words.append(w[0])
		if len(entitis) == 0:
			return None
		text_entity = text_preprocess(' '.join(words))
		text_entity = re.sub('_password_', '[_password_]', \
			text_entity)
		return {'text_entity':text_entity2entity_context_list(\
			text_entity), \
			'password':entitis}
	except:
		return None

'''
from sms_utility_nlp_conll import *

language_detect(u"This is an English test")

language_detect(u"Mahal q naka higa ndn aq.nagpapaantok ndn.")
'''
def language_detect(input):
	if input is None:
		return None
	try:
		return langid.classify(input)[0]
	except:
		return None
################sms_nlp_conll_ultility.py####################