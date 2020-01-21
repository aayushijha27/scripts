# Importing Scrapy Library
import scrapy
import numpy as np
import re
import pymongo
# Creating a new class to implement Spider
class AmazonReviewsSpider(scrapy.Spider):

	# Spider name
	name = 'amazon'

	# Domain names to scrape
	allowed_domains = ['amazon.in']

	# Base URL for the MacBook air reviews
	
	myBaseUrl ='https://www.amazon.in/Apple-MacBook-13-inch-Storage-1-4GHz/product-reviews/B07V5PH9HM/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='
	start_urls=[]

	################# Add Connection ############
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	################# Create/Add Database ###########
	mydb = myclient["ecommerce"]
	################ Create collection/table ############
	mycol = mydb["productinfo"]

	# Creating list of urls to be scraped by appending page number a the end of base url
	for i in range(1,20):
		start_urls.append(myBaseUrl+str(i))

	# Defining a Scrapy parser
	def parse(self,response):
		yield scrapy.Request(self.start_urls[0],callback=self.parse1,dont_filter=True, meta ={
                    'handle_httpstatus_all': True,
                    'dont_retry': True,
					'dont_redirect': True
                })

	def parse1(self, response):
		############ create list #############
		mylist = []
		title = response.xpath("//h1[@class='a-size-large a-text-ellipsis']/a/text()").extract()
		price = response.xpath("//span[@class='a-color-price arp-price']/text()").extract()

		ids = response.xpath('//*[@class="a-section review aok-relative"]/@id').extract()
		for idss in ids:
			stars = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/div[2]/a[1]/i/span/text()').extract())
			user = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/div[1]/a/div[2]/span/text()').extract())
			date = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/span/text()').extract())
			review = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/div[4]/span/span/text()').extract())
		# Using regex cleaning the review 

			if review is not None:
				review_cleaned = review.replace('\d+', ' ')
				review_cleaned = re.sub(r'[^\a-zA-Z]', ' ', review_cleaned)
				review_cleaned = re.sub(r'[^\w\s#@/:% .,_-]+',' ',review_cleaned)    
				review_cleaned = re.sub(r'www.\S+|http\S+', '', review_cleaned)
				review_cleaned = re.sub(r'[^\w\s]+', ' ', review_cleaned)
				review_cleaned = re.sub(r'[\t\n\r\f\v]+',' ',review_cleaned)
								# import pdb; pdb.set_trace()
			else:
				review_cleaned = ''
			
			item = {'stars' : stars,
					'user' : user,
					'date' : date,
					'review' : review,
					'review_cleaned': review_cleaned,
					'title' : title,
					'price' : price
					
				}
			############ append results into list #############
			mylist.append(item)

			print(item)
		############# insert multiple results in mongodb in the form of list ####################
		x = self.mycol.insert_many(mylist)
