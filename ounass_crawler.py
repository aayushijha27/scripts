# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import csv
import requests
from datetime import datetime

class OunasSpider1(scrapy.Spider):
	name = 'ounass1'
	handle_httpstatus_list = [404,503]
	start_urls = ['https://www.namshi.com/']
	
	def __init__(self,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}

	def parse(self, response):
		with open('new.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				url = row[0]
				url = url.split('.ae')[0]+'.ae/api'+url.split('.ae')[1]
				for items in range(1, 100):
					url = url  + '?sortBy=popularity-asc&p=' + str(items) + '&facets=0'
					yield scrapy.Request(url=url,headers=self.headers,callback=self.parse1)
	
	def parse1(self, response):
		
		abc = json.loads(response.text)['hits']
		for i in range(0,len(abc)):
			brand = abc[i]['designerCategoryName']
			product_description = BeautifulSoup(abc[i]['description'],'lxml').text.strip()
			sale_price = abc[i]['minPrice']
			if sale_price == '':
				sale_price = abc[i]['price']
			original_price = abc[i]['price']
			sizeAndFit = BeautifulSoup(abc[i]['sizeAndFit'],'lxml').text.strip()
			product_code = abc[i]['sku']
			_imageurl = abc[i]['_imageurl']
			product_name = abc[i]['name']
			color = abc[i]['analytics']['color']

			
			disc =  abc[i]['discountText']
			
			
			
			now = datetime.now()
			current_date_time = now.strftime("%d/%m/%Y %H:%M:%S")
			currency_code = response.url
			currency_code = currency_code.split('.')[-1]
			currency_code = currency_code.split('/')[0]
			if currency_code == 'ae':
				currency_code = 'AED'
			else:
				currency_code = 'SAR'


			item = {
				'brand' : brand,
			  'product_description' : product_description,
				'product_name' : product_name,
				'SKU' : product_code,
				'image_url': _imageurl,
				'product_size' : sizeAndFit,
				'Color' : color,
				'sale_price' : sale_price,
				'original_price' : original_price,
				'currency_code' : currency_code,
				'discount_amount' : disc,		
				'Advertiser' : 'Ounass',
				'Last Scraped Time' : current_date_time
				
			}
			yield item 


		
