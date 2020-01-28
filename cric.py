# -*- coding: utf-8 -*-
import scrapy
import json
from bs4 import BeautifulSoup

class CricSpider(scrapy.Spider):
	name = 'cric'
	start_urls = ['https://www.cricbuzz.com/']

	def __init__(self,name=None,*args,**kwargs):
		self.name=name
		self.headers = {
			'Accept':'application/json, text/plain, */*',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
			'Sec-Fetch-Mode':'cors',
		}

	def parse(self, response):
		if ' ' in self.name:
			self.name=self.name.replace(' ','%20')
		if '_' in self.name:
			self.name=self.name.replace('_','%20')
		url = 'https://www.cricbuzz.com/api/search/results?q='+str(self.name)
		yield scrapy.Request(url=url,headers=self.headers,callback=self.parse1)
	
	def parse1(self,response):
		playerlist = json.loads(response.text)['playerList']
		for player in playerlist:
			pid = player['id']
			name= player['title']
			country = player['country']

			url = 'https://www.cricbuzz.com/profiles/'+str(pid)+'/'+str(name.replace(' ','-'))
			headers = {
				'Upgrade-Insecure-Requests':'1',
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
				'Sec-Fetch-Mode':'navigate',
				'Sec-Fetch-User':'?1',
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			}
			yield scrapy.Request(url=url,headers=headers,callback=self.parse2,
							meta={'name':name,'country':country})
	
	def parse2(self,response):
		name = response.meta['name']
		country = response.meta['country']
		soup = BeautifulSoup(response.text,'lxml')
		batting_ipl_m = ''
		batting_ipl_inn = ''
		batting_ipl_no = ''
		batting_ipl_runs = ''
		batting_ipl_hs = ''
		batting_ipl_avg = ''
		batting_ipl_bf = ''
		batting_ipl_sr = ''
		batting_ipl_100 = ''
		batting_ipl_200 = ''
		batting_ipl_50 = ''
		batting_ipl_4s = ''
		batting_ipl_6s = ''
		batting_test_m = ''
		batting_test_inn = ''
		batting_test_no = ''
		batting_test_runs = ''
		batting_test_hs = ''
		batting_test_avg = ''
		batting_test_bf = ''
		batting_test_sr = ''
		batting_test_100 = ''
		batting_test_200 = ''
		batting_test_50 = ''
		batting_test_4s = ''
		batting_test_6s = ''
		batting_odi_m = ''
		batting_odi_inn = ''
		batting_odi_no = ''
		batting_odi_runs = ''
		batting_odi_hs = ''
		batting_odi_avg = ''
		batting_odi_bf = ''
		batting_odi_sr = ''
		batting_odi_100 = ''
		batting_odi_200 = ''
		batting_odi_50 = ''
		batting_odi_4s = ''
		batting_odi_6s = ''
		batting_t20_m =''
		batting_t20_inn = ''
		batting_t20_no = ''
		batting_t20_runs = ''
		batting_t20_hs = ''
		batting_t20_avg = ''
		batting_t20_bf = ''
		batting_t20_sr = ''
		batting_t20_100 = ''
		batting_t20_200 = ''
		batting_t20_50 = ''
		batting_t20_4s = ''
		batting_t20_6s = ''
		bowling_ipl_m = ''
		bowling_ipl_inn = ''
		bowling_ipl_b = ''
		bowling_ipl_runs = ''
		bowling_ipl_wkts = ''
		bowling_ipl_bbi = ''
		bowling_ipl_bbm = ''
		bowling_ipl_econ = ''
		bowling_ipl_avg = ''
		bowling_ipl_sr = ''
		bowling_ipl_5w = ''
		bowling_ipl_10w = ''
		bowling_test_m = ''
		bowling_test_inn = ''
		bowling_test_b = ''
		bowling_test_runs = ''
		bowling_test_wkts = ''
		bowling_test_bbi = ''
		bowling_test_bbm = ''
		bowling_test_econ = ''
		bowling_test_avg = ''
		bowling_test_sr = ''
		bowling_test_5w = ''
		bowling_test_10w = ''
		bowling_odi_m = ''
		bowling_odi_inn = ''
		bowling_odi_b = ''
		bowling_odi_runs = ''
		bowling_odi_wkts = ''
		bowling_odi_bbi = ''
		bowling_odi_bbm = ''
		bowling_odi_econ = ''
		bowling_odi_avg = ''
		bowling_odi_sr = ''
		bowling_odi_5w = ''
		bowling_odi_10w = ''
		bowling_t20_m = ''
		bowling_t20_inn = ''
		bowling_t20_b = ''
		bowling_t20_runs = ''
		bowling_t20_wkts = ''
		bowling_t20_bbi = ''
		bowling_t20_bbm = ''
		bowling_t20_econ = ''
		bowling_t20_avg = ''
		bowling_t20_sr = ''
		bowling_t20_5w = ''
		bowling_t20_10w = ''
	
		for table in soup.findAll('div',class_='cb-plyr-tbl'):
			if 'Batting Career Summary' in table.text:
				for tabl in table.find('tbody').findAll('tr'):
					if 'IPL' in tabl.text:
						ipl = tabl.findAll('td')
						batting_ipl_m = ipl[1].text.strip()
						batting_ipl_inn = ipl[2].text.strip()
						batting_ipl_no = ipl[3].text.strip()
						batting_ipl_runs = ipl[4].text.strip()
						batting_ipl_hs = ipl[5].text.strip()
						batting_ipl_avg = ipl[6].text.strip()
						batting_ipl_bf = ipl[7].text.strip()
						batting_ipl_sr = ipl[8].text.strip()
						batting_ipl_100 = ipl[9].text.strip()
						batting_ipl_200 = ipl[10].text.strip()
						batting_ipl_50 = ipl[11].text.strip()
						batting_ipl_4s = ipl[12].text.strip()
						batting_ipl_6s = ipl[13].text.strip()
					
					elif 'Test' in tabl.text:
						test = tabl.findAll('td')
						batting_test_m = test[1].text.strip()
						batting_test_inn = test[2].text.strip()
						batting_test_no = test[3].text.strip()
						batting_test_runs = test[4].text.strip()
						batting_test_hs = test[5].text.strip()
						batting_test_avg = test[6].text.strip()
						batting_test_bf = test[7].text.strip()
						batting_test_sr = test[8].text.strip()
						batting_test_100 = test[9].text.strip()
						batting_test_200 = test[10].text.strip()
						batting_test_50 = test[11].text.strip()
						batting_test_4s = test[12].text.strip()
						batting_test_6s = test[13].text.strip()
					
					elif 'ODI' in tabl.text:
						odi = tabl.findAll('td')
						batting_odi_m = odi[1].text.strip()
						batting_odi_inn = odi[2].text.strip()
						batting_odi_no = odi[3].text.strip()
						batting_odi_runs = odi[4].text.strip()
						batting_odi_hs = odi[5].text.strip()
						batting_odi_avg = odi[6].text.strip()
						batting_odi_bf = odi[7].text.strip()
						batting_odi_sr = odi[8].text.strip()
						batting_odi_100 = odi[9].text.strip()
						batting_odi_200 = odi[10].text.strip()
						batting_odi_50 = odi[11].text.strip()
						batting_odi_4s = odi[12].text.strip()
						batting_odi_6s = odi[13].text.strip()
					
					elif 'T20I' in tabl.text:
						t20 = tabl.findAll('td')
						batting_t20_m = t20[1].text.strip()
						batting_t20_inn = t20[2].text.strip()
						batting_t20_no = t20[3].text.strip()
						batting_t20_runs = t20[4].text.strip()
						batting_t20_hs = t20[5].text.strip()
						batting_t20_avg = t20[6].text.strip()
						batting_t20_bf = t20[7].text.strip()
						batting_t20_sr = t20[8].text.strip()
						batting_t20_100 = t20[9].text.strip()
						batting_t20_200 = t20[10].text.strip()
						batting_t20_50 = t20[11].text.strip()
						batting_t20_4s = t20[12].text.strip()
						batting_t20_6s = t20[13].text.strip()
			
			elif 'Bowling Career Summary' in table.text:
				for tabl in table.find('tbody').findAll('tr'):
					if 'IPL' in tabl.text:
						ipl = tabl.findAll('td')
						bowling_ipl_m = ipl[1].text.strip()
						bowling_ipl_inn = ipl[2].text.strip()
						bowling_ipl_b = ipl[3].text.strip()
						bowling_ipl_runs = ipl[4].text.strip()
						bowling_ipl_wkts = ipl[5].text.strip()
						bowling_ipl_bbi = ipl[6].text.strip()
						bowling_ipl_bbm = ipl[7].text.strip()
						bowling_ipl_econ = ipl[8].text.strip()
						bowling_ipl_avg = ipl[9].text.strip()
						bowling_ipl_sr = ipl[10].text.strip()
						bowling_ipl_5w = ipl[11].text.strip()
						bowling_ipl_10w = ipl[12].text.strip()
						
					elif 'Test' in tabl.text:
						test = tabl.findAll('td')
						bowling_test_m = test[1].text.strip()
						bowling_test_inn = test[2].text.strip()
						bowling_test_b = test[3].text.strip()
						bowling_test_runs = test[4].text.strip()
						bowling_test_wkts = test[5].text.strip()
						bowling_test_bbi = test[6].text.strip()
						bowling_test_bbm = test[7].text.strip()
						bowling_test_econ = test[8].text.strip()
						bowling_test_avg = test[9].text.strip()
						bowling_test_sr = test[10].text.strip()
						bowling_test_5w = test[11].text.strip()
						bowling_test_10w = test[12].text.strip()
					
					elif 'ODI' in tabl.text:
						odi = tabl.findAll('td')
						bowling_odi_m = odi[1].text.strip()
						bowling_odi_inn = odi[2].text.strip()
						bowling_odi_b = odi[3].text.strip()
						bowling_odi_runs = odi[4].text.strip()
						bowling_odi_wkts = odi[5].text.strip()
						bowling_odi_bbi = odi[6].text.strip()
						bowling_odi_bbm = odi[7].text.strip()
						bowling_odi_econ = odi[8].text.strip()
						bowling_odi_avg = odi[9].text.strip()
						bowling_odi_sr = odi[10].text.strip()
						bowling_odi_5w = odi[11].text.strip()
						bowling_odi_10w = odi[12].text.strip()
					
					elif 'T20I' in tabl.text:
						t20 = tabl.findAll('td')
						bowling_t20_m = t20[1].text.strip()
						bowling_t20_inn = t20[2].text.strip()
						bowling_t20_b = t20[3].text.strip()
						bowling_t20_runs = t20[4].text.strip()
						bowling_t20_wkts = t20[5].text.strip()
						bowling_t20_bbi = t20[6].text.strip()
						bowling_t20_bbm = t20[7].text.strip()
						bowling_t20_econ = t20[8].text.strip()
						bowling_t20_avg = t20[9].text.strip()
						bowling_t20_sr = t20[10].text.strip()
						bowling_t20_5w = t20[11].text.strip()
						bowling_t20_10w = t20[12].text.strip()
					
		item = {
			'name':name,
			'country':country,
			'batting_ipl_m':batting_ipl_m,
			'batting_ipl_inn':batting_ipl_inn,
			'batting_ipl_no':batting_ipl_no,
			'batting_ipl_runs':batting_ipl_runs,
			'batting_ipl_hs':batting_ipl_hs,
			'batting_ipl_avg':batting_ipl_avg,
			'batting_ipl_bf':batting_ipl_bf,
			'batting_ipl_sr':batting_ipl_sr,
			'batting_ipl_100':batting_ipl_100,
			'batting_ipl_200':batting_ipl_200,
			'batting_ipl_50':batting_ipl_50,
			'batting_ipl_4s':batting_ipl_4s,
			'batting_ipl_6s':batting_ipl_6s,
			'batting_test_m':batting_test_m,
			'batting_test_inn':batting_test_inn,
			'batting_test_no':batting_test_no,
			'batting_test_runs':batting_test_runs,
			'batting_test_hs':batting_test_hs,
			'batting_test_avg':batting_test_avg,
			'batting_test_bf':batting_test_bf,
			'batting_test_sr':batting_test_sr,
			'batting_test_100':batting_test_100,
			'batting_test_200':batting_test_200,
			'batting_test_50':batting_test_50,
			'batting_test_4s':batting_test_4s,
			'batting_test_6s':batting_test_6s,
			'batting_odi_m':batting_odi_m,
			'batting_odi_inn':batting_odi_inn,
			'batting_odi_no':batting_odi_no,
			'batting_odi_runs':batting_odi_runs,
			'batting_odi_hs':batting_odi_hs,
			'batting_odi_avg':batting_odi_avg,
			'batting_odi_bf':batting_odi_bf,
			'batting_odi_sr':batting_odi_sr,
			'batting_odi_100':batting_odi_100,
			'batting_odi_200':batting_odi_200,
			'batting_odi_50':batting_odi_50,
			'batting_odi_4s':batting_odi_4s,
			'batting_odi_6s':batting_odi_6s,
			'batting_t20_m':batting_t20_m,
			'batting_t20_inn':batting_t20_inn,
			'batting_t20_no':batting_t20_no,
			'batting_t20_runs':batting_t20_runs,
			'batting_t20_hs':batting_t20_hs,
			'batting_t20_avg':batting_t20_avg,
			'batting_t20_bf':batting_t20_bf,
			'batting_t20_sr':batting_t20_sr,
			'batting_t20_100':batting_t20_100,
			'batting_t20_200':batting_t20_200,
			'batting_t20_50':batting_t20_50,
			'batting_t20_4s':batting_t20_4s,
			'batting_t20_6s':batting_t20_6s,
			'bowling_ipl_m':bowling_ipl_m,
			'bowling_ipl_inn':bowling_ipl_inn,
			'bowling_ipl_b':bowling_ipl_b,
			'bowling_ipl_runs':bowling_ipl_runs,
			'bowling_ipl_wkts':bowling_ipl_wkts,
			'bowling_ipl_bbi':bowling_ipl_bbi,
			'bowling_ipl_bbm':bowling_ipl_bbm,
			'bowling_ipl_econ':bowling_ipl_econ,
			'bowling_ipl_avg':bowling_ipl_avg,
			'bowling_ipl_sr':bowling_ipl_sr,
			'bowling_ipl_5w':bowling_ipl_5w,
			'bowling_ipl_10w':bowling_ipl_10w,
			'bowling_test_m':bowling_test_m,
			'bowling_test_inn':bowling_test_inn,
			'bowling_test_b':bowling_test_b,
			'bowling_test_runs':bowling_test_runs,
			'bowling_test_wkts':bowling_test_wkts,
			'bowling_test_bbi':bowling_test_bbi,
			'bowling_test_bbm':bowling_test_bbm,
			'bowling_test_econ':bowling_test_econ,
			'bowling_test_avg':bowling_test_avg,
			'bowling_test_sr':bowling_test_sr,
			'bowling_test_5w':bowling_test_5w,
			'bowling_test_10w':bowling_test_10w,
			'bowling_odi_m':bowling_odi_m,
			'bowling_odi_inn':bowling_odi_inn,
			'bowling_odi_b':bowling_odi_b,
			'bowling_odi_runs':bowling_odi_runs,
			'bowling_odi_wkts':bowling_odi_wkts,
			'bowling_odi_bbi':bowling_odi_bbi,
			'bowling_odi_bbm':bowling_odi_bbm,
			'bowling_odi_econ':bowling_odi_econ,
			'bowling_odi_avg':bowling_odi_avg,
			'bowling_odi_sr':bowling_odi_sr,
			'bowling_odi_5w':bowling_odi_5w,
			'bowling_odi_10w':bowling_odi_10w,
			'bowling_t20_m':bowling_t20_m,
			'bowling_t20_inn':bowling_t20_inn,
			'bowling_t20_b':bowling_t20_b,
			'bowling_t20_runs':bowling_t20_runs,
			'bowling_t20_wkts':bowling_t20_wkts,
			'bowling_t20_bbi':bowling_t20_bbi,
			'bowling_t20_bbm':bowling_t20_bbm,
			'bowling_t20_econ':bowling_t20_econ,
			'bowling_t20_avg':bowling_t20_avg,
			'bowling_t20_sr':bowling_t20_sr,
			'bowling_t20_5w':bowling_t20_5w,
			'bowling_t20_10w':bowling_t20_10w,
		}
		yield item



			

	 