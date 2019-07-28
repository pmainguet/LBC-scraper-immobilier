# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Offer(scrapy.Item):
    city = scrapy.Field()
    zipcode = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    posted_on = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
    time_online = scrapy.Field()
    type = scrapy.Field()
    rooms = scrapy.Field()
    surface = scrapy.Field()
    price_surface = scrapy.Field()
    ges = scrapy.Field()
    classe_energie = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    siret_agence = scrapy.Field()
    quartier = scrapy.Field()
    pass
