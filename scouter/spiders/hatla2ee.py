# -*- coding: utf-8 -*-
import scrapy


class Hatla2eeSpider(scrapy.Spider):
    name = 'hatla2ee'
    allowed_domains = ['https://eg.hatla2ee.com/ar/car']
    start_urls = ['http://https://eg.hatla2ee.com/ar/car/']

    def parse(self, response):
        pass
