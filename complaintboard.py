# -*- coding: utf-8 -*-
import scrapy

class ComplaintboardSpider(scrapy.Spider):
	name = 'complaintboard'
	def __init__(self, text=None, key=None, param=None, *args, **kwargs):
		# self.text = json.loads(param)['text']
		# self.key = int(json.loads(param)['key'])
		self.text=text
		self.key=key
		
	def start_requests(self):
		self.text = self.text.title()
		# if ' ' in self.text:
		# 	self.text = self.text.replace(' ','%20') 
		
		for i in range(1, 40):
			url = 'https://www.complaintboard.in/?search=' + str(self.text) + '&page=' + str(i)
			yield scrapy.Request(url=url, callback=self.parse)
	
	def parse(self, response):
		head = response.xpath('//h4/a/@href').extract()
		for head in head:
			head = 'https://www.complaintboard.in'+str(head)
			#import pdb; pdb.set_trace()
			yield scrapy.Request(head, callback=self.actual)
		
	def actual(self, response):
		reviews = ''.join(response.xpath("//td[@class='complaint']/div/div/text()").extract()).strip()
		if '\n' in reviews:
			reviews = reviews.replace('\n',' ')
		date = ''.join(response.xpath("//tr/td[@class='small']/text()").extract()).strip()
		if '\xa0' in date:
			date = date.replace('\xa0','')
		# import pdb; pdb.set_trace()

		item = {'Reviews':reviews,'Date':date}
		yield(item)

		

		



	
	
	
	
	
	
	