# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import requests
import pandas as pd
import csv


class GlassdoorSpider(scrapy.Spider):
    name = 'glassdoor'

    count = 1

    def start_requests(self):
        urls = []
        for i in range(1, 100):
            urls.append('https://www.glassdoor.co.in/Reviews/Northwestern-Mutual-Reviews-E2919_P' + str(i) + '.htm')


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        f = open('glassdoor_northwest.csv', 'a')
        writer = csv.writer(f)
        text = response.xpath('//div[@class="hreview"]').extract()
        #user = []
        for items in text:
            items = HtmlResponse(url="my html string", body=items, encoding='utf-8')
            date = items.xpath('//time[@class="date subtle small"]/text()').extract()
            author = items.xpath('//span[@class = "authorJobTitle reviewer"]/text()').extract()
            location = items.xpath('//span[@class = "authorLocation"]/text()').extract()
            work_exp = items.xpath('//p[@class = " tightBot mainText"]/text()').extract()
            pros = items.xpath('//p[@class = " pros mainText truncateThis wrapToggleStr"]/text()').extract()
            cons = items.xpath('//p[@class = " cons mainText truncateThis wrapToggleStr"]/text()').extract()
            string = str(pros) + " " + str(cons)
            #user.append([date, author, location, work_exp, pros, cons])
            writer.writerow([str(date).replace("\'","").replace('\\t','').replace('\\r',"").replace('\\n',' ').replace('\\','').lstrip('[').rstrip(']').replace("', '",'').replace('\xa0',''), str(author).replace("\'","").replace('\\t','').replace('\\r',"").replace('\\n',' ').replace('\\','').lstrip('[').rstrip(']').replace("', '",'').replace('\xa0',''), str(location).replace("\'","").replace('\\t','').replace('\\r',"").replace('\\n',' ').replace('\\','').lstrip('[').rstrip(']').replace("', '",'').replace('\xa0',''), str(work_exp).replace("\'","").replace('\\t','').replace('\\r',"").replace('\\n',' ').replace('\\','').lstrip('[').rstrip(']').replace("', '",'').replace('\xa0',''), str(string).replace("\'","").replace('\\t','').replace('\\r',"").replace('\\n',' ').replace('\\','').lstrip('[').rstrip(']').replace("', '",'').replace('\xa0','')])
        #df = pd.DataFrame(user, columns = ['Date', 'Name', 'Location', 'Work_exp', 'Pros', 'Cons'])

            #print(date, author, location, work_exp, pros, cons)
            # print("date : " + str(date))
            # print("author : " + str(author))
            # print("location : " + str(location))
            # print("work_exp : " + str(work_exp))
            # print("pros : " + str(pros))
            # print("cons : " + str(cons))
            # print('-------------------------------------------------------------------------------------')
        # print(len(date), len(author), len(location), len(work_exp), len(pros), len(cons))
        # for items in range(len())
# user = []
# for items in range(len(date)):
#     user.append([date[items], author[items], location[items],
#                  work_exp[items], pros[items], cons[items]])

# df = pd.DataFrame(user)
# print(df.head())
