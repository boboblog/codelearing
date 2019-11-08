# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = (
        'http://www.itcast.cn/',
    )

    # 参数：每一个url传回的response对象
    # 作用：解析返回的网页数据response.body，提取结构化数据（生成item）
    def parse(self, response):
        # # 获取网站标题
        # context = response.xpath('/html/head/title/text()')
        # # 提取网站标题
        # title = context.extract()
        # print(title)
        items = []
        for each in response.xpath("//div[@class='li_txt']"):
            # 将得到的数据封装到一个ItcastItem对象
            item = ItcastItem()
            # extract()方法返回的都是unicode字符串
            name = each.xpath("h3/text()").extract()
            title = each.xpath("h4/text()").extract()
            info = each.xpath("p/text()").extract()
            # xpath返回的是一个元素的列表
            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]

            items.append(item)

        return items
