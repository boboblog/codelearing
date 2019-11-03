# -*- coding: utf-8 -*-
import scrapy


class TulingSpider(scrapy.Spider):
    name = "tuling"
    allowed_domains = ["itcast.cn"]
    start_urls = (
        'http://www.itcast.cn/',
    )

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        filename = "tea.html"
        with open(filename, 'wb', encoding='utf-8') as f:
            f.write(response.body)
