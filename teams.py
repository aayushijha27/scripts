# -*- coding: utf-8 -*-
import scrapy
import time
import json
from bs4 import BeautifulSoup

class TeamsSpider(scrapy.Spider):
	name = 'teams'
	start_urls = ['https://www.cricbuzz.com/']
	def parse(self, response):
		url = 'https://www.cricbuzz.com/cricket-stats/icc-rankings/women/teams'
		yield scrapy.Request(url=url,callback=self.parse1)

	def parse1(self, response):

		
		soup = BeautifulSoup(response.text,'lxml')
		i=0
		for table in soup.findAll('div',class_='cb-col cb-col-100 cb-padding-left0'):
			if i==0:
				category = 'ODI'
			elif i==1:
				category = 'T20'
			i+=1
			for div in table.findAll('div',class_='cb-col cb-col-100 cb-font-14 cb-brdr-thin-btm text-center'):
				data = div.findAll('div')
				
				position = data[0].text.strip()
				team = data[1].text.strip()
				rating = data[2].text.strip()
				points = data[3].text.strip()
				
				item = 		{
								'position': position,
								'team': team,
								'rating':rating,
								'points':points,
								'category':category
								# 'type' : '',
								
							}
				yield item
