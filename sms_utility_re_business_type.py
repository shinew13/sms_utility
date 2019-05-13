##############sms_utility_re_business_type.py##############
import re

re_telecom = '(^1204$|etisalat|([^a-z]|^)(du|from uae|omantel)([^a-z]|$))'.lower()
re_finance = '(^(971500000000|fin house|DFM)$|stanchart|WstrnUnion|MENACORP|ALFALAH EXC|emiratesnbd|rakbank|adcbalert|nbad|adib|xchange|bank|exch|hsbc|([^a-z]|^)(cbi|adcb|dib|fgb|ei sms|cbd|BOS)([^a-z]|$))'.lower()
re_clinic = '(3338|IBNNAFEESMC|magrabi|clinic|medical|hosp|([^a-z]|^)(nmc|ahs|saudigerman|daralshifaa|dha)([^a-z]|$))'.lower()
re_education = '(PISMS|DXBChamber|SRSDUBAI|SajayaGirls|velocitysbt|school|schol|sch([^a-z]|$)|college|^(ens|ADU)$|([^a-z]|^)(hbmsu)([^a-z]|$)|^EDI$)'.lower()
re_public_service = '(Khidmah|AAM RESALAH|addc|ADCP|DHAID\-MUN|MOCCAE|shjplanning|salik|police|gov([^a-z]|$)|([^a-z]|^)(DMAT|dnrd|moccae|addc|rta|moi|adec|emiratesid|aadc|dewa|uae\_traffic|saaed|EVG)([^a-z]|$)|^(ded|evg|DDC|DGW)$)'.lower()
re_express = '(([^a-z]|^)(post|ups|dhl|emrtspost)([^a-z]|$))'.lower()
re_IT = '(wifi|^(1499)$)'.lower()
re_media = '(([^a-z]|^)(events|news|uae barq|ecssr|barq)([^a-z]|$))'.lower()
re_insurance = '(insur|([^a-z]|^)daman([^a-z]|$))'.lower()
re_marketing = '(^(6269|3085|fnc|sms|emc)$|Afrina|NAILS SYMPH|971502955504|REVOLUTION|971506569205|971558597010|Najo_Secret|SAXCLUB|Parisgallry|CHEEKYMNKYS|netotrade|sephora|homecentre|mall([^a-z]|$)|([^s]|^)mart|([^a-z]|^)(michaelkors|boutique|gold|big ticket|alnadwa|greenvalley|FitnesFirst|ECCO|NOSE|Ford)([^a-z]|$))'.lower()
re_transport = '(([^a-z]|^)(etihad|air india)([^a-z]|$)|flightinfo|airway|taxi)'.lower()
re_hotel = '(ALANFAL|hotel|jumeirah|^SMS$)'.lower()
re_private_service = '(hr\.sharjah|SAMSUNG)'.lower()
re_multiple = '(^(8080|2474|3579|4567)$|([^a-z]|^)(1012|jobalert)([^a-z]|$))'.lower()
re_entertainment = '(^(OSN|1151)$|Dubainight|eLifeTV|museum(s)?|zoo)'.lower()
re_app = '(google|facebook|souq|twitter|instagram|whatsapp|skype|uber)'.lower() 

'''
usage:
input = '1204'
id2business_type(input)
'''
def id2business_type(input):
	try:
		input = input.lower().strip()
		if bool(re.search('(emiratesnbd|rakbank|adcbalert|nbad|adib|xchange|bank|exch|hsbc|([^a-z]|^)(adcb|dib)([^a-z]|$))', \
			input)) \
			or bool(re.search(re_finance, input)):
			return 'finance'
		if bool(re.search('(clinic|medical|hosp|([^a-z]|^)(nmc|ahs|stanchart)([^a-z]|$))',\
			input)) \
			or bool(re.search(re_clinic, input)):
			return 'clinic'
		if bool(re.search('(school|schol|sch([^a-z]|$)|college)',\
			input)) \
			or bool(re.search(re_education, input)):
			return 'education'
		if bool(re.search('(police|gov([^a-z]|$)|([^a-z]|^)(addc|rta)([^a-z]|$))',\
			input)) \
			or bool(re.search(re_public_service, input)):
			return 'government'
		if bool(re.search('([^a-z]|^)(post|ups|dhl)([^a-z]|$)',\
			input)) \
			or bool(re.search(re_express, input)):
			return 'express'
		if bool(re.search('wifi',\
			input)) \
			or bool(re.search(re_IT, input)):
			return 'it'
		if bool(re.search('([^a-z]|^)(du|etisalat)([^a-z]|$)',\
			input)) \
			or bool(re.search(re_telecom, input)):
			return 'telecom'
		if bool(re.search('(news|uae barq)',\
			input)) \
			or bool(re.search(re_media, input)):
			return 'media'
		if bool(re.search('(insur)',\
			input)) \
			or bool(re.search(re_insurance, input)):
			return 'insurance'
		if bool(re.search('(mall|([^s]|^)mart|([^a-z]|^)gold([^a-z]|$))',\
			input)) \
			or bool(re.search(re_marketing, input)):
			return 'retailer'
		if bool(re.search('(pray)',\
			input)):
			return 'religion'
		if bool(re.search('(hotel)',\
			input)) \
			or bool(re.search(re_hotel, input)):
			return 'hotel'
		if bool(re.search('(([^a-z]|^)(etihad)([^a-z]|$)|flightinfo|airway|taxi)',\
			input)) \
			or bool(re.search(re_transport, input)):
			return 'transportation'
		if bool(re.search(re_app, input)):
			return 'app'
		if bool(re.search(re_entertainment, input)):
			return 'entertainment'
		if bool(re.search(re_multiple, input)):
			return 'multiple_business'
		if bool(re.search(re_private_service, input)):
			return 'service'
	except:
		return None

'''
usage:

input = 'Dear parent, your child has been abscent today.'
input = u"""
There was a purchase transaction of AED  373.75 on your Card XXXX7983 at SPINNEYS                 SHARJAH      AE on 12/12/2016 1:09:13 AM. Total available balance is AED 25873.29.
"""
text2business_type(input)
'''
def text2business_type(input):
	try:
		input = input.strip().lower()
		if bool(re.search(\
			r'dear(\s+)parent|your(\s+)child|tuition(\s+)fee|dear(\s)student([^a-z]|$)', \
			input)):
			return 'education'
		if bool(re.search(r'dear patient|dear pt([^a-z]|$)', \
			input))\
			or (\
			bool(re.search(r'medical|radiology|clinic|dental|physcian|surgery|dr\.|healing center', input))\
			and \
			bool(re.search(r'appointment|book|remind|confirm', input))):
			return 'clinic'
		if bool(re.search(r'([^a-z]|^)(salary|debit|credit|transaction|withdrawn|loan|purchase|deposit|spen(t|d))([^a-z]|$)', input)) \
			and bool(re.search(r'([^a-z]|^)(bank|finance|avail|atm|account|a\/c|a\\c|((available|avl\.)(\s+)(balance|limit)))([^a-z]|$)', input)):
			return 'finance'
		if bool(re.search('\.gov\.ae', input)):
			return 'government'
	except:
		return None
##############sms_utility_re_business_type.py##############
