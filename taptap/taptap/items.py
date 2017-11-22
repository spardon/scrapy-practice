# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TaptapItem(Item):
    name = Field()
    produce = Field()
    kind = Field()
    rating = Field()
    lables = Field()
    rank_kind = Field()
    created_at = Field()
    updated_at = Field()

