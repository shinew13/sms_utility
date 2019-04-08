import re

'''
input = u"<http://rdf.freebase.com/ns/m/0q8d00b>"
link2entity_id(input)
'''

def link2entity_id(input):
	try:
		entity_id = re.search(r'\/m\/[^ ]+\>', input).group()
		entity_id = re.sub(r'^|\>$', '', entity_id)
		entity_id = entity_id.strip()
		return entity_id
	except:
		return None

def entity_text2processed(input):
	try:
		input = input.lower()
		input = input.split('(')[0]
		input = re.sub('[^a-z0-9]+', ' ', input)
		input = input.strip()
		return input
	except:
		return None
