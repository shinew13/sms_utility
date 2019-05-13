##############sms_utility_re_profile.py##############
import re
from sms_utility_re import *
from sms_utility_re_event import *

re_i = "(i|we)"
re_you = "(you|u)"
re_my = '(my|our|mine|mi)'
re_your = '(your|ur)'

re_will = "(look[^\w]+forward[^\w]+to|will|will[^\w]+be|ll|can|may|could|(am|m|are|r|be)|(am|m|are|r|be)[^\w]+going[^\w]+to|shall|must|(have|has|had)([^\w]+to)?|want[^\w]+to|need)"
re_be = '(am|\'m|m|are|r|be|is|was|were|been|has been|have been|will be|has being|have being)'

re_in = "(back[^\w]+)?(from|to|in|on|with|via|toward|for|into|onto|against|by|upon|of|about)"

re_dear = "(good|bad|excellent|busy|rich|fucking|last|dear|dearest|lovely|little|sweet|handsome|beautiful|only|best|valued|wonderful|the([^\w]+)?best|real|big|precious|small)"
re_adj = "(major|right|old|certain|national|hard|high|political|good|human|best|late|different|federal|able|young|long|better|only|other|black|low|easy|international|white|local|public|sure|real|full|big|little|free|possible|early|important|new|strong|true|special|recent|great|clear|large|bad|economic|social|small|military|whole)"
re_adj = '('+re_dear+'|'+re_adj+')'
re_a_an_the = '(a|an|the|one|[a-z]+\'s|my|your|his|her|their|our|[0-9]+)'

re_hello = '((good|gd|gud|happy|asalam|salaam)([^\w]+)?(luck|afternoon|afternon|mrg|o alekum|walikum|day|birthday|morning|am|evng|eve|moring|night|nite|evening|new([^\w]+)?year)|hw([^\w]+)?r([^\w]+)?u|how([^\w]+)?are([^\w]+)?you|how([^\w]+)?r([^\w]+)?u|dear|morning|hello|hi|hey|salam|salaams|morning|gudmg|evening|hellow|goodmorning|sorry)'
re_missyou = '((love|luv|miss|kiss|thank|bless)([^\w]+)?(you|u|u2)([^\w]+so[^\w]+mch)?|im([^\w]+)?sorry|i\'m[^\w]+sorry|i[^\w]+am[^\w]+sorry|i[^\w]+m[^\w]+sorry|good([^\w]+)?luck|ok|okey|sure|tanx|thanks|you are welcome)'
re_regard = '(regard|rgd|regards)'

re_i_am = '(this[^\w]+is|i[^\w]+am|i\'m|im|my[^\w]+name[^\w]+is|mine[^\w]+name[^\w]+is|my[^\w]+name)'
re_you_are = '(you|u)[^\w]+(are|r)'
re_talk_beginning = '(sorry|i|you|they|it|that|this|the|u|your|ur|my|our|we|their|how|what|when|where|who|sure|ok|yes|are([^\w]+)?you|are([^\w]+)?u|can i|can([^\w]+)?we|im|please|there|today|tomorrow|its|can([^\w]+)?you|pls)'

re_have_other = "(having|have|had|obtain|get|hold|need|start|finish)"
re_have = "(obtain|bring|corner|parlay|cut|snag|buy([^\w]+)?off|rack([^\w]+)?up|return|get|bear|snowball|compass|reap|realize|possess|earn|teem([^\w]+)?with|build([^\w]+)?up|yield|bag|grab|enjoy|booty|get([^\w]+)?hold([^\w]+)?of|catching|haul|pick([^\w]+)?up|extract|accomplish|cash([^\w]+)?in([^\w]+)?on|take([^\w]+)?in|latch([^\w]+)?on([^\w]+)?to|access|make([^\w]+)?a([^\w]+)?killing|score|sit([^\w]+)?on|net|hustle|effect|capture|receipts|cop|receive|buy([^\w]+)?into|keep|have([^\w]+)?in([^\w]+)?hand|evoke|retain|own|secure|revenue|win|lock([^\w]+)?up|come([^\w]+)?by|carry|buy([^\w]+)?out|make([^\w]+)?a([^\w]+)?buy|glean|occupy|returns|snap([^\w]+)?up|acquire|part|gain|catch|hold|pull|include|get([^\w]+)?hands([^\w]+)?on|fetch|clean([^\w]+)?up|share|accept|elicit|attain|have|chalk([^\w]+)?up|proceeds|hog|make|admit|wangle|takings|take|holding|gate|educe|draw|annex|procure|extort|land|clear|bring([^\w]+)?in|inherit|succeed([^\w]+)?to)(ing|ed|d)?"
re_have = '('+re_have+'|'+re_have_other+')'

re_verbs = "(would|help|give|feel|move|play|need|say|have|go|seem|find|try|use|let|want|make|show|will|should|start|live|call|take|might|tell|be|begin|run|do|get|may|hear|know|ask|come|look|like|could|work|put|see|keep|leave|turn|can|become|think|talk|mean)"
re_very = r'(very|so+|fucking)'

re_negative_status = r'(sick|ill|bad|terrible|not good|sarcastic|narcissistic|heavy|bitter|obnoxious|foolish|disgruntled|hurtful|disgusted|irritated|nasty|oppressive|anxious|horrified|annoyed|resentful|sick|guilty|downcast|overbearing|angry|sadistic|moody|cold|pessimistic|sad|chilly|thirsty|nervous|tired|weak|evil|terrible|dreadful|dirty|ugly|dreary|awful|stupid|dumb|aggravated|miserable|mad|grumpy|tearful|selfish|depressed|sour)'
re_positive_status = r'(good|wanderful|exellent|not bad|great|interesting|lovely|best|health|fresh|open|animated|devoted|loving|sympathetic|encouraging|supportive|kind|clever|warm|hopeful|happy|amazed|free|wonderful|clean|strong|beautiful|excited|great|bold|gorgeous|attractive|better|agreeable|brave|calm|delightful|festive|gentle|jolly|proud|shy|optimistic|cheerful|upbeat|joyful|sweet|serene|respectful|appreciative|contented|jubilant)'

re_positive_act = r'(love|loves|loving|like|likes|care|cares|respect|glorify|crazy about|crazy for|crazy over|in love with|pray|bless|glorify|praise|thank|honor|kiss|miss|admire|agree|support|trust|believe|wish|enjoy|respect|value)'
re_negative_act = r'(hate|hates|hating|worry|worrying|worries|mad about|doubt|afraid of|fear|fuck|fucked|fuk|loss|lost|angry|disagree|laugh at|against)'

re_dr = r'(dr|mr|mrs|ms|prof|miss)'
'''
from sms_utility_re_profile import *
input = ' [jim] is a awful person '
text_entity2text_entity_negative(input)

input = ' i worry about [jim] '
text_entity2text_entity_negative(input)
'''
re_patterns_negative = [\
	r' _entity_ '\
	+r'('+re_be+' )'\
	+'('+re_a_an_the+' )*'\
	+'('+re_very+' )*'\
	+re_negative_status\
	+r' ',\
	r' _entity_ '\
	+r'('+re_be+' )'\
	+r'(not )'\
	+'('+re_a_an_the+' )*'\
	+'('+re_very+' )*'\
	+re_positive_status\
	+r' ',\
	r' '+re_negative_act+r' '\
	+r'('+re_in+r' )*'\
	+'_entity_ ']
def text_entity2text_entity_negative(input):
	for pattern in re_patterns_negative:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input


'''
from sms_utility_re_profile import *
input = ' [jim] is not a bad person '
text_entity2text_entity_positive(input)

input = ' i love [jim] he is ok '
text_entity2text_entity_positive(input)
'''
re_patterns_positive = [\
	r' _entity_ '\
	+r'('+re_be+' )'\
	+'('+re_a_an_the+' )*'\
	+'('+re_very+' )*'\
	+re_positive_status\
	+r' ',\
	r' _entity_ '\
	+r'('+re_be+' )'\
	+r'(not )'\
	+'('+re_a_an_the+' )*'\
	+'('+re_very+' )*'\
	+re_negative_status\
	+r' ',\
	r' '+re_positive_act+r' '\
	+r'('+re_in+r' )*'\
	+r'_entity_ ']
def text_entity2text_entity_positive(input):
	for pattern in re_patterns_positive:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
extract sener name context

usage:
from sms_utility_re_profile import *

text_entity2text_sender_name_context(\
	' this is _entity_ _puntuation_ i ')

text_entity2text_sender_name_context(' [jim] here from china ')
text_entity2text_sender_name_context(' this is [jim] here ')

text_entity2text_sender_name_context(\
	' this is _name_ _puntuation_ s _title_ _puntuation_ _entity_ ')
'''
re_this_is = r'(this is|i am|im|i _puntuation_ m|my name is)'
sender_name_context1 = 	\
	r' (regards|regard|rgd) '\
	+r'(_title_ )*(_puntuation_ )*_entity_ (_puntuation_ )*_end_ '
sender_name_context2 = 	\
	r' _entity_ here from '
sender_name_context3 = 	\
	r' '+re_this_is+r' '\
	+r'(_title_ )*_entity_ '\
	+r'(here|from|of|_end_) '
sender_name_context4 = \
	r' '+re_this_is+r' '\
	+r'(_name_ _puntuation_ s _title_ (_puntuation_ )*)(_title_ )*_entity_ '
sender_name_context5 = 	\
	r' '+re_this_is+r' '\
	+r'(_title_ )*_entity_ '\
	+r'(_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_end_) '

re_sender_name = [\
	sender_name_context1,\
	sender_name_context2,\
	sender_name_context3,\
	sender_name_context4,\
	sender_name_context5]
def text_entity2text_sender_name_context(input):
	for pattern in re_sender_name:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
extract the indicator of context of receiver is sender's role

usage:

from sms_utility_re_profile import *

input = u'  _start_ our request for tomorrow trailer for _name_ to be cancelled _puntuation_ as don _puntuation_ t receive the empty _name_ from offshore _puntuation_ thanks _puntuation_ [anas] _end_  '

input = u" _start_ sorry _entity_ i "
receiver_is_senders_entity(input)

input = u" _start_ my dear [jim] how are you "
receiver_is_senders_entity(input)

input = u" hello [jim] i will come "
receiver_is_senders_entity(input)

input = u" good thank you [jim] _end_ "
receiver_is_senders_entity(input)

input = u" you are the best [father] hahaha "
receiver_is_senders_entity(input)

input = u" thanks [jim] _end_ "
receiver_is_senders_entity(input)

input = u" _start_ dear dr _puntuation_ [brexendorff] _puntuation_ mr _puntuation_ "
receiver_is_senders_entity(input)
'''

re_receiver_is_senders_entity1 = \
	' _start_ ('+re_my+' )?'\
	+'('+re_dear+' )?'\
	+'(_title_ )*'\
	+'(_puntuation_ )*'\
	+'_entity_ '\
	+'(_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_end_) '

re_receiver_is_senders_entity2 = \
	' ('+re_hello+') '\
	+'(_puntuation_ )*'\
	+'('+re_my+' )?('+re_dear+' )?'\
	+'_entity_ (_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_puntuation_) '

re_receiver_is_senders_entity3 = \
	' ('+re_missyou+') '\
	+'(_puntuation_ )*'\
	+'('+re_my+' )?('+re_dear+' )?'\
	+'_entity_ (_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_puntuation_) '

re_receiver_is_senders_entity4 = \
	' '+re_you_are+' '\
	+'('+re_my+'|the best|best) '\
	+'('+re_dear+' )*'\
	+'_entity_ '

re_receiver_is_senders_entity_all = [\
	re_receiver_is_senders_entity1,\
	re_receiver_is_senders_entity2,\
	re_receiver_is_senders_entity3,\
	re_receiver_is_senders_entity4\
	]

def receiver_is_senders_entity(input):
	for pattern in re_receiver_is_senders_entity_all:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
receiver title

usage:

input = u" _start hi _entity_ _name_ how are you _end_ "
text_entity2text_receiver_title_indicator(input)
'''
re_receiver_title_indicator1 = \
	' _start_ ('+re_my+' )?'\
	+'('+re_dear+' )?'\
	+'_entity_ '\
	+'(_puntuation_ )*'\
	+'(_name_ )*'\
	+'(_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_end_) '

re_receiver_title_indicator2 = \
	' ('+re_hello+') '\
	+'(_puntuation_ )*'\
	+'('+re_my+' )?('+re_dear+' )?'\
	+'_entity_ '\
	+'(_puntuation_ )*'\
	+'(_name_ )*'\
	+'(_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_puntuation_) '

re_receiver_title_indicator3 = \
	' ('+re_missyou+') '\
	+'(_puntuation_ )*'\
	+'('+re_my+' )?('+re_dear+' )?'\
	+'_entity_ '\
	+'(_puntuation_ )*'\
	+'(_name_ )*'\
	+'(_puntuation_ )*'\
	+'('+re_talk_beginning+'|'\
	+re_hello+'|'\
	+re_missyou+'|'\
	+'_puntuation_) '

re_receiver_title_indicator_all = [\
	re_receiver_title_indicator1,\
	re_receiver_title_indicator2,\
	re_receiver_title_indicator3,\
	re_receiver_is_senders_entity4\
	]

def text_entity2text_receiver_title_indicator(input):
	for pattern in re_receiver_title_indicator_all:
		output = extract_entity_by_re(input, \
			pattern,\
			replace_entity_by_wildcard = True,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
re_title = '(boss|student)'
receiver_title_match(re_title, 'boss, good morning')
receiver_title_match(re_title, 'hi, my lovely students')
receiver_title_match(re_title, 'you are a good boss')
'''
def receiver_title_match(re_title, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:		
		context = re.search(\
			'^([^\w]+)?'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_title+'(s|es)?'\
			+'[^\w]+'\
			+'('+re_talk_beginning+'|'\
			+re_hello+'|'\
			+re_missyou+')'\
			+'([^\w]|$)',\
			input).group()
	except:
		pass
	try:		
		context = re.search(\
			'([^\w]|^)'\
			+'('+re_hello+'|'\
			+re_missyou+')'+'[^\w]+'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_title+'(s|es)?'\
			+'([^\w]|$)',\
			input).group()
	except:	
		pass
	try:		
		context = re.search(\
			'(^|[^\w])'+re_you_are+'[^\w]+'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_title+'(s|es)?'\
			+'($|[^\w])',\
			input).group()
	except:
		pass
	return re.sub('(^[^\w]+|[^\w]+$)',\
		'', context).strip()

####
'''
re_title = '(boss|student|dr)'
sender_title_match(re_title, 'i am her students')
sender_title_match(re_title, 'hi, my lovely boss')
sender_title_match(re_title, 'you are a good boss')
sender_title_match(re_title, 'This is Dr Wang')
'''
def sender_title_match(re_title, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search(\
			'([^\w]|^)'+re_i_am+'[^\w]+'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_title+'(s|es)?'\
			+'([^\w]|$)',\
			input).group()
	except:
		pass
	try:
		context = re.search(\
			'([^\w]|^)'+re_regard+'[^\w]+'\
			+re_title+'(s|es)?'\
			+'[^\w]+[a-z]{3,}([^\w]+)?$',\
			input).group()
	except:
		pass
	return re.sub('(^[^\w]+|[^\w]+$)',\
		'', context).strip()


'''
re_verb_other = "(finish)"
re_regularverbs = "(befriend|consider|trickle|dance|scratch|rob|invent|protest|coach|battle|follow|hate|milk|row|extoll|depend|calculate|unpack|flash|scold|tickle|charge|moor|swoop|skip|sputter|smile|dislike|include|sway|fax|garden|rhyme|stipulate|wave|toss|mourn|decide|bleach|cook|span|trouble|wipe|arrange|exaggerate|die|marry|shock|list|try|race|vanquish|enjoy|chew|work|force|pledge|fence|sigh|direct|chomp|sign|jump|fold|burnish|enjoin|bake|admire|dial|curse|appear|cover|wreck|rot|squeeze|whimper|melt|crush|rub|suspect|infuse|reply|appeal|exercise|satisfy|wail|punch|water|explore|entertain|decipher|shriek|change|wait|box|search|voice|theorize|boast|auction|chant|screech|bow|harass|yield|smoke|permit|bob|ruin|pause|love|divide|stray|manage|cross([^\w]+)?examine|loosen|replace|peer|post|plow|proceed|snoop|injure|paste|trounce|exhort|irritate|implore|live|doubt|call|recommend|encode|wed|fret|type|breathe|flap|relax|afford|impress|reign|warn|excuse|drown|hurry|scribble|savor|annoy|grill|join|recall|challenge|pretend|pour|reproduce|remain|drill|arrive|fetch|claim|compare|tap|want|taunt|predict|lock|chip|share|accept|stroke|caution|slip|sense|train|allege|occur|guarantee|sip|end|memorize|provide|dress|travel|comfort|damage|pine|delay|gnaw|worry|cajole|reject|answer|stir|sin|plant|mar|attend|watch|dive|use|scoff|sneak|bawl|reflect|produce|waver|gasp|man|refuse|criticize|attempt|remember|whistle|amuse|counter|appreciate|greet|inform|switch|maintain|jail|scoot|deceive|enter|offend|operate|order|talk|whip|recite|pester|help|pant|serve|consent|peck|move|tempt|trade|sob|program|ogle|suffer|adopt|thank|fit|acknowledge|pray|fix|hail|fade|carve|mail|fool|crash|hop|smash|nod|dam|practice|bat|introduce|dock|bang|spill|sack|kiss|interrupt|scatter|blink|complain|possess|name|rant|edit|drop|explode|merge|trap|pinch|found|hijack|submerge|scorch|skate|harm|bump|fish|strip|reduce|vote|unlock|connect|measure|happen|wander|surprise|contend|flower|concur|stitch|miss|confess|testify|precede|increase|sparkle|encourage|mate|print|lecture|cause|correct|disclose|grease|profess|spot|forgive|release|bestow|imagine|ask|embarrass|cough|care|perform|agree|omit|skateboard|turn|place|swing|blush|scare|blind|shave|suspend|prevent|relate|number|hoot|echo|hook|instruct|long|carry|radiate|jabber|warm|regret|moan|guess|quilt|paint|divorce|tow|attach|attack|shiver|storm|inflate|boil|listen|hug|thaw|pump|hum|writhe|park|stress|snatch|vouch|part|attract|copy|crawl|postulate|rebuff|nail|translate|elope|lament|double|stammer|shampoo|crave|matter|store|iron|rate|declare|steer|lick|clip|strengthen|retort|pass|mine|slap|murder|stash|dictate|need|pry|unfasten|invite|screw|ponder|groan|soak|wink|offer|divulge|note|mix|tick|pop|punish|wonder|heal|slow|play|prick|allow|trace|gild|quote|object|reach|educate|evaporate|yawn|barrage|plan|crochet|multiply|coil|deny|interject|covet|gather|flow|face|digress|clean|thunder|weigh|scream|marvel|shop|urge|bomb|inspire|barter|cheat|retire|dupe|volunteer|paddle|utter|fear|debate|trot|toast|wriggle|envy|grunt|tire|explain|jolt|jam|sprout|mend|announce|stain|jab|hope|handle|babble|lighten|rock|stop|strut|beam|state|strum|report|dye|gel|reveal|earn|bar|cry|borrow|remove|proclaim|stuff|gush|contain|ban|kill|grab|enchant|preach|dump|expel|frame|reiterate|beg|trick|bare|seal|fail|close|bark|hammer|concern|yodel|blurt|equivocate|sail|please|label|favor|mug|hiss|juggle|preserve|notice|avow|venture|extend|grumble|deliver|interfere|spray|concentrate|spare|spoil|jog|broil|spark|comb|vanish|improve|exclaim|stun|last|glide|license|joke|decay|emit|assure|admit|succeed|brag|settle|buzz|argue|approve|comment|suggest|conclude|color|confide|loan|insist|walk|whisper|laugh|rave|trust|mumble|raise|arrest|stamp|wobble|shout|concede|mark|gaze|treat|interest|recognize|threaten|fry|tug|empty|dry|fire|infect|excite|protect|deter|assert|snap|lift|dote|demand|present|reverse|sound|twist|look|affirm|value|employ|ail|suppose|remind|balance|plead|guide|pack|supply|bathe|whine|telephone|brake|jest|return|shift|sever|chase|whirl|growl|develop|open|inquire|saw|belong|cross|unite|trip|baste|pad|emphasize|propose|advise|surmise|oil|balk|itch|applaud|nest|pick|rain|alert|delight|dust|pedal|climb|expand|cycle|lower|drain|snow|mention|drip|berate|cheer|drone|command|howl|wrestle|load|usurp|bellow|fume|bruise|obtain|risk|press|identify|touch|polish|glue|rescue|blot|hint|snicker|point|wash|realize|allude|add|dare|crack|falter|save|ski|kick|grip|hover|march|sniff|prefer|singe|mow|snarl|bandage|knot|vacuum|judge|stunt|strap|grin|desire|knock|snore|like|shade|signal|hunt|zoom|ignore|collect|continue|snort|sympathize|clap|sketch|crowd|tumble|back|bounce|speculate|escape|star|bore|transport|shrug|bless|slice|confirm|pet|pelt|avoid|separate|lean|ice|track|floss|behave|inject|peg|hinder|obey|peel|poke|tour|inspect|communicate|enunciate|step|bolt|immigrate|ache|peep|stay|bury|plug|zip|tease|roar|jeer|choke|surround|chop|stretch|stow|swear|act|croak|repair|own|owe|visit|float|articulate|guard|harness|promise|brush|apologize|wrap|quiz|emigrate|gurgle|stare|rely|rejoice|deal|prepare|support|question|chide|tame|start|suit|untie|analyze|bubble|head|complete|form|believe|brand|mutter|evacuate|undress|admonish|heat|dole|heap|grate|overflow|level|count|pull|rush|waste|consist|wish|bargain|record|decorate|hand|reprimand|highlight|clear|expect|trim|camp|taste|frighten|describe|influence|haunt|soothe|examine|cure|exist|file|request|curl|tremble|check|film|fill|spell|nag|x([^\w]+)?ray|deserve|molt|pat|tip|scrape|upstage|flood|nap|book|terrify|branch|test|tie|sneer|smell|roll|repeat|intend|besiege|shelter|stutter|welcome|squash|wallow|drag|stab|puncture|snooze|sneeze|desert|land|yelp|phone|invest|curve|rule|observe|compete|time|push|fasten|yell|receive|rinse)"
re_irregularverbs = "(forget|forbidden|knelt|slung|sleep|trodden|go|sung|uphold|swam|overdid|show|send|sent|fly|string|rise|overdone|foretell|fall|tear|dig|leave|sang|undone|dealt|outdo|woven|overdo|withheld|strung|cost|hide|beaten|handwrote|learned|told|led|chose|drew|met|let|sing|outdone|overseen|partaken|foresee|forbid|win|brought|thrust|overhear|spoke|prove|inlay|taken|tell|hurt|overtake|stick|broke|known|hold|shoot|wore|ride|worn|learn|meet|shook|spun|slid|bent|give|flung|rode|heard|slit|overheard|bend|arise|sought|swung|sit|foreseen|write|cling|swore|sworn|stand|outdid|fed|lay|grow|overtaken|inbred|mislead|crept|pay|dream|make|wind|foresaw|dreamed|waylay|held|shake|tore|chosen|torn|feel|choose|hidden|outbid|woken|fling|wake|flew|break|flee|fled|did|slide|found|went|mean|taught|begun|forgot|borne|shown|laid|lain|got|outrun|shut|risen|forgive|undo|put|teach|bleed|thrown|ate|keep|stride|swing|fallen|think|feed|rang|breed|undid|blown|spoken|oversaw|done|awoke|ring|drove|partook|bitten|given|interwoven|bite|slept|weave|misunderstood|took|outgrown|waylaid|grew|showed|gotten|were|misunderstand|ran|awoken|say|have|seen|seek|sat|sell|lie|clung|built|overtook|take|begin|knew|paid|eaten|stood|bred|upset|drive|came|shot|mistook|trod|bring|wrung|find|ground|sewn|partake|meant|do|hit|get|beat|bear|hid|wring|weaved|rung|bought|wrote|sew|blew|set|swept|burst|freeze|bled|see|overeat|said|learnt|forecast|written|won|drawn|burned|kneel|handwritten|sold|wear|overeaten|come|kneeled|oversee|became|bet|forgotten|drunk|sweep|swum|withdrawn|speak|quit|tread|been|dug|drank|woke|threw|wet|ridden|understand|catch|spin|arisen|frozen|cast|mistake|overspent|sting|outran|rid|overspend|grown|saw|began|wound|stridden|inlaid|drink|hang|driven|inbreed|flown|arose|build|weep|overthrew|kept|spent|grind|thought|withdraw|outgrow|spend|left|blow|sprang|cut|interweave|rose|had|spread|overthrow|gave|swim|read|stung|know|dreamt|bit|burnt|overate|overthrown|lost|misled|lose|hung|become|shed|deal|spring|understood|bore|outgrew|creep|lead|handwrite|forgiven|be|run|burn|sprung|broken|offset|throw|shaken|wept|withdrew|foretold|swear|forgave|strode|froze|bound|fight|stuck|fought|upheld|was|forbade|buy|hear|eat|made|born|shrunk|gone|caught|proved|bind|proven|wove|shrink|draw|sling|lend|felt|fell|shrank|lent|sewed|withhold|awake)"
'''

'''
input = u"i will go to a visa"
re_object = u"(visa)"
object_match_sender(re_object, input)
'''
def object_match_sender(re_object, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search("(^|[^\w])"\
			+re_i+"([^\w]+)?"\
			+'('+re_will+"[^\w]+)?"\
			+re_verbs\
			+"(ed|d|es|s|ing|en)?[^\w]+"\
			+'('+re_in+'[^\w]+)?'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_object\
			+"($|[^\w])",\
			input).group()
	except:
		pass	
	return re.sub('(^[^\w]+|[^\w]+$)', '', context).strip()

'''
input = u"can you go to the office"
re_object = u"(office)"
object_match_receiver(re_object, input)
'''
def object_match_receiver(re_object, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search("(^|[^\w])"\
			+re_you+"([^\w]+)?"\
			+'('+re_will+"[^\w]+)?"\
			+re_verbs\
			+"(ed|d|es|s|ing|en)?[^\w]+"\
			+'('+re_in+'[^\w]+)?'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_object\
			+"($|[^\w])",\
			input).group()
	except:
		pass	
	return re.sub('(^[^\w]+|[^\w]+$)', '', context).strip()


'''
re_belonging = '(off|duty)'
status_match_sender(re_belonging, 'i will be off')
'''
def status_match_sender(re_status, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search("(^|[^\w])"\
			+re_i+"([^\w]+)?"\
			+'('+re_will+"[^\w]+)?"\
			+re_be+'[^\w]+'\
			+re_status\
			+"(ed|d|es|s|ing|en)?($|[^\w])",\
			input).group()
	except:
		pass	
	return re.sub('(^[^\w]+|[^\w]+$)', '', context).strip()

'''
re_belonging = '(off|duty)'
status_match_receiver(re_belonging, 'you will be off')
'''
def status_match_receiver(re_status, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search("(^|[^\w])"\
			+re_you+"([^\w]+)?"\
			+'('+re_will+"[^\w]+)?"\
			+re_be+'[^\w]+'\
			+re_status\
			+"(ed|d|es|s|ing|en)?($|[^\w])",\
			input).group()
	except:
		pass	
	return re.sub('(^[^\w]+|[^\w]+$)', '', context).strip()

'''
re_belonging = '(work|report)'
verb_match_sender(re_belonging, 'i will work ')
'''
def verb_match_sender(re_verb, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search("(^|[^\w])"\
			+re_i\
			+"([^\w]+"+re_will+")?[^\w]+"\
			+re_verb\
			+"(ed|d|es|s|ing|en)?($|[^\w])",\
			input).group()
	except:
		pass	
	return re.sub('(^[^\w]+|[^\w]+$)', '', context).strip()

'''
re_belonging = '(work|report)'
verb_match_receiver(re_belonging, 'you are working')
'''
def verb_match_receiver(re_verb, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:
		context = re.search("(^|[^\w])"\
			+re_you\
			+"([^\w]+"+re_will+")?[^\w]+"\
			+re_verb\
			+"(ed|d|es|s|ing|en)?($|[^\w])",\
			input).group()
	except:
		pass	
	return re.sub('(^[^\w]+|[^\w]+$)', '', context).strip()

'''
re_belonging = '(boss|company|salary)'
belonging_match_receiver(re_belonging, 'ur last companys')
belonging_match_receiver(re_belonging, 'you will have a good salary')
'''
def belonging_match_receiver(re_belonging, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:		
		context = re.search('(^|[^\w])'\
			+re_your+'[^\w]+'\
			+'('+re_adj+'[^\w]+)?'\
			+re_belonging+'(s|es)?'\
			+'($|[^\w])', input).group()
	except:
		pass
	try:		
		context = re.search('(^|[^\w])'\
			+re_you+'[^\w]+'\
			+'('+re_will+'[^\w]+)?'\
			+re_have+'[^\w]+'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_belonging+'(s|es)?'\
			+'($|[^\w])', input).group()
	except:
		pass
	return re.sub('(^[^\w]+|[^\w]+$)',\
		'', context).strip()

'''
re_belonging = '(boss|company|salary|book)'
belonging_match_sender(re_belonging, 'my last books')
belonging_match_sender(re_belonging, 'i will have a good salary')
'''
def belonging_match_sender(re_belonging, input):
	if input is None:
		return None
	input = input.lower().strip()
	try:		
		context = re.search('(^|[^\w])'\
			+re_my+'[^\w]+'\
			+'('+re_adj+'[^\w]+)?'\
			+re_belonging+'(s|es)?'\
			+'($|[^\w])', input).group()
	except:
		pass
	try:		
		context = re.search('(^|[^\w])'\
			+re_i+'[^\w]+'\
			+'('+re_will+'[^\w]+)?'\
			+re_have+'[^\w]+'\
			+re_a_an_the\
			+'('+re_adj+'[^\w]+)?'\
			+re_belonging+'(s|es)?'\
			+'($|[^\w])', input).group()
	except:
		pass
	return re.sub('(^[^\w]+|[^\w]+$)',\
		'', context).strip()

'''
from sms_utility_re_profile import *
'''

'''
sender home town

this is _name_ from [xxx]
my parents|family|child in|at|from|coming from [xxx]
am _name_ from [xxx]
i go back to [xxx]
my [xxx] passport|citizen|citizenship
my birth place|location|country
'''
re_i_am_processed = r'(i am|i _puntuation_ m|im|this is|my name is|am|my name)'

re_from = r'((back|down) )*(from|frm|fr)'
re_family = r'(parent|parents|mother|father|son|daughter|child|children|family|family member|wife|husband|relatives)'
re_in = r'(in|at|with|to|for|on|from)'
re_passport = r'(passport|pass port|birth certificate|citizen|citizenship|nationality|national)'
re_i_have = r'(i|i am|i _puntuation_ m) (have|own|get|hold|obtain|had|got|holding)'
re_the = r'(a|an|the|our|one|this|that|my|your|ur|his|her|their|its)'
re_hometown = r'(hometown|home town|country|birthplace|birth place|birth locatin|home country)'

re_sender_hometown_context1 = \
	r' '+re_i_am_processed+r' '\
	r'(_title_ )*'\
	+r'((_name_ )+(_puntuation_ )*(_name_ )*([a-z]+ )?)*'\
	+re_from+r' '\
	+r'_entity_ '

re_sender_hometown_context2 = \
	r' '+re_my+r' '\
	+re_family+r' '\
	+r'('+re_from+r'|'\
	+re_in+r'|coming from) '\
	+r'_entity_ '

re_sender_hometown_context3 = \
	r' '+re_i_will+r' '\
	+r'((go|going|went|gone) )*'\
	+r'(back to|back from|back|back in) '\
	+r'_entity_ '

re_sender_hometown_context4 = \
	r' '+re_my+r' '\
	+r'_entity_ '\
	+re_passport+r' '

re_sender_hometown_context5 = \
	r' '+re_i_have+r' '\
	+r'('+re_the+r' )*'\
	+r'_entity_ '\
	+re_passport+r' '

re_sender_hometown_context6 = \
	r' '+re_my+r' '\
	+re_hometown+r' '\
	+r'('+re_in+r' )*'\
	+r'_entity_ '

re_sender_hometown_context = [\
	re_sender_hometown_context1,\
	re_sender_hometown_context2,\
	re_sender_hometown_context3,\
	re_sender_hometown_context4,\
	re_sender_hometown_context5,\
	re_sender_hometown_context6\
	]

def sender_hometown_context(input):
	for pattern in re_sender_hometown_context:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

'''
sender_hometown_context(' this is _title_ _name_ from _entity_ ')
'''

'''
matching the context of home location

from sms_utility_re_profile import * 

input = ' my home add is in _puntuation_ _entity_ xxxx '
sender_home_location_context(input)

input = ' i live on _entity_ '
sender_home_location_context(input)

input = ' this is _name_ from _entity_ '
sender_home_location_context(input)
'''
sender_home_location_context1 = \
	r' my (home|apt|villa|house|unit|apartment|condo|residence|flat|family) '\
	+r'((add|address|location|place) )*'\
	+r'((is|has been|was) )*'\
	+r'(('+re_in+'|near|close to|near to) )*'\
	+r'((_puntuation_)+ )*'\
	+'_entity_ '

sender_home_location_context2 = \
	r' (i|my familiy|we) '\
	+r'((am|m|_puntuation_ m|are|r|have) )*'\
	+r'(live|living|lived) '\
	+r'(('+re_in+'|near|close to|near to) )*'\
	+'_entity_ '

sender_home_location_context_indicators = [\
	sender_home_location_context1,\
	sender_home_location_context2,\
	re_sender_hometown_context1]

def sender_home_location_context(input):
	for pattern in sender_home_location_context_indicators:
		output = extract_entity_by_re(input, \
			pattern,\
			return_none_if_not_matched = True)
		if output is not None:
			return output
	return input

##############sms_re_profile_utility.py##############
