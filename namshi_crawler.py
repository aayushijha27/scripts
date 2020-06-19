# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
from datetime import datetime

class NamshiSpider1(scrapy.Spider):
	name = 'namshi1'
	handle_httpstatus_list = [404,503]
	start_urls = ['https://www.namshi.com/']
 
	def __init__(self,state=None,subcategory=None,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
		# self.state=state
	
	def start_requests(self):
		with open('namshi.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				main_url = row[0]
				
				yield scrapy.Request(url=main_url,headers=self.headers,callback=self.parse)
	
	def parse(self,response):
		pages = int(''.join(response.xpath('//ul[@id="pagination"]/p/text()').extract()).strip().split('of')[1].strip())
		for i in range(1,pages+1):
			url = response.url + 'page-' + str(i)
			
			yield scrapy.Request(url=url,headers=self.headers,callback=self.parse1)
	
	def parse1(self,response):
		
		leng = len(response.xpath('//*[@id="catalog_listings"]/li').extract())
		# import pdb; pdb.set_trace()
		link = response.url 
		# link = link.split('/')[2]
		
		if 'en-oman.namshi.com' in link:

			for i in range(1,leng+1):
				product_link = 'https://en-oman.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract()) 
			
				yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
		elif 'en-ae.namshi.com' in link:
			for i in range(1,leng+1):
				product_link = 'https://en-ae.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract()) 
			
				yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
		elif 'en-sa.namshi.com' in link:
			for i in range(1,leng+1):
				product_link = 'https://en-sa.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract()) 
			
				yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
		
		elif 'ar-oman.namshi.com' in link:

			for i in range(1,leng+1):
				product_link = 'https://ar-oman.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract()) 
			
				yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
		elif 'ar-ae.namshi.com' in link:
			for i in range(1,leng+1):
				product_link = 'https://ar-ae.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract()) 
			
				yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
		elif 'ar-sa.namshi.com' in link:
			for i in range(1,leng+1):
				product_link = 'https://ar-sa.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract()) 
			
				yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
		
	
	def parse2(self,response):
		brand = ''.join(response.xpath("//h2/a/text()").extract()).strip()
		product_url = response.url
		title = ''.join(response.xpath("//h1[@class='product__name']/text()").extract())
		actual_price = ''.join(response.xpath("//span[@class='pre-reduction']/text()").extract()).replace('AED','').replace('SAR','').replace('OMR','') or ''.join(response.xpath("//div[@class='product__details']/p/span/text()").extract()[0]).replace('AED','').replace('SAR','').replace('OMR','')
		
		sale_price = ''.join(response.xpath("//span[@class='reduction']/text()").extract()).replace('AED','').replace('SAR','').replace('OMR','')
		
		if sale_price == '':
			sale_price = actual_price
		else:
			pass
		
		product_description = ''.join(response.xpath("//div[@class='info_shortdescription info_content']/ul/li/text()").extract()) or ''.join(response.xpath("//div[@class='info_shortdescription info_content']/p/font/text()").extract())
		product_size = ''.join(response.xpath("//ul[@id='product_size']/li/label/span/text()").extract())
		img_url = ''.join(response.xpath('//*[@id="product_carousel"]/div[1]/img/@src').extract())
		discount_amt = ''.join(response.xpath("//span[@class='reduction_message_amount']/text()").extract())
		currency_code = response.xpath("//p[@class='product__price']/span/text()").extract()[0].split()[1]
		now = datetime.now()
		current_date_time = now.strftime("%d/%m/%Y %H:%M:%S")
		
		
		# import pdb; pdb.set_trace()
		item = {
				'brand' : brand,
				'product_name' : title,
				'original_price' : actual_price,
				'sale_price' : sale_price,
				'product_url' : product_url,
				'product description' : product_description,
				'product size' : product_size,
				'image_url' : img_url,
				'discount_amount' : discount_amt,
				'currency_code' : currency_code,
				'Advertiser' : 'Namshi',
				'Last Scraped Time' : current_date_time

				}  
		soup = BeautifulSoup(response.text,'lxml')
		table = soup.find('table',class_='product_attributes')
		for tr in table.findAll('tr'):
			key = tr.findAll('th')[0].text.strip()
			value = tr.findAll('th')[1].text.strip()
			item[key] = value
		yield item     
