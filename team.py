# -*- coding: utf-8 -*-
import scrapy
import time
import json
from bs4 import BeautifulSoup
import pymongo

class TeamSpider(scrapy.Spider):
	name = 'team'
	start_urls = ['https://www.icc-cricket.com/']
	################# Add Connection ############
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	################# Create/Add Database ###########
	mydb = myclient["cricket"]
	################ Create collection/table ############
	mycol = mydb["oditeamrankmen"]
	def parse(self, response):
		url = 'https://www.icc-cricket.com/rankings/mens/team-rankings/odi'
		yield scrapy.Request(url=url,callback=self.parse1)

	def parse1(self, response):
		
		soup = BeautifulSoup(response.text,'lxml')
		############ create list #############
		mylist = []

		table = soup.find('table').find('tbody')
		for tr in table.findAll('tr'):
			data = tr.findAll('td')
			
			position = data[0].text.strip()
			team = data[1].text.strip()
			weighted_matches = data[2].text.strip()
			points = data[3].text.strip()
			rating = data[4].text.strip()

			item = 		{
							'position': position,
							'team': team,
							'weight':weighted_matches,
							'points':points,
							'rating':rating,
							# 'type' : '',
							'category':'ODI'
						}
			############ append results into list #############
			mylist.append(item)

			print(item)
		############# insert multiple results in mongodb in the form of list ####################
		x = self.mycol.insert_many(mylist)