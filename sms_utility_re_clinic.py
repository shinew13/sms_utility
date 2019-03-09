import re

'''
dr name 
disease 
hospital
patient
appointment time
'''

'''
extract clinic deparment from clinic appoint reminding sms

usage:
input = u"From Universal Hospital LLC Dear Abid Hussain Mohammad Sadiq, Your appointment with Dr. GEORGEY KOSHY KUNNUMPURAM has been rescheduled. The new appointment is on 13 Dec 2016 15:20 with Dr. GEORGEY KOSHY KUNNUMPURAM(Cardiology).P"
input = u"The new appointment is on 13 Dec 2016 15:20 with Dr. GEORGEY KOSHY KUNNUMPURAM(Cardiology).Please"
input = u"GHULAM HUSSAIN QADIR has appt. on 01/02/2017 at 21:04 in CARDIOLOGY Clinic RASHID HOSPITAL. "
input = u"You have an appointment with Dr Andrew Devine-Family Medicine  on 13/12/2016 at 10:40. Please reply by sending "
extract_clinic_appartment_name(input)
'''
def extract_clinic_appartment_name(input):
	try:
		output = re.search(\
			r"appointment with Dr [a-z\- ]*\-[a-z ]*\-".lower(),\
			input.lower())\
			.group()
		output = re.sub('^appointment with Dr [a-z ]*\-'.lower(), '',output)
		output = re.sub('\-$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"with Dr\. [a-z \.\-]{5,30} \([a-z \-]{5,30}\) on ".lower(),\
			input.lower())\
			.group()
		output = re.sub('^.*\(', '',output)
		output = re.sub('\).*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"with Dr\. [a-z \.\-]{5,30}\([a-z \-]{5,30}\)\.".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^.*\(', '',output)
		output = re.sub(r'\).*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"Hospital\: You have an appointment with [a-z \.\-]{5,30}\, [a-z \-]{5,30} on ".lower(),\
			input.lower())\
			.group()
		output = re.sub('^.*\, ', '',output)
		output = re.sub(' on.*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"Your appointment with Dr\. [a-z \.\-]{5,30} in [a-z \-]{5,30} Department on ".lower(),\
			input.lower())\
			.group()
		output = re.sub('^.* in ', '',output)
		output = re.sub(' department.*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"has appt\. on [\d\/\:]{4,15} at [\d\/\:]{4,15} in [a-z \-]{5,30} Clinic [a-z ]{5,30} HOSPITAL".lower(),\
			input.lower())\
			.group()
		output = re.sub('^.* in ', '',output)
		output = re.sub(' clinic.*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"Appointment of [a-z\d\/\- ]{4,30} at Clinic \d+\-Cardiology is on".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^.*clinic \d+\-', '',output)
		output = re.sub(r' is on*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"with Dr\.* [a-z ]{5,30}\-[a-z ]{2,30} (is on|is|has|on|in|at|\.at) ".lower(),\
			input.lower())\
			.group()
		output = re.sub('^with dr\.* [a-z ]{5,30}\-', '',output)
		output = re.sub(' (is on|is|has|on|in|at|\.at) $', '',output)
		output = output.strip()
		return output
	except:
		pass
	return None

'''
extract appointment time from sms

usage:

input = u"appointment tomorrow date:14/Dec/16 with Dr MOHAMAD FADL ABOUDAN .At:01:00 PM."
input = u"Dear Patient, Your appointment with Dr. SAMEEM  MAJID on 13/Dec/16 at 12:00 PM. is confirmed,Please bring your insurance card along with valid Emirates"
input = u"Dear Nukhba , your Appointment with Dr. Dr. HARSHVARDHAN at ASTER GARDENS MEDICAL  CENTRE is confirmed on 15/12/2016 at 19:40. Kindly reach the recept"
input = u"Please be informed that your appointment has been confirmed with Dr. Anurag Sapolia on December 15th 2016 at 12:30. For further information or rescheduling your appointment call 043500600."
input = u"Dear Mr. CHRISTOPHER DAVID MCLAUGHLIN, your appointment with Dr. HAMEED HUSSAIN ABDULCADER at GARDENS SPECIALITY CLINIC(BR OF DM) is confirmed on 13/12/2016 at 07:00 PM. Kindly reach the reception 10 min prior to your appointment time. For any queries, call 04 4 400 500"
extract_appointment_time(input)
'''

def extract_appointment_time(input):
	try:
		output = re.search(\
			r"appointment with Dr.*? in .*? on [a-z]+[ ]+\d+ \d+  [^a-z ]+(am|pm) at".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr.*? in .*? on | at$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"appointment with Dr [a-z\- ]* on [\d\/]* at [\d\:]*\.".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr [a-z\- ]* on '.lower(), '',output)
		output = re.sub(r'\.$', '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"booked on [\d\-\/\\\:\, ]{5,25} with Dr".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^.* on ', '',output)
		output = re.sub(r' with.*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"appointment tomorrow date\:[a-z\d\/]{5,15} with Dr [a-z \.]{5,30} \.At\:[\d\: a-z]{5,15}\.".lower(),\
			input.lower())\
			.group()
		output1 = re.sub(r'^.*date\:', '',output)
		output1 = re.sub(r' with.*$', '',output1)
		output2 = re.sub(r'^.*at\:', '',output)
		output2 = re.sub(r'\.$', '',output2)
		output = output1 +' '+output2
		return output
	except:
		pass
	try:
		output = re.search(\
			r"Your appointment with Dr\. [a-z \.]{5,30} on [a-z\d\/]{5,15} at [\d\: a-z]{5,15}\. is".lower(),\
			input.lower())\
			.group()
		output1 = re.sub(r'^.* on ', '',output)
		output1 = re.sub(r' at .*$', '',output1)
		output2 = re.sub(r'^.* at ', '',output)
		output2 = re.sub(r'\. .*$', '',output2)
		output = output1 +' '+output2
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your Appointment with Dr\. Dr\. [a-z \.]{5,30} at [a-z \.]{5,40} is confirmed on [a-z\d\/]{5,15} at [\d\: a-z]{5,15}\.".lower(),\
			input.lower())\
			.group()
		output1 = re.sub(r'^.* on ', '',output)
		output1 = re.sub(r' at .*$', '',output1)
		output2 = re.sub(r'^.* at ', '',output)
		output2 = re.sub(r'\. .*$', '',output2)
		output = output1 +' '+output2
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your appointment has been confirmed with Dr\. [a-z \.]{5,30} on [a-z\d\\\/ ]{5,40} at [\d\: a-z]{5,15}\.".lower(),\
			input.lower())\
			.group()
		output1 = re.sub(r'^.* on ', '',output)
		output1 = re.sub(r' at .*$', '',output1)
		output2 = re.sub(r'^.* at ', '',output)
		output2 = re.sub(r'\. .*$', '',output2)
		output = output1 +' '+output2
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your appointment with Dr\. [a-z \.]{5,30} at [a-z\,\. ]{10,100} on [a-z\d\\\/ ]{5,40} at [\d\: a-z]{5,15} is".lower(),\
			input.lower())\
			.group()
		output1 = re.sub(r'^.* on ', '',output)
		output1 = re.sub(r' at .*$', '',output1)
		output2 = re.sub(r'^.* at ', '',output)
		output2 = re.sub(r' is.*$', '',output2)
		output = output1 +' '+output2
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your appointment on [a-z\d\,\: ]{5,30} with Dr".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^.* on ', '',output)
		output = re.sub(r' with.*$', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r" with Dr[a-z\.\- ]* on [\d\\\/]{5,15} at [a-z\d\\\/\: ]{5,15} is ".lower(),\
			input.lower())\
			.group()
		output1 = re.sub(r'^.* on ', '',output)
		output1 = re.sub(r' at .*$', '',output1)
		output2 = re.sub(r'^.* at ', '',output)
		output2 = re.sub(r' is.*$', '',output2)
		output = output1 +' '+output2
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your appointment with Dr[\.a-z ]* at .* is confirmed on [\d\/]* at [\d\:a-z ]*\.".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^your appointment with Dr[\.a-z ]* at .* is confirmed on '.lower(), '',output)
		output = re.sub(r'\.$'.lower(), '',output)
		return output
	except:
		pass
	return None

'''
extract dr name from sms

usage:

input = u"MediClinic City Hospital:You have an appointment with Dr Andrew Devine-Family Medicine  on 06/03/2016 at 09:40. Please reply by sending   1 to Confirm"
extract_dr_name(input)
'''

def extract_dr_name(input):
	try:
		output = re.search(\
			r"appointment with Dr\. [a-z ]+ in [a-z\- ]+ Department".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr\. | in [a-z\- ]+ Department$'.lower(), '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"with Dr\.* [a-z \.]{5,30} (is on|is|has|on|in|at|\.at|\() ".lower(),\
			input.lower())\
			.group()
		output = re.sub('^with dr\.* ', '',output)
		output = re.sub(' (is on|is|has|on|in|at|\.at|\() $', '',output)
		return output
	except:
		pass
	try:
		output = re.search(\
			r"with Dr\.* [a-z \.]{5,30}\-".lower(),\
			input.lower())\
			.group()
		output = re.sub('^with dr\.* ', '',output)
		output = re.sub('\-$', '',output)
		return output
	except:
		pass
	return None

'''
input = u"Dear Mariam, your appointment with Dr. Walid Sayed is on 18/12/2016 at 10:00 AM at the HealthPlus Fertility Center. Phone:026433494 Directions:"
input = "FATMA JASSIM ABDULLA Z RAFI has appt. on 26/10/2015 at 12:00 in ANTE NATAL CARE Clinic LATIFA HOSPITAL . For cancellation please call 042193296 or vip"
input = u"Mediclinic City Hospital- Bldg 37, Dubai Healthcare City. Location map http://bit.ly/2frPT7S: You have an appointment with Dr Sarah Ehtisham-Paediatrics  on 13/12/2016 at 12:00. Please reply by sending 1 to Confirm"
input = u"  MediClinic City Hospital:You have an appointment with Dr Mahmoud Marashi-Oncology/Haemotology  on 06/10/2015 at 16:20. Please reply "
input = u"You have an appointment at AHD with DR. HUSSEIN NAJI  on  14 Dec 2016  at 1000 .Pls reply Y to confirm or N to Cancel. "
input = u"Saudi German hospital Dubai reminds you of your appointment tomorrow date:13/Dec/16 with Dr FADIA  FADEL .At:10:15 AM.(please come 15 minutes before your appointment time).If you want to cancel or change your appointment please call 043890000.Thank you. We Care."
input = u"Dear Mr. CHRISTOPHER DAVID MCLAUGHLIN, your appointment with Dr. HAMEED HUSSAIN ABDULCADER at GARDENS SPECIALITY CLINIC(BR OF DM) is confirmed on 13/12/2016 at 07:00 PM. Kindly reach the reception 10 min prior to your appointment time. For any queries, call 04 4 400 500"
extract_clinic_name(input)
'''

def extract_clinic_name(input):
	try:
		output = re.search(\
			r"appointment with Dr.*? in [a-z\- ]+ Department on .*? at [a-z ]+ Hospital".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr.*? in [a-z\- ]+ Department on .*? at |$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"appointment with Dr.*? in .*? on .*? at [a-z ]+ Hospital\, [a-z ]{4,20} is".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr.*? in .*? on .*? at | is$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"appointment with Dr.*? is on .*? at .*? at the [a-z ]+ Center\.".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr.*? is on .*? at .*? at the |\.$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"appointment with Dr.*? is on .*? at .*? at the [a-z ]+ Center\.".lower(),\
			input.lower())\
			.group()
		output = re.sub(r'^appointment with Dr.*? is on .*? at .*? at the |\.$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your appointment with Dr.* is on .* at [a-z\d\: ]{4,10} at the [a-z ]{5,40}\.".lower(),\
			input.lower())\
			.group()
		output = re.sub('^.*at the ', '',output)
		output = re.sub('\.$', '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"has appt\. on .* at .* in .* Clinic [a-z ]{5,40} \.".lower(),\
			input.lower())\
			.group()
		output = re.sub('^has appt\. on .* at .* in .* clinic ', '',output)
		output = re.sub(' \.$', '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"^[^\w]*.*\. Location map.*You have an appointment with Dr".lower(),\
			input.lower())\
			.group()
		output = re.sub('^[^\w]*', '',output)
		output = re.sub('\. Location map.*You have an appointment with Dr$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"^[^\w]*[a-z ]{4,40}\:You have an appointment with Dr".lower(),\
			input.lower())\
			.group()
		output = re.sub('^[^\w]*', '',output)
		output = re.sub('\:You have an appointment with Dr$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"You have an appointment at [a-z ]{3,30} with DR".lower(),\
			input.lower())\
			.group()
		output = re.sub('^You have an appointment at '.lower(), '',output)
		output = re.sub(' with DR$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"^[^\w]*[a-z ]{3,30} reminds you of your appointment tomorrow date.{3,20} with Dr".lower(),\
			input.lower())\
			.group()
		output = re.sub('^[^\w]*'.lower(), '',output)
		output = re.sub(' reminds you of your appointment tomorrow date.{3,20} with Dr$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	try:
		output = re.search(\
			r"your appointment with Dr[\.a-z ]* at [a-z\-\(\) ]* is confirmed".lower(),\
			input.lower())\
			.group()
		output = re.sub('^your appointment with Dr[\.a-z ]* at '.lower(), '',output)
		output = re.sub(' is confirmed$'.lower(), '',output)
		output = output.strip()
		return output
	except:
		pass
	return None

def extract_patient_name(input):
	try:
		output = re.search(r"Dear Ms\. [A-Za-z ]{4,40}, your appointment with Dr", input).group()
		output = re.sub(r'^Dear Ms\. |\, your appointment with Dr$', '',output)
		output = output.strip().lower()
		output = re.sub(r"patient", '', output)
		if len(output) >= 1:
			return output
	except:
		pass
	try:
		output = re.search(r"Dear [A-Za-z ]{4,40}\, your appointment with Dr", input).group()
		output = re.sub(r'^Dear |\, your appointment with Dr$', '',output)
		output = output.strip().lower()
		output = re.sub(r"patient", '', output)
		if len(output) >= 1:
			return output
	except:
		pass
	return None

input = u"Dear Patient, Your appointment with Dr. Serag Mohd. in DENTAL Department on Mar  7 2016  2:30PM at GMC Hospital is confirmed. (Visit Thumbay Pharmacy 24/7)"
print extract_clinic_name(input)