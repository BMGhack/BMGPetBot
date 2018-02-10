"""
Twitterbot for posting about animals needing homes.
For #BMGHack, others are welcome to adapt to their purposes.
Thanks to https://github.com/codeforamerica/CutePets for the Ruby based version

10/26/2017 SDC initial
1/6/2018 SDC Pull from the city website now. Leaving petfinder functionality in there in case somebody wants to use it.
1/20/2018 SDC don't save image to temp file! Also additional function for lambda stuff

TODOs:
put up in the cloud
Docker file so anybody can play along with ease 
'punch up' the text

"""

from config import *
import requests
import tweepy
import json
import os
from fetchers.petfetcher import get_city_website_pet
import base64
import io

"""
Tweet about said pet
"""
def tweet(api, message, pet_pic_url):
    filename = 'temp.jpg'
    if pet_pic_url:
        img_file = get_image_blob(pet_pic_url)
        api.update_with_media(filename, status=message, file=img_file, lat=LATITUDE, long=LONGITUDE)
    else:
        api.update_status(status=message, lat=LATITUDE, long=LONGITUDE)

def get_image_blob(url):
    response = requests.get(url)
    pic = base64.b64encode(response.content)
    pic = io.BytesIO(base64.b64decode(pic))
    return pic

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