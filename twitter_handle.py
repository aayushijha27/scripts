# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
import os
import time
from time import sleep
from datetime import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from contextlib import closing
from selenium.webdriver import Chrome
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from w3lib.url import url_query_cleaner
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # search BY id or class or anything
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import selenium as se
import numpy as np
from textblob import TextBlob
import logging
from selenium.webdriver.common.action_chains import ActionChains
import tweepy 
  
class TwitterHandleSpider(scrapy.Spider):
	name = 'twitter_handle'
	start_urls = ['https://www.google.com/']
	consumer_key = "FOa2S6sArS49x60OBrjDdg4gd" 
	consumer_secret = "7p0CTPorWkh7ozC5QXyi6h4T8lHadBawVGGhPIU3GS1j1ugGvA"
	access_key = "899716738777964544-Dz7Y5Fc2ojDt87CgTIti8JHFepdjRAh"
	access_secret = "cMhYz5sBxastaZKw5b5HbF4KO0281LxgD17s5tqwYCuFD"
	
	def __init__(self, genre=None, text=None, limit=None, url=None, *args, **kwargs):
		self.text = text
		self.limit = 200

	def parse(self, response): 
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret) 
		auth.set_access_token(self.access_key, self.access_secret) 
		api = tweepy.API(auth) 
		count=0
		# comments_list = []
		for status in tweepy.Cursor(api.user_timeline, screen_name=self.text, tweet_mode="extended").items(self.limit):
			count=count+1
			user = api.get_user(self.text)
			try:
				display_url = status.entities['media'][0]['display_url']
			except:
				display_url = ''
			item = {
					'count':count,
					'Text':status.full_text,
					'Tweet id':status.id,
					'Tweet Created At':status.created_at,
					'Display URL':display_url,
					'Retweets Count':status.retweet_count,
					"Likes":status.favorite_count,
					"Username":user.name,
					"Screen Name":user.screen_name,
					"User ID":user.id,
					"Location":user.location,
					"Following":user.friends_count,
					"Number of Post":user.statuses_count,
					"Description":user.description,
					"Followers":user.followers_count,
					"Favourites_count":user.favourites_count,
					"Date of Joining":user.created_at,
			}
			yield item
			# comments_list.append(item)
		# print(comments_list)