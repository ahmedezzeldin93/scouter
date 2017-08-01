# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request

from scouter.items import CarItem
from scouter import utils


class OlxEgSpider(CrawlSpider):
    name = 'olx-eg'
    allowed_domains = ['https://olx.com.eg/en/vehicles/cars/']
    start_urls = ['http://https://olx.com.eg/en/vehicles/cars//']
    RESTRICT_CSS = '#offers_table div.ads.ads--list'
    rules = [Rule(LinkExtractor(restrict_css=RESTRICT_CSS, unique=True), callback='parse_item')]


    def start_requests(self):
        return [Request(url, dont_filter=True, callback=self.parse_category) for url in self.start_urls]


    def parse_category(self, response):
        logging.info('Parsing category: %s', response.url)
        PAGING_PARAMETER_NAME = 'page'
        ZEROBASED_PAGING = False
        parse_requests = super(OlxEgSpider, self).parse(response)
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
        item['cid'] = utils.get_item_from_list(response.css('.offercontentinner .x-large.clr small span.inlblk')
                                               .xpath('normalize-space()').extract())
        item['title'] = utils.get_item_from_list(response.css('.offercontentinner h1').xpath('text()').extract())
        item['ts'] = response.css('.offercontentinner .x-large.clr small span.pdingleft10').xpath('text()').extract_first()
        item['brand'] = response.css('table.details td a').xpath('normalize-space(text())').extract_first()
        item['model'] = response.css('table.details td a').xpath('text()').extract()[2]
        item['description'] = response.css('#textContent p').xpath('normalize-space()').extract()
        item['extra_images'] = response.css('#offerdescription .photo-glow img').xpath('@src').extract()
        item['specs'] = response.css('table.details th, table.details td a').xpath('normalize-space(text())').extract()
        item['price'] = response.css('#offerbox .pricelabel strong').xpath('normalize-space(text())').re('[\d,]+')
        item['owner_details'] = {}
        return item
