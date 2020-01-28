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

class InstaSpider(scrapy.Spider):
	name = 'instagram'
	start_urls = ['https://www.instagram.com/accounts/emailsignup/']
	limit=20

	def __init__(self, text=None, mail=None, password=None, param=None, *args, **kwargs):
		self.text = text
	
	def parse(self,response):
		options = se.webdriver.ChromeOptions()
		prefs = {"profile.default_content_setting_values.notifications" : 2}
		options.add_experimental_option("prefs",prefs)
		# options.add_argument('headless')
		path = os.getcwd() + '/chromedriver'
		driver = se.webdriver.Chrome(chrome_options=options, executable_path=path)
		wait = WebDriverWait(driver,20)
		
		driver.get('https://www.instagram.com/'+str(self.text)+'/?hl=en')
		data = driver.find_elements_by_xpath('//*[@class="-nal3 "]')
		handle_post = ''
		handle_followers = ''
		handle_following = ''
		for dat in data:
			if 'post' in dat.text:
				handle_post = dat.text.strip()
				if 'posts' in  handle_post:
					handle_post = handle_post.replace('posts','')
				if 'post' in handle_post:
					handle_post = handle_post.replace('post','')
				if '.' in handle_post:
					handle_post = handle_post.replace('.','')
				if ',' in handle_post:
					handle_post = handle_post.replace(',','')
				if 'K' in handle_post:
					handle_post = handle_post.replace('K','000')
				if 'M' in handle_post:
					handle_post = handle_post.replace('M','0000')
				if 'B' in handle_post:
					handle_post = handle_post.replace('B','00000')
			elif 'follower' in dat.text:
				handle_followers = dat.text.strip()
				if 'followers' in  handle_followers:
					handle_followers = handle_followers.replace('followers','')
				if 'follower' in handle_followers:
					handle_followers = handle_followers.replace('follower','')
				if '.' in handle_followers:
					handle_followers = handle_followers.replace('.','')
				if ',' in handle_followers:
					handle_followers = handle_followers.replace(',','')
				if 'K' in handle_followers:
					handle_followers = handle_followers.replace('K','000')
				if 'M' in handle_followers:
					handle_followers = handle_followers.replace('M','0000')
				if 'B' in handle_followers:
					handle_followers = handle_followers.replace('B','00000')
			elif 'following' in dat.text:
				handle_following = dat.text.strip()
				if 'following' in  handle_following:
					handle_following = handle_following.replace('following','')
				if '.' in handle_following:
					handle_following = handle_following.replace('.','')
				if ',' in handle_following:
					handle_following = handle_following.replace(',','')
				if 'K' in handle_following:
					handle_following = handle_following.replace('K','000')
				if 'M' in handle_following:
					handle_following = handle_following.replace('M','0000')
				if 'B' in handle_following:
					handle_following = handle_following.replace('B','00000')
		
		url_list = []
		for item in range(int(self.limit)):
			wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
			sleep(3)
			urls = driver.find_elements_by_xpath('//*[@class="v1Nh3 kIKUG  _bz0w"]/a')
			for url in urls:
				url_list.append(url.get_attribute('href'))
		
		unique_list = []
		for x in url_list:
			if x not in unique_list:
				unique_list.append(x)
		
		# import pdb; pdb.set_trace()
		# next_u = []
		# for next_url in unique_list:
		# 	next_u.append(next_url)
		
		for next_ur in unique_list:
			driver.get(next_ur)
			wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="C4VMK"]')))
			flag=1
			while flag<=5:
				try:
					driver.find_element_by_xpath('//*[@class="glyphsSpriteCircle_add__outline__24__grey_9 u-__7"]').click()
				except:
					break
				flag+=1
			comm = driver.find_element_by_xpath('//*[@class="C4VMK"]')
			try:
				post_location = driver.find_element_by_xpath('//*[@class="O4GlU"]').text.strip()
			except:
				post_location = ''
			post_username = comm.find_element_by_xpath('//*[@class="_6lAjh"]').text
			try:
				post = comm.find_element_by_xpath('//*[@title="Edited"]').text
			except:
				posts = comm.text.split('\n')[1:-1]
				post = ''		
				for pos in posts:
					post = str(post) + ' ' + str(pos)
				post = post.strip()
			post_date = comm.find_element_by_xpath('//*[@class="FH9sR Nzb55"]').get_attribute('title')
			try:
				post_views = driver.find_element_by_xpath('//*[@class="vcOH2"]').text
				if 'views' in post_views:
					post_views = post_views.replace('views','').strip()
				if 'view' in post_views:
					post_views = post_views.replace('view','').strip()
				if ',' in post_views:
					post_views = post_views.replace(',','').strip()
			except:
				post_views = ''
			try:
				post_likes = driver.find_element_by_xpath('//*[@class="Nm9Fw"]').text
				if 'likes' in post_likes:
					post_likes = post_likes.replace('likes','').strip()
				if 'like' in post_likes:
					post_likes = post_likes.replace('like','').strip()
				if ',' in post_likes:
					post_likes = post_likes.replace(',','').strip()
			except:
				post_likes = ''
			
			comm_len = driver.find_elements_by_xpath('//*[@class="C4VMK"]')
			for comm in comm_len[1:]:
				try:
					time = comm.find_element_by_xpath('//*[@class="FH9sR Nzb55"]').get_attribute('title')
					time = parse(time)
					time = datetime.strftime(time, '%d-%m-%Y')
				except:
					time = ''		
				try:
					user_data = comm.text.split('\n')
					username = user_data[0]
					comment = user_data[1]
					try:
						comment_like = comm.find_element_by_xpath('//*[@class="FH9sR"]').text
						if 'likes' in comment_like:
							comment_like = comment_like.replace('likes','').strip()
						if 'like' in comment_like:
							comment_like = comment_like.replace('like','').strip()
						if ',' in comment_like:
							comment_like = comment_like.replace(',','').strip()
						if 'Reply' in comment_like:
							comment_like = comment_like.replace('Reply','').strip()
					except:
						comment_like = ''
					# user_link = comm.find_element_by_tag_name('a')
					# user_link.send_keys(Keys.CONTROL + Keys.RETURN)
					# WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2)) 
					# main_window = driver.window_handles[0]
					# new_window = driver.window_handles[1]
					# driver.switch_to_window(new_window)
					
					# soup = BeautifulSoup(driver.page_source,'lxml')
					# soup1 = soup.findAll('li',class_='Y8-fY')
					# posts = ''
					# followers = ''
					# following = ''
					# for li in soup1:
					# 	if 'posts' in li.text:
					# 		posts =  li.find('span').text.strip()
					# 		if ',' in posts:
					# 			posts = posts.replace(',','')
					# 	elif 'followers' in li.text:
					# 		followers = li.find('span')
					# 		try:
					# 			followers = followers['title']
					# 		except:
					# 			followers = followers.find('span')
					# 			followers = followers['title']
					# 		if ',' in followers:
					# 			followers = followers.replace(',','')
					# 	elif 'following' in li.text:
					# 		following = li.find('span').text.strip()
					# 		if ',' in following:
					# 			following = following.replace(',','') 
					item = {
							'handle_posts' : str(handle_post),
							'handle_followers' : str(handle_followers),
							'handle_following' : str(handle_following),
							'post_username' : str(post_username),
							'post_location' : str(post_location),
							'post' : str(post),
							'post_date' : str(post_date),
							'post_views' : str(post_views),
							'post_likes' : str(post_likes),
							'username' : str(username),
							'comment' : str(comment),
							'comment_like' : str(comment_like),
							'comment_date' : str(time),
							'post_link' : str(next_ur)
							# 'no_of_posts' : str(posts),
							# 'no_of_followers' : str(followers),
							# 'no_of_following' : str(following),
						}
					yield item
				except:
					pass
				# driver.close()
				# driver.switch_to_window(main_window)
			# wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ckWGn"]')))
				
		driver.close()

