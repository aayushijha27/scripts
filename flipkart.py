import scrapy
import csv 
from bs4 import BeautifulSoup
class FlipkartSpider(scrapy.Spider):

	# Spider name
	name = 'flipkart'
	handle_httpstatus_list = [404,503]
	# Domain names to scrape
	allowed_domains = ['flipkart.com']
	start_urls = ['www.flipkart.com/']
 
	def __init__(self,text=None,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
		
	def parse(self, response):
		with open('data.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				product_url = row[0]
				yield scrapy.Request(url=product_url,dont_filter=True,headers=self.headers,callback=self.parse1,meta={'product_url':row[0])
	
	
	def parse(self, response):
		brand = response.xpath("//span[@class='_2J4LW6']/text()").extract()
		product_name = ''.join(response.xpath("//span[@class='_35KyD6']/text()").extract())
		sale_price = response.xpath("//div[@class='_1vC4OE _3qQ9m1']/text()").extract()
		original_price = response.xpath("//div[@class='_3auQ3N _1POkHg']/text()").extract()[1]
		discount_percentage = response.xpath("//div[@class='VGWI6T _1iCvwn _9Z7kX3']/span/text()").extract()
		star_rating = response.xpath("//div[@class='hGSR34 bqXGTW']/text()").extract()
		no.of_rating = ''.join(response.xpath("//span[@class='_38sUEc']/span/text()").extract()).split('and')[0]
		no.of_reviews = ''.join(response.xpath("//span[@class='_38sUEc']/span/text()").extract()).split('and')[1]
		offers = response.xpath("//div[@class='_3D89xM']/span/li/span/text()").extract()
		return_policy = response.xpath("//div[@class='_20PGcF']/text()").extract()[0]
		cod = response.xpath("//div[@class='_20PGcF']/text()").extract()[1]
		product_code = response.url
		product_code = product_code.split('=')[1]
		product_url = response.url
# 		import pdb; pdb.set_trace()

		item = {

			'brand':brand,
			'product name':product_name,
			'sale_price':sale_price,
			'original_price':original_price,
			'discount percentage':discount_percentage,
			'star rating':star_rating,
			'no of ratings':no.of_rating,
			'no.of reviews':no.of_reviews,
			'offers' : offers,
			'return policy' : return_policy,
			'cod_available' : cod,
			'product_code':product_code,
			'product url':product_url
		}

		yield item




	
