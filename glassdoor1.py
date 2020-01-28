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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.parser import parse
import selenium as se
from scrapy.http import HtmlResponse


class playstoreSpider(scrapy.Spider):
	name = 'glassdoor1'
	start_urls = ['https://www.glassdoor.co.in/Reviews/index.htm']
	limit=5
	
	def __init__(self, text=None, param=None, *args, **kwargs):
		self.text = 'Naukri.com'
		self.headers = { 
					'Upgrade-Insecure-Requests' : '1',
					'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
					'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		}
	
	def parse(self,response):
		if ' ' in self.text:
			self.text = self.text.replace(' ','+')
		url = 'https://www.glassdoor.co.in/Reviews/company-reviews.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword='+str(self.text)+'&sc.keyword='+str(self.text)+'&locT=&locId=&jobType='
		yield scrapy.Request(url, headers=self.headers, callback=self.parse1, dont_filter=True)
	
	def parse1(self,response):
		if 'Work here? Get a FREE Employer Account' in response.text:
			yield scrapy.Request(response.url, headers=self.headers, callback=self.parse2)
		else:
			try:
				url = ''.join(response.xpath('//*[@id="MainCol"]/div[1]/div[2]/div[1]/div[2]/div[1]/a/@href').extract())
				url = 'https://www.glassdoor.co.in' + str(url)
				yield scrapy.Request(url, headers=self.headers, callback=self.parse2)
			except:
				pass
		
	def parse2(self,response):
		reviews = ''.join(response.xpath('//*[@id="EIProductHeaders"]/div/a[2]/span[1]/text()').extract()).strip()
		url = ''.join(response.xpath('//*[@id="EIProductHeaders"]/div/a[2]/@href').extract())
		url = 'https://www.glassdoor.co.in' + str(url)

		yield scrapy.Request(url, headers=self.headers, callback=self.parse3, dont_filter = True)
		
	def parse3(self,response):

		no_reviews = ''.join(response.xpath('//*[@id="EIProductHeaders"]/div/a[2]/span[1]/text()').extract()).strip()
		if no_reviews:
			if '.' in no_reviews:
				no_reviews = no_reviews.replace('.','')
			
			if ',' in no_reviews:
				no_reviews = no_reviews.replace(',','')
			
			if ('k' in no_reviews) and (len(no_reviews) > 2):
				no_reviews = no_reviews.strip().replace('k','00')
			
			elif ('k' in no_reviews) and (len(no_reviews) <= 2):
				no_reviews = no_reviews.strip().replace('k','000')
			
			rang = int(int(no_reviews)/10)
			
			if int(rang) == 0:
				rang = 2

			url1 = response.url.split('.h')[0]
			
			for i in range(1,int(rang)):
				url = url1 + '_P' + str(i) + '.htm'
				yield scrapy.Request(url, headers=self.headers, callback = self.parse4, dont_filter=True)
		
		
	def parse4(self,response):
		text = response.xpath('//div[@class="hreview"]').extract()
		if text:
			for items in text:
				items = HtmlResponse(url="my html string", body=items, encoding='utf-8')
				
				date = ''.join(items.xpath('//time[@class="date subtle small"]/text()').extract()).strip()
				if date:
					date = date
				else:
					date = ''
				
				location = ''.join(items.xpath('//span[@class = "authorLocation"]/text()').extract()).strip()
				if location:
					location = location
				else:
					location = ''
				
				pros = items.xpath('//p[@class = " pros mainText truncateThis wrapToggleStr"]/text()').extract()
				if pros:
					pros = ''.join(pros).strip()
				else:
					pros = items.xpath('//p[@class = "pros mainText truncateThis wrapToggleStr"]/text()').extract()
				
				cons = items.xpath('//p[@class = " cons mainText truncateThis wrapToggleStr"]/text()').extract()
				if cons:
					cons = ''.join(cons).strip()
				else:
					cons = items.xpath('//p[@class = "cons mainText truncateThis wrapToggleStr"]/text()').extract()
				
				string = str(pros) + " " + str(cons)
				if (date != '14 Mar 2018' and location != 'Mbuji-Mayi (Democratic Republic of Congo)') and (date != '8 Jan 2018' and location != 'Lubumbashi (Democratic Republic of Congo)') and (date != '23 Sep 2018' and location != 'Libreville (Gabon)') and (date != '1 Jul 2018' and location != ''):
					item = {
									'date' : date,
									'location' : location,
									'review' : string
					}
					yield item