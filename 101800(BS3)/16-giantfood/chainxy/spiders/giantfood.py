import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
from selenium import webdriver
from lxml import html
import pdb

class giantfood(scrapy.Spider):
	name = 'giantfood'
	domain = 'https://www.giantfood.com/store/'
	history = []

	def start_requests(self):
	
		init_url  = 'http://giantfood.com/store/locator/'
		# init_url = 'http://giantfood.com/store/e4265c00-98fa-11e0-be08-005056954a3e/?storeid=e4265c00-98fa-11e0-be08-005056954a3e&submit=find'
		yield scrapy.Request(url=init_url, callback=self.body) 

	def body(self, response):
		store_list = response.xpath('//select[@id="storeid"]//option')
		for store in store_list:
			key = self.validate(store.xpath('./@value'))
			detail_url = self.domain + key + '/?storeid=' + key + '&submit=find'
			yield scrapy.Request(url=detail_url, callback=self.parse_page)

	def parse_page(self, response):
	# try:
		store = response.xpath('//div[@class="location-details"]//div[@class="location"]//ul')
		item = ChainItem()
		check = len(store.xpath('.//li[1]//p/text()').extract())
		if check == 2:
			item['store_name'] = self.validate(store.xpath('.//li[1]//p/text()[2]')).split('#')[0].strip()			
			item['store_number'] = self.validate(store.xpath('.//li[1]//p/text()[2]')).split('#')[1].strip()
			item['address'] = self.validate(store.xpath('.//li[1]//h3/text()'))
			item['address2'] = ''
			address = self.validate(store.xpath('.//li[1]//p/text()[1]'))
			item['city'] = address.split(',')[0].strip()
			item['state'] = address.split(',')[1].strip().split(' ')[0].strip()
			item['zip_code'] = address.split(',')[1].strip().split(' ')[1].strip()
		elif check == 3 :
			item['store_name'] = self.validate(store.xpath('.//li[1]//p/text()[3]')).split('#')[0].strip()			
			item['store_number'] = self.validate(store.xpath('.//li[1]//p/text()[3]')).split('#')[1].strip()
			item['address'] = self.validate(store.xpath('.//li[1]//h3/text()'))
			item['address2'] = self.validate(store.xpath('.//li[1]//p/text()[1]'))
			address = self.validate(store.xpath('.//li[1]//p/text()[2]'))
			item['city'] = address.split(',')[0].strip()
			item['state'] = address.split(',')[1].strip().split(' ')[0].strip()
			item['zip_code'] = address.split(',')[1].strip().split(' ')[1].strip()
		else :
			item['store_name'] = self.validate(store.xpath('.//li[1]//p/text()[4]')).split('#')[0].strip()			
			item['store_number'] = self.validate(store.xpath('.//li[1]//p/text()[4]')).split('#')[1].strip()
			item['address'] = self.validate(store.xpath('.//li[1]//h3/text()'))
			item['address2'] = ''
			address = self.validate(store.xpath('.//li[1]//p/text()[3]'))
			item['city'] = address.split(',')[0].strip()
			item['state'] = address.split(',')[1].strip().split(' ')[0].strip()
			item['zip_code'] = address.split(',')[1].strip().split(' ')[1].strip()

		item['country'] = 'United States'
		item['phone_number'] = self.validate(store.xpath('.//li[2]//p/text()'))
		item['latitude'] = ''
		item['longitude'] = ''
		h_temp = ''
		hour_list = response.xpath('//aside[@class="sidebar grid-two-column"]//div[@class="hours tile sidebar outline"][1]//ul//li')
		for hour in hour_list:
			h_temp += self.validate(hour.xpath('.//span[@class="time-span"]/text()')) + ' ' + self.validate(hour.xpath('.//span[@class="time-open"]/text()')) + ', '
		item['store_hours'] = h_temp[:-2]
		item['store_type'] = ''
		item['other_fields'] = ''
		item['coming_soon'] = ''
		yield item	
	# except:
	# 	pdb.set_trace()
		

	def validate(self, item):
		return item.extract_first().strip()