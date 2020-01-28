# -*- coding: utf-8 -*-
import scrapy
import time
import json
from bs4 import BeautifulSoup
from . import dataframe

class CricketSpider(scrapy.Spider):
	name = 'cricket'
	start_urls = ['https://www.cricbuzz.com/']
	def parse(self, response):
		url = 'https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting'
		yield scrapy.Request(url=url,callback=self.parse1)

	def parse1(self, response):
		
		soup = BeautifulSoup(response.text,'lxml')
		i = 0
		for div in soup.findAll('div',class_='cb-col cb-col-100 cb-padding-left0'):
			if i==0:
				category = 'TEST'
			elif i==1:
				category = 'ODI'
			elif i==2:
				category = 'T20'
			i+=1
			for div1 in div.findAll('div',class_='cb-col cb-col-100 cb-font-14 cb-lst-itm text-center'):
				position = div1.find('div',class_='cb-col cb-col-16 cb-rank-tbl cb-font-16').text.strip()
				name = div1.find('a',class_='text-hvr-underline text-bold cb-font-16').text.strip()
				country = div1.find('div',class_='cb-font-12 text-gray').text.strip()
				rating = div1.find('div',class_='cb-col cb-col-17 cb-rank-tbl pull-right').text.strip()
				# item = 		{
				# 				'position': position,
				# 				'name': name,
				# 				'country':country,
				# 				'rating':rating,
				# 				'category':category
				# 				# 'type' : '',
								
				# 			}
				# yield item

				position = []
				name = []
				country = []
				rating = []
				type = []
				category = [] 

				position.append(str(position))
				name.append(str(name))
				rating.append(str(rating))
				type.append(str(type))
				category.append(str(category))

				dataframe.player_df(self,position,name,country,rating,type,category)


