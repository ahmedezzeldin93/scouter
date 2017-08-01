# -*- coding: utf-8 -*-

BOT_NAME = 'scouter'

SPIDER_MODULES = ['scouter.spiders']
NEWSPIDER_MODULE = 'scouter.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

COOKIES_ENABLED = False

MONGO_URI = 'mongodb://scouter:1A2B3C4D_@127.0.0.1:27017'
MONGO_DATABASE = 'scouter'


DOWNLOADER_MIDDLEWARES = {
    'scouter.middlewares.RandomUserAgentMiddleware': 543,
}

ITEM_PIPELINES = {
    'scouter.pipelines.DuplicatesPipeline': 1,
    'scouter.pipelines.MongoPipeline': 2,
}
