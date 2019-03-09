#################sms_utility_re_attitude.py#################
import re
from sms_utility_re import *

r_you_are = r'(you|u) (are|r)'
re_the = r'(a|an|the|our|one|this|that|my|your|ur|his|her|their|its)'

re_like = r'(like|love|kiss|kissing|bless|miss|wish|loving|respect|wish)'
re_hate = r'(hate|hating|fuk|fk|curse)'
re_you = r'(you|u)'

re_good = r'(good|wanderful|great|best|strong|beautiful|gorgeous|sweet)'
re_bad = r'(terrible|selfish|bad)'

re_so = r'(so+|such|very)'

###sender like receiver
'''
input = u" i love you "
sender_like_receiver_re(input)

input = u" you are the best "
sender_like_receiver_re(input)
'''
re_sender_like_receiver1 = r' '\
	+re_like+r' '\
	+re_you+r' '
re_sender_like_receiver2 = r' '\
	+r_you_are+r' '\
	+r'('+re_the+r' )*'\
	+r'('+re_so+r' )*'\
	+re_good+r' '

re_sender_like_receiver = [\
	re_sender_like_receiver1,\
	re_sender_like_receiver2\
	]

def sender_like_receiver_re(input):
	for pattern in re_sender_like_receiver:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

###sender hate receiver
'''
input = u" fuck you "
sender_hate_receiver_re(input)

input = u" you are bad man "
sender_hate_receiver_re(input)
'''
re_sender_hate_receiver1 = r' '\
	+re_hate+r' '\
	+re_you+r' '
re_sender_hate_receiver2 = r' '\
	+r_you_are+r' '\
	+r'('+re_the+r' )*'\
	+re_bad+r' '

re_sender_hate_receiver = [\
	re_sender_hate_receiver1,\
	re_sender_hate_receiver2\
	]

def sender_hate_receiver_re(input):
	for pattern in re_sender_hate_receiver:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input
#################sms_utility_re_attitude.py#################