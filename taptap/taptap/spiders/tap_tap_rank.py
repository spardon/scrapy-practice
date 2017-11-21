# -*- coding: utf-8 -*-
import scrapy
import re
import json
import logging
from lxml import etree
from ..item import TaptapItem


class TapTapRankSpider(scrapy.Spider):
    name = 'tap_tap_rank'
    allowed_domains = ['taptap.com']

    def start_requests(self):
        """
            起始请求
        """
        logging.info(">>>>>>>>> 获取首页")
        url = 'https://www.taptap.com/top/download'
        yield scrapy.Request(url=url, call_back=self.parse_type)

    def parse_type(self, response):
        if response.status == 200:
            rank_urls = response.xpath("//section/ul/li//a/@href").extract()
            rank_keyword = response.xpath("//section/ul/li//a//span/text()")

            for i, rank_url in enumerate(rank_urls):
                yield scrapy.Request(
                    url=rank_url,
                    meta={'keyword': rank_keyword[i]},
                    callback=self.parse_api_url
                )

    def parse_api_url(self, response):
        api_url = response.xpath('//button[text()="更多"]/@data-url').extract_first()
        app_type = re.findall('type=(.*)\&total.*', api_url)[0]

        api_base_url = 'https://www.taptap.com/ajax/top/download'

        get_payload = {'page': 1, 'type': app_type, 'total': 30}

        yield scrapy.Request(
            url=api_base_url,
            body=get_payload,
            meta={'keyword': response.meta['keyword']},
            callback=self.parse_rank_info    
        )

    def parse_rank_info(self, response):
        data = json.loads(response.text)

        next_url = data['data']['next']

        if next_url:
            yield scrapy.Request(
                url=next_url,
                meta={'keyword': response.meta['keyword']},
                callback=self.parse_rank_info
            )
        html = data['data']['html']
        doc = etree.HTML(html)
        item_list = doc.xpath('//div[@class="taptap-top-card"]')

        for item in item_list:
            # app 名称
            name = item.xpath('.//h4/text()')[0] if item.xpath('.//h4/text()') else None

            if not name:
                continue

            # 出品方
            produce = item.xpath('.//p[@class="card-middle-author"]/a/text()')[0]
            # 分类
            kind = item.xpath('.//div[@class="card-middle-footer"]/a/text()')[0]
            # 评分
            rating = item.xpath('.//p[@class="middle-footer-rating"]/span/text()')[0]
            # 标签
            lables = item.xpath('.//div[@class="card-tags"]/a/text()')

            pi = TaptapItem(
                name=name, produce=produce,
                kind=kind, rating=rating,
                lables=lables
            )
            yield pi


