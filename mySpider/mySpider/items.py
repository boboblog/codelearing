import scrapy
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


class JobItem(scrapy.Item):
    # 岗位名称
    job_name = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 工作地点
    workplace = scrapy.Field()
    # 薪资
    pay = scrapy.Field()
    # 发布时间
    release_time = scrapy.Field()
    # 职位信息
    job_detail = scrapy.Field()
    # 联系方式
    contact_way = scrapy.Field()
    # 公司信息
    company_detail = scrapy.Field()


class ItcastItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()

