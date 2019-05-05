################sms_utility_re.py################
'''
https://github.com/vi3k6i5/flashtext
https://medium.com/@Alibaba_Cloud/why-you-should-use-flashtext-instead-of-regex-for-data-analysis-960a0dc96c6a
'''
import re
from hashlib import md5
from collections import *
import numpy

try:
	import regex
except:
	pass

#https://en.wikipedia.org/wiki/List_of_Unicode_characters
#https://en.wikipedia.org/wiki/Arabic_script_in_Unicode
re_puntuation = r"(\!|\"|\#|\$|\%|\&|\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@)+"

re_arabic_number = u'[\+\-\$\%]*[\d\u0660-\u0669\u06F0-\u06F9]+(([\.\,\:\-\\\/\u066A-\u066C][\d\u0660-\u0669\u06F0-\u06F9]+)+)?[\+\-\$\%]*'
re_arabic_putuation = u'[\u060C-\u060F\u061F\u066D\u06DD\u06DE\u06E9\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@]+'
re_arabic_non_letter = u'[^\u0600-\u06FF\u0750-\u077f\w]+'
re_newline = u'([\n\r]\s*)'
regex_email = re.compile(("([A-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[A-z0-9!#$%&'*+\/=?^_`"
	"{|}~-]+)*(@)(?:[A-z0-9](?:[A-z0-9-]*[A-z0-9])?(\.|"
	"\sdot\s))+[A-z0-9](?:[A-z0-9-]*[A-z0-9])?)"))

#https://blog.csdn.net/chivalrousli/article/details/77412329
re_chinese_letter = u'[\u4E00-\u9FA5\u9FA6-\u9FEF]'
re_chinese_puntutation = u'[\u3000-\u303F\uFF00-\uFFEF]'

#https://arabic.desert-sky.net/g_pronouns_poss.html
re_end_my = u'(\u064a)'
re_end_our = u'(\u0646\u0627)'
#
re_end_your = u'(\u0643|\u0643\u0645\u0627|\u0643\u0648|\u0643\u0645)'
re_end_your_male = u'(\u0643\u064e|\u0643\u0645)'
re_end_your_female = u'(\u0643\u0650|\u0643\u0646)'
#
re_end_his = u'(\u0647)'
re_end_her = u'(\u0647\u0627)'
re_end_their = u'(\u0647\u0645\u0627|\u0647\u0645|\u0647\u0646)'

re_arabic_end_all = r'('+re_end_my\
	+ r'|' + re_end_our\
	+ r'|' + re_end_your\
	+ r'|' + re_end_your_male\
	+ r'|' + re_end_your_female\
	+ r'|' + re_end_his\
	+ r'|' + re_end_her\
	+ r'|' + re_end_their\
	+r')'

num_max_text_len = 50
num_max_context_len = 6
num_max_name_len = 3
num_word_max = 200000

'''
usage:

from sms_utility_re import *

text_preprocess('I live at abu Dhabi, and you? my numbrer is 24389 ok\n \n hahah \n\n it is ok \n\n ',\
ignore_linebreak = False)

text_preprocess('this is 823.894289')
text_preprocess('ok 378 439 384758 jktne')

text_preprocess(u"\u0623\u064a\u0646 \u0646\u0661\u0662\u0663 \u0627\u0644\u0645\u062f\u064a\u0631\u061f")

text_preprocess(u"\u0623\u0628\u064a \u0648\u0623\u0645\u0643 \u0642\u0627\u062f\u0645")

text_preprocess(u"\u0627\u0628\u064a")

text_preprocess(u"6438 eam999.gn@gex.com _number_ and _email_",
	ignore_email = False,
	ignore_number = False)

text_preprocess(u"this xg_gex@324.com is 888:888 a _number_ and _,_ is a _email_ ",\
	ignore_email = False)

text_preprocess(u" this is gxgn@gma.com this $123")
'''
def text_preprocess(input,\
	ignore_puntuation = False,\
	ignore_number = False,\
	ignore_linebreak = True,\
	ignore_email = False,\
	ignore_start_end_space_indicator = False,\
	scape_entity = False,\
	seperate_arabic_ending = False):
	try:
		input = input.strip()
		if ignore_email is False:
			input = re.sub(regex_email, ' _email_ ', input)
		if ignore_number is False:
			input = re.sub(re_arabic_number, ' _number_ ', input)
		if ignore_linebreak is False:
			input = re.sub(re_newline, ' _linebreak_ ', input)
		if ignore_puntuation is False:
			input = re.sub(re_arabic_putuation, ' _puntuation_ ', input)
		input = re.sub(re_arabic_non_letter, ' ', input)
		if ignore_start_end_space_indicator is True:
			input = ' '+ input.strip().lower() +' '
		else:
			input = ' _start_ '+ input.strip().lower() +' _end_ '
		'''
		seperate the arabic ending from the work, inserting a space between
		the word and the ending
		'''
		if seperate_arabic_ending is True:
			word_with_ending = [r' ' + word.group() 
				for word \
				in re.finditer(\
				r'[^ ]{2,}'+re_arabic_end_all+r' ', \
				input)]
			for word in word_with_ending:
				word_old = word
				ending = re.search(re_arabic_end_all+r' ', word).group()
				word_new = re.sub(re.escape(ending), r' '+ending, word_old)
				input = re.sub(re.escape(word_old), word_new, input)
		return input
	except:
		return None

'''
if scape_entity is False:				
else:
	for sub_text in re.split('_[a-z]{1,}_', input):
		sub_text1 = re.sub(re_arabic_putuation, \
			' _puntuation_ ', sub_text)
		input = re.sub(sub_text, sub_text1, input)
'''

'''
usage:

indicator_preprocess('Abu Dhabi')

indicator_preprocess(u"\u0623\u0628\u0648 \u0638\u0628\u064a")
indicator_preprocess(u"yal&ccedil;in")

indicator_preprocess(u"\u0632\u0648\u062c\u064a\u0647")

'''
def indicator_preprocess(indicator, \
	ignore_puntuation = False,\
	ignore_space_at_start_and_end = False,\
	seperate_arabic_ending = False):
	try:
		indicator = re.sub(r'^\"|\"$', '', indicator.strip())
		if len(indicator) == 0:
			return None
		indicator = re.sub('\[[^\[\]]*\]', ' _entity_ ', indicator)
		indicator = re.sub(re_arabic_number, ' _number_ ', indicator)
		if ignore_puntuation is False:
			indicator = re.sub(re_arabic_putuation, ' _puntuation_ ', indicator)		
		indicator = re.sub(re_arabic_non_letter, ' ', indicator)
		indicator = ' '+indicator.strip()+' '
		if seperate_arabic_ending is True:
			word_with_ending = [r' ' + word.group() 
				for word \
				in re.finditer(\
				r'[^ ]{2,}'+re_arabic_end_all+r' ', \
				indicator)]
			for word in word_with_ending:
				word_old = word
				ending = re.search(re_arabic_end_all+r' ', word).group()
				word_new = re.sub(re.escape(ending), r' '+ending, word_old)
				indicator = re.sub(re.escape(word_old), word_new, indicator)
		if ignore_space_at_start_and_end is True:
			indicator = indicator.strip()
		indicator = indicator.lower()
		return indicator
	except:
		return None

'''
convert a text_entity to a list of entity candidats for hasing search for
a larget set of entities

usage:
from sms_utility_re import *
input = ' _start_ this is jim and yan liang _end_ '
output = text_entity2text_entity_subset(input)
output = text_entity2text_entity_subset(input,\
	max_number_word = 100)

entities = ['jim', 'yan liang', 'abu _not_ abu dhabi']
entities_set = set(entities)
entiteis_not = [e for e in entities if '_not_' in e]
list(entities_set.intersection(set(output)))+entiteis_not
'''
def text_entity2text_entity_subset(input,\
	max_number_word = None):
	try:
		output = []
		num_word = len(input.strip().split(' '))
		if max_number_word is None:
			max_number_word = num_word
		else:
			max_number_word = numpy.minimum(num_word,max_number_word)
		for num_word1 in range(1,max_number_word+1):
			output += [e.group().strip() for e \
				in regex.finditer(r' ([^ ]+ ){'+str(num_word1)+'}', \
				input, overlapped=True)]
		return output
	except:
		return None

'''
usage:

text = ' _start_ i live at abu dhabi _puntuation_ and you _puntuation_ my numbrer is _number_ ok _end_ '
indicator = ' abu dhabi '
text_indicator_match(text, indicator)

indicator = ' eid _not_ eid mubarak '
text_indicator_match(' eid mubarak this is jim ', indicator)
text_indicator_match(' eid this is jim ', indicator)

text = ' _start_ good morning _puntuation_ my name is [jim] _puntuation_ how are you _end_ '
indicator = ' my name is [ahmode]'
text_indicator_match(text, \
	indicator_preprocess(indicator))

indicator = "this is mr _not_ this is mr _name_'s"
text = "' _start_ this is mr _name_ _puntuation_ s assistant _end_ '"
text_indicator_match(text_preprocess(text), \
	indicator_preprocess(indicator))


indicator = "ramadan _not_ ramadan mubarak"
text = "' _start_ this is mr ramadan _end_ '"
text_indicator_match(text_preprocess(text), \
	indicator_preprocess(indicator))

indicator = " mr _not_ mr _puntuation_ mrs _not_ mr _puntuation_ ms "
text = "dear mr/ms, how are you"
text_indicator_match(text_preprocess(text), \
	indicator_preprocess(indicator))
'''
def text_indicator_match(text, indicator):
	try:
		text = re.sub('\[[^\[\]]*\]', '_entity_', text)
		text = re.sub('\s+', ' ', text)
		if '_not_' not in indicator:
			return indicator in text
		else:
			indicators = indicator.split('_not_')
			positive_indiccator = indicators[0]
			if positive_indiccator in text:
				output  = True
			for idx in range(1, len(indicators)):
				if indicators[idx] in text:
					output = False
			return output
	except:
		return False

'''
usage:

input = ' _start_ this is [jim] and _name_ _number_ hi _puntuation_ _end_ '
process_text2words(input, \
	ignore_start_and_end = True,\
	irgore_number = True,\
	irgnore_puntuation = True,\
	ignoare_entity = True)
process_text2words(input, ignoare_entity = False)
'''
def process_text2words(input, \
	ignore_start_and_end = False,\
	irgore_number = False,\
	irgnore_puntuation = False,\
	ignoare_entity = False):
	try:
		input = re.sub('\s+', ' ', input).strip()
		if ignore_start_and_end is True:
			input = re.sub('(^_start_)|(_end_$)', '', input)
		if irgore_number is True:
			input = re.sub('\s+_number_\s+', ' ', input)
		if irgnore_puntuation is True:
			input = re.sub('\s+_puntuation_\s+', ' ', input)
		if ignoare_entity is True:
			input = re.sub('\s+_[a-z]+_\s+', ' ', input)
			input = re.sub('\s+\[[^\[\]]+\]\s+', ' ', input)
		input = re.sub('\s+', ' ', input)
		return input.strip().split(' ')
	except:
		return None

'''
convet a text a list of idx

usage:

input = u"Good morning, sir, how are you 123 67?"
print text2word_idx(input)
print text2word_idx('I have 30 40 books')

print text2word_idx(\
	u"\u0647\u0630\u0627 \u0647\u0648 \u062c\u064a\u0645", \
	language_code = 'ar')
'''
def text2word_idx(input,\
	max_word_num = 200000,\
	language_code = 'en',\
	package = 're',\
	ignore_digit = True):
	try:
		if ignore_digit:
			input = re.sub('[0-9]+', '0', input)
		words = text2words(input, \
			language_code = language_code,\
			package = package)
		words = [w for w in words if w not in ['']]
		return word_list2word_idx(words)
	except:
		return None

'''
usage:

preprocessed_text_entity2context_idx(\
	'_start_ sir [rashed] is not come _end_')

preprocessed_text_entity2context_idx(\
	'_start_ sir [jim wang] _end_')
'''
def preprocessed_text_entity2context_idx(input):
	try:
		left_context = input.split('[')[0].strip().split(' ')
		right_context = input.split(']')[-1].strip().split(' ')
		name = re.search('\[.*\]', input).group().strip().split(' ')
		return {'left_word_idx': word_list2word_idx(left_context),\
			'right_word_idx': word_list2word_idx(right_context),\
			'entity_word_idx': word_list2word_idx(name)}
	except:
		return None

'''
convet a list of words to a list of idx

usage:

from sms_nlp_conll_ultility import *

u'morning'.encode('utf-8')

u'morning'.encode('utf-8')

input = [u'Good', u'morning', u',', u'Noel', u'Smith', u'.', u'This', u'is', u'Mr']
print word_list2word_idx(input)

[317924L, 381322L, 314168L, 290642L, 368046L, 117879L, 341030L, 37208L, 250631L]


words = text2words(u"\u0647\u0630\u0627 \u0647\u0648 \u062c\u064a\u0645", \
	language_code = 'ar')
print word_list2idx(words)

print word_list2idx([u"\u0647\u0630\u0627", u"\u0647\u0648", u"\u062c\u064a\u0645"])
'''
hash_function = lambda w: \
	int(md5(w.encode('utf-16')).hexdigest(), 16)

def word_list2word_idx(input):
	try:
		return [(hash_function(w.lower()) \
		% (num_word_max - 1) + 1) \
		for w in input]
	except:
		return None

'''
convert a text entity to a list of entity_contexts

usage:

input = ' hw r u [dr] and your family dear [prof] this is a [dr] and your [student] ha ha '
text_entity2entity_context_list(input)

[' hw r u [dr] and your family dear prof this is a dr and your student ha ha ', ' hw r u dr and your family dear [prof] this is a dr and your student ha ha ', ' hw r u dr and your family dear prof this is a [dr] and your student ha ha ', ' hw r u dr and your family dear prof this is a dr and your [student] ha ha ']

input = " _start_ [sheikha] a gentle reminder of [sheikh] _puntuation_ s and your _meet_ with [ms shanahan] at _number_ am tomorow _number_ th _month_ in [al] mamoura _puntuation_ thank you _end_ "
text_entity2entity_context_list(input,\
	context_entity_replacy_by_wildcard = True,\
	entity_type = 'name')

[' hw r u [dr] and your family dear  this is a  and your  ha ha ', ' hw r u _name_ and your family dear [prof] this is a  and your  ha ha ', ' hw r u _name_ and your family dear _name_ this is a [dr] and your  ha ha ', ' hw r u _name_ and your family dear _name_ this is a _name_ and your [student] ha ha ']
'''
def text_entity2entity_context_list(input, \
	context_entity_replacy_by_wildcard = False,\
	entity_type = 'entity'):
	try:
		if '[' not in input:
			return None
		context_idx = zip([i for i in range(len(input)) \
			if input[i] == '['],
			[i for i in range(len(input)) \
			if input[i] == ']'])
		context = [(input[0:start], \
			input[start:end+1] ,\
			input[end+1:])
			for start, end in context_idx]
		if context_entity_replacy_by_wildcard is True:
			context = [re.sub('\[[^\[\]]+\]', '_'+entity_type+'_', e[0])\
				+e[1]\
				+re.sub('\[[^\[\]]+\]', '_'+entity_type+'_', e[2])\
				for e in context]
		else:
			context = [re.sub('(\[|\])', '', e[0])\
				+e[1]\
				+re.sub('(\[|\])', '', e[2])\
				for e in context]
		return context
	except:
		return None

'''
convert a csv file of indicators to a list of indicators

usage:

rm indicator.csv
vi indicator.csv
i this is a indicator

another one
"this is the last one, and you"
there are 100 apples

from sms_utility_re import *

print extract_indicator_list_from_csv(\
	'indicator.csv')
'''
def extract_indicator_list_from_csv(indicator_file,\
	put_space_before_and_after_entity = True):
	try:
		indicators = open(indicator_file)\
			.read().decode('utf-8').strip().split('\n')
		output = []
		for indicator in indicators:
			indicator1 = indicator_preprocess(indicator, \
				ignore_space_at_start_and_end \
				= not put_space_before_and_after_entity)
			if indicator1 is not None:
				output.append(indicator1)
		output = list(set(output))
		return output
	except:
		return None

'''
match a text against a list of indicators

input = u"""
your boss is here
"""
match_indicator(input, [' your boss ', ' chef it ', ' hi my dear dr '])

indicators = [' dear xxxxx ', ' morning my xxxxx ', ' hw r u xxxxx ', ' sssss xxxxx we ']
input = '[dr] we and your family. dear 00'
match_indicator(input, indicators)

match_indicator('you have missed 100 calls', [' missed 0 calls'])

input = u"abc 6879 \u0627\u0644\u062a\u062e\u0641\u064a\u0636\u0627\u062a \u0639\u0646\u062f \u0646\u0627\u062c\u0648\u0632 \u0633\u064a\u0643\u0631\u062a \u0648\u062a\u0634\u0645\u0644"
indicators = [u" \u0627\u0644\u062a\u062e\u0641\u064a\u0636\u0627\u062a \u0639\u0646\u062f ", u" \u0644\u062a \u062d\u062f\u064a\u062b\u0627 \u0644\u0644\u0623\u0645 "]
print match_indicator(input, indicators,\
	language_code = 'ar')

input = ' sssss xxxxx here how are you '
indicators = [' sssss xxxxx here ']
match_indicator(input, indicators)

input = 'dear sir how are you'
indicators = [' dear sir _not_ dear sir madam ', ' how ']
match_indicator(input, indicators)
'''
def match_indicator(input, \
	indicators,\
	max_indicator_to_match = 5000,\
	language_code = 'en',\
	return_original_entity = False):
	try:
		if language_code == 'en':
			input = input.lower().strip()
			if return_original_entity is True:
				entity = re.search('\[[^\[\]]*\]', input).group()
				entity = re.sub('[^\w]+', '', entity)
			else:
				input = re.sub('\[[^\[\]]*\]', '_entity_', input)
			input = re.sub('[^\w]+', ' ', input)
			input = re.sub('[0-9]+', '0', input)
			input = ' _start_ '+ input.strip() +' _end_ '
			for indicator in indicators[0:max_indicator_to_match]:
				if return_original_entity is True:
					indicator = re.sub('_entity_', entity, indicator)
				if indicator in input:
					return indicator.strip()
				if '_not_' in indicator:
					positive_indicator = ' '+indicator.split('_not_')[0].strip()+' '
					negative_indicator = ' '+indicator.split('_not_')[1].strip()+' '
					if positive_indicator in input\
						and negative_indicator not in input:
						return indicator.strip()
			return None
		if language_code == 'ar':
			input = input.lower().strip()
			input = re.sub('\[[^\[\]]*\]', 'xxxxx', input)
			input = re.sub(u'[^\w\u0600-\u06ff\u0750-\u077f]+', ' ', input)
			input = re.sub('[0-9]+', '0', input)
			input = ' _start_ '+ input.strip() +' _end_ '
			for indicator in indicators[0:max_indicator_to_match]:
				if indicator in input:
					return indicator.strip()
			return None
	except:
		return None

'''
merging a list of entities to a preprocessed text
replacing the entities in the text by [entity]

usage:

from sms_utility_re import * 

entitis = [' abu dhabi ', \
	' uae ',\
	' jim _not_ jim wang ', \
	' zhang ', \
	' zhang guohui ', \
	' xxx ']

marge_entity2preprocessed_text(\
	' i will go to abu dhabi and uae ',\
	entitis)

marge_entity2preprocessed_text(\
	' i will go to abu dhabi uae ',\
	entitis,\
	nearby_entity_merge = True)

marge_entity2preprocessed_text(\
	' this is zhang and zhang guohui  ',\
	entitis)

marge_entity2preprocessed_text(\
	' i am jim wang ',\
	entitis)

marge_entity2preprocessed_text(\
	' jim and wang ',\
	entitis)
'''
def marge_entity2preprocessed_text(text, \
	entitis, \
	nearby_entity_merge = False):
	try:
		#fiter and sor the entities
		entitis = [entity for entity in entitis \
			if entity.split('_not_')[0] in text]
		entitis.sort(key=len, reverse=True)
		#merge entities 
		for entity in entitis:
			#generate the positive and negative entities
			if '_not_' in entity:
				entity_list = entity.split('_not_')
				entity_positive = entity_list[0]
				entity_negatives = entity_list[1:]
			else:
				entity_positive = entity
				entity_negatives = []
			#search the texts which doen't have entities yet
			not_matched = [e.group() for e \
				in re.finditer('(^|\])[^\[\]]+(\[|$)', text)]
			#match the entites to the text
			for str_not_matched in not_matched:
				if entity_positive in str_not_matched \
					and len([negative for negative \
					in entity_negatives \
					if negative in str_not_matched]) == 0:
					str_not_matched1 = re.sub(entity_positive, \
					' ['+entity_positive.strip()+'] ', \
					str_not_matched)
					text = re.sub(re.escape(str_not_matched), \
					str_not_matched1, text)
			text = re.sub('\s+', ' ', text)
		if nearby_entity_merge is True:
			text = re.sub('\] \[', ' ', text)
		return text
	except:
		return text

'''
replace the entities in the context by entity wildcard 
while not touching the text in the balackets

usage:

input = ' _start_ i will go to dubai mall dubai and then leave dubai to give you [100 aed] how do you think _end_ '

entities = [' dubai ', ' dubai mall ']

entity_type = 'location'

text_context2text_context_entity_wildcard(input,\
	entities,\
	entity_type = entity_type,\
	nearby_entity_merge = False)

text_context2text_context_entity_wildcard(' this is a [text] ',\
	None)
'''
def text_context2text_context_entity_wildcard(input,\
	entities = None,\
	entity_type = 'entity',\
	nearby_entity_merge = True):
	try:
		entities.sort(key=len, reverse=True)
		for entity in entities:
			not_matcheds = [e.group() for e \
				in re.finditer('(^|\])[^\[\]]+(\[|$)', input)]
			for not_matched in not_matcheds:
				not_matched_wild = re.sub(entity, \
					' _'+entity_type+'_ ', not_matched)
				input = re.sub(re.escape(not_matched), \
					not_matched_wild, input)
		if nearby_entity_merge is True:
			input = re.sub('(_'+entity_type+'_ )+',\
				'_'+entity_type+'_ ', input)
		return input
	except:
		return input

'''
match a text to a list of entityies and return the replaced text
of the entities

usage:

from sms_re_utility import *

entities = [' representative ', ' painter ', ' barrister ', ' dr ', ' professor ', ' prof ']
input = "good morning, representative wang, how are you. this is your dr. i am a prof and my professor is good "
print match_entity(input, entities)

input = "dfasag fgaaad"
print match_entity(input, entities)


input = "Sayed Mohamod, hi this is Jim, Jan is not here.  how are you? mr wang 0000 9999"
match_entity(input, \
	entities = ['Jim', 'wang', 'Sayed', 'Mohamod', 'Jan'],\
	keep_original_text = True,\
	nearby_entity_merge = True)

match_entity(input, \
	entities = ['Jim', 'wang', 'Sayed', 'Mohamod', 'Jan'],\
	keep_original_text = True,\
	nearby_entity_merge = True,\
	entity_wildcard = 'name')

input = "V can I call? I spoke to axel"
entities = ["axel"]

input = u"Hi (Zeeshan). Are you alright to come tonight. My wife will meet you. I have been called to a late meeting and not sure if I can be there tonight but my wife's name is Lisa"
entities = ['Zeeshan', 'Lisa']
print match_entity(input, \
	entities = entities,\
	only_return_entity_included = True,\
	nearby_entity_merge = True,\
	entity_wildcard = 'name',\
	keep_original_text = True)
'''
def match_entity(input, entities,\
	max_entities_to_match = 1000,\
	keep_original_text = False,\
	entity_wildcard = None,\
	nearby_entity_merge = False,\
	only_return_entity_included = True,\
	match_by_word = False):
	try:
		if keep_original_text is True:
			input = re.sub('(\[|\])', '', input)
			for name in entities:
				name_context = re.search('(^|[^\w])'+name+'($|[^\w])',\
					input).group()
				name_context1 = name_context.split(name)[0] \
					+'['+name+']'\
					+name_context.split(name)[1]
				input = re.sub(re.escape(name_context), name_context1, input)
		else:
			input = input.lower().strip()
			input = re.sub('[^\w]+', ' ', input)
			input = re.sub('[0-9]+', '0', input)
			input = ' '+input.strip()+' '
			if match_by_word is True:
				words = input.split(' ')
				for word in words:
					if ' '+word+' ' in entities:
						input = re.sub(' '+word+' ', \
						' ['+word+'] ', \
						input)
			else:
				for entity in entities[0:max_entities_to_match]:
					if entity.lower() in input:
						input = re.sub(' '+entity.lower().strip()+' ', \
						' ['+entity.lower().strip()+'] ', \
						input)
		if '[' not in input and only_return_entity_included is True: 
			return None
		else:
			if nearby_entity_merge is True:
				input = re.sub('\]\s+\[', ' ', input)
			if entity_wildcard is not None:
				input = text_entity2text_entity_wildcard(\
					input,\
					entity_wildcard = entity_wildcard)	
			return input
	except:
		pass
	return None

'''
replace the entity with brackets by a _wildcard_

usage:

input = ' this is [dr] wang '
entity_wildcard = 'occupation'
text_entity2text_entity_wildcard(input,\
	entity_wildcard = 'occupation')


input = " _start_ [ _location_  _clinic_  _location_ ] confirms "
text_entity2text_entity_wildcard(input,\
	entity_wildcard = 'entity')
'''
def text_entity2text_entity_wildcard(input,\
	entity_wildcard = 'entity'):
	try:
		return re.sub('\[[^\[\]]+\]', \
			'_'+entity_wildcard+'_', \
			input)
	except:
		return None

'''
given a list of words and a list of names, outoput a 
text with all the names neighboring inside brackets

usage:

words = ["Hi","this","is","Jim","Wang","how","are","you","Mr","Sayed"]
names = ["wang","sayed","jim"]

print words_entity2text_entity(words, names,\
	entity_wildcard = 'name')

Hi this is [Jim Wang] how are you Mr [Sayed]
'''
def words_entity2text_entity(words, entities, \
	nearby_entity_merge = True,\
	entity_wildcard = None):
	try:
		words_name = ['['+word+']' \
		if word.lower() in entities else word \
		for word in words]
		text_name = (' '.join(words_name)).strip()
		if nearby_entity_merge:
			text_name = re.sub('\] \[', ' ', text_name)
		if entity_wildcard is not None:
			text_name = text_entity2text_entity_wildcard(\
				text_name,\
				entity_wildcard = entity_wildcard)
		return text_name
	except:
		return None

'''
input = ' good morning [dr] ahmad i m so sorry '
text_entity2entity(input)
'''
def text_entity2entity(input):
	try:
		return re.sub('( \[|\] )', '', \
		re.search(' \[.*\] ', input)\
		.group()).strip()
	except:
		return None

'''
extract entities from text-entity

usage:

input = u' i work for [abu dhabi] bank and [abu dhabi] finance before this is jim smith from [dubai] islamic bank how are you '
text_entity2entities(input)

'''
def text_entity2entities(input):
	try:
		output = [e.group() for e \
			in re.finditer('\[[^\[\]]+\]', input)]
		output=  [re.sub('(\[|\])', '', e).strip() for 
			e in output]
		if len(output) > 0:
			return output
		else:
			return None
	except:
		return None 

'''
input = ' i work for rak bank and _location_ finance before this is _name_ from [_location_ islamic bank] how are you '
entities = [u'abu dhabi', u'dubai']
entity_type = 'location'

text_wildcard_entity_recovery(input, \
	entities, \
	entity_type)

text_wildcard_entity_recovery(input, \
	entities, \
	entity_type,\
	only_recover_entities_in_bracket = True)


output:
u' i work for rak bank and abu dhabi finance before this is _name_ from [dubai islamic bank] how are you '
'''

def text_wildcard_entity_recovery(input, \
	entities, \
	entity_type,\
	with_bracket = False):
	try:
		if isinstance(entities, list) is False:
			entities = [entities]
		text = input.split('_'+entity_type+'_')
		if with_bracket is False:
			for idx in range(len(entities)):
				text[idx] = text[idx]+entities[idx]
		else:
			for idx in range(len(entities)):
				text[idx] = text[idx]+'['+entities[idx]+']'
		return ''.join(text)
	except:
		return input

'''
input = ' i work for [_location_ bank] and _location_ finance before this is _name_ from [_location_ islamic bank] how are you '
sub_entities = [u'rak', u'abu dhabi', u'dubai']
sub_entity_type = 'location'

text_entity_wildcard_subentity_recovery(input, \
	sub_entities, \
	sub_entity_type)
'''
def text_entity_wildcard_subentity_recovery(input, \
	sub_entities, \
	sub_entity_type):
	try:
		output = text_wildcard_entity_recovery(input, \
			entities = sub_entities, \
			entity_type = sub_entity_type)
		entities = text_entity2entities(output)
		input = text_entity2text_entity_wildcard(\
			input)
		return text_wildcard_entity_recovery(input, \
			entities, \
			entity_type = 'entity',\
			with_bracket = True)
	except:
		return input

'''
select the major element from an array

usage:

input = ['a', 'a', 'b', 'c']
array_major(input)
'''
def array_major(input):
    if input is None:
        return None
    if len(input) == 0:
        return None
    if len(list(set(input))) == 1:
        return input[0]
    try:
        data = Counter(input)
        return data.most_common(1)[0][0]
    except:
        return None

'''
return the entity from a list of entities with the largest score

usage: 

entities = ['Jim', 'China']
scores = [1.0, 0.5781889558]

max_entity_score(entities, scores)
'''

def max_entity_score(entities, scores):
    try:
        max_idx = np.argmax(scores)
        return {'entity': entities[max_idx],\
        'score': scores[max_idx]}
    except:
        return None

'''
input = u"456.5678.678 3274,678.567 w7485 10 1: 567.567"

re_pattern = r'\d+((([\.\,]+)?\d+)+)?'

extract_entity_by_re(input, re_pattern)

re_pattern = '(wang|wan)'

input = u" this is wang, and wan will come, but wangk is wrong"

extract_entity_by_re(input, re_pattern)

extract_entity_by_re(u" xx $1231 xxx", re_arabic_number)

extract_entity_by_re(u" xx gdgn@gds.com te ", regex_email)

'''
def extract_entity_by_re(input, \
	re_pattern,\
	replace_entity_by_wildcard = False,\
	return_none_if_not_matched = False):
	try:
		###remove the brakets
		input = re.sub('(\[|\])', ' ', input)
		input_original = input
	except:
		return input
	try:
		if replace_entity_by_wildcard is True:
			input = re.sub('\[[^\[\]]+\]', ' _entity_ ', input)
			input = re.sub('\s+', ' ', input)
		else:
			input = re.sub('(\[|\])', '', input)
		date_array = [e.group() \
			for e in re.finditer(\
			re_pattern,	input)]
		if len(date_array) == 0:
			if return_none_if_not_matched is True:
				return None
			else:
				return input_original
		date_array.sort(key=len, reverse=True)
		for entity in date_array:
			#check if this number has been matched as a part of an entity
			not_matched = [e.group() for e \
				in re.finditer('(^|\])[^\[\]]+(\[|$)', input)]
			for str_not_matched in not_matched:
				if entity in str_not_matched:
					str_not_matched1 = re.sub(re.escape(entity), \
					' ['+entity.strip()+'] ', str_not_matched)
					input = re.sub(re.escape(str_not_matched), \
					str_not_matched1, input)	
		input = re.sub('\s+', ' ', input)	
		return input
	except:
		return input_original

'''
extract number from text

usage:

from sms_utility_re import *

text_preprocess(extract_number('10-10 -100 12.12.13/45/78/44 12, 12.0'))

extract_date_number('10-10 -100 12.12.13/45/78/44 12, 12.0')

extract_time_number('10-10 -100 12.12.13/45/78/44 12, 12:0')

extract_number('xgn [gsg] igmd')

extract_number(' $843 ')
'''
def extract_number(input):
	return extract_entity_by_re(input, \
		re_arabic_number)

'''
extract emails from text and put the into blackets 

usage:

input =  '978:887 my email is jywang.ieee@gmail.com but [ my company ] email is jingya.wang@pegassu.ae.   '
print text2text_email(input)

input = u"4896 cgx Xdsg@453.com "
input = text2text_email(input)
input = text_entity2text_entity_wildcard(input, 'email')
input = extract_number(input)
input = text_entity2text_entity_wildcard(input, 'number')
input = text_preprocess(input)
print(input)


from sms_utility_re import *

extract_email(' gnsg [gdsg]  nsgdsg')
'''
def extract_email(input):
	return extract_entity_by_re(input, \
		regex_email)

def text2text_email(input):
	return extract_entity_by_re(input, \
		regex_email)

'''
def text2text_email(input):
	try:
		input = re.sub('(\[|\])', ' ', input)		
		emails = [email[0] \
			for email in re.findall(regex_email, input) \
			if not email[0].startswith('//')]
		for email in list(set(emails)):
			input = re.sub(email, ' ['+email+'] ', input) 
		return input
	except:
		return None
'''

'''
extract the first name from a name merged
usage: 

extract_first_name('Jim  Wang')

extract_first_name('Jim')
'''
def extract_first_name(input):
	try:
		input = re.sub('[^\w]+', ' ', input)
		return input.split(' ')[0].strip()
	except:
		return None

'''
rm date_time.csv
vi date_time.csv
i13/12/2016 at 16:20
13-DEC-2016 15:00
December 16th 2016 at 10:30
12-Jan-2017 at 18:00
13/12/2016 at 13:45:00 
Dec 13 2016 4:20PM
December 13th 2016 at 20:30
Tuesday, 13 Dec 2016 at 9:30am
15/12/2016 at 10:15:00
December 13th 2016 at 09:30
13th of December at 5:00pm
this week
next friday
last month
today
tomorrow

date_time_indicators = date_time_indicator_extract('date_time.csv')

for t in date_time_indicators:
	print t

'''

re_number = '[0-9]+'
re_month = '(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sept|sep|oct|nov|dec)'
re_weekday = '(sunday|sun|monday|mon|tuesday|tues|wednesday|wed|thursday|thurs|friday|fri|saturday|sat)'
re_next = '(next|last)'
re_day = '(today|tomorrow|yesterday|year|month|week|hour|minute|season|weekend|sec|seconds|second)'

def date_time_indicator_extract(date_csv):
	try:
		output = []
		for indicator in open(date_csv).readlines():
			indicator = indicator.strip().lower()
			indicator = re.escape(indicator).lower()
			indicator = re.sub(re_number, re_number, indicator)
			indicator = re.sub(re_month, re_month, indicator)
			indicator = re.sub(re_weekday, re_weekday, indicator)
			indicator = re.sub(re_day, re_day, indicator)
			indicator = re.sub(re_next, re_next, indicator)
			output.append(indicator)
		return list(set(output))
	except:
		return None

'''
input = "December 13th 2016 at 20:30 December 13th 2016 at 20:30 and 15/12/2016 at 10:15:00 but Dec 13 2016 4:20PM"
extract_date_time(input, date_time_indicators)

'[december 13th 2016 at 20:30] [december 13th 2016 at 20:30] and [15/12/2016 at 10:15]:00 but [dec 13 2016 4:20pm]'
'''
def extract_date_time(input, date_time_indicators):
	entities = []
	input = re.sub('(\[|\])', '', input.lower())
	for indicator in date_time_indicators:
		try:
			entity = re.search(indicator, input).group()
			input = re.sub(entity, '['+entity+']', input)
		except:
			pass
	return input

'''
'''
def replace_puntuation(input):
	try:
		return re.sub('(\s)*_puntuation_(\s)*', ' ', input).strip()
	except:
		return None

'''
the following is for the rest api of single message processing
'''

'''
giving the input text and the entity lists, output the 
processed text with the target entity 

usage:

input = u"this is jim wang"
entities = {'name':['jim','wang']}
target_entity = 'name'
target_entity_nearby_merge = True

text_entities2text_entity(input,\
	entities,\
	target_entity,\
	target_entity_nearby_merge = True)
'''
def text_entities2text_entity(input,\
	entities,\
	target_entity,\
	target_entity_nearby_merge = False):
	try:
		text_entity = text_preprocess(input)
		text_entity = marge_entity2preprocessed_text(\
			text_entity,\
			entitis = entities[target_entity],\
			nearby_entity_merge = \
			target_entity_nearby_merge)
		return text_entity
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

input = u"this is jim from dubai llc and i live in abu dhabi island "
entities = entity_matching(input)
text_entities2text_comb_entity(input, \
	entities,\
	sub_entities = ['location', 'placetype', \
	'orgnizationtype', 'name'],\
	comb_entity_indicator = place_indicator)

input = u" this is dr jim wang from pegasus"
entities = {'name': ['jim','wang'], 'title':['dr']}
person_indicator = ['_title_', 'miss _name_', '_title_ _name_', '_title_ _puntuation_ _title_ _puntuation_ _name_', '_name_ al _name_', 'al _puntuation_ _name_', '_title_ _puntuation_ _name_', '_name_', 'miss _puntuation_ _name_']
text_entities2text_comb_entity(input, \
	entities,\
	sub_entities = ['name', 'title'],\
	comb_entity_indicator = person_indicator)

input = u" 100 million aed"
entities = {'currency': ['aed'], 'number':['100']}
text_entities2text_comb_entity(input, \
	entities,\
	sub_entities = ['number', 'currency'],\
	comb_entity_indicator = money_indicator)
'''
def text_entities2text_comb_entity(input, \
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

'''
from sms_utility_re import *
usage:

input = u"this is jim wang , i live in dubai uad"
entities = {"number":[],"email":[],"name":["jim","wang"],"location":["dubai"],"orgnization":[],"title":[],"role":[],"currency":[],"weekday":[],"month":[],"placetype":[],"orgnizationtype":[],"documenttype":[],"documentformat":[]}
entities_context_wildcard = ['name', 'location']
nearby_entity_merge = [True, False]

text_entities2text_entities_wildcard(input,\
	entities,\
	entities_context_wildcard,\
	nearby_entity_merge = None)
'''
def text_entities2text_entities_wildcard(\
	input,\
	entities,\
	entities_context_wildcard,\
	nearby_entity_merge = None,\
	input_text_preprocessed = False):
	try:
		if nearby_entity_merge is None:
			nearby_entity_merge = \
			len(entities_context_wildcard)*[False]
		if input_text_preprocessed:
			text_entity = input
		else:
			text_entity = text_preprocess(input)
		for entity, nearby_entity_merge1 \
			in zip(entities_context_wildcard, \
			nearby_entity_merge):
			text_entity = marge_entity2preprocessed_text(\
				text_entity,\
				entitis = entities[entity],\
				nearby_entity_merge = nearby_entity_merge1)
			text_entity = text_entity2text_entity_wildcard(\
				text_entity,\
				entity_wildcard = entity)
		return text_entity
	except:
		return None

'''
from sms_utility_re import *

input = u" _start_ dear mr [jim wang] i am at dubai regards [sayed ahmed] _end_ "
entities = {"name": ["ahmed","sayed","jim","wang"],"location": ["dubai"],"title": ["mr"]}
target_entity = 'name'
target_entity_nearby_merge = True
context_entities_wildcard = ['location', 'title', 'name']
context_entities_nearby_merge = [True, True, True]

output = text_entites2text_entity_context_wild_list(\
	input, \
	entities, \
	target_entity, \
	context_entities_wildcard,\
	context_entities_nearby_merge = \
	context_entities_nearby_merge)
'''
def text_entites2text_entity_context_wild_list(\
	input, \
	entities, \
	target_entity, \
	context_entities_wildcard,\
	context_entities_nearby_merge = None,\
	input_text_preprocessed = True,\
	context_target_entity_replacy_by_wildcard = True):
	try:
		if input_text_preprocessed is not True:
			input = text_preprocess(input)
		target_entity_list = text_entity2entities(input)
		text_entity = text_entity2text_entity_wildcard(\
			input,\
			target_entity)
		###
		text_entity = text_entities2text_entities_wildcard(\
			text_entity,\
			entities = entities,\
			entities_context_wildcard = context_entities_wildcard,\
			nearby_entity_merge = \
			context_entities_nearby_merge,\
			input_text_preprocessed = True)
		text_entity = text_wildcard_entity_recovery(text_entity, \
			entities = target_entity_list, \
			entity_type = target_entity, \
			with_bracket = True)
		text_entity_list = text_entity2entity_context_list(\
			text_entity, \
			context_entity_replacy_by_wildcard = \
			target_entity in context_entities_wildcard or \
			context_target_entity_replacy_by_wildcard,\
			entity_type = target_entity)
		return text_entity_list
	except Exception as e:
		print(str(e))
		return None


'''
matching a text_entity to indicator function and indicator list

input = u" get the documents by [monday 7 am] _end_"
text_entity_categorization(input,
	output_entity_name = 'document_transfer_time',
	indicator_func = document_transfer_time_context_match,\
	indicator_list = document_transfer_time_context_indicator)
'''
def text_entity_categorization(input,
	output_entity_name = 'entity',
	indicator_func = None,\
	indicator_list = None):
	try:
		output = {}
		entity = text_entity2entity(input)
		#print(preprocessed_text_entity2context_idx(text_entity1))
		text_entity1 = text_entity2text_entity_wildcard(\
			input)
		if indicator_func is not None:
			indicator1 = text_entity2entity(\
				indicator_func(text_entity1))
			if indicator1 is not None:
				return {output_entity_name:entity, \
					output_entity_name+'_indicator': indicator1}
		if indicator_list is not None:
			indicator2 = text_entity2entity(\
				marge_entity2preprocessed_text(\
				text_entity1, indicator_list, \
				nearby_entity_merge = True))
			if indicator2 is not None:
				return {output_entity_name:entity, \
					output_entity_name+'_indicator': indicator2}
		return None
	except:
		return None

'''
matching a text_entity to indicator and fucntions

usage:

from sms_utility_re import * 
from sms_utility_re_event import * 

input = u" _start_ i will be moving to _location_ "

text_categorization(input, 
	indicator_func = travel_traveler_sender_match,\
	indicator_list = ['i will be moving'])
'''
def text_categorization(input, 
	indicator_func = None,\
	indicator_list = None):
	try:
		if indicator_func is not None:
			indicator1 = text_entity2entity(\
				indicator_func(input))
			if indicator1 is not None:
				return indicator1
		if indicator_list is not None:
			indicator2 = text_entity2entity(\
				marge_entity2preprocessed_text(\
				input, indicator_list, \
				nearby_entity_merge = True))
			if indicator2 is not None:
				return indicator2
		return None
	except:
		return None
################sms_utility_re.py################
