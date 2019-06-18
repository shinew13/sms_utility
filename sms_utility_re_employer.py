##################sms_utility_re_employer.py################
import re
from sms_utility_re import *

re_i_employer = r'(i|we|this)'

re_my_employer = r'(my|our)'

re_work_employer = r'(work|am working|are working)'

re_in_employer = r'(at|in|with|for|from)'

re_company_employer = r'(company|employer|institute)'

re_be_employer = r'(is|was|has been|will be|m)'

re_regards_employer = r'(regards|regard|regd)'

re_thanks_employer = r'(thanks|thank you|thank you very much|sincerely)'

re_email_ending_employer = r'(regards|regard|regd|thanks|thank you|thank you very much|sincerely)'
# re_regards_employer + re_thanks_employer

re_am_employer = r'(_puntuation_ m|am|this is)'

re_sender_employer_context1 = r' ' \
                      + re_i_employer + r' ' \
                      + re_work_employer + r' ' \
                      + re_in_employer + r' ' \
                      + '_entity_ '

re_sender_employer_context2 = r' ' \
                      + re_my_employer + r' ' \
                      + re_company_employer + r' ' \
                      + re_be_employer + r' ' \
                      + '_entity_ '

re_sender_employer_context3 = r' ' \
                      + re_regards_employer + r' ' \
                      + r'((\w+) ){0,2}' \
                      + r'_name_ ' \
                      + r'((\w+) ){0,2}' \
                      + '(_puntuation_ )*(from )*_entity_ (_puntuation_ )*_end_ '

re_sender_employer_context4 = r' ' \
                      + re_i_employer + r' ' \
                      + re_be_employer + r' ' \
                      + r'((\w+) ){0,3}' \
                      + 'from ((\w+) ){0,3}_entity_ '

re_sender_employer_context5 = r' ' \
                      + re_am_employer + r' ' \
                      + r'((\w+) ){0,2}' \
                      + '_name_ ((\w+) ){0,2}' \
                      + r'(_puntuation_ )*_entity_ '

re_sender_employer_context6 = r' from _entity_ here '

re_sender_employer_context7 = r' (here|regards) from ((\w+) ){0,2}_entity_ '

re_sender_employer_context8 = r' (am|m|this) (_name_|calling) ((\w+) ){0,1}from _entity_'

re_sender_employer_context9 = r' this is ((\w+) ){0,2}of _entity_ '

re_sender_employer_context10 = r' ' \
                       + re_regards_employer + r' ' \
                       + r'((\w+) ){0,2}_name_ ((\w+) ){0,2}' \
                       + r'(_puntuation_ )*_entity_ '

re_sender_employer_context11 = r' ' \
                       + re_i_employer + r' ' \
                       + re_be_employer + r' ' \
                       + r'_name_ ' \
                       + r'((\w+) ){0,2}' \
                       + r'(from )*' \
                       + '_entity_ '

re_sender_employer_context12 = r' ' \
                       + re_regards_employer + r' ' \
                       + r'((\w+) ){1,3}' \
                       + r'_entity_ _end_ '

re_sender_employer_context13 = r' ' \
                       + re_thanks_employer + r' ' \
                       + r'((\w+) ){0,3}_entity_ ((\w+) ){0,2}_end_ '

re_sender_employer_context14 = r' my (office|boss|colleague|work) (at|in|of|for) _entity_ '

re_sender_employer_context15 = r' my _entity_ _puntuation_ s (office|boss|colleague|work) '

re_sender_employer_context16 = r' '\
	+re_regards_employer \
	+ r' ((\w+) ){0,2}from _entity_ _end_'

re_sender_employer_context17 = r' '+re_regards_employer + r' _name_ _puntuation_ _entity_ '

re_sender_employer_context18 = r' '+re_regards_employer + r' _name_ from ((\w+) ){0,2}regarding _entity_ ' 
# todo  _name_ from LOCATION_NAME regarding [adib]

re_sender_employer_context19 = r' '+re_email_ending_employer+' _puntuation_ _name_ _entity_ '

re_sender_employer_context20 = r' '+re_i_employer + re_be_employer + r' _name_ _entity_ '

re_sender_employer_context21 = r' '+re_email_ending_employer + r' _name_ ((\w+) ){0,3} _entity_ '

re_sender_employer_context22 = r' you have ((\w+) ){0,3} account with _entity_ (we|i) (are|am){0,1} (offering|offer) ((\w+) ){0,3}'

re_sender_employer_context23 = r' '+re_email_ending_employer+ r' _puntuation_ _name_ _puntuation_ from _entity_ '

re_sender_employer_context24 = r' here is _name_ from _entity_ '

re_sender_employer_context25 = r' '+re_email_ending_employer + r' _name_ (_number_ ){0,3}_entity_ '

re_sender_employer_context26 = r' '+re_email_ending_employer + r' _puntuation_ regards _puntuation_ _entity_ '

re_sender_employer_context27 = r' '+re_email_ending_employer + r' _name_ from _entity_ '

re_sender_employer_context28 = r' '+re_thanks_employer + r' _name_ _puntuation_ this _name_ from _entity_ '

# the last re postfix
max_ix = 28
re_sender_employer_context = []
for ix in range(1, max_ix + 1):
    eval("re_sender_employer_context." + "append" + "(re_sender_employer_context" + str(ix) + ")")


def sender_employer_context_match(input):
    for pattern in re_sender_employer_context:
        output = extract_entity_by_re(input, \
                                      pattern, \
                                      replace_entity_by_wildcard=True, \
                                      return_none_if_not_matched=True)
        if output is not None:
            return output
    return input


input = u""" i am working from _entity_ """
print(sender_employer_context_match(input))

##################sms_utility_re_employer.py################
