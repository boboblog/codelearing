# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['douban.com']
    # start_urls = ['https://movie.douban.com/chart']

    def start_requests(self):
        yield Request(url='https://movie.douban.com/chart', callback=self.parse_rank)

    # 处理豆瓣电影排行榜页面
    def parse_rank(self, response):
        for item in response.css('tr.item'):
            detail_url = item.css('a.nbg::attr(href)').extract_first()
            img_url = item.css('a.nbg > img::attr(src)').extract_first()
            main_name = item.css('div.pl2 > a::text').extract_first()
            other_name = item.css('div.pl2 > a > span::text').extract_first()
            brief = item.css('p.pl::text').extract_first()
            main_name = main_name.replace('\n', '').replace(' ', '')
            yield {
                'detail_url': detail_url,
                'img_url': img_url,
                'name': main_name + other_name,
                'brief': brief
            }
            yield Request(url=detail_url+'comments?status=P',
                          callback=self.parse_comments,
                          meta={'movie': main_name})

    # 处理豆瓣电影评论页面
    def parse_comments(self, response):
        for comments in response.css('.comment-item'):
            username = comments.css('span.comment-info > a::text').extract_first()
            comment = comments.css('span.short::text').extract_first()
            yield {
                'movie': response.meta['movie'],
                'username': username,
                'comment': comment
            }
        next_url = response.css('a.next::attr(href)').extract_first()
        if next_url:
            yield Request(url=response.url[:response.url.find('?')]+next_url,
                          callback=self.parse_comments,
                          meta=response.meta)
