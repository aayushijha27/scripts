import scrapy
import csv
from bs4 import BeautifulSoup
import csv
import os
import json
from datetime import datetime
from dateutil.parser import parse

class AmazonSpider(scrapy.Spider):
	# Spider name
	name = 'amazo'
	handle_httpstatus_list = [404,503]
	# Domain names to scrape
	start_urls = ['https://www.amazon.in/']

	def __init__(self,text=None,*args,**kwargs):
			self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
	
	def parse(self, response):
		with open('dr.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				url = 'https://www.amazon.in/dp/'+str(row[0])
				yield scrapy.Request(url= url,headers=self.headers,callback=self.parse1,
									 meta={'asin':row[0]})


	def parse1(self, response):

		product_name = ''.join(response.xpath("//span[@class='a-size-large']/text()").extract()).strip() or ''.join(response.xpath("//span[@class='a-size-large product-title-word-break']/text()").extract()).strip()
		asin = response.meta['asin']
		product_url = response.url
		brand_name = ''.join(response.xpath("//*[@id='bylineInfo']/text()").extract()).strip()
		if 'VAIDYA' in brand_name:
			account = "DR VAIDYAS"
		elif 'Rico' in brand_name:
			account = "RICO"
		elif 'PrintOctopus' in brand_name:
			account = "PRINTOCTOPUS"
		elif 'Knight & Rook' in brand_name:
			account = "PRINTOCTOPUS"
		elif 'Sattviko' in brand_name:
			account = "SATTVIKO"
		
		no_of_rating = ''.join(response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract()).replace('ratings' ,'')
		
		# import pdb; pdb.set_trace()
		######################PRINTOCTOPUS#########################################
		price =  ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		# deal_price = ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip().split('-')[0].split('.')[0]
		# max_amt =  ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip()
		# if max != '':
		# 	max_amt = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		# else:
		# 	max_amt = ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip().split('.')[0]

		# min_amt =  ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip().split('.')[0]
		# if min_amt == '':
		# 	min_amt = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		# mrp =  ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip().split('-')[1].split('.')[0]
		
		# min_amt =  ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip().split('-')[0].split('.')[0]
		# max_amt =  ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip().split('-')[1].split('.')[0]
		
		################################## For other accounts #######################################s
		mrp = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		price = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		deal_price = ''.join(response.xpath("//span[@class='a-size-medium a-color-price priceBlockBuyingPriceString']/text()").extract()).strip().split('.')[0]
		min_amt = ''.join(response.xpath("//span[@class='a-size-medium a-color-price priceBlockBuyingPriceString']/text()").extract()).strip().split('.')[0]
		if min_amt == '':
			min_amt = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		else :
			min_amt = ''.join(response.xpath("//span[@class='a-size-medium a-color-price priceBlockBuyingPriceString']/text()").extract()).strip().split('.')[0]
		max_amt  =  ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		if max_amt == '':
			max_amt = ''.join(response.xpath("//span[@class='a-size-medium a-color-price priceBlockBuyingPriceString']/text()").extract()).strip().split('.')[0]
		else:
			max_amt = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip().split('.')[0]
		
		savings = ''.join(response.xpath("//td[@class='a-span12 a-color-price a-size-base priceBlockSavingsString']/text()").extract()).strip()
		stock =  ''.join(response.xpath("//span[@class='a-size-medium a-color-success']/text()").extract()).strip()
		bullets = ''.join(response.xpath("//span[@class='a-list-item']/text()").extract()).strip().replace('\n',' ').strip()
		bullets = bullets.replace('  ','')
		seller_name = ''.join(response.xpath("//*[@id='sellerProfileTriggerId']/text()").extract()).strip()
		delivery_date = ''.join(response.xpath("//*[@id='ddmDeliveryMessage']/b/text()").extract()).strip()
		number_of_qa = ''.join(response.xpath('//a[@class="a-link-normal askATFLink"]/span/text()').extract()).strip()
		soup = BeautifulSoup(response.text,'lxml')
		one_time_purchase = " ".join(''.join(response.xpath('//div[@id="oneTimeBuyBox"]/div/div/a/h5/div/div[2]/span/text()').extract()).strip().split()).strip()
		subscribeandsave_price = " ".join(''.join(response.xpath('//span[@id="sns-base-price"]/text()').extract()).strip().split()).strip()
		star_rating = " ".join("".join(response.xpath('//span[@id="acrPopover"]/@title').extract()).split()).strip().replace('stars','')
		star_rating = star_rating.split(' ')[0]
		returns =  ''.join(response.xpath("//span[@class='a-size-small not-returnable-icon-label']/text()").extract()).strip()
		img_url = response.xpath("//span[@class='a-button-text']/img/@src").extract()[0]
		img_url1 = response.xpath("//span[@class='a-button-text']/img/@src").extract()[1]
		img_url2 = response.xpath("//span[@class='a-button-text']/img/@src").extract()[2]
		now = datetime.now()
		current_date_time = now.strftime("%d/%m/%Y %H:%M:%S")
		soup = BeautifulSoup(response.text,'lxml')
		
		average_rating = ''
		number_of_customer_reviews = ''
		seller_rank = ''
		product_dimensions = ''
		item_model_number = ''
		batteries = ''
		item_weight = ''
		shipping_weight = ''
		shipping_information = ''
		date_first_listed_on_amazon = ''
		if soup.find('div',id='detail-bullets'):
			table = soup.find('div',id='detail-bullets')
			content = table.find('div',class_='content')
			if content:
				for li in content.findAll('li'):
					if "Shipping Weight" in li.text:
						try:
							shipping_weight = li.find('a').text.strip()
						except:
							shipping_weight = li.text.strip()
							if 'Shipping Weight:' in shipping_weight:
								shipping_weight = shipping_weight.replace('Shipping Weight:','')
					elif 'Shipping Information' in li.text:
						try:
							shipping_information = li.find('a').text.strip()
						except:
							shipping_information = li.text.strip()
							if 'Shipping Information:' in shipping_information:
								shipping_information = shipping_information.replace('Shipping Weight:','')
					# elif 'ASIN' in li.text:
					# 	asin = li.text
					# 	if 'ASIN' in asin:
					# 		asin = asin.replace('ASIN','').strip()
					# 	if ':' in asin:
					# 		asin = asin.replace(':','').strip()
					# 	asin = asin.strip()
					elif 'Customer Reviews:' in li.text:
						average_rating =  li.find('span',class_='a-icon-alt')
						if average_rating:
							average_rating = average_rating.text.split('out')[0].strip()
						number_of_customer_reviews = li.find('span',class_='a-size-small')
						if number_of_customer_reviews:
							number_of_customer_reviews = number_of_customer_reviews.text.strip()
					elif 'Amazon Best Sellers Rank' in li.text:
						seller_rank = li.text
						if 'Amazon Best Sellers Rank:' in seller_rank:
							seller_rank = seller_rank.replace('Amazon Best Sellers Rank:','').strip()
						if '(' in seller_rank:
							seller_rank = seller_rank.split('(')[0]
						if 'in' in seller_rank:
							seller_rank = seller_rank.split('in')[0].strip()
					elif 'Product Dimensions' in li.text:
						product_dimensions = li.text
						if 'Product Dimensions:' in product_dimensions:
							product_dimensions = " ".join(product_dimensions.replace('Product Dimensions:','').strip().split())
					elif 'Item model number' in li.text:
						item_model_number = li.text
						if 'Item model number:' in item_model_number:
							item_model_number = item_model_number.replace('Item model number:','').strip()
					elif 'Batteries' in li.text:
						batteries = li.text
						if 'Batteries' in li.text:
							batteries = batteries.replace('Batteries','').strip()
					elif 'Date first listed on Amazon' in li.text:
						date_first_listed_on_amazon = li.text
						if 'Date first listed on Amazon' in li.text:
							date_first_listed_on_amazon = batteries.replace('Date first listed on Amazon','').strip()
					elif 'Item Weight' in li.text:
						item_weight = li.text.strip()
						if 'Item Weight:' in item_weight:
							item_weight = item_weight.replace('Item Weight:','')
						
		# elif soup.find('div',id="detailBullets"):
		# 	table = soup.find('div',id="detailBullets")
		# 	for li in table.findAll('li'):
		# 		if 'Shipping Information' in li.text:
		# 			shipping_information = li.find('span').findAll('span')[1].text.strip()
		# 		# elif 'ASIN' in li.text:
		# 		# 	asin = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'Item model number' in li.text:
		# 			item_model_number = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'Date first listed on Amazon' in li.text:
		# 			date_first_listed_on_amazon = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'ASIN' in li.text:
		# 			asin = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'Batteries' in li.text:
		# 			batteries = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'Product Dimensions' in li.text:
		# 			product_dimensions = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'Amazon Best Sellers Rank' in li.text:
		# 			seller_rank = li.text
		# 			if '.zg_hrsr { margin: 0; padding: 0; list-style-type: none; }.zg_hrsr_item { margin: 0 0 0 10px; }.zg_hrsr_rank { display: inline-block; width: 80px; text-align: right; }' in seller_rank:
		# 				seller_rank = seller_rank.replace('.zg_hrsr { margin: 0; padding: 0; list-style-type: none; }.zg_hrsr_item { margin: 0 0 0 10px; }.zg_hrsr_rank { display: inline-block; width: 80px; text-align: right; }','').strip()
		# 			seller_rank = " ".join(seller_rank.split()).strip()
		# 		elif 'Customer Reviews' in li.text:
		# 			average_rating = li.find('div',id="detailBullets_averageCustomerReviews")
		# 			average_rating = average_rating.find('span',id="acrPopover")['title']
		# 			if 'out' in average_rating:
		# 				average_rating = average_rating.split('out')[0].strip()
		# 		elif 'Shipping Weight' in li.text:
		# 			shipping_weight = li.find('span').findAll('span')[1].text.strip()
		# 		elif 'Item Weight' in li.text:
		# 			item_weight = li.find('span').findAll('span')[1].text.strip()

		# elif soup.find('table',id="productDetails_detailBullets_sections1"):
		# 	table = soup.find('table',id="productDetails_detailBullets_sections1")
		# 	if table:
		# 		for tr in table.findAll('tr'):
		# 			if ('Product Dimensions' in tr.text) or ('Package Dimensions' in tr.text):
		# 				product_dimensions = tr.find('td').text.strip()
		# 			elif 'Item Weight' in tr.text:
		# 				item_weight = tr.find('td').text.strip()
		# 			elif 'Shipping Weight' in tr.text:
		# 				shipping_weight = tr.find('td').text.strip()
		# 			# elif 'ASIN' in tr.text:
		# 			# 	asin = tr.find('td').text.strip()
		# 			elif 'Item model number' in tr.text:
		# 				item_model_number = tr.find('td').text.strip()
		# 			elif 'Best Sellers Rank' in tr.text:
		# 				seller_rank = tr.find('td').text.strip()
		# 				seller_rank = seller_rank.split('(')[0].replace('#',' ')
		# 				sub_category_rank = tr.find('td').text.strip()
		# 				sub_category_rank = sub_category_rank.split(')')
		# 				sub_category_rank =  sub_category_rank[1].split('#')[1].strip()
		# 				sub_category_rank1 = tr.find('td').text.strip()
		# 				sub_category_rank1 = sub_category_rank1.split('#')[-1]
		# 			elif 'Customer Reviews' in tr.text:
		# 				average_rating = tr.find('td').text.strip().split()[-5]
		# 				number_of_customer_reviews = ''
		# 			elif 'Shipping Weight' in tr.text:
		# 				shipping_weight = tr.find('td').text.strip()
		# 			elif 'Date first listed on Amazon' in tr.text:
		# 				date_first_listed_on_amazon = tr.find('td').text.strip()
		# 			elif 'Shipping Information' in tr.text:
		# 				shipping_information = tr.find('td').text.strip()
		# 			elif 'Batteries' in tr.text:
		# 				batteries = tr.find('td').text.strip()
					
		
		elif soup.find('div',id='detail_bullets_id'):
			table = soup.find('div',id='detail_bullets_id').find('div',class_='content')
			for li in table.findAll('li'):
				if ('Product Dimensions' in li.text) or ('Package Dimensions' in li.text):
					product_dimensions = ' '.join(li.text.replace('Product Dimensions:','').strip().split()).strip()
				elif 'Item Weight' in li.text:
					item_weight = ' '.join(li.text.replace('Item Weight:','').strip().split()).strip()
				elif 'Shipping Weight' in li.text:
					shipping_weight = ' '.join(li.text.replace('Shipping Weight:','').strip().split()).strip()
				# elif 'ASIN' in li.text:
				# 	asin = ' '.join(li.text.replace('ASINs:','').strip().split()).strip()
				elif 'Item model number' in li.text:
					item_model_number = ' '.join(li.text.replace('Item model number:','').strip().split()).strip()
				elif 'Amazon Bestsellers Rank' in li.text:
					# import pdb; pdb.set_trace()
					seller_rank = li.text
					seller_rank = seller_rank.split('#')[1]
					seller_rank = seller_rank.split('(')[0]
					# import pdb; pdb.set_trace()
					sub_category_rank = seller_rank.split('#')[-1]
					sub_category_rank = sub_category_rank.replace('\n','\t').strip()

				elif 'Customer Reviews' in li.text:
					average_rating = ' '.join(li.text.replace('Customer Reviews:','').strip().split()).strip()
					number_of_customer_reviews = ' '.join(li.text.replace('Customer Reviews:','').strip().split()).strip()
					
				elif 'Shipping Weight' in li.text:
					shipping_weight = ' '.join(li.text.replace('Shipping Weight:','').strip().split()).strip()
				elif 'Date first available at Amazon.in' in li.text:
					date_first_listed_on_amazon = ' '.join(li.text.replace('Date first listed on Amazon:','').strip().split()).strip()
					date_first_listed_on_amazon = date_first_listed_on_amazon.split(':')[1]
				elif 'Shipping Information' in li.text:
					shipping_information = ' '.join(li.text.replace('Shipping Information:','').strip().split()).strip()
				elif 'Batteries' in li.text:
					batteries = ' '.join(li.text.replace('Batteries:','').strip().split()).strip()

		else:
			print('No Product Details')
		# import pdb; pdb.set_trace()
		item = {
					'product name' : product_name,
					'Brand_Name':brand_name,
					'Brand_Name':brand_name,
					'product_url' : product_url,
					'Mrp': mrp,
					'Deal_Price' : deal_price,
					'Savings' : savings,
					'Stock' : stock,
					'Seller Name' : seller_name,
					'bullets' : bullets,
					'number_of_qa':number_of_qa,
					'asin':asin,
					'delivery_date' : delivery_date,
					'one_time_purchase':one_time_purchase,
					'subscribeandsave_price':subscribeandsave_price,
					'no_of_rating':no_of_rating,
					'star rating':star_rating,
					'max_amt' : max_amt,
					'min_amt' : min_amt,
					'returns' : returns,
					'img_url': img_url,
					'img_url1' : img_url1,
					'img_url2' : img_url2,
					'sub_category_rank' : sub_category_rank,
					'main rank' : seller_rank,
					'date first available' : date_first_listed_on_amazon,
					'Account' : account
				
				}
		yield item
			
