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



class FacebookAnalyticsSpider(scrapy.Spider):
	name = 'facebook_analytics'
	start_urls = ['https://www.facebook.com/']
	
	def __init__(self, limit=None, text=None, mail=None, password=None, url=None, *args, **kwargs):
		self.limit = '10'
		self.text = text
		self.url = 'https://www.facebook.com/pg/tradeindia/posts/?ref=page_internal'
		self.mail = 'aayushijha27@gmail.com'
		self.passsword = 'lenevo2019'
	
	def parse(self,response):
		options = se.webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		options.add_experimental_option("prefs",prefs)
		# options.add_argument('headless')
		path = os.getcwd() + '/chromedriver'
		driver = se.webdriver.Chrome(chrome_options=options, executable_path=path)
		wait = WebDriverWait(driver,50)
		driver.get(response.url)

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

		driver.get(self.url)

		sleep(5)
		for item in range(int(self.limit)):
			wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
			sleep(3)
		
		
		wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="_1dwg _1w_m _q7o"]')))
		try:
			no_of_posts = len(driver.find_elements_by_xpath('//*[@class="_1dwg _1w_m _q7o"]'))
		except:
			no_of_posts = 0
		
		try:
			no_of_likes = driver.find_elements_by_xpath('//*[@class="_3dlg"]/span/span')
			if no_of_likes:
				total_no_of_likes = 0
				for likes in no_of_likes:
					if likes:
						likes = likes.text
						if 'likes' in likes:
							likes = likes.replace('likes','').strip()
						if 'like' in likes:
							likes = likes.replace('like','').strip()
						if '.' in likes:
							likes = likes.replace('.','')
						if ',' in likes:
							likes = likes.replace(',','')
						if 'K' in likes:
							likes = likes.replace('K','000')
						if 'M' in likes:
							likes = likes.replace('M','0000')
						if 'B' in likes:
							likes = likes.replace('B','00000')
					
						total_no_of_likes = int(total_no_of_likes) + int(likes)
		except:
			total_no_of_likes = 0
		
		
		total_no_of_comments = 0
		no_of_comments = driver.find_elements_by_xpath('//*[@class="_3hg- _42ft"]')
		if no_of_comments:
			total_no_of_comments = 0
			for comments in no_of_comments:
				if comments:
					comments = comments.text

					if 'Comments' in comments:
						comments = comments.replace('Comments','').strip()
					if 'Comment' in comments:
						comments = comments.replace('Comment','').strip()
					if '.' in comments:
						comments = comments.replace('.','')
					if ',' in comments:
						comments = comments.replace(',','')
					if 'K' in comments:
						comments = comments.replace('K','000')
					if 'M' in comments:
						comments = comments.replace('M','0000')
					if 'B' in comments:
						comments = comments.replace('B','00000')

					total_no_of_comments = int(total_no_of_comments) + int(comments)
		

		
		total_no_of_shares = 0
		no_of_shares = driver.find_elements_by_xpath('//*[@class="_3rwx _42ft"]')
		if no_of_shares:
			total_no_of_shares = 0
			for shares in no_of_shares:
				if shares:
					shares = shares.text
				if 'Shares' in shares:
					shares = shares.replace('Shares','').strip()
				if 'Share' in shares:
					shares = shares.replace('Share','').strip()
				if '.' in shares:
					shares = shares.replace('.','')
				if ',' in shares:
					shares = shares.replace(',','')
				if 'K' in shares:
					shares = shares.replace('K','000')
				if 'M' in shares:
					shares = shares.replace('M','0000')
				if 'B' in shares:
					shares = shares.replace('B','00000')

				total_no_of_shares = int(total_no_of_shares) + int(shares)

		item = {
				'total_no_of_posts' : str(no_of_posts),
				'total_no_of_likes' : str(total_no_of_likes),
				'total_no_of_comments' : str(total_no_of_comments),
				'total_no_of_shares' : str(total_no_of_shares)
			}
		yield item 
		# print(item)