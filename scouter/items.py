# -*- coding: utf-8 -*-
from scrapy import Item, Field


class CarItem(Item):
    cid = Field()
    title = Field()
    brand = Field()
    model = Field()
    price = Field()
    main_image = Field()
    extra_images = Field()
    description = Field()
    category = Field()
    specs = Field()
    owner_details = Field()
    classified_timestamp = Field()
