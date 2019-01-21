import scrapy
import csv
import pandas as pd
# from . import cleaning_csvs as cl
import datetime
from dateutil import parser
import re
f = open('data.txt','r')
input = f.read()
input2 = input.split(' ')

reviews1 = []
sources1 = []

class BusinessInsiderSpider(scrapy.Spider):
    name = 'business_insider'
    def start_requests(self):
        urls = []

        a = 'https://www.businessinsider.in/searchresult.cms?query='
        for name1 in input2:
            a = a + name1 + str("+")


        for items in range(1,50):
            urls.append(a +'&sortorder=effectivedate&curpg='+str(items))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        links = response.xpath('//h3/a/@href').extract()
        for link in links:
            yield scrapy.Request(url='https://www.businessinsider.in'+str(link),callback=self.actual)
            ef actual(self,response):

                # head = response.xpath('//h1/text()').extract()
                #date1.append(response.xpath("//span[@itemprop='datePublished']/text()").extract()
                sources1.append('Business Insider')
                reviews1.append(str(response.xpath('//h3/a/text()').extract())
