import scrapy
from scrapy.http import HtmlResponse
import csv
class AmazonSpider(scrapy.Spider):
    name = 'amazon_reviews'
    def start_requests(self):
        urls  = []
        for i in range(1,3000):
            urls.append('https://www.amazon.in/Redmi-Pro-Black-64GB-Storage/product-reviews/B07DJHXWZZ/ref=cm_cr_getr_d_paging_btm_'+ '?showViewpoints=1&pageNumber='+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback = self.parse)

    def parse(self, response):
        f = open('amazon_reviews.csv', 'a', encoding='latin')
        writer = csv.writer(f)
        # links = response.xpath("//p[@class='_2xgU1']/text()").extract()
        revs = response.xpath('//div[@class="a-section celwidget"]').extract()
        for items in revs:
            i = HtmlResponse(url='string', body=items, encoding='utf-8')
            stars = i.xpath('//span[@class="a-icon-alt"]/text()').extract()
            date = i.xpath("//span[@class='a-size-base a-color-secondary review-date']/text()").extract()
            review = i.xpath("//span[@class='a-size-base review-text']/text()").extract()
            string = ' '.join(review)
            try:
                writer.writerow([stars, date, string])
            except:
                pass
