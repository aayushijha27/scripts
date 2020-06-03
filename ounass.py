# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv

class OunassSpider1(scrapy.Spider):
	name = 'ounass'
	handle_httpstatus_list = [404,503,302,301,303,307]
	start_urls = ['https://www.ounass.ae/']
	def __init__(self,category=None,subcategory=None,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
	
	def start_requests(self):
		# url = 'https://www.ounass.ae/shop-bernadette-floral-cotton-balloon-skirt-for-women-213805053_23.html'
		# yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)
		with open('data.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				product_url = row[0]
				yield scrapy.Request(url=product_url,dont_filter=True,headers=self.headers,callback=self.parse,meta={'product_url': row[0] })

	def parse(self,response):
		product_url = response.meta['product_url']
		brand = ''.join(response.xpath("//div[@class='Brief']/a/text()").extract())
		product_name = ''.join(response.xpath("//div[@class='Brief-title']/text()").extract())
		product_sale_price =  ''.join(response.xpath("//span[@class='Brief-minPrice']/text()").extract()).replace('AED','')
		product_original_price = ''.join(response.xpath("//span[@class='Brief-price']/text()").extract()).replace('AED','')
		if product_original_price == '':
			product_original_price = ''.join(response.xpath("//span[@class='Brief-minPrice']/text()").extract()).replace('AED','')
		product_id = ''.join(response.xpath("//div[@class='Share-sku']/text()").extract()).split()[2]
		reward = ''.join(response.xpath("//span[@class='EarnAmberPoints-points']/text()").extract())
		editor_advice = response.xpath("//div[@class='TabView TabView__default TabView__briefCopyAttributes']/div/div/div/p/text()").extract()[0]
		img_url = response.xpath("//div[@class='Gallery']/div/button/img/@src").extract()[0]
		img_url = 'https:' + img_url
		img_url_1 = response.xpath("//div[@class='Gallery']/div/button/img/@src").extract()[1]
		img_url_1 = 'https:' + img_url_1
		img_url_2 = response.xpath("//div[@class='Gallery']/div/button/img/@src").extract()[2]
		img_url_2 = 'https:' + img_url_2
		

		# more_options_links = ''.join(response.xpath("//div[@class='Product-hoverPartial']/a/@href").extract())
		

		more_options_names  = response.xpath("//div[@class='Product-name']/text()").extract()
		more_options_price = response.xpath("//span[@class='Product-minPrice']/text()").extract()
		more_options = dict(zip(more_options_names , more_options_price))
		import pdb; pdb.set_trace()
		item = { 

			'product_url' : product_url,
			'brand' : brand,
			'product_name' : product_name,
			'reward' : reward,
			'product_id' : product_id,
			'product_sale_price' : product_sale_price,
			'product_original_price' : product_original_price,
			'img_url' : img_url,
			'img_url_1' : img_url_1,
			'img_url_2' : img_url_2,
			'more_options' : more_options
		}
		yield item 
		
		# import pdb; pdb.set_trace()