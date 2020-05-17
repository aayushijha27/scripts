import scrapy
import csv 
from bs4 import BeautifulSoup
class AmazonSpider(scrapy.Spider):

	# Spider name
	name = 'amazon_product'
	handle_httpstatus_list = [404,503]
	# Domain names to scrape
	allowed_domains = ['amazon.in']
	start_urls = ['https://www.amazon.in/']
 
	def __init__(self,text=None,*args,**kwargs):
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}
	def parse(self, response):
		with open('reviews.csv','r') as f:
			reader = csv.reader(f)
			next(reader)
			for row in reader:
				product_url = row[0]
				
				yield scrapy.Request(url=product_url,headers=self.headers,callback=self.parse1)

	def parse1(self, response):
	
		product_name = ''.join(response.xpath("//span[@class='a-size-large']/text()").extract()).strip()
		# product_url = response.meta['product_url']
		
		brand_name = response.xpath("//*[@id='bylineInfo']/text()").extract()
		no_of_rating = ''.join(response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract()).replace('ratings' ,'')
		mrp = ''.join(response.xpath("//span[@class='priceBlockStrikePriceString a-text-strike']/text()").extract()).strip()
		deal_price = ''.join(response.xpath("//*[@id='priceblock_ourprice']/text()").extract()).strip()
		savings = ''.join(response.xpath("//td[@class='a-span12 a-color-price a-size-base priceBlockSavingsString']/text()").extract()).strip()
		stock =  ''.join(response.xpath("//span[@class='a-size-medium a-color-success']/text()").extract()).strip()
		bullets = ''.join(response.xpath("//span[@class='a-list-item']/text()").extract()).strip()
		seller_name = ''.join(response.xpath("//*[@id='sellerProfileTriggerId']/text()").extract()).strip()
		product_description = ''.join(response.xpath("//div[@class='a-section a-spacing-top-mini launchpad-module launchpad-module-brand-description-left']/div/p/text()").extract()).strip() or ''.join(response.xpath("//div[@class='a-section a-spacing-small']/p/text()").extract()).strip()
		star_rating = " ".join(star_rating.split('out')[0].strip().split()).strip()
		number_of_qa = ''.join(response.xpath('//a[@class="a-link-normal askATFLink"]/span/text()').extract()).strip()
		sponsored_urls = response.xpath('//div[@id="sp_detail"]//li[@class="a-carousel-card"]/div/a/@href').extract()
		sponsored_titles = response.xpath('//div[@id="sp_detail"]//li[@class="a-carousel-card"]/div/a/@title').extract()
		sponsored = dict(zip(sponsored_titles,sponsored_urls))
		sales_rank = ''.join(response.xpath("//*[@id='SalesRank']/text()").extract()).strip() or ''.join(response.xpath("//*[@id='SalesRank']/td[2]/text()").extract()).strip()
		asin = response.xpath("//div[@class='content']/ul/li[3]/text()").extract() or response.xpath("//*[@id='prodDetails']/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]/text()").extract()
		date_first_available = response.xpath("//div[@class='content']/ul/li[4]/text()").extract() or  response.xpath("//*[@id='prodDetails']/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[4]/td[2]/text()").extract()
		one_time_purchase = " ".join(''.join(response.xpath('//div[@id="oneTimeBuyBox"]/div/div/a/h5/div/div[2]/span/text()').extract()).strip().split()).strip()
		subscribeandsave_price = " ".join(''.join(response.xpath('//span[@id="sns-base-price"]/text()').extract()).strip().split()).strip()
		if product_name != '':
			item = {
				'product name' : product_name,
				'Product Description' : product_description,
				'Product_Title':product_name,
				'Brand_Name':brand_name,
				# 'Product_Url': product_url,
				# 'ranking':ranking,
				'No.of Rating': no_of_rating,
				'Mrp': mrp,
				'Deal_Price' : deal_price,
				'Savings' : savings,
				'Stock' : stock,
				'Seller Name' : seller_name,
				'bullets' : bullets,
				'sponsored':sponsored,
				'number_of_qa':number_of_qa,
				'sales_rank':sales_rank,
				'Asin':asin,
				'date_first_available':date_first_available,
				'one_time_purchase':one_time_purchase,
				'subscribeandsave_price':subscribeandsave_price,
				'star_rating':star_rating

				}
		review_link = ''.join(response.xpath("//*[@id='reviews-medley-footer']/div[2]/a/@href").extract())
		review_link = "https://www.amazon.in/" + review_link

		yield scrapy.Request(url=review_link,headers=self.headers,callback=self.parse2,meta=item)

	def parse2(self,response):
		
		item ={
			'product name':response.meta['product name'],
			'Product Description':response.meta['Product Description'],
			'Product_Title':response.meta['Product_Title'],
			'Brand_Name':response.meta['Brand_Name'],
			# 'product_url':response.meta['product_url'],
			# 'ranking':response.meta['ranking'],
			'No.of Rating':response.meta['No.of Rating'],
			'Mrp':response.meta['Mrp'],
			'Deal_Price':response.meta['Deal_Price'],
			'Savings':response.meta['Savings'],
			'Stock':response.meta['Stock'],
			'Seller Name':response.meta['Seller Name'],
			'bullets':response.meta['bullets'],
			'sponsored':response.meta['sponsored'],
			'number_of_qa':response.meta['number_of_qa'],
			'sales_rank':response.meta['sales_rank'],
			'Asin':response.meta['Asin'],
			'date_first_available':response.meta['date_first_available'],
			'subscribeandsave_price':response.meta['subscribeandsave_price'],
			'one_time_purchase':response.meta['one_time_purchase'],
			'star_rating':response.meta['star_rating']

		}
		results = ''.join(response.xpath('//span[@data-hook="cr-filter-info-review-count"]/text()').extract()).split(' ')[-2].strip()
		if int(results) >10:
			results = int(int(results)/10)+1
			for i in range(1,int(results)+1):
				url = response.url+'&pageNumber='+str(i)
				yield scrapy.Request(url=url,headers=self.headers,callback=self.parse3,meta=item)
		else:
			yield scrapy.Request(url=response.url,headers=self.headers,callback=self.parse3,meta=item)
	
	def parse3(self,response):
		title = response.xpath("//*[@id='cm_cr-product_info']/div/div[2]/div/div/div[2]/div[1]/h1/a/text()").extract()
		ids = response.xpath('//*[@class="a-section review aok-relative"]/@id').extract()
		
		#global analyser
		for idss in ids:
			stars = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/div[2]/a[1]/i/span/text()').extract())
			user = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/div[1]/a/div[2]/span/text()').extract())
			date = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/span/text()').extract())
			review = ''.join(response.xpath('//*[@id="customer_review-'+str(idss)+'"]/div[4]/span/span/text()').extract())
	
			item = {
					'product name':response.meta['product name'],
					'Product Description':response.meta['Product Description'],
					'Product_Title':response.meta['Product_Title'],
					'Brand_Name':response.meta['Brand_Name'],
					# 'Product_Url':response.meta['Product_Url'],
					'No.of Rating':response.meta['No.of Rating'],
					'Mrp':response.meta['Mrp'],
					'Deal_Price':response.meta['Deal_Price'],
					'Savings':response.meta['Savings'],
					'Stock':response.meta['Stock'],
					'Seller Name':response.meta['Seller Name'],
					'bullets':response.meta['bullets'],
					'sponsored':response.meta['sponsored'],
					'stars' : stars,
					'user' : user,
					'date' : date,
					'review' : review,
					'Product Name' : title,
					'number_of_qa':response.meta['number_of_qa'],
					'sales_rank':response.meta['sales_rank'],
					'Asin':response.meta['Asin'],
					'date_first_available':response.meta['date_first_available'],
					'subscribeandsave_price':response.meta['subscribeandsave_price'],
					'one_time_purchase':response.meta['one_time_purchase'],
					'star_rating':response.meta['star_rating']
					# 'product_url':response.meta['product_url'],
					# 'ranking':response.meta['ranking']
		
			}
			yield item
		
		
	
		
		
  		
				 






  		