##################sms_utility_re_employer.py################
import re
from sms_utility_re import *

re_i_employer = r'(i|we)'

re_my_employer = r'(my|our)'

re_work_employer = r'(work|am working|are working)'

re_in_employer = r'(at|in|with|for)'

re_company_employer = r'(company|employer|institute)'

re_be_employer = r'(is|was|has been|will be)'

re_regards_employer = r'(regards|regard|regd)'

re_sender_employer_context1 = r' '\
	+re_i_employer+r' '\
	+re_in_employer+r' '\
	+'_entity_ '

re_sender_employer_context2 = r' '\
	+re_my_employer+r' '\
	+re_be_employer+r' '\
	+'_entity_ '

re_sender_employer_context3 = r' '\
	+re_regards_employer+r' _name_ '\
	+'(from)* _entity_ _end_ '

re_sender_employer_context = [\
	re_sender_employer_context1,\
	re_sender_employer_context2,\
	re_sender_employer_context3]

def sender_employer_context_match(input):
	for pattern in re_sender_employer_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
input = u" regards _name_ from _entity _end_ "
sender_employer_context_match(input)
'''

##################sms_utility_re_employer.py################
