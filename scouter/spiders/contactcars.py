# -*- coding: utf-8 -*-
import logging
import re
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from scouter.items import CarItem
from scouter import utils


class ContactCarsSpider(CrawlSpider):
    """
    Contact Cars Spider
    """

    name = 'contactcars'
    allowed_domains = ['contactcars.com']
    start_urls = ['http://www.contactcars.com/usedcars']
    RESTRICT_CSS = '.large-8.columns .panel a.u-list'
    rules = [Rule(LinkExtractor(restrict_css=RESTRICT_CSS, unique=True), callback='parse_item')]


    def start_requests(self):
        return [Request(url, dont_filter=True, callback=self.parse_category) for url in self.start_urls]


    def parse_category(self, response):
        logging.info('Parsing category: %s', response.url)
        PAGING_PARAMETER_NAME = 'page'
        ZEROBASED_PAGING = False
        parse_requests = super(ContactCarsSpider, self).parse(response)
        for request in parse_requests:
            yield request
        logging.info('getting the next page of %s' % response.url)
        next_url = utils.get_next_page_url(response.url, PAGING_PARAMETER_NAME, 0 if ZEROBASED_PAGING else 1)
        logging.info('the next url is %s' % next_url)
        yield Request(next_url, callback=self.parse_category)


    def parse_item(self, response):
        self.logger.info("Parsing product page %s", response.url)
        car_item = CarItem()
        utils.initialize_item(item_fields=car_item.fields, item=car_item)
        item_populated = self.populate_item(response, car_item)
        return item_populated


    def populate_item(self, response, item):
        item['cid'] = utils.get_item_from_list(re.findall(r'/(\d+)', response.url))
        item['title'] = response.css('.row h1[itemprop="name"]').xpath('normalize-space(text())').extract()
        item['category'] = response.css('ul.breadcrumbs text[itemprop="name"]').xpath('normalize-space(text())').extract()[1:-1]
        item['brand'] = response.css('.row .orange p').xpath('text()').extract()
        item['model'] = response.xpath('normalize-space(//div[@class="row"]/descendant::div[@class="panel"]/descendant::table/descendant::td/text())').extract()
        item['description'] = response.css('.row p[itemprop="description"]').xpath('normalize-space(text())').extract()
        item['extra_images'] = response.css('#gallery-list img').xpath('@src').extract()
        item['specs'] = filter(None, response.css('.row .panel table td b, .row .panel table td')
                               .xpath('normalize-space(text())').extract())
        item['price'] = response.css('.row .orange span').xpath('text()').re('([\d,]+)')
        item['owner_details'] = {}
        return item
