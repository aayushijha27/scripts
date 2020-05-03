# -*- coding: utf-8 -*-
import scrapy
import csv
import pandas as pd

class NamshiSpider(scrapy.Spider):
	name = 'namshi'
	custom_settings = {'HTTPERROR_ALLOW_ALL': True}
	handle_httpstatus_list = [301,500, 502, 503, 504, 400, 403, 408]
	start_urls = ['https://www.namshi.com/']
 
	def __init__(self,text=None,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
	def parse(self, response):
		with open('test.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				product_url = row[13]
				# url = 'https://en-sa.namshi.com/buy-nike-nsw-shine-cropped-t-shirt-w589034a.html'
				yield scrapy.Request(url=product_url,headers=self.headers,callback=self.parse1)
	
	def parse1(self, response):
		try:
			product_price = response.xpath("//span[@class='pre-reduction']/text()").extract()
			if product_price != " ": 
				brand_name = ''.join(response.xpath("//h2/a/text()").extract())
				product_url = response.url
				product_name = ''.join(response.xpath("//h1[@class='product__name']/text()").extract())
				price = response.xpath("//div[@class='product__details']/p/span/text()").extract()[0]
				reduction_price = response.xpath("//span[@class='reduction']/text()").extract()
				product_usps = ''.join(response.xpath("//section[@class='product-usps']/div/text()").extract())
				delivery = ''.join(response.xpath("//p[@class='product__deliveryestimation']/text()").extract()).strip()
				rewards = ''.join(response.xpath("//div[@class='skywards_reward_miles']/text()").extract())
				product_description = ''.join(response.xpath("//div[@class='info_shortdescription info_content']/ul/li/text()").extract())
				info_care = ''.join(response.xpath("//div[@class='info_content']/table/tr/th/text()").extract())
				offer = ''.join(response.xpath("//div[@class='catalog-tag']/text()").extract())
				product_size = response.xpath("//ul[@id='product_size']/li/label/span/text()").extract()
				img_url = ''.join(response.xpath('//*[@id="product_carousel"]/div[2]/img/@src').extract())
		# import pdb; pdb.set_trace()
		except:
			pass
		item = {'Brand name' : brand_name,
				'Product name' : product_name,
				'Product price' : product_price,
				'Price' : price,
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

		