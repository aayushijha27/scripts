# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
import os
import time
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from contextlib import closing
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from w3lib.url import url_query_cleaner
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By # search BY id or class or anything
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.parser import parse
import selenium as se
import numpy as np
#from textblob import TextBlob
import logging


class Mouth1Spider(scrapy.Spider):
    name = 'mouthshut'
    start_urls = ['https://www.mouthshut.com/']

    def __init__(self, url=None, key=None, param = None, *args, **kwargs):
        self.url = url

    def parse(self ,response):
        options = se.webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        # options.add_argument('headless')
        path = os.getcwd() + '/chromedriver'
        # import pdb; pdb.set_trace()
        driver = se.webdriver.Chrome(chrome_options=options, executable_path=path)
        driver.get(self.url)
        wait = WebDriverWait(driver,50)
        # import pdb; pdb.set_trace()
        for item in range(1,41):
            url = self.url+'-'+'page-'+str(item)
            # import pdb; pdb.set_trace()
            driver.get(url)
            sleep(5)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="col-10 review"]'))) #more reviewdata
            sleep(5)
            read_more = driver.find_elements_by_xpath('//*[@class="more reviewdata"]/a')
            #click###
            for more in read_more:
                try:
                    more.click()
                except:
                    pass
            
            soup = BeautifulSoup(driver.page_source,'lxml')
            all_reviews = soup.findAll('div',class_='row review-article')
            for reviews in all_reviews:
                username = reviews.find('div',class_='user-ms-name').find('a').text.strip()
                review = reviews.find('div',class_='more reviewdata').text.strip()
                date = reviews.find('div',class_='rating').findAll('span')
                date = date[1].text.strip()
                ratings = reviews.find('div',class_='rating').find('span').findAll('i')
                i = 0
                j = 5
                for rating in ratings:
                    rati = rating['class'][1]                 
                    if 'unrated-star' in rati:
                        i+=1
                rating = int(j) - int(i)    
                item = {'username' : username,
                        'review' : review,
                        'date' : date,
                        'rating' : rating
                    }
                yield item
        

        driver.close()
    