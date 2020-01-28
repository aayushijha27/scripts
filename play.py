# -*- coding: utf-8 -*-
import scrapy
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.parser import parse
import selenium as se

class PlaySpider(scrapy.Spider):
	name = 'play'
	start_urls = ['https://play.google.com/store/apps']
	
	def __init__(self, text=None, limit=None, param=None, *args, **kwargs):
		# self.text = json.loads(param)['text']
		# self.key = int(json.loads(param)['key'])
		self.text = text
		self.limit = int(limit)
	
	def parse(self,response):
		options = se.webdriver.ChromeOptions()
		# options.add_argument('headless')
		path = os.getcwd()+'/chromedriver'
		driver = se.webdriver.Chrome(chrome_options=options, executable_path=path)
		wait = WebDriverWait(driver,50)
		driver.get(response.url)
		sleep(3)
		########################### For text ################################
		# wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="gbqfq"]'))).send_keys(self.text)
		# wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="gbqfb"]'))).click()
		# sleep(3)
		# app_name = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/c-wiz/c-wiz/c-wiz/div/div[2]/div[1]/c-wiz/div/div/div[2]/div/div/div[1]/div/div/div[1]/a/div').text
		# app_url = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/c-wiz/c-wiz/c-wiz/div/div[2]/div[1]/c-wiz/div/div/div[2]/div/div/div[1]/div/div/div[1]/a').get_attribute('href')

		# if ' ' in self.text:
		# 	self.text = self.text.split(' ')[0]
		
		# if (self.text in app_url) or (self.text in app_name):
		####################################################################

		################################ For URL Specific #################################
		# app_url = 'https://play.google.com/store/apps/details?id=com.zoomcar&hl=en'
		app_url = 'https://play.google.com/store/apps/details?id=com.locon.housing&hl=en'
		###################################################################################
		driver.get(app_url)
		driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[6]/div').click()
		for item in range(int(self.limit)):
			wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
			sleep(3)
			try:
				driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div').click()
			except:
				pass
		comments_list = []
		soup = BeautifulSoup(driver.page_source,'lxml')
		for div in soup.findAll('div',jscontroller='H6eOGe'):
			# print(div)
			try:
				user_name = div.find('span',class_='X43Kjb')
				username =  user_name.text.strip()
			except:
				username = ''
			try:
				review_date = div.find('span',class_='p2TkOb')
				date = review_date.text.strip()
				# date = data_cleaning.data_clean(date)
				date = parse(date)
				date = datetime.strftime(date, '%d-%m-%Y')
			except:
				date = ''
			try:
				review = div.find('span',jsname='bN97Pc')
				review = review.text.strip()
				emoji_pattern = re.compile("["
											u"\U0001F600-\U0001F64F"  # emoticons
											u"\U0001F300-\U0001F5FF"  # symbols & pictographs
											u"\U0001F680-\U0001F6FF"  # transport & map symbols
											u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
											"]+", flags=re.UNICODE)
				review = emoji_pattern.sub(r'', review)
			except:
				review = ''
			
			item = {
									'Post' : '',
									'Username': str(username),
									'Comment': str(review),
									'Date': str(date),
									'source' : 'Playstore'
								}

			# print(comments_list)
			yield item
			# driver.close()
			# comment = []
			# date = []
			# source1 = []
			# for item in comments_list:
			# 	comment.append(item['Comment'])
			# 	date.append(item['Date'])
			# 	source1.append(item['source'])
			
			# data_frame.make_dataframe(date, comment, source1, self.text, key1=self.key)

		# else:
		# driver.close()
