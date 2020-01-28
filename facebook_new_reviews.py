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
#import data_cleaning
#from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#translator=Translator()

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
	
	def __init__(self, limit=None, text=None, mail=None, password=None, 	url=None, *args, **kwargs):
		self.limit = '30'
		self.text = text
		self.url = 'https://www.facebook.com/pg/Fractureme/posts/?ref=page_internal'
		self.mail = 'jha_aayushi@yahoo.com'
		self.passsword = 'redminote6pro'
	
	def parse(self,response):
		options = se.webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		options.add_experimental_option("prefs",prefs)
		# options.add_argument('headless')
		path = os.getcwd() + '/chromedriver'
		driver = se.webdriver.Chrome(chrome_options=options, executable_path=path)
		wait = WebDriverWait(driver,50)
		driver.get(response.url)
		
							 ##### Login Page #####
		
					#############################################
					#            ENTERING USERNAME              # 
					#############################################
					
		wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]'))).send_keys(str(self.mail))
		
					#############################################
					#            ENTERING PASSWORD              # 
					#############################################
		
		wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pass"]'))).send_keys(str(self.passsword))
		
					#############################################
					#               CLICK LOGIN                 # 
					#############################################
					
		sleep(1)

		wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbutton"]'))).click()

		try:
			driver.find_element_by_xpath('//*[@id="checkpointSubmitButton"]').click()
		except:
			pass
					#############################################
					#              SEARCH KEYWORD               # 
					#############################################
		# sleep(1)
		# wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="_5861 navigationFocus textInput _5eaz"]/input[2]'))).send_keys(str(self.text))
		
		# wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='_42ft _4jy0 _4w98 _4jy3 _517h _51sy _4w97']"))).click()
		
		# wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class=" _5vwz _45hc"][6]/a'))).click()
		
		# page_text = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="_32mo"]/span'))).text

		# if self.text.title() in str(page_text):
			
		# 	wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="_32mo"]'))).click()
			
		# 	wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="_2yau"]')))
			
		# 	abc = driver.find_elements_by_xpath('//*[@class="_2yau"]')
		
		# for ab in abc:
		# 	if 'Posts' in ab.text:
		# 		ab.click()
		# sleep(3)
		
		driver.get(self.url)
		# wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="u_0_x"]/div[4]/a'))).click()


		for item in range(int(self.limit)):
			wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
			sleep(3)
		
		#############################################################################################################
					
							#############################################
							#              FOR REVIEW PAGE              # 
							#############################################
		
		################### Click See More in Reviews ##########################
		# try:
		# 	see_m = driver.find_elements_by_xpath('//*[@class="see_more_link"]')
		# 	for see_more in see_m:
		# 		see_more.click()
		# except:
		# 	pass

		# soup = BeautifulSoup(driver.page_source,'lxml')
		# for div in soup.findAll('div',class_='_5pcr userContentWrapper'):
		# 	div1 = div.find('h5', class_='_7tae _14f3 _14f5 _5pbw _5vra')
		# 	try:
		# 		username = div1.find('span',class_='fwb').text.strip()
		# 	except:
		# 		username = ''
		# 	try:
		# 		date = div.find('a',class_='_5pcq').find('abbr')['title'].split(',')[0]
		# 		# olddate = parse(date)
		# 		# date = datetime.strftime(olddate, '%d-%m-%Y')
		# 	except:
		# 		date = ''
		# 	review = ''
		# 	review = div.find('div',class_='_5pbx userContent _3576').text.strip()
		# 	emoji_pattern = re.compile("["
		# 								u"\U0001F600-\U0001F64F"  # emoticons
		# 								u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		# 								u"\U0001F680-\U0001F6FF"  # transport & map symbols
		# 								u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		# 								u"\U00002702-\U000027B0"
		# 								u"\U000024C2-\U0001F251"
		# 								u"\U00010000-\U0010ffff"
		# 								"]+", flags=re.UNICODE)
		# 	review = emoji_pattern.sub(r'', review)
		# # 	if review:
		# 		review_cleaned = review.replace('\d+', '')
		# 		review_cleaned = re.sub(r'www.\S+|http\S+', '', review_cleaned)
		# 		review_cleaned = re.sub(r'[^\w\s]+', '', review_cleaned)
		# 	else:
		# 		review_cleaned = ''
			
		# 	polarity = ''
		# 	sentiment = ''

		# 	if review_cleaned:
		# 		polarity = self.analyser.polarity_scores(review_cleaned)
				
		# 		if (polarity["compound"] <= -0.1):
		# 			sentiment = "Very Bad"
		# 		elif (polarity["compound"] > -0.1) and (polarity["compound"]<0.0):
		# 			sentiment = "Bad"
		# 		elif (polarity["compound"] <= 0.0) and (polarity["compound"]>=0.05):
		# 			sentiment = "Neutral"
		# 		elif (polarity["compound"] > 0.05) and (polarity["compound"] < 0.5):
		# 			sentiment = "Good"
		# 		else:
		# 			sentiment = "Very Good"
			
				
			
		# 	# review_translated = translator.translate([review_cleaned],dest='en')
		# 	# review_translated = review_translated[0].text
			# if review:
			# 	item = {
			# 			'username' : username,
			# 			'date' : date,
			# 			'review' : review,
			# 			# 'review_cleaned' : review_cleaned,
			# 			# polarity':polarity["compound"],
			# 			# 'review_translated' : review_translated,
			# 			# 'polarity' : polarity,
			# 			# 'sentiment' : sentiment
			# }

			# yield item
		

		##############################################################################################################
		
		
		wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3ccb')))
		
		
		all_box = driver.find_elements_by_class_name('_3ccb')
		

		for box in all_box:
			
		# 				#############################################
		# 				#          FOR VIEW MORE COMMENTS           # 
		# # 				#############################################
			try:
				driver.find_element_by_xpath('//*[@class="_4swz _293g"]/a').click()
			except:
				pass
				
		# 				############################################
		# 				#		FOR VIEW MORE REPLIES             # 
		# 				############################################
						
			try:
				abc = driver.find_elements_by_xpath('//*[@class="_4swz _1i3s _293g"]/a')
				for ab in abc: 
					ab.click()
			except:
				pass
			
		# 				############################################
		# 				#		FOR SEE MORE COMMENTS             # 
		# 				############################################
			
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
		# 			#		 FOR EXTRACTING POSTS             # 
		# 			############################################
			try:
				post = div.find('div',class_='_5pbx userContent _3576')
				
				try:
					like = div.find('span',class_='_3dlh _3dli').text.strip()
				except:
					like = '0'
				
				try:
					share = div.find('span',class_='_355t _4vn2').text.strip()
				except:
					share = '0'
				
				try:
					no_of_comments = div.find('a', class_='_3hg- _42ft').text.strip()
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
					
					comment_p = div.find('div',class_='_3w53')
					if comment_p:
						pass
						
					else:
						comment_p = div.find('div',class_='_4299')

					for data in comment_p.findAll('div',class_='_42ef'):
						
		# 					#############################################
		# 					#          FOR EXTRACTING USERNAME          # 
		# 					#############################################
						
						username = data.find('a',class_='_6qw4')
						if username:
							try:
								username = username.text.strip()
							except:
								pass
						else:
							username = ''
							#############################################
		# 					#          FOR EXTRACTING COMMENT           # 
		# 					#############################################
						try:
							reply_link = data.find('a',class_='_6qw7')['href']
						except:
							reply_link = ''

						comment = data.find('span',class_='_3l3x')
						if comment:
							try:
								comment = comment.text.strip()
								comment = str(comment)
								emoji_pattern = re.compile("["
												u"\U0001F600-\U0001F64F"  # emoticons
												u"\U0001F300-\U0001F5FF"  # symbols & pictographs
												u"\U0001F680-\U0001F6FF"  # transport & map symbols
												u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
												u"\U00002702-\U000027B0"
												u"\U000024C2-\U0001F251"
												u"\U00010000-\U0010ffff"
												"]+", flags=re.UNICODE)
								comment = emoji_pattern.sub(r'', comment)
								if comment is not None:
									comment_cleaned = comment.replace('\d+', '')
									comment_cleaned = re.sub(r'www.\S+|http\S+', '', comment_cleaned)
									comment_cleaned = re.sub(r'[^\w\s]+', '', comment_cleaned)
								else:
									comment_cleaned = ''
								
							except:
								pass
						else:
							comment = ''
							comment_cleaned = ''
						# review_translated = translator.translate([comment_cleaned],dest='en')
						# review_translated = review_translated[0].text
						# import pdb; pdb.set_trace()
		# 				#############################################
		# 				#         FOR POLARITY & SENTIMENTS         # 
		# 				#############################################
						if comment_cleaned is not None:
					
							polarity = self.analyser.polarity_scores(comment_cleaned)
					

							if (polarity["compound"] <= -0.1):
								sentiment = "Very Bad"
							elif (polarity["compound"] > -0.1) and (polarity["compound"]<0.0):
								sentiment = "Bad"
							elif (polarity["compound"] <= 0.0) and (polarity["compound"]>=0.05):
								sentiment = "Neutral"
							elif (polarity["compound"] > 0.05) and (polarity["compound"] < 0.5):
								sentiment = "Good"
							else:
								sentiment = "Very Good"

		# # 				#############################################
		# # 				#          FOR EXTRACTING DATES             # 
		# # 				#############################################
						
						
						date = data.find('a',class_='_6qw7')
						
						if date:
							try:
								date = date.find('abbr')['data-tooltip-content'].split('at')[0].split(',')[1].strip()
								from datetime import datetime
								from dateutil.parser import parse
								date = parse(date)
								date = datetime.strftime(date, '%d-%m-%Y')
							except:
								try:
									date = date.find('abbr').text.strip()
									# date = data_cleaning.data_clean(date)
								except:
									pass
						else:
							date = ''
						# if (post != '') or (comment != ''):
							
						item = {
								'post' : post,
								'like' : like,
								'share' : share,
								'reply_link' : reply_link,
								'no_of_comments' : no_of_comments,
								'username' : username,
								'comment' : comment,
								'comment_cleaned' : comment_cleaned,
								# 'review_translated' : review_translated,
								'polarity' : polarity,
								'sentiment' : sentiment, 
								'date' : date
							}
						yield item
						
			
			except:
				pass
		
################################################################################################################			
			
			
			# 			#############################################
			# 			#         FOR EXTRACTING ALL DATA           # 
			# 			#############################################
			
			# for box in all_box:
			# 	i=0
			# 	while i==0:
					
			# 					#############################################
			# 					#          FOR VIEW MORE COMMENTS           # 
			# 					#############################################
					# try:
					# 	#driver.find_element_by_class_name('UFIPagerLink').click()
					# 	#wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="_4sxc _42ft"]'))) 
					# 	driver.find_element_by_xpath('//*[@class="_4swz _293g"]/a').click()
						
					# except:
					# 	i=1
					
			# 					#############################################
			# 					#         FOR VIEW MORE REPLIES             # 
			# 					#############################################
								
					# try:
					# 	abc = driver.find_elements_by_xpath('//*[@class="_4swz _1i3s _293g"]/a')
					# 	for ab in abc: 
					# 		ab.click()
					# except:
					# 	pass
					
			# 					#############################################
			# 					#         FOR SEE MORE COMMENTS             # 
			# 					#############################################
					
					# try:	'comment_cleaned' : comment_cleaned,
					# 				'Date': date,
					# 				'polarity' : polarity,
					# 				'sentiment' : sentiment
					# 	}
					# 	abd = driver.find_elements_by_xpath('//*[@class="_5v47 fss"]')
					# 	for ad in abd:
					# 		ad.click()
					# except:
					# 	pass
			
			


#################################################################################################################



					#############################################
					#        EXTRACT DATA WITHOUT LOGIN         # 
					#############################################
		# wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="commentable_item"]')))

		# soup = BeautifulSoup(driver.page_source,'lxml')
		# for div2 in soup.findAll('form',class_='commentable_item'):
			
		# 	for div3 in div2.findAll('div',class_='_3b-9 _j6a'):
		# 		for div4 in div3.findAll('div',class_='UFICommentContentBlock'):
					
		# 			#############################################
		# 			#          FOR EXTRACTING USERNAME          # 
		# 			#############################################

		# 			user = div4.find('a',class_='UFICommentActorName')
		# 			username = user.text.strip()
					
		# 			#############################################
		# 			#          FOR EXTRACTING COMMENT           # 
		# 			#############################################
		# 			comment = div4.find('span',class_='UFICommentBody')
		# 			if 'see more' in comment:
		# 				comment = comment.replace('see more','')
					
		# 			comment = comment.text.strip()
					
		# 			#############################################
		# 			#           FOR REMOVING EMOJIS             # 
		# 			#############################################
					
		# 			emoji_pattern = re.compile("["
		# 										u"\U0001F600-\U0001F64F"  # emoticons
		# 										u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		# 										u"\U0001F680-\U0001F6FF"  # transport & map symbols
		# 										u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		# 										u"\U00002702-\U000027B0"
		# 										u"\U000024C2-\U0001F251"
		# 										u"\U00010000-\U0010ffff"
		# 										"]+", flags=re.UNICODE)
		# 			comment = emoji_pattern.sub(r'', comment)
		# 			if comment != '':
		# 				headers = {'Content-Type' : 'application/json'}
		# 				formdata = {'text' : str(comment)}
		# 				comment1 = requests.post('http://ec2-13-233-230-28.ap-south-1.compute.amazonaws.com:5500/', data=json.dumps(formdata), headers=headers)
		# 				translated_comment = comment1.text.strip()

		# 				#############################################
		# 				#            FOR DATA CLEANING              # 
		# 				#############################################
						
		# 				comment_cleaned = str(translated_comment)
		# 				comment_cleaned = comment_cleaned.replace('\d+', '')
		# 				comment_cleaned = re.sub(r'www.\S+|http\S+', '', comment_cleaned)
		# 				comment_cleaned = re.sub(r'[^\w\s]+', '', comment_cleaned)
						
		# 				#######################################	'comment_cleaned' : comment_cleaned,
		# 							'Date': date,
		# 							'polarity' : polarity,
		# 							'sentiment' : sentiment
		# 				}######
		# 				#         FOR POLARITY & SENTIMENTS         # 
		# 				#############################################
						
		# 				polarity = TextBlob(comment_cleaned).sentiment.polarity

		# 				if (polarity <= -0.5) & (polarity >= -1):
		# 					sentiment = 'Very Bad'
		# 				elif (polarity > -0.5) & (polarity < 0.0):
		# 					sentiment = 'Bad'
		# 				elif (polarity <= 0.5) & (polarity > 0.0):
		# 					sentiment = "Good"
		# 				elif (polarity > 0.5) & (polarity <= 1.0):
		# 					sentiment = "Very Good"
		# 				else:
		# 					sentiment = 'Neutral'

		# 				#############################################
		# 				#          FOR EXTRACTING DATES             # 
		# 				#############################################


		# 				date = div4.find(class_='UFISutroCommentTimestamp livetimestamp')
		# 				dates = date['title']
		# 				oldformat=parse(dates)
		# 				new_date = datetime.strftime(oldformat, '%Y-%m-%d')
		# 				date =  new_date
						
		# 				item = { 	
		# 							# 'Post' : post,
		# 							'Username': username,
		# 							'Comment': comment,
		# 							'translated_comment' : translated_comment,
		# 							'comment_cleaned' : comment_cleaned,
		# 							'Date': date,
		# 							'polarity' : polarity,
		# 							'sentiment' : sentiment
		# 				}
		# 				yield item
		# 			else:
		# 				pass
		# else:
		# 	logging.info('NO PAGE FOUND FOR KEYWORD SEARCH')
		# 	pass
		driver.close()