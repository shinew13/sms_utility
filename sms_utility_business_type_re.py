##############sms_utility_business_type_re##############
import re

'''
usage:
input = 'QTR Airways'
id2business_type(input)
'''
def id2business_type(input):
	try:
		input = input.lower().strip()
		if bool(re.search('(emiratesnbd|rakbank|adcbalert|nbad|adib|xchange|bank|exch|hsbc|([^a-z]|^)(adcb|dib)([^a-z]|$))', \
			input)):
			return 'finance'
		if bool(re.search('(clinic|medical|hosp|([^a-z]|^)(nmc|ahs|stanchart)([^a-z]|$))',\
			input)):
			return 'clinic'
		if bool(re.search('(school|schol|sch([^a-z]|$)|college)',\
			input)):
			return 'education'
		if bool(re.search('(police|gov([^a-z]|$)|([^a-z]|^)(addc|rta)([^a-z]|$))',\
			input)):
			return 'government'
		if bool(re.search('([^a-z]|^)(post|ups|dhl)([^a-z]|$)',\
			input)):
			return 'express'
		if bool(re.search('wifi',\
			input)):
			return 'it'
		if bool(re.search('([^a-z]|^)(du|etisalat)([^a-z]|$)',\
			input)):
			return 'telecom'
		if bool(re.search('(news|uae barq)',\
			input)):
			return 'media'
		if bool(re.search('(insur)',\
			input)):
			return 'insurance'
		if bool(re.search('(mall|([^s]|^)mart|([^a-z]|^)gold([^a-z]|$))',\
			input)):
			return 'retailer'
		if bool(re.search('(pray)',\
			input)):
			return 'religion'
		if bool(re.search('(hotel)',\
			input)):
			return 'hotel'
		if bool(re.search('(([^a-z]|^)(etihad)([^a-z]|$)|flightinfo|airway|taxi)',\
			input)):
			return 'transportation'
	except:
		return None

'''
usage:

input = 'Dear parent, your child has been abscent today.'
text2business_type(input)
'''
def text2business_type(input):
	try:
		input = input.strip().lower()
		if bool(re.search(\
			'dear(\s+)parent|your(\s+)child|tuition(\s+)fee|dear(\s)student([^a-z]|$)', \
			input)):
			return 'education'
		if bool(re.search('dear patient|dear pt([^a-z]|$)', \
			input))\
			or (\
			bool(re.search('medical|radiology|clinic|dental|physcian|surgery|dr\.|healing center', input))\
			and \
			bool(re.search('appointment|book|remind|confirm', input))):
			return 'clinic'
		if bool(re.search('([^a-z]|^)(salary|debit|credit|transaction|withdrawn|loan|purchase|deposit|spen(t|d))([^a-z]|$)', input)) \
			and bool(re.search('([^a-z]|^)(bank|finance|avail|atm|account|a/c|a\\c|(available|avl\.)(\s+)(balance|limit))([^a-z]|$)', input)):
			return 'finance'
		if bool(re.search('\.gov\.ae', input)):
			return 'government'
	except:
		return None
##############sms_utility_business_type_re##############
