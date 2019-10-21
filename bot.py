import botogram

import re
# import urllib,urllib3
import sys

GENDER_CHOICES = {
	"Female": ["f", "female", "2", "2.female"],
	"Male": ["m", "male", "1", "1.male"],
}
YEAR_CHOICES = {
	"1st": ["first", "one", "1", "1st"],
	"2nd": ["second", "two", "2", "2nd"],
	"3rd": ["third", "three", "3", "3rd"],
	"4th": ["fourth", "four", "4", "4th"],
}
LANG_CHOICES = {
	1: "Python 2/3",
	2: "C++",
	4: "C",
	8: "Java",
}

my_handle = "YOUR_HANDLE"




bot = botogram.create("YOUR_TELEGRAM_API_TOKEN")
bot.about = """
	Welcome to CSEC-CPD registration bot.
	You can use this bot to register for CSEC-CPD membership."""
bot.owner = my_handle


class memory:

	def __init__(self):
		self.names = {}
		self.ids = {}
		self.genders = {}
		self.emails = {}
		self.phone_nums = {}
		self.years = {}
		self.langs = {}
		self.stages = {}    

	def get_stage(self,cid):
		if cid in self.stages:
			return self.stages[cid]
		return None

	def get_lang(self,cid):
		if cid in self.langs:
			return self.langs[cid]
		return None

	def get_name(self,cid):
		if cid in self.names:
			return self.names[cid]
		return None

	def get_id(self,cid):
		if cid in self.ids:
			return self.ids[cid]
		return None

	def get_gender(self,cid):
		if cid in self.genders:
			return self.genders[cid]
		return None

	def get_email(self,cid):
		if cid in self.emails:
			return self.emails[cid]
		return None

	def get_phone_num(self,cid):
		if cid in self.phone_nums:
			return self.phone_nums[cid]
		return None

	def get_year(self,cid):
		if cid in self.years:
			return self.years[cid]
		return None

	def set_stage(self,cid,val):
		self.stages[cid] = val

	def set_lang(self,cid,val):
		self.langs[cid] = val

	def set_name(self,cid,val):
		self.names[cid] = val

	def set_id(self,cid,val):
		self.ids[cid] = val

	def set_gender(self,cid,val):
		self.genders[cid] = val

	def set_email(self,cid,val):
		self.emails[cid] = val

	def set_phone_num(self,cid,val):
		self.phone_nums[cid] = val

	def set_year(self,cid,val):
		self.years[cid] = val
	def debug(self):
		print(self.names)
		print(self.ids)
		print(self.genders)
		print(self.emails)
		print(self.genders)
		print(self.phone_nums)
		print(self.years)
		print(self.langs)
		print(self.stages)


Memory = memory()

@bot.command("register")
def register_command(chat, message, args):
	"""
		Register for club membership
	"""

	Memory.set_stage(chat.id, 0)
	chat.send("Alright, you chose to register. Let's start with your full name?")


@bot.command("reset")
def reset_command(chat, message, args):
	"""
		Reset progress and start registration from the beginning
	"""

	Memory.set_stage(chat.id, 0)
	chat.send(
		"Your progress has been reset. So let's start again by telling me your full name.")


@bot.command("abort")
def abort_command(chat, message, args):
	"""
		Abandon all progress and stop registration process
	"""
	Memory.set_stage(chat.id, -1)
	chat.send(
		"You have chosen to abort. If you would like to start over, click /register.")


@bot.process_message
def responder(chat, message):
	# Memory.debug()
	# print(message.text)
	stage = Memory.get_stage(chat.id)
	if stage == -1:
		chat.send(
			"Incorrect Input Detected!!! Use /help to see available commands.")
	elif stage == 0:

		if not re.match("([A-Z][a-z]{3,} )([A-Z][a-z]{3,} )?([A-Z][a-z]{3,})", message.text):
			chat.send("Incorrect format!!! Please input your full name...")
		else:
			Memory.set_name(chat.id, message.text)
			Memory.set_stage(chat.id, 1)
			chat.send("Good, now input you ID number in the correct format.")
	elif stage == 1:
		if re.match("(r\/)[0123456789]{3,5}\/08", message.text.lower()):
			chat.send(
				"Dear GC, we are very sorry to inform you that you are not eligible for membership at CSEC-CPD.")
			Memory.set_stage(chat.id, -1)
		if not re.match("(a\/ur|ugr\/)[0123456789]{4,5}\/(09|10|11|12)", message.text.lower()):
			chat.send("Incorrect ID format!!! Please use the regular ID format.")
		else:
			Memory.set_id(chat.id, message.text.lower())
			Memory.set_stage(chat.id, 2)
			chat.send(
				"Great, next choose your appropriate gender \n \t1. Male \n \t2. Female")
	elif stage == 2:
		msg = message.text.lower()
		gender = None

		if msg in GENDER_CHOICES["Male"]:
			gender = "Male"
		elif msg in GENDER_CHOICES["Female"]:
			gender = "Female"

		if gender:
			Memory.set_gender(chat.id, gender)
			Memory.set_stage(chat.id, 3)
			chat.send(
				"You're halfway there. The next field is your email address.")
		else:
			chat.send("Incorrect/Unrecognized gender selected!!! Please choose from these given selections \n\t1. Male\n\t2. Female")
	elif stage == 3:
		if not re.match("[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+", message.text):
			chat.send(
				"Incorrect Email address format!!! Please use the proper format of email address")
		else:
			Memory.set_email(chat.id, message.text)
			Memory.set_stage(chat.id, 4)
			chat.send("Awesome, the next item on the list is your phone number")
	elif stage == 4:
		if not re.match("(\+2519|09)[0-9]{8}", message.text):
			chat.send(
				"Incorrect Phone number format!!! Please use the proper phone number format")
		else:
			Memory.set_phone_num(chat.id, message.text)
			Memory.set_stage(chat.id, 5)
			chat.send("Almost there! What year are you currently in?")
	elif stage == 5:
		year = None
		if message.text.isnumeric():
			if int(message.text) > 4:
				chat.send("Only students upto 4th year can join CSEC-CPD.")
			else:
				year = message.text
		else:
			for yr in YEAR_CHOICES:
				if message.text in YEAR_CHOICES[yr]:
					year = yr
					break
		if year:
			Memory.set_year(chat.id, year)
			Memory.set_stage(chat.id, 6)
			chat.send("Final question, Please input the sum of the values of the programming languages you are proficient in from the given list \
						\n\n\t For Python 2/3 => 1\
						\n\t For C++ => 2\
						\n\t For C => 4\
						\n\t For Java => 8\
						\n\nExample:\
						\n\tIf you can code in C++ only, C++ has 2 so you should input 2\
						\n\tor if you can code in Python 2/3, C and Java, you should input 13 because 1 + 4 + 8 = 13\
						")
		else:
			chat.send(
				"Unrecognized input!!! Please specify what year are you currently in.")
	elif stage == 6:
		try:
			val = int(message.text)
			langs = []
			if val>15 or val<1:
				chat.send("Incorrect value entered!!! The sums only range from 1 to 15.")
			
			for i in range(3,-1,-1):
				np = pow(2,i)
				if np > val:
					continue
				langs.append(LANG_CHOICES[np])
				val-=np
			Memory.set_lang(chat.id, langs)
			if fill_form(
				Memory.get_name(chat.id),
				Memory.get_id(chat.id),
				Memory.get_gender(chat.id),
				Memory.get_email(chat.id),
				Memory.get_phone_num(chat.id),
				Memory.get_year(chat.id),
				Memory.get_lang(chat.id)):
				
				
				chat.send("Done! Congratulations, You have successfully registered for membership of CSEC-CPD. The Examination dates will be announced soon. In the mean time join our channel for more information about CSEC-ASTU and ICPC in general.\n@CSEC_ASTU")            
			else:
				chat.send("Internal Error!!! Please try to /register again and if the problem persists contact me at " + my_handle + ". ")
			
			Memory.set_stage(chat.id,-1)
			
		except ValueError:
			chat.send("Incorrect number entered!!! Please only use digits in the input.")

def fill_form(name,id,gender,email,phone,year,langs):
	try:
		
		fields = []
		fields.append(tuple([['Name'],name]))
		fields.append(tuple([['Id'],id]))
		fields.append(tuple([['Gender'],gender]))
		fields.append(tuple([['Email'],email]))
		fields.append(tuple([['Phone'],phone]))
		fields.append(tuple([['Year'],year]))
		fields.append(tuple([0,":".join(langs)]))
			
		csv_fields = ",".join([i[1]for i in fields]) 
		
		print(csv_fields)
		
		with open("db.csv","a") as f:
			f.write(csv_fields+"\n")
		
		return True
	except:
		print(sys.exc_info())

if __name__ == "__main__":
	bot.run(workers=1)
