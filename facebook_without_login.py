# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
import os
import time
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from contextlib import closing
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from w3lib.url import url_query_cleaner
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # search BY id or class or anything
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.parser import parse
import selenium as se
import numpy as np
#from textblob import TextBlob
import logging
# import data_cleaning
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
translator=Translator()

logging.getLogger().setLevel('INFO')
logging.getLogger('boto').setLevel('INFO')
logging.getLogger('scrapy.core.engine').setLevel('INFO')
logging.getLogger('scrapy.core.scraper').setLevel('INFO')
logging.getLogger('scrapy.proxies').setLevel('WARNING')
logging.getLogger('scrapy.middleware').setLevel('WARNING')
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel('WARNING')
logging.getLogger('botocore.vendored.requests.packages.urllib3.connectionpool').setLevel('WARNING')


class FacebookReviewsSpider(scrapy.Spider):
	name = 'facebook_new'
	start_urls = ['https://www.facebook.com/']
	analyser = SentimentIntensityAnalyzer()
	
	def __init__(self, limit=None, text=None, date=None, url=None, *args, **kwargs):
		self.limit = '40'
		self.text = text
		self.date = parse('24/05/2019')
	
	def parse(self,response):
		options = se.webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		options.add_experimental_option("prefs",prefs)
		# options.add_argument('headless')
		path = os.getcwd() + '/chromedriver'
		driver = se.webdriver.Chrome(chrome_options=options, executable_path=path)
		wait = WebDriverWait(driver,50)

		url = 'https://www.facebook.com/pg/'+str(self.text)+'/posts/?ref=page_internal'
		driver.get(url)
		# for item in range(int(self.limit)):
		
		# j=0
		# date_len = ['0']pyto
		# from dateutil.parser import parse
		# past_date = self.date
		# while j==0:
		# 	wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
		# 	sleep(5)
		# 	abc = driver.find_elements_by_xpath('//*[@class="_5pcq"]/abbr')
		# 	# date_len.append(len(abc))
		# 	for ab in abc:
		# 		last_date = ab.get_attribute('title').split(',')[0]
		# 		last_date = parse(last_date)
		# 		if last_date <= past_date:
		# 			j+=1
		# 		# elif int(date_len[-1])==int(date_len[-2]):
		# 		# 	j+=1
		# 		else:
		# 			j=0
		for item in range(int(self.limit)):
			wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
			sleep(3)			
		
		wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3ccb')))
		
		all_box = driver.find_elements_by_class_name('_3ccb')
		

		for box in all_box:
						#############################################
						#          FOR VIEW MORE COMMENTS           # 
						#############################################
			try:
				driver.find_element_by_xpath('//*[@class="_4swz _7a93"]/a').click()
			except:
				pass
				
						############################################
						#		FOR VIEW MORE REPLIES             # 
						############################################
						
			# try:
			# 	abc = driver.find_elements_by_xpath('//*[@class="_4swz _7a9e _7a93"]/a')
			# 	for ab in abc: 
			# 		ab.click()
			# except:
			# 	pass
			
						############################################
						#		FOR SEE MORE COMMENTS             # 
						############################################
			
			try:
				abd = driver.find_elements_by_xpath('//*[@class="_5v47 fss"]')
				for ad in abd:
					ad.click()
			except:
				pass


		sleep(3)
		soup = BeautifulSoup(driver.page_source,'lxml')
		for div in soup.findAll('div', class_='_3ccb'):
					############################################
					#		 FOR EXTRACTING POSTS             # 
					############################################
			
			post = div.find('div',class_='_5pbx userContent _3576')
			post_date = div.find('span',class_='z_c3pyo1brp').find('abbr')['title']
			from datetime import datetime
			from dateutil.parser import parse
			post_date = parse(post_date)
			post_date = datetime.strftime(post_date, '%Y-%m-%d')
			
			try:
				post_like = div.find('span',class_='_3dlh _3dli').text.strip()
			except:
				post_like = '0'
			
			try:
				post_share = div.find('span',class_='_355t _4vn2').text.strip()
				if post_share:
					if 'shares' in post_share:
						post_share = post_share.replace('shares','').strip()
					elif 'share' in post_share:
						post_share = post_share.replace('share','')
			except:
				share = '0'
			
			try:
				no_of_comments = div.find('a', class_='_3hg- _42ft').text.strip()
				if no_of_comments:
					if 'comments' in no_of_comments:
						no_of_comments = no_of_comments.replace('comments','').strip()
					elif 'comment' in no_of_comments:
						no_of_comments = no_of_comments.replace('comment','')
			except:
				no_of_comments = ''
			
			if post != '':
				try:
					post = post.text.strip()
				except:
					pass
				try:
					if 'See Translation' in post:
						post = post.replace('See Translation','')
				except:
					pass
				
				comment_p = div.find('div',class_='_7a8-')
				if comment_p:
					pass
				else:
					comment_p = div.find('div',class_='_4299')
				try:
					for data in comment_p.findAll('div',class_='_42ef'):
						
							#############################################
							#          FOR EXTRACTING USERNAME          # 
							#############################################
						
						username = data.find(class_='_6qw4')
						if username:
							try:
								username = username.text.strip()
							except:
								pass
						else:
							username = ''
							#############################################
							#          FOR EXTRACTING COMMENT           # 
							#############################################
						try:
							reply_link = data.find('a',class_='_6qw7')['href']
						except:
							reply_link = ''

						comment = data.find('span',class_='_3l3x').text.strip()
						
						date = data.find('a',class_='_6qw7')
						
						if date:
							date = date.find('abbr')['data-tooltip-content']
							from datetime import datetime
							from dateutil.parser import parse
							date = parse(date)
							date = datetime.strftime(date, '%Y-%m-%d')
						else:
							date = ''
						# if (post != '') or (comment != ''):
							
						item = {
								'post' : post,
								'post_date' : str(post_date),
								'post_like' : post_like,
								'post_share' : post_share,
								'reply_link' : reply_link,
								'no_of_comments' : no_of_comments,
								'username' : username,
								'comment' : comment,
								'date' : date
							}
						yield item
						print(item)
				except:
					item = {
								'post' : post,
								'post_date' : str(post_date),
								'post_like' : post_like,
								# 'post_share' : post_share,
								'reply_link' : '',
								'no_of_comments' : '',
								'username' : '',
								'comment' : '',
								'date' : ''
							}
					yield item
					print(item)

