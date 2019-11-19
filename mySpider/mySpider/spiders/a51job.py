# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from ..items import JobItem
from ..items import JobItemLoader


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['https://www.51job.com/']
    # start_urls = ['http://https://www.51job.com//']

    # 北京地区的java岗位
    def start_requests(self):
        yield Request(url='https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,1.html?'
                           'lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99'
                           '&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9'
                           '&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
                      callback=self.parse)

    # 处理职位列表页面
    def parse(self, response):
        for item in response.css('div.dw_table > div.el'):
            job_name = item.css('p.t1> span > a::text').extract_first()
            if job_name is not None:
                job_name = job_name.replace('\r', '').replace('\n', '').replace(' ', '')
            company_name = item.css('span.t2 > a::text').extract_first()
            published_time = item.css('span.t5::text').extract_first()
            workplace = item.css('span.t3::text').extract_first()
            salary = item.css('span.t4::text').extract_first()
            detail_url = item.css('p.t1 > span > a::attr(href)').extract_first()
            if detail_url is not None:
                yield Request(url=detail_url, callback=self.parse_detail, dont_filter=True,
                              meta={'job_name': job_name, 'company_name': company_name,
                                    'published_time': published_time, 'workplace': workplace, 'salary': salary})
        # 获得下一页数据的url
        next_url = response.css('li.bk > a::attr(href)').extract()[-1]
        # 当前页数
        on = int(response.css('div.p_in > ul > li.on::text').extract_first())
        if on < 10:
            if next_url:
                # dont_filter，消除allowed_domains的限制
                yield Request(url=next_url, callback=self.parse, dont_filter=True)

    # 处理职位详情页面
    def parse_detail(self, response):
        # 通过item loader加载item。使用了loader，在item中设置的processor才会生效
        item_loader = JobItemLoader(item=JobItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_value('job_name', response.meta['job_name'])
        item_loader.add_value('company_name', response.meta['company_name'])
        item_loader.add_value('published_time', response.meta['published_time'])
        item_loader.add_value('workplace', response.meta['workplace'])
        item_loader.add_value('salary', response.meta['salary'])

        message = response.css('.tCompany_center .tHeader .in .cn .msg::attr(title)').extract_first("").split('|')
        for item in message:
            if '招' in item and '人' in item:
                item_loader.add_value("number_of_people", item)
            elif '经验' in item and '年' in item:
                item_loader.add_value("experience", item)
            elif '本科' in item or '硕士' in item or '博士' in item or '大专' in item:
                item_loader.add_value("education", item)

        for item in response.css('div.tCompany_main > div.tBorderTop_box'):
            category = item.css('h2 > span::text').extract_first()
            if category == '职位信息':
                position_type = "".join(item.css('div.bmsg > div.mt10 > p.fp > a.el::text').extract())
                position_detail = "".join(item.css('div.bmsg > p::text').extract())
                item_loader.add_value('position_type', position_type)
                item_loader.add_value('position_detail', position_detail)
            elif category == '联系方式':
                location = "".join(item.css('div.bmsg > p::text').extract())
                item_loader.add_value('location', location)
            elif category == '公司信息':
                company_detail = item.css('div.tmsg::text').extract_first()
                item_loader.add_value('company_detail', company_detail)

        items = item_loader.load_item()
        yield items



