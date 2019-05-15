#################sms_utility_re_attitude.py#################
import re
from sms_utility_re import *

r_you_are = r'(you|u) (are|r)'
re_the = r'(a|an|the|our|one|this|that|my|your|ur|his|her|their|its)'

re_like = r'(like|love|kiss|kissing|bless|miss|wish|loving|respect|wish)'
re_hate = r'(hate|hating|curse|kill)'
re_you = r'(you|u)'

re_good = r'(good|wanderful|great|best|strong|beautiful|gorgeous|sweet)'
re_bad = r'(terrible|selfish|bad|disgusting)'

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

input = u" i do not want to see you "
sender_hate_receiver_re(input)

input = u"  i will kill u  "
sender_hate_receiver_re(input)
'''
re_lier = r'(lier|liar|asshole|dog|slut|bastard|jerk|bitch|son of bitch|motherfucker|mother fucker|fucker|loser|cheater|prostitiute|idiot|bullshit|bull shit)'
re_fuck = r'(fuck|fucking|fuk|fk)'

re_sender_hate_receiver1 = r' '\
	+re_i_will+r' '\
	+re_hate+r' '\
	+re_you+r' '

re_sender_hate_receiver2 = r' '\
	+r_you_are+r' '\
	+r'('+re_so+r' )*'\
	+r'('+re_the+r' )*'\
	+re_bad+r' '

re_sender_hate_receiver3 = \
	r' (i|we) '\
	+r'(don _punctuation_ t|dont|do not|) '\
	+r'want to (see|talk to|c) '\
	+r'(you|u|your face|ur face) '

re_sender_hate_receiver4 = r' '\
	+r_you_are+r' '\
	+r'('+re_the+r' )*'\
	+re_lier+r' '

re_sender_hate_receiver5 = r' '\
	+re_fuck+r' '\
	+re_you+r' '

re_sender_hate_receiver = [\
	re_sender_hate_receiver1,\
	re_sender_hate_receiver2,\
	re_sender_hate_receiver3,\
	re_sender_hate_receiver4,\
	re_sender_hate_receiver5]

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
