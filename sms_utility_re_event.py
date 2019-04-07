###########sms_utility_re_event.py###########
import re
from sms_utility_re import *

re_i_will = r'(i am|_start_ will|i was|we|i|i will|i will be|i am going to|i _puntuation_ m going to|we will|i had|i have to|i need|i had to|i _puntuation_ ll|i plan|i need to|i am|i gotta|lets|we _puntuation_ re|we can|im gonna|im|i _puntuation_ m|i _puntuation_ m gonna|im going|we shall|i shall|we are|we r|we _puntuation_ ll|i have|i had|i _puntuation_ going|i am attending|i am able|let _puntuation_ s|let us|let us have)'
re_you_will = r'(you|you will|you will be|you had|you _puntuation_ ll|you plan|you need to|you are|you gotta|lets|you can|ur gonna|ur|u r|you r|u are|you are gonna|im going|you shall|you are|you r|you _puntuation_ ll|you have|you had|you _puntuation_ going|you are able|let _puntuation_ s|let us|let us have|are you|r u|are u|will you|could you|are you going)'
re_will = r'(is|will|shall|is going to|will go|had|_puntuation_ ll|was|were|has|have|having|going to|is coming|will be|cancelled|cancel)'
re_my = r'(my|our)'
re_your = r'(your|ur)'

re_at = r'(in|on|at|by)'
re_in = r'(in|at|with|to|for|on|from)'
re_the = r'(a|an|the|our|one|this|that|my|your|ur|his|her|their|its)'
re_today = r'(today|tomorrow|at _number_|then|now|just|still|right now)( (morning|evening|afternoon|night))*'
re_to = r'((back|down) )*(to|into)'
re_of = r'(of|for|with|togerther with|from)'
re_with = r'(with|togerther with|between (u|you|me|him|her|them) and)'
re_me = r'(me|you|u|him|her|it|them|_name_|_title_)'
re_from = r'((back|down) )*(from|frm|fr)'
re_have = r'(have|had|having|will have|own|hold|holding|get|got|getting|obtain|gain|receive|take|taking|token|receive|receiving|accept|accepting)'
re_make = r'(make|made|making|conduct|conduting|conducted)'
re_at_place = re_at+r' '\
	+r'('+re_the+r' )*'\
	+r'(_location_|_location_ _placetype_)'

re_go_to = r'(go to|going to|went to|go|gonna)'
re_at_location = re_at+r' '\
	+r'('+re_the+r' )*'\
	+r'_location_'

re_please = r'(please|pls|plz)'

'''
indicators of travel event
'''
re_travel = r'(travel|travel|travelling|trip|way|fly|flight|driving|boarding|drive|move)'
re_travel_from = r'(depart|departure)'
re_travel_to = r'(visit|visited|visiting|arriving|arrive|arrived)'
re_travel_all = r'((business|personal|duty) )*('\
	+re_travel+r'|'\
	+re_travel_from+r'|'\
	+re_travel_to+r')'
re_travelling = r'(travelling|going|coming|leaving|flying|driving|boarding|departing|visiting|arriving)'
re_go = '(come|go|going|coming)'
re_leave = r'(leave|left|leaving)'


'''
input = u" [jim] will go to a travel "
travel_traveler_context_match(input)

input = u" [jim] leave _location_ "
travel_traveler_context_match(input)

input = u" [jim] _puntuation_ s travel "
travel_traveler_context_match(input)

input = u" travel of [jim] "
travel_traveler_context_match(input)

input = u" [ceo] travelling from "
travel_traveler_context_match(input)
'''
re_traveler1 = r' _entity_ '\
	+r'('+re_will+' )'\
	r'((to|for) )*'\
	+r'('+re_the+' )*'\
	+re_travel_all+' '
re_traveler2 = r' _entity_ '\
	+r'('+re_will+r' )*'\
	+'('+re_go+r'|'+re_leave+r') '\
	+r'('+re_to+r' )*'\
	+r'('+re_the+r' )*'\
	+'_location_ '
re_traveler3 = r' _entity_ (in|on|_puntuation_ s) '\
	+re_travel_all+r' '
re_traveler4 = r' '+re_travel_all+' '\
	+re_of+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '
re_traveler5 = r' ('+re_go+'|'\
	+re_travel_all+r'|'\
	+re_leave+r') '\
	+re_with+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '
re_traveler6 = r' _entity_ '\
	+re_travelling+r' '\
	+r'('+re_from+r'|'\
	+re_to+r') '\

re_travel_traveler_context = [re_traveler1,\
	re_traveler2,\
	re_traveler3,\
	re_traveler4,\
	re_traveler5,\
	re_traveler6]

def travel_traveler_context_match(input):
	for pattern in re_travel_traveler_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *
input = u" depart _entity_ "
travel_from_location_context_match(input)

input = u" leave today to _place_ from the _entity_ "
travel_from_location_context_match(input)

input = u" go to _place_ from the _entity_ "
travel_from_location_context_match(input)
'''

re_travel_from_location1 = \
	r' (depart|leave|exit|leaving|left) '\
	+r'(('+re_today+r') )*'\
	+r'(to _place_ )*'\
	+r'(('+re_from+r') )*'\
	+r'('+re_the+r' )*'\
	+r'_entity_ '

re_travel_from_location2 = \
	r' ('+re_travel\
	+r'|'+re_go\
	+r'|'+re_leave+r') '\
	+r'(('+re_today+r') )*'\
	+r'(to _place_ )*'\
	+re_from+r' '\
	+r'('+re_the+' )*'\
	+r'_entity_ '

re_travel_from_location_context = [\
	re_travel_from_location1,
	re_travel_from_location2\
	]

def travel_from_location_context_match(input):
	for pattern in re_travel_from_location_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *

input = u" come today _entity_ "
travel_to_location_context_match(input)

input = u" go from _place_ to the [uae] "
travel_to_location_context_match(input)
'''

re_travel_to_location1 = \
	r' ('+re_travel_to+r'|'\
	+re_go+r') '\
	+r'(('+re_today+r') )*'\
	+r'('+re_from+r' _place_ )*'\
	+r'('+re_to+r' )*'\
	+r'('+re_the+r' )*'\
	r'_entity_ '

re_travel_to_location2 = \
	r' ('+re_travel_all+r'|'\
	+re_travelling+r'|'\
	+re_go+r'|'\
	+re_leave+r') '\
	+r'(('+re_today+r') )*'\
	+r'('+re_from+r' _place_ )*'\
	+re_to+r' '\
	+r'('+re_the+r' )*'\
	r'_entity_ '

re_travel_to_location3 = \
	r' welcome to _entity_ '

re_travel_to_location_context = [\
	re_travel_to_location1,\
	re_travel_to_location2,\
	re_travel_to_location3\
	]

def travel_to_location_context_match(input):
	for pattern in re_travel_to_location_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input


'''
input = u" trip on the [monday] "
travel_time_context_match(input)

input = u" [monday] _puntuation_ s travel "
travel_time_context_match(input)

input = u" departure time will be [next month] "
travel_time_context_match(input)

input = u" to _location_ on [monday] "
travel_time_context_match(input)
'''
re_travel_time1 = r' ('+re_travel_all+r'|'\
	+re_travelling+r'|'\
	+re_go+r'|'\
	+re_leave+r') '\
	+r'(('+re_in+r'|of) )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_travel_time2 = r' _entity_ _puntuation_ s '\
	+re_travel_all+r' '
re_travel_time3 = r' '+re_travel_all+r' '\
	+r'((date|time) )*'\
	+re_will+r' '\
	+r'('+re_in+' )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_travel_time4 = r' (from|to) _location_ '\
	+r'((at|on|after|before|by) )*'\
	+r'_entity_ '
re_travel_travel_time_context = [re_travel_time1,\
	re_travel_time2,\
	re_travel_time3,\
	re_travel_time4]

def travel_time_context_match(input):
	for pattern in re_travel_travel_time_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *
input = u' welcome to _location_ '
travel_traveler_receiver_match(input)
'''
re_travel_traveler_receiver1 = \
	r' (your|ur) (_location_ )*'\
	+re_travel_all+' '

re_travel_traveler_receiver2 = \
	r' '+re_you_will+r' '\
	r'('+re_today+r' )*'\
	+re_go+' '\
	+r'('+re_in+r' )*'\
	+r'('+re_the+r' )*'\
	+r'_location_ '

re_travel_traveler_receiver3 = \
	r' '+re_travel_all+' '\
	r'(togerther with|with) (you|u) '

re_travel_traveler_receiver4 = \
	r' welcome to _location_ '

re_travel_traveler_receiver5 = \
	r' '+re_you_will+r' '\
	r'('+re_today+r' )*'\
	+r'('+re_in+r' )*'\
	+r'('+re_the+r' )*'\
	+re_travel_all+r' '

re_travel_traveler_receiver_match = [\
	re_travel_traveler_receiver1,\
	re_travel_traveler_receiver2,\
	re_travel_traveler_receiver3,\
	re_travel_traveler_receiver4,\
	re_travel_traveler_receiver5\
	]

def	travel_traveler_receiver_match(input):
	for pattern in re_travel_traveler_receiver_match:
		output = extract_entity_by_re(input, \
			pattern, \
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
input = u' my way to _location_ '
travel_traveler_sender_match(input)
'''

traveler_sender1 = r' on my way '
re_travel_traveler_sender_match = [\
	traveler_sender1,\
	r' (my|our) (_location_ )*'+re_travel_all+' ',\
	r' '+re_i_will+r' '\
	r'('+re_today+' )*'\
	+r'('+re_in+' )*'\
	+r'('+re_the+' )*'\
	+re_travel_all+r' ',\
	r' '+re_i_will+r' '\
	+re_go+' '\
	+r'('+re_in+' )*'\
	+r'('+re_the+' )*'\
	+r'_location_ ',\
	r' '+re_travel_all+' '\
	r'(togerther with|with) (me|us) ',\
	r' _start_ '+re_in+' ('+re_the+' )*'+re_travel_all+' ',
	r' _start_ '+re_travelling+' '\
	+r'((back )*'+re_in+' )*'\
	+r'('+re_the+' )*'\
	+r'_location_ '\
	]

def	travel_traveler_sender_match(input):
	for pattern in re_travel_traveler_sender_match:
		output = extract_entity_by_re(input, \
			pattern, return_none_if_not_matched = True)
		if output is not None:
			return output
	return input


'''
indicators of meeting event
'''
re_meet = r'(meet|meeting|visit|visiting|conversion|visiting|chat|presentation|discussion)'
re_see = r'(see|meet|met|visit)'
re_dinner = r'(dinner|lunch|tea|tea time)'
re_talk = r'(talk|speak|spoke|talking|discussed|discuss)'

re_meeting_all = r'('\
	+re_meet+r'|'\
	+re_dinner+r')'

'''
sender in the meeting

from sms_utility_re_event import *

input = u" i see it "
meeting_sender_attend_match(input)

input = u" _start_ still in a meeting with "
meeting_sender_attend_match(input)

input = u" i am now in a meeting "
meeting_sender_attend_match(input)

input = u" a meeting today with me "
meeting_sender_attend_match(input)

input = u" talk now with me "
meeting_sender_attend_match(input)

input = u" talk now to me "
meeting_sender_attend_match(input)

input = u" i will today talk to you "
meeting_sender_attend_match(input)

input = u" i will today visit you "
meeting_sender_attend_match(input)

input = u" see you "
meeting_sender_attend_match(input)

from sms_utility_re_event import *
input = u" tea at _location_ with me "
meeting_sender_attend_match(input)
'''
re_sender_meeting1 = r' '+re_my+r' '\
	+re_meet+r' '
re_sender_meeting2 = r' _start_ '\
	r'('+re_today+' )*'\
	+re_in+r' '\
	+r'('+re_the+r' )*'\
	+re_meet+r' '
re_sender_meeting3 = r' '+re_i_will+r' '\
	r'('+re_today+' )*'\
	+re_in+r' '\
	+r'('+re_the+r' )*'\
	+re_meet+r' '
re_sender_meeting4 = r' '+re_meeting_all+r' '\
	r'('+re_today+' )*'\
	+re_with+r' (me|us) '
re_sender_meeting5 = r' ('+re_talk+r'|'\
	+re_see+r') '\
	r'('+re_today+' )*'\
	+re_with+r' me '
re_sender_meeting6 = r' '+re_i_will+r' '\
	+r'('+re_today+' )*'\
	+r'('+re_at_location+' )*'\
	+r'('+re_talk+r'|'\
	r'(meet|met|visit|see you|c u|see u)) '
re_sender_meeting7 = r' (see|c) (you|u) '\
	+re_at+r' '
re_sender_meeting8 = r' '+re_i_will+r' '\
	+r'('+re_today+' )*'\
	+r'('+re_go_to+r'|'\
	+re_have+r') '\
	+r'('+re_the+r' )*'\
	+re_meet+r' '
re_sender_meeting9 = r' (us|me) '\
	+re_to+r' '\
	+'('+re_meet\
	+'|'+re_talk+') '
re_sender_meeting10 = r' we (see|c) '
re_sender_meeting11 = r' ('+re_dinner+r'|'\
	+re_meet+r') '\
	+r'('+re_today+r' )*'\
	+r'('+re_at_location+r' )*'\
	+re_with+r' '\
	+r'(me|us) '
re_sender_meeting12 = r' '+re_my+r' '\
	+re_dinner+r' '\
	+re_with+r' '\
	+r'('+re_the+r' )*'\
	+re_me+r' '
re_sender_meeting13 = r' _start_ meeting _end_ '
re_sender_meeting14 = r' _start_ can _puntuation_ t talk '
re_sender_meeting15 = r' i _puntuation_ m in a meetin '

re_sender_in_meeting = [re_sender_meeting1,\
	re_sender_meeting2,\
	re_sender_meeting3,\
	re_sender_meeting4,\
	re_sender_meeting5,\
	re_sender_meeting6,\
	re_sender_meeting7,\
	re_sender_meeting8,\
	re_sender_meeting9,\
	re_sender_meeting10,\
	re_sender_meeting11,\
	re_sender_meeting12,\
	re_sender_meeting13,\
	re_sender_meeting14,\
	re_sender_meeting15\
	]

def meeting_sender_attend_match(input):
	for pattern in re_sender_in_meeting:
		output = extract_entity_by_re(input, \
			pattern, \
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *
input = u" see you "
meeting_receiver_attend_match(input)

input = u" your meeting "
meeting_receiver_attend_match(input)

input = u" you are now in the meeting "
meeting_receiver_attend_match(input)

input = u" talk now to you "
meeting_receiver_attend_match(input)

input = u" you will now at _location_ meet him "
meeting_receiver_attend_match(input)

input = u" see you at "
meeting_receiver_attend_match(input)

input = u" you will still have the meeting "
meeting_receiver_attend_match(input)

input = u" you to meet "
meeting_receiver_attend_match(input)

input = u" dinner today at _location_ with you "
meeting_receiver_attend_match(input)

input = u" your dinner with _title_ "
meeting_receiver_attend_match(input)

input = u" _start_ did you _name_ my _title_ re lease _number_ _end_ "
meeting_receiver_attend_match(input)
'''
re_receiver_meeting1 = r' '+re_your+r' '\
	+re_meet+r' '
re_receiver_meeting2 = r' '+re_you_will+r' '\
	+r'('+re_today+' )*'\
	+r'(see|c) '\
	+r'('+re_the+r' )*'\
	+re_me+r' '
re_receiver_meeting3 = r' '+re_you_will+r' '\
	r'('+re_today+' )*'\
	+re_in+r' '\
	+r'('+re_the+r' )*'\
	+re_meet+r' '
re_receiver_meeting4 = r' '+re_meeting_all+r' '\
	r'('+re_today+' )*'\
	+re_with+r' (you|u) '
re_receiver_meeting5 = r' ('+re_talk+r'|'\
	+re_see+r') '\
	+r'('+re_today+' )*'\
	+r'('+re_with+' )*'\
	r'(you|u) '
re_receiver_meeting6 = r' '+re_you_will+r' '\
	+r'('+re_today+' )*'\
	+r'('+re_at_location+' )*'\
	+r'('+re_talk+r'|'\
	r'(meet|met|visit)) '
re_receiver_meeting7 = r' (see|c) (you|u) '\
	+re_at+r' '
re_receiver_meeting8 = r' '+re_you_will+r' '\
	+r'('+re_today+' )*'\
	+r'('+re_go_to+r'|'\
	+re_have+r') '\
	+r'('+re_the+r' )*'\
	+re_meet+r' '
re_receiver_meeting9 = r' (you|u) '\
	+re_to+r' '\
	+'('+re_meet\
	+'|'+re_talk+') '
re_receiver_meeting11 = r' ('+re_dinner+r'|'\
	+re_meet+r') '\
	+r'('+re_today+r' )*'\
	+r'('+re_at_location+r' )*'\
	+re_with+r' '\
	+r'(you|u) '
re_receiver_meeting12 = r' '+re_your+r' '\
	+re_dinner+r' '\
	+re_with+r' '\
	+r'('+re_the+r' )*'\
	+re_me+r' '
re_receiver_meeting13 = r' (please|pls) '\
	+r'('+re_talk\
	+r'|'+re_meet+r') '

re_receiver_in_meeting = [re_receiver_meeting1,\
	re_receiver_meeting2,\
	re_receiver_meeting3,\
	re_receiver_meeting4,\
	re_receiver_meeting5,\
	re_receiver_meeting6,\
	re_receiver_meeting7,\
	re_receiver_meeting8,\
	re_receiver_meeting9,\
	re_receiver_meeting11,\
	re_receiver_meeting12,\
	re_receiver_meeting13\
	]

def meeting_receiver_attend_match(input):
	for pattern in re_receiver_in_meeting:
		output = extract_entity_by_re(input, \
			pattern, \
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *
input = u" meet in _location_ _placetype_ _entity_ "
meeting_time_context_match(input)

input = u" [monday] _puntuation_ s meeting "
meeting_time_context_match(input)

input = u" meeting date will be in the [next month] "
meeting_time_context_match(input)

input = u" talk in the [6 pm] "
meeting_time_context_match(input)

input = u" talk to you in the [monday] "
meeting_time_context_match(input)

input = u" on the [monday] i will meet "
meeting_time_context_match(input)

input = u" dinner at [3] "
meeting_time_context_match(input)
'''
re_meeting_time1 = r' '+re_meet+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_at_place+r' )*'\
	+r'(('+re_in+r'|of) )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_meeting_time2 = r' _entity_ _puntuation_ s '\
	+re_meeting_all+r' '
re_meeting_time3 = r' '+re_meeting_all+r' '\
	+r'((date|time) )*'\
	+re_will+r' '\
	+r'('+re_in+' )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_meeting_time4 = r' ('+re_talk+r'|'\
	+re_see+r') '\
	+r'('+re_with+r' )*'\
	+r'('+re_the+r' )*'\
	+r'(_name_|_title_|you|u|me|him|her|them) '\
	+r'(('+re_in+r'|of) )*'\
	+r'('+re_the+r' )*'\
	+'_entity_ '
re_meeting_time5 = r' '+re_meeting_all+r' '\
	+re_of+r' '\
	+r'('+re_the+r' )*'\
	+r'(_name_|_title_) '\
	+r'(('+re_in+r'|of) )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_meeting_time6 = r' (('+re_in+r'|of) )*'\
	+r'('+re_the+r' )*'\
	+'_entity_ '\
	r'('+re_i_will\
	+r'|'+re_you_will+r') '\
	+re_meeting_all+r' '
re_meeting_time7 = r' '+re_dinner+r' '\
	+r'(('+re_in+r'|of) )'\
	+r'('+re_the+' )*'\
	+'_entity_ '

re_meeting_meeting_time_context = [re_meeting_time1,\
	re_meeting_time2,\
	re_meeting_time3,\
	re_meeting_time4,\
	re_meeting_time5,\
	re_meeting_time6,\
	re_meeting_time7]

def meeting_time_context_match(input):
	for pattern in re_meeting_meeting_time_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input


'''
from sms_utility_re_event import *

input = u" today _puntuation_ s meeting with [adco] is at _number_ "
meeting_location_context_match(input)

input = u" meet today with you in _entity_ "
meeting_location_context_match(input)

input = u" meeting place will be in the _entity_ "
meeting_location_context_match(input)

input = u" meet place is in the _entity_ "
meeting_location_context_match(input)

input = u" talk to you in _entity_ "
meeting_location_context_match(input)

input = u" meeting with the _title_ in the _entity_ "
meeting_location_context_match(input)

input = u" in the _entity_ i will meet "
meeting_location_context_match(input)

input = u" tea time with you at _entity_ "
meeting_location_context_match(input)

input = u" _entity_ meeting "
meeting_location_context_match(input)

from sms_utility_re_event import *
input = u" to _entity_ to meet "
meeting_location_context_match(input)
'''

re_meeting_location1 = r' '+re_meet+r' '\
	+r'('+re_today+r' )*'\
	+r'('+re_with+r' )*'\
	+r'('+re_the+r' )*'\
	+r'('+re_me+r' )*'\
	+r'('+re_at+r'|of) '\
	+r'('+re_the+r' )*'\
	+'_entity_ '
re_meeting_location2 = r' _entity_ _puntuation_ s '\
	+re_meeting_all+r' '
re_meeting_location3 = r' '+re_meeting_all+r' '\
	+r'('+re_today+r' )*'\
	+r'((place|location) )*'\
	+re_will+r' '\
	+r'('+re_at+' )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_meeting_location4 = r' ('+re_talk+r'|'\
	+re_see+r') '\
	+r'('+re_with+r' )*'\
	+r'('+re_the+r' )*'\
	+r'('+re_me+r') '\
	+r'('+re_today+r' )*'\
	+r'(('+re_at+r'|of) )*'\
	+r'('+re_the+r' )*'\
	+'_entity_ '
re_meeting_location5 = r' '+re_meeting_all+r' '\
	+re_of+r' '\
	+r'('+re_the+r' )*'\
	+r'(_name_|_title_) '\
	+r'('+re_today+r' )*'\
	+r'(('+re_at+r'|of) )*'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_meeting_location6 = r' (('+re_at+r'|of) )*'\
	+r'('+re_the+r' )*'\
	+'_entity_ '\
	r'('+re_i_will\
	+r'|'+re_you_will+r') '\
	+re_meeting_all+r' '
re_meeting_location7 = r' '+re_dinner+r' '\
	+r'('+re_with+r' )*'\
	+r'('+re_the+r' )*'\
	+r'('+re_me+r') '\
	+r'('+re_today+r' )*'\
	+r'(('+re_at+r'|of) )'\
	+r'('+re_the+' )*'\
	+'_entity_ '
re_meeting_location8 = r' _entity_ (_puntuation_ )*'\
	r'(meeting|meet|meetings|conversion) '
re_meeting_location9 = r' (to|go|going|come|coming) _entity_ (to|for) '\
	+r'('+re_meeting_all\
	+r'|'+re_talk+r') '

re_meeting_meeting_location_context = [\
	re_meeting_location1,\
	re_meeting_location2,\
	re_meeting_location3,\
	re_meeting_location4,\
	re_meeting_location5,\
	re_meeting_location6,\
	re_meeting_location7,\
	re_meeting_location8,\
	re_meeting_location9]

def meeting_location_context_match(input):
	for pattern in re_meeting_meeting_location_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
input = u"  meet at _entity_  "
meeting_attendee_context_match(input)

input = u" [ceo] will be in a meeting "
meeting_attendee_context_match(input)

input = u" [ceo] will see the _person_ in meeting "
meeting_attendee_context_match(input)

input = u" [ceo] in a meeting "
meeting_attendee_context_match(input)

input = u" presentation with the [ceo] "
meeting_attendee_context_match(input)

input = u" talk to the [eco] "
meeting_attendee_context_match(input)

from sms_utility_re_event import *
input = u" meet at [al] "
meeting_attendee_context_match(input)
'''
re_meeting_attendee1 = r' '+re_see+r' '\
	+r'('+re_today+r' )*'\
	+r'('+re_the+r' )*'\
	+r'_entity_ '
re_meeting_attendee2 = r' _entity_ '\
	+re_will+r' '\
	+r'('+re_in+r' )*'\
	+r'('+re_the+r' )*'\
	+re_meet+' '
re_meeting_attendee3 = r' _entity_ '\
	+re_will+r' '\
	+re_see+r' '\
	+r'('+re_in+r' )*'\
	+r'('+re_the+r' )*'\
	'_person_ '
re_meeting_attendee4 = r' _entity_ '\
	+r'(in|_puntuation_ s)*'\
	+r'('+re_the+r' )*'\
	+re_meet+' '
re_meeting_attendee5 = r' '+re_meeting_all+r' '\
	+re_of+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '
re_meeting_attendee6 = r' '+re_talk+r' '\
	+re_with+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '
re_meeting_attendee_context = [re_meeting_attendee1,\
	re_meeting_attendee2,\
	re_meeting_attendee3,\
	re_meeting_attendee4,\
	re_meeting_attendee5,\
	re_meeting_attendee6]

def meeting_attendee_context_match(input):
	for pattern in re_meeting_attendee_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
money transfer indicators
'''
re_give = r'(give|giving|send|sent|receive|collect|received|receiving|sending|sent)'
re_pay = r'(pay|payment|transfer|deposit|paying|settle|paid)'
re_money = r'(rent|rental|salary|fee|bill|money|_currency_ _number_|_number_ _currency_|_number_|balance)'
re_account = r'(account|bank account|acc|bank acc|card)'
re_charge = r'(charge|charging|charged)'
re_receive = r'(get|receive|received|receiving|obtain|getting|obtained|obtaining|collect|collecting|collected)'
re_send = r'(give|giving|given|send|sent|sending|deposit|return|forward|forwarding|forwarded)'
re_money_none_number = r'(rent|rental|salary|fee|bill|money|_currency_ _number_|_number_ _currency_|balance)'

'''
from sms_utility_re_event import *

input = u" payment u "
money_transfer_to_receiver(input)

input = u" _number_ _currency_ from _title_ to your bank account "
money_transfer_to_receiver(input)

input = u" you will now receive from _name_ the money "
money_transfer_to_receiver(input)

input = u" _number_ _currency_ right now from me to u "
money_transfer_to_receiver(input)

input = u" pay you the money "
money_transfer_to_receiver(input)

input = u" pay you "
money_transfer_to_receiver(input)
'''
re_money_transfer_to_receiver1 = \
	r' ('+re_pay+r'|'\
	+re_money_none_number+r') '\
	+r'('+re_from+r' '+re_me+r' )*'\
	+re_to+' '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '

re_money_transfer_to_receiver2 = \
	r' '+re_you_will+r' '\
	+r'('+re_today+r' )*'\
	+re_receive+r' '\
	+r'('+re_from+r' '+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_to_receiver3 = \
	r' '+re_money_none_number+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_to+' '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '

re_money_transfer_to_receiver4 = \
	r' ('+re_pay+r'|'\
	+re_send+r') '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_to_receiver5 = \
	r' (pay|paying|paid|deposit) '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '

re_money_transfer_to_receiver6 = \
	r' (transfer|settle) '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '\
	+r'('+re_the+r' )*'\
	+re_money+r' '

re_money_transfer_to_receiver = [\
	re_money_transfer_to_receiver1,\
	re_money_transfer_to_receiver2,\
	re_money_transfer_to_receiver3,\
	re_money_transfer_to_receiver4,\
	re_money_transfer_to_receiver5,\
	re_money_transfer_to_receiver6\
	]

def money_transfer_to_receiver(input):
	for pattern in re_money_transfer_to_receiver:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *

input = u" send money to me "
money_transfer_to_sender(input)

input = u" give me _number_ _currency_ "
money_transfer_to_sender(input)

input = u" payment to me "
money_transfer_to_sender(input)

input = u" money from you to my account "
money_transfer_to_sender(input)
'''
re_money_transfer_to_sender1 = \
	r' ('+re_pay+r'|'\
	+re_money_none_number+r') '\
	+r'('+re_from+r' '+re_me+r' )*'\
	+re_to+' '\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '

re_money_transfer_to_sender2 = \
	r' '+re_i_will+r' '\
	+r'('+re_today+r' )*'\
	+re_receive+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_to_sender3 = \
	r' '+re_money_none_number+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_to+' '\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '

re_money_transfer_to_sender4 = \
	r' ('+re_pay+r'|'\
	+re_send+r') '\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_to_sender5 = \
	r' '+re_pay+r' '\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '

re_money_transfer_to_sender = [\
	re_money_transfer_to_sender1,\
	re_money_transfer_to_sender2,\
	re_money_transfer_to_sender3,\
	re_money_transfer_to_sender4,\
	re_money_transfer_to_sender5\
	]

def money_transfer_to_sender(input):
	for pattern in re_money_transfer_to_sender:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *

input = u" your payment "
money_transfer_from_receiver(input)

input = u" can you make payment "
money_transfer_from_receiver(input)

input = u" pay the money to _name_ from you "
money_transfer_from_receiver(input)

input = u" charge today from u "
money_transfer_from_receiver(input)

input = u" _currency_ _number_ from u "
money_transfer_from_receiver(input)

input = u" u to send _currency_ _number_ "
money_transfer_from_receiver(input)

input = u" please pay "
money_transfer_from_receiver(input)

input = u" pls give me the money "
money_transfer_from_receiver(input)
'''
re_money_transfer_from_receiver1 = \
	r' '+re_you_will+r' '\
	+r'('+re_make+r' )*'\
	+re_pay

re_money_transfer_from_receiver2 = \
	r' ('+re_pay+r'|'\
	+re_money_none_number+r') '\
	+r'('+re_to+r' '+re_me+r' )*'\
	+re_from+' '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '

re_money_transfer_from_receiver3 = \
	r' '+re_you_will+r' '\
	+r'('+re_today+r' )*'\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_from_receiver4 = \
	r' '+re_charge+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') )*'\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '

re_money_transfer_from_receiver5 = \
	r' '+re_money_none_number+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_from+' '\
	+r'(you|u|'+re_your+r' '\
	+re_account+') '

re_money_transfer_from_receiver6 = \
	r' (you|u|'+re_your+r' '\
	+re_account+') '\
	+re_to+r' '\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_from_receiver7 = \
	r' (please|pls) '\
	+re_pay+r' '

re_money_transfer_from_receiver8 = \
	r' (please|pls) '\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_from_receiver9 = \
	r' '+re_your+r' '\
	+re_pay+r' '

re_money_transfer_from_receiver = [\
	re_money_transfer_from_receiver1,\
	re_money_transfer_from_receiver2,\
	re_money_transfer_from_receiver3,\
	re_money_transfer_from_receiver4,\
	re_money_transfer_from_receiver5,\
	re_money_transfer_from_receiver6,\
	re_money_transfer_from_receiver7,\
	re_money_transfer_from_receiver8,\
	re_money_transfer_from_receiver9\
	]

def money_transfer_from_receiver(input):
	for pattern in re_money_transfer_from_receiver:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
from sms_utility_re_event import *

input = u" i will deposit the money to your account "
money_transfer_from_sender(input)

input = u" i will make transfer "
money_transfer_from_sender(input)

input = u" payment to _name_ from my bank account  "
money_transfer_from_sender(input)

input = u" charge from my acc "
money_transfer_from_sender(input)

input = u" charge today from my account  "
money_transfer_from_sender(input)

input = u" receive money to you from me  "
money_transfer_from_sender(input)

input = u" send money to you from me  "
money_transfer_from_sender(input)
'''
re_money_transfer_from_sender1 = \
	r' '+re_i_will+r' '\
	+r'('+re_make+r' )*'\
	+re_pay

re_money_transfer_from_sender2 = \
	r' ('+re_pay+r'|'\
	+re_money_none_number+r') '\
	+r'('+re_to+r' '+re_me+r' )*'\
	+re_from+' '\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '

re_money_transfer_from_sender3 = \
	r' '+re_i_will+r' '\
	+r'('+re_today+r' )*'\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_from_sender4 = \
	r' '+re_charge+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') )*'\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '

re_money_transfer_from_sender5 = \
	r' '+re_money_none_number+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_from+' '\
	+r'(me|us|'+re_my+r' '\
	+re_account+') '

re_money_transfer_from_sender6 = \
	r' (me|us|'+re_my+r' '\
	+re_account+') '\
	+re_to+r' '\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money_none_number+r' '

re_money_transfer_from_sender = [\
	re_money_transfer_from_sender1,\
	re_money_transfer_from_sender2,\
	re_money_transfer_from_sender3,\
	re_money_transfer_from_sender4,\
	re_money_transfer_from_sender5,\
	re_money_transfer_from_sender6\
	]

def money_transfer_from_sender(input):
	for pattern in re_money_transfer_from_sender:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
input = u" pay [100 aed] "
money_transfer_amount_context_match(input)

input = u" payment of [100 aed] "
money_transfer_amount_context_match(input)

input = u" [100 aed] from your bank account "
money_transfer_amount_context_match(input)

input = u" give you [100 aed] "
money_transfer_amount_context_match(input)

input = u" give you [100] min "
money_transfer_amount_context_match(input)

input = u" pay you [100] "
money_transfer_amount_context_match(input)

input = u" give [100 aed] to you "
money_transfer_amount_context_match(input)

input = u" give [100] to you "
money_transfer_amount_context_match(input)
'''
re_money_transfer_amount1 = r' '+re_pay+r' '\
	+r'('+re_to+r' )*'\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	r'_entity_ '
re_money_transfer_amount2 = r' '+re_pay+r' '\
	+r'('+re_of+r' )*'\
	+r'('+re_the+r' )*'\
	r'_entity_ '
re_money_transfer_amount3 = r' _entity_ '\
	+r'('+re_from+r'|'\
	+re_to+r') '\
	+r'('+re_the+r' )*'\
	+re_account+r' '

re_money_transfer_amount4 = r' '+re_give+r' '\
	+r'('+re_to+r' )*'\
	+r'('+re_me+r' )'\
	+r'('+re_the+r' )*'\
	r'_entity_ '
re_money_transfer_amount5 = r' '+re_give+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '\
	+r'('+re_to+r' )'

re_money_transfer_amount = [re_money_transfer_amount1,\
	re_money_transfer_amount2,\
	re_money_transfer_amount3]

re_money_give_amount = [re_money_transfer_amount1,\
	re_money_transfer_amount2,\
	re_money_transfer_amount3,\
	re_money_transfer_amount4,\
	re_money_transfer_amount5]

re_minut = r'(min|mins|minute|mnts|m|s|h|mi|more min|day|days|year|years|month|week|minutes|hour|hours|hr|second|snd)'

def money_transfer_amount_context_match(input):
	'''
	if bool(re.search(r"_entity_ "+re_minut, input)):
		for pattern in re_money_transfer_amount:
			output = extract_entity_by_re(input, \
				pattern,\
				replace_entity_by_wildcard = True,\
				return_none_if_not_matched = True)
			if output is not None:
				return output
	else:
	'''
	for pattern in re_money_give_amount:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
money transfer indicator

input = u" will pay on [sunday] "
money_transfer_time_context_match(input)

input = u" will sent you _number_ on [sunday] "
money_transfer_time_context_match(input)

input = u" on the [monday] i will pay "
money_transfer_time_context_match(input)

input = u" on [sunday] i will give the money "
money_transfer_time_context_match(input)

input = u" on [sunday] _puntuation_ s pay "
money_transfer_time_context_match(input)
'''

re_money_transfer_time1 = r' '+re_pay+r' '\
	+r'('+re_to+r' )*'\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+r'('+re_money+r' )*'\
	+r'('+re_at+r' )*'\
	+r'('+re_the+r' )*'\
	r'_entity_ '
re_money_transfer_time2 = r' '+re_give+r' '\
	+r'('+re_to+r' )*'\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_money+r' '\
	+r'('+re_at+r' )*'\
	+r'('+re_the+r' )*'\
	'_entity_ '
re_money_transfer_time3 = r' '+re_at+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '\
	+r'(('+re_i_will+r'|'+re_you_will+r'|((_name_|_title_|he|she|they) )*'+re_will+') )*'\
	+re_pay+r' '
re_money_transfer_time4 = r' '+re_at+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '\
	+r'(('+re_i_will+r'|'+re_you_will+r'|((_name_|_title_|he|she|they) )*'+re_will+') )*'\
	+re_give+r' '\
	+r'('+re_the+r' )*'\
	+re_money+r' '
re_money_transfer_time5 = r'_entity_ '\
	+r'_puntuation_ s '\
	+re_pay+r' '

re_money_transfer_time = [re_money_transfer_time1,\
	re_money_transfer_time2,\
	re_money_transfer_time3,\
	re_money_transfer_time4,\
	re_money_transfer_time5]

def money_transfer_time_context_match(input):
	for pattern in re_money_transfer_time:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
document delivery
'''

re_document = r'(page|pages|tkt|visa page|cheque book|business card|file|files|pdf|offer|offers|order|orders|id|emirates id|eid|emirate id|ticket|report|reports|reporting|tickets|form|forms|packet|packets|qoutation|cv|resume|scan|copy|copies|driving licence|licence|document|documents|doc|docs|paper|visa|passport|visas|pass port|passports|agreement|contract|papers|photo|pic|picture|pictures|notary|cheque|check|visa page|card|book|books|list|notebook|text book|buill|statement|budget|plan|invoice|receipt|notification|notify|notice)'
re_need = r'(want|wanting|need|needed|wants|wanted|require|required|requiring|request|requesting|requested|ask for|asked for|asking for|call for|called for|calling for|look for|looking for)'

'''
document_transfer_to_sender
'''

re_document_transfer_to_sender1 = \
	r' ('+re_document+r') '\
	+r'('+re_from+r' '+re_me+r' )*'\
	+re_to+' '\
	+r'('+re_me+' and )*'\
	+r'(me|us) '

re_document_transfer_to_sender2 = \
	r' '+re_i_will+r' '\
	+r'('+re_today+r' )*'\
	+r'('+re_receive\
	+r'|'+re_need+r') '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_to_sender3 = \
	r' '+re_document+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_to+' '\
	+r'('+re_me+' and )*'\
	+r'(me|us) '

re_document_transfer_to_sender4 = \
	r' ('\
	+re_send+r') '\
	+r'('+re_me+' and )*'\
	+r'(me|us) '\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_to_sender5 = \
	r' '+re_document+r' '\
	+re_to+r' '\
	+r'('+re_me+r' and )* '\
	+r'(me|us|my) '

re_document_transfer_to_sender = [\
	re_document_transfer_to_sender1,\
	re_document_transfer_to_sender2,\
	re_document_transfer_to_sender3,\
	re_document_transfer_to_sender4,\
	re_document_transfer_to_sender5\
	]

def document_transfer_to_sender(input):
	for pattern in re_document_transfer_to_sender:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
document_trassfer_to_email

usage:

input = u' to this mail address _entity_ '
print(document_transfer_to_email(input))
'''
re_email = r'(mail address|email ad|bank email id|id|email|email id|personal email|email address|email add|mail)'

re_document_transfer_to_email1 = \
	r' '+re_to+r' '\
	+r'('+re_my+r'|'+re_your+r'|'+re_the+r' )*'\
	+r'('+re_email+r' )*'\
	+r'(please )*'\
	+r'(_puntuation_ )*'\
	+r'(_email_ )*'\
	+r'_entity_ '

re_document_transfer_to_email2 = \
	r' '+re_document+r' '\
	+re_to+r' '\
	+r'(_puntuation_ )*'\
	+r'(_email_ )*'\
	+r'_entity_ '

re_document_transfer_to_email = [\
	re_document_transfer_to_email1,\
	re_document_transfer_to_email2
	]

def document_transfer_to_email(input):
	for pattern in re_document_transfer_to_email:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
input = u' emirates id copies to _entity_ '
document_transfer_to_email(input)
'''

'''
document_transfer_from_receiver
'''

re_document_transfer_from_receiver1 = \
	r' '+re_please+r' '\
	+re_send+r' '\
	+r'('+re_my+r'|'+re_your+r'|'+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_from_receiver2 = \
	r' '+re_you_will+r' '\
	+r'('+re_today+r' )*'\
	+re_send+r' '\
	r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_from_receiver3 = \
	r' ('+re_send+r'|'+re_need+r') '\
	+re_your+r' '\
	+re_document+r' '

re_document_transfer_from_receiver4 = \
	r' '+re_document+r' '\
	+r'('+re_to+r' '+re_me+r' )*'\
	+re_from+' '\
	+r'(you|u|'+re_your+r') '

re_document_transfer_from_receiver5 = \
	r' '+re_i_will+r' '\
	+re_receive+r' '\
	+re_your+r' '\
	+re_document+r' '

re_document_transfer_from_receiver = [\
	re_document_transfer_from_receiver1,\
	re_document_transfer_from_receiver2,\
	re_document_transfer_from_receiver3,\
	re_document_transfer_from_receiver4,\
	re_document_transfer_from_receiver5\
	]

def document_transfer_from_receiver(input):
	for pattern in re_document_transfer_from_receiver:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input


'''
document_transfer_time
'''

re_document_transfer_time1 = r' '+re_give+r' '\
	+r'('+re_to+r' )*'\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '\
	+r'('+re_at+r' )*'\
	+r'('+re_the+r' )*'\
	'_entity_ '

re_document_transfer_time2 = r' '+re_at+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '\
	+r'(('+re_i_will+r'|'+re_you_will+r'|((_name_|_title_|he|she|they) )*'+re_will+') )*'\
	+re_give+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_time = [\
	re_document_transfer_time1,\
	re_document_transfer_time2\
	]

def document_transfer_time_context_match(input):
	for pattern in re_document_transfer_time:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
document_transfer_document_context
'''

re_share = r'(share|shared|sharing|)'
re_bring = r'(bring|brought|take|toke|taken)'

re_document_transfer_document_context1 = \
	r' ('+re_send+r'|'\
	+re_give+r'|'\
	+re_need+r'|'\
	+re_share+r'|'\
	+re_bring+r'|'\
	+re_receive+r') '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+r'_entity_ '

re_document_transfer_document_context2 = \
	r' _entity_ '\
	+r'('+re_from+r'|'\
	+re_to+r') '\
	+re_me+r' '

re_document_transfer_document_context = [\
	re_document_transfer_document_context1,\
	re_document_transfer_document_context2\
	]

def document_transfer_document_context(input):
	for pattern in re_document_transfer_document_context:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
document transfer from sender
'''

re_document_transfer_from_sender1 = \
	r' '+re_i_will+r' '\
	+r'('+re_today+r' )*'\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_from_sender2 = \
	r' '+re_document+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_from+' '\
	+r'(me|us|'+re_my+') '

re_document_transfer_from_sender3 = \
	r' (me|us) '\
	+re_to+r' '\
	+re_send+r' '\
	+r'('+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_from_sender = [\
	re_document_transfer_from_sender1,\
	re_document_transfer_from_sender2,\
	re_document_transfer_from_sender3\
	]

def document_transfer_from_sender(input):
	for pattern in re_document_transfer_from_sender:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
document transfer to receiver
'''

re_document_transfer_to_receiver1 = \
	r' ('+re_document+r') '\
	+r'('+re_from+r' '+re_me+r' )*'\
	+re_to+' '\
	+r'(you|u|'+re_your+') '

re_document_transfer_to_receiver2 = \
	r' '+re_you_will+r' '\
	+r'('+re_today+r' )*'\
	+re_receive+r' '\
	+r'('+re_from+r' '+re_me+r' )*'\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_to_receiver3 = \
	r' '+re_document+r' '\
	+r'('+re_today+r' )*'\
	+r'(('+re_from+r'|'\
	+re_to+r') '+re_me+r' )*'\
	+re_to+' '\
	+r'(you|u|'+re_your+') '

re_document_transfer_to_receiver4 = \
	r' ('+re_send+r') '\
	+r'(you|u) '\
	+r'('+re_the+r' )*'\
	+re_document+r' '

re_document_transfer_to_receiver = [\
	re_document_transfer_to_receiver1,\
	re_document_transfer_to_receiver2,\
	re_document_transfer_to_receiver3,\
	re_document_transfer_to_receiver4\
	]

def document_transfer_to_receiver(input):
	for pattern in re_document_transfer_to_receiver:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input
###########sms_utility_re_event.py###########
