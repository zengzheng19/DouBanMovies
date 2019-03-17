# -*- coding: utf-8 -*-
import scrapy

'''
使用豆瓣提供的电影分类api获取全部电影地址，
使用蜻蜓代理提供代理，获取豆瓣电影2分以上全部电影的年份，评分，评论数量等字段信息。
'''
from DouBanTop250.items import Doubantop250Item

import json
import time
import re

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest


class DoubanapiSpider(CrawlSpider):

    name = 'DouBanAPI'
    tabs = [["U", "近期热门"], ["T", "标记最多"], ["S", "评分最高"], ["R", "最新上映"]]

    def start_requests(self):
        return[Request("https://www.douban.com/",
                       meta={'cookiejar': 1},
                       callback=self.post_login)]

    def post_login(self, response):
        return[FormRequest.from_response(response, meta={'cookiejar': 1},
                                         formdata={
                                                    'ck': '',
                                                    'ticket': '',
                                                    "user": '132****792',
                                                    "password": 'password',
                                                    "remember": 'False'
                                                }, callback=self.after_login, dont_filter=True
                                                )
        ]

    def after_login(self, response):
        year_ranges = ['2019,2019', '2018,2018', '2010,2017', '2000,2009', '1990,1999', ' 1980,1989', '1970,1979',
                       '1960,1969', '1,1959']
        # 分值在0,2之间的电影多为未上映或评分人数少，且详情少的电影，无爬去价值。因此去掉该分值范围
        score_ranges = ['2,3', '3,4', '4,5', '5,6', '6,7', '7,8', '8,9', '9,10']
        for year_range in year_ranges:
            for score_range in score_ranges:
                page = 0
                index_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range='+score_range+'&tags=电影&start='+str(page)
                if year_range:
                    index_url = (index_url+'&year_range='+year_range)
                time.sleep(.4)
                yield Request(index_url, callback=self.parse_index, meta={'page': page, 'cookiejar': 1})

    def parse_index(self, response):
        index_list = json.loads(response.body)['data']
        if len(index_list) > 0:
            page = response.meta['page']
            page += 20
            # 正则替换start=部分
            pattern = re.compile('start=\d.*')
            new_index_url = re.sub(pattern,'start=%d'%page, response.url)
            print('new_index_url', new_index_url)
            time.sleep(1)
            yield Request(new_index_url, callback=self.parse_index, meta={'page': page, 'cookiejar': 1})
            url_list = []
            for index in index_list:
                url_list.append(index['url'])
            for url in url_list:
                yield Request(url, callback=self.parse_item, meta={'cookiejar' : 1})
        else: return

    def parse_item(self, response):
        l = ItemLoader(item=Doubantop250Item(), response=response)
        l.add_xpath('title', '//h1/span[1]/text()')
        l.add_xpath('score', '//strong[@class="ll rating_num"][1]/text()')
        l.add_xpath('ranking', '//span[@class="top250-no"][1]/text()')
        l.add_xpath('votes', '//span[@property="v:vtoes"][1]/text()')
        l.add_xpath('director','//a[@rel="v:directedBy"][1]/text()')
        l.add_xpath('rating_of_5stars', '//div[@class="ratings-on-weight"]//span[@class="rating_per"]/text()')
        l.add_value('url',response.url)
        l.add_xpath('descriptions', 'string(//div[@id="info"])')
        return l.load_item()



