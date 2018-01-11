# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class XiaoquInfoItem(Item):
    id = Field()
    name = Field()
    reference_price = Field()
    address = Field()
    times = Field()


class ZufangInfoItem(Item):
    id = Field()
    name = Field()
    zu_price = Field()
    type = Field()
    area = Field()
    zu_price_per = Field()
    url = Field()
    price_per = Field()
