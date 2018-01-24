"""

Scrapin'

A little more text massaging needed.

Handle no img CITY_SITE_BASE


Weird cases:
Adoption Fee Waived Gracie is:
Cat
Domestic Short Hair
Female
Senior
Large
C17111545

I am deaf Rocky is:
Dog
Pit Bull Terrier
Male
Young Adult
Large

"""
from bs4 import BeautifulSoup
import requests
import random
import re

name_re = re.compile('\.w?(.*?)is:');
CITY_SITE_BASE = 'https://bloomington.in.gov'


def get_citywebsite_pet(pick_random = False):
	print('fetch it')
	print('%s/animal-shelter/animals' % CITY_SITE_BASE)
	request = requests.get('%s/animal-shelter/animals' % CITY_SITE_BASE)
	request_text = request.text
	print("soup time")
	soup = BeautifulSoup(request_text, "html.parser") #, "html.parser")
	print("got dat soup")
	nodes = soup.find_all("article") # section",{"id":"asm_animals"})
	print("%s animules" % len(nodes))

	if pick_random:
		index = random.randrange(len(nodes))
	else:
		index = 0

	node = nodes[index]

	url = node.a['href']
	try:
		img = node.img['src']
		print(img)
	except:
		print("No image found")

	print(url)

	r = requests.get('%s/%s' % (CITY_SITE_BASE, url))
	print(r)
	#print(r.text)
	soup = BeautifulSoup(r.text, "html.parser")
	#intro
	nodes = soup.find_all("div",{"id":"intro"})
	animule_text = nodes[0].text.split('Apply')[0].strip()
	print(animule_text)
	# not quite splitting properly
	splitty = name_re.split(animule_text)
	print(splitty)
	if len(splitty) != 1:
		animule_text = ("%s is: %s" % (splitty[-2], splitty[-1]))
	print("Survey says:\n\n\n_____")
	animule_text = '\n'.join(animule_text.split("\n")[:6])
	animule_text = animule_text.replace("Adoption Fee Waived","Adoption Fee Waived.")
	print(animule_text)
# trim if too long!
	animule_text = animule_text[:280]

	return {
		"pic": '%s/%s' % (CITY_SITE_BASE, img),
		"link":'%s/%s' % (CITY_SITE_BASE, url),
		"description": animule_text
	}


if __name__ == '__main__':
	print(get_citywebsite_pet(True))
