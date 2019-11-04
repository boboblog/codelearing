# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from mySpider import items


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['https://www.51job.com/']
    # start_urls = ['http://https://www.51job.com//']

    # 北京地区的java岗位
    def start_requests(self):
        yield Request(url='https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,1.html?'
                           'lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99'
                           '&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9'
                           '&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', callback=self.parse_job_list)

    # 处理职位列表页面
    def parse_job_list(self, response):
        job_list_items = {}
        for item in response.css('div.dw_table > div.el'):
            i = 0
            job_name = item.css('p.t1> span > a::text').extract_first()
            if job_name is not None:
                job_name = job_name.replace('\r', '').replace('\n', '').replace(' ', '')
            company_name = item.css('span.t2 > a::text').extract_first()
            workplace = item.css('span.t3::text').extract_first()
            pay = item.css('span.t4::text').extract_first()
            release_time = item.css('span.t5::text').extract_first()
            yield{
                'job_name': job_name,
                'company_name': company_name,
                'workplace': workplace,
                'pay': pay,
                'release_time': release_time
            }
        next_url = response.css('li.bk > a::attr(href)').extract_first()
        print('------------------------'
              '------------------------'
              'next_url= '+next_url)
        if next_url:
            yield Request(url=next_url, callback=self.parse_job_list)


    # # 处理职位详情页面
    # def parse_job_detail(self, response):
    #     global job_list_items
    #
    #     pass
