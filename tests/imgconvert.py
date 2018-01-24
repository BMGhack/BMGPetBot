"""
Twitterbot for posting about animals needing homes.
For #BMGHack, others are welcome to adapt to their purposes.
Thanks to https://github.com/codeforamerica/CutePets for the Ruby based version

10/26/2017 SDC initial
1/6/2018 SDC Pull from the city website now. Leaving petfinder functionality in there in case somebody wants to use it.

TODOs:
put up in the cloud
Docker file so anybody can play along with ease 
'punch up' the text

Note, have to change to not save temp file

"""

from config import *
import requests
import tweepy
import json
import os
from fetchers.petfetcher import get_city_website_pet

"""
Tweet about said pet

Can't save to local file on AWS Lambda tho
"""
def tweet(api, message, pet_pic_url):
    filename = 'temp.jpg'
    if pet_pic_url:
        request = requests.get(pet_pic_url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            api.update_with_media(filename, status=message)
            os.remove(filename)
        else:
            print("Unable to download image")
    else:
        api.update(status=message)


def post_a_pet():
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    pet = get_city_website_pet(pick_random = True)
    print(pet)
    tweet(api, "%s\n%s" % (pet["description"], pet["link"]), pet["pic"])

def handler(event, context):
    post_a_pet()

if __name__ == '__main__':
    post_a_pet()
