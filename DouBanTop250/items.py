# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubantop250Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    score = scrapy.Field()
    ranking = scrapy.Field()
    votes = scrapy.Field()
    director = scrapy.Field()
    descriptions = scrapy.Field()
    rating_of_5stars = scrapy.Field()
    url=scrapy.Field()
    comments = scrapy.Field()
    type=scrapy.Field()
    year=scrapy.Field()
    ScreenWriter=scrapy.Field()
    # language = scrapy.Field()
    ReleaseDate = scrapy.Field()
    # duration = scrapy.Field()
    # starRates = scrapy.Field()


class DoubanPages(scrapy.Item):
    # define the fields for your item here like:
    failed_url=scrapy.Field()