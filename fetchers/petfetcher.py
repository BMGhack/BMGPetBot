"""
This code is for interaction with Pet-related APIs
Petfinder API: https://www.petfinder.com/developers/api-docs

10/26/2017 SDC Initial
1/4/2018 SDC minor restructuring plus 'pet randomization'
1/5/2018 SDC pull from Bloomington website
"""

from config import *
import requests
import tweepy
import json
import os
from random import randrange
from bs4 import BeautifulSoup
import requests
import random
import re

name_re = re.compile('\.w?(.*?)is:');
CITY_SITE_BASE = 'https://bloomington.in.gov'

PETFINDER_URL = "http://api.petfinder.com/"
PETFINDER_ADJECTIVES = {
	'housebroken':'house trained',
	'housetrained':'house trained',
	'noClaws':'declawed',
	'altered':'altered',
	'noDogs':'',
	'noCats':'',
	'noKids':'',
	'hasShots':'',
	'specialNeeds':''
}

"""
City site stuff
"""
def get_city_website_pet(pick_random = False):
	request = requests.get('%s/animal-shelter/animals' % CITY_SITE_BASE)
	request_text = request.text
	soup = BeautifulSoup(request_text, "html.parser") #, "html.parser")
	nodes = soup.find_all("article") # section",{"id":"asm_animals"})
	if pick_random:
		index = random.randrange(len(nodes))
	else:
		index = 0
	node = nodes[index]
	url = node.a['href']
	img = None
	try:
		img = node.img['src']
		img = '%s%s' % (CITY_SITE_BASE, img)
	except:
		print("No image found")
	r = requests.get('%s/%s' % (CITY_SITE_BASE, url))
	soup = BeautifulSoup(r.text, "html.parser")
	#intro
	nodes = soup.find_all("div",{"id":"intro"})
	animule_text = nodes[0].text.split('Apply')[0].strip()
	splitty = name_re.split(animule_text)
	#add tags
	lines = splitty[-1].split("\n")
	tags = ["#%s" % lines[1], "#adoptdontshop", "#rescue", "#adoptme", "#shelterpets"]
	if len(splitty) != 1:
		animule_text = ("%s is: %s" % (splitty[-2], splitty[-1]))
     
	animule_text = '\n'.join(animule_text.split("\n")[:6])
	animule_text = animule_text.replace("Adoption Fee Waived","Adoption Fee Waived.")
	animule_text = animule_text + "\n" + " ".join(tags)
# trim if too long!
	animule_text = animule_text[:280]

	return {
		"pic": img,
		"link":'%s%s' % (CITY_SITE_BASE, url),
		"description": animule_text
	}

"""
construct a description for petfinder pet
"""
def get_petfinder_description(pet_json):
	description = "%s %s %s" % (get_petfinder_option(pet_json['options']),
								get_petfinder_sex(pet_json['sex']['$t']),
								get_petfinder_breed(pet_json['breeds'])) 
	return description

"""
Photolink from petfinder (if there is one)
"""
def get_petfinder_photo(pet_json):
	try:
		return pet_json['media']['photos']['photo'][2]['$t']
	except: # ok that's a bit hacky!
		return ""

"""
Pull info for a pet
location can be zip or City, State
"""
def get_petfinder_pet(location, count=25, pick_random = False):
	params = {
	  'format':'json',
	  'key':PETFINDER_API_KEY,
	 'location':location,
	  'output':'full',
	  'count': count
	}
	r = requests.post("%s/pet.find" % (PETFINDER_URL), params)
	d = json.loads(r.text)

	# TODO - check response type - have question in to petfinder re: their response types

	# check validity
	status_message = d['petfinder']['header']['status']['message']
	if status_message:
		status_message = status_message['$t']
		if status_message == 'shelter opt-out':
			raise Exception('The chosen shelter opted out of being accesible via the API')
		elif status_message == 'unauthorized key':
			raise Exception('Check that your Petfinder API key is configured correctly')
		elif status_message:
			raise Exception('Unexpected error: %s' % status_message)

	if pick_random:
		index = randrange(len(d["petfinder"]["pets"]["pet"]))
		pet = d["petfinder"]["pets"]["pet"][index]
	else:
		pet = d["petfinder"]["pets"]["pet"][0]
	return {
		"pic": get_petfinder_photo(pet),
		"link":"https://www.petfinder.com/petdetail/%s" % (pet['id']['$t']),
		"name": pet['name']['$t'],# capitalize?
		"description": get_petfinder_description(pet)
	}

def get_petfinder_sex(sex_abbreviation):
	if sex_abbreviation.lower() == 'f':
		return 'female'
	else:
		return 'male'

def get_petfinder_option(options):
	if options['option']:
		# note - weirdly handles single option...
		if type(options['option']) == dict:
			options = PETFINDER_ADJECTIVES.get(options['option']['$t'])
		else:
			options =  ",".join([PETFINDER_ADJECTIVES.get(opt['$t'],"") for opt in options['option'] if opt])
	else:
  		options = option_hash['$t']
	if options[0] == ',':
		options = options[1:]
	return options

def get_petfinder_breed(breeds):
	if isinstance(breeds['breed'],(list)):
		return "%s mix" % ("/".join(breeds['breed']))
	else:
		return breeds['breed']['$t']

def create_petfinder_message(greeting, pet_description, pet_name, pet_link):
	if pet_description[0] in ('a','e','i','o','u'):
		full_description = "an %s" % (pet_description)
	else:
		full_description = "a %s" % (pet_description)
	message = "%s %s. I am %s. %s" % (greeting, pet_name, full_description, pet_link)
	if len(message) > 200:
		message = message[:200] # this could lead to some weird looking tweets
	return message

# ye olde style testing
if __name__ == '__main__':
	p = get_petfinder_pet("47403")
	print(p)