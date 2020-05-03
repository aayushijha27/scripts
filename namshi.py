# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv

class NamshiSpider1(scrapy.Spider):
	name = 'namshi1'
	start_urls = ['https://www.namshi.com/']
 
	def __init__(self,category=None,subcategory=None,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
		self.category = category
		self.subcategory = 'new-arrivals'
	
	def start_requests(self):
		# if self.category == 'kids':
		# 	url = 'https://en-sa.namshi.com/kids/' + str(self.subcategory)
		# 	yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)
		# elif self.category == 'women':
		# 	url = 'https://en-sa.namshi.com/women/' + str(self.subcategory)
		# 	yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)
		# elif self.category == 'men':
		# 	url = 'https://en-sa.namshi.com/men/' + str(self.subcategory)
		# 	yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)

		url = 'https://en-global.namshi.com/'
		yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)
	
	def parse(self,response):
		pages = int(''.join(response.xpath('//ul[@id="pagination"]/p/text()').extract()).strip().split('of')[1].strip())
		for i in range(1,pages+1):
			url = response.url + 'page-' + str(i)
			yield scrapy.Request(url=url,headers=self.headers,callback=self.parse1)
	
	def parse1(self,response):
		leng = len(response.xpath('//*[@id="catalog_listings"]/li').extract())
		for i in range(1,leng+1):
			product_link = 'https://en-sa.namshi.com' + ''.join(response.xpath('//*[@id="catalog_listings"]/li['+str(i)+']/a/@href').extract())
			yield scrapy.Request(url=product_link,headers=self.headers,callback=self.parse2)
	
	def parse2(self,response):
		brand_name = response.xpath("//h2/a/text()").extract()
		product_url = response.url
		product_name = ''.join(response.xpath("//h1[@class='product__name']/text()").extract())
		product_price = ''.join(response.xpath("//span[@class='pre-reduction']/text()").extract())
		price = ''.join(response.xpath("//div[@class='product__details']/p/span/text()").extract()[0])
		reduction_price = ''.join(response.xpath("//span[@class='reduction']/text()").extract())
		product_usps = ''.join(response.xpath("//section[@class='product-usps']/div/text()").extract())
		delivery = ''.join(response.xpath("//p[@class='product__deliveryestimation']/text()").extract()).strip()
		rewards = ''.join(response.xpath("//div[@class='skywards_reward_miles']/text()").extract())
		product_description = ''.join(response.xpath("//div[@class='info_shortdescription info_content']/ul/li/text()").extract())
		offer = ''.join(response.xpath("//div[@class='catalog-tag']/text()").extract())
		product_size = ''.join(response.xpath("//ul[@id='product_size']/li/label/span/text()").extract())
		img_url = ''.join(response.xpath('//*[@id="product_carousel"]/div[2]/img/@src').extract())

		soup = BeautifulSoup(response.text,'lxml')

		table = soup.find('table',class_='product_attributes')
		info_care = {}
		for tr in table.findAll('tr'):
			key = tr.findAll('th')[0].text.strip()
			value = tr.findAll('th')[1].text.strip()
			info_care[key] = value
  		
		item = {
				'Brand name' : brand_name,
				'Product name' : product_name,
				'Product price' : product_price,
				'Reduction price' : reduction_price,
				'Product usps' : product_usps,
				'Delivery' : delivery,
				'Product_url' : product_url,
				'Rewards' : rewards,
				'Product description' : product_description,
				'Info care' : info_care,
				'Offer' : offer,
				'Price' : price,
				'Product size' : product_size,
				'Image url' : img_url
				
				}  
		yield item     
