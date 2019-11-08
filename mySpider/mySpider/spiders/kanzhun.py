# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request


class KanZhunSpider(scrapy.Spider):
    name = 'kanzhun'
    allowed_domains = ['https://www.kanzhun.com/']
    # start_urls = ['http://https://www.highpin.cn/zhiwei/qw_%E5%8C%97%E4%BA%AC%20.html/']

    # 北京地区的在校生招聘信息
    def start_requests(self):
        yield Request(url='https://www.kanzhun.com/jobli_0-t_0-e_108-d_0-s_0-j_0-k_0/p/?cityCode=7&ka=select-jingyan-8',
                      callback=self.parse_list)

    # 处理职位列表页面
    def parse_list(self, response):
        for item in response.css('div.wrap_style search-jobs-list has-haitou > sparrow'):
            response.css('div.wrap_style search-jobs-list > sparrow')
            job_name = item.css('dl.clearfix spw > dd > h3.r_tt > a::text').extract_first()
            detail_url = item.css('dl.clearfix spw > dd > p.jieshao > a::attr(href)').extract_first()
            company_name = item.css('dl.clearfix spw > dd > h3.r_tt > a::text').extract_first()
            pay = item.css('dl.clearfix spw > dd > p.request grey_99 > span::text').extract_first()
            yield {
                'job_name': job_name,
                'company_name': company_name,
                'pay': pay
            }
            yield Request(url=detail_url, callback=self.parse_detail, dont_filter=True,
                          meta={'job_name': job_name, 'company_name': company_name})
        # 获得下一页数据的url
        next_url = response.css('div.page_wrap > div.f_pager > a.p_next::attr(href)').extract_first()
        # 当前页数
        on = int(response.css('iv.page_wrap > div.f_pager > a.current::text').extract_first())
        if on < 1:
            if next_url:
                # dont_filter，消除allowed_domains的限制
                yield Request(url=next_url, callback=self.parse_list, dont_filter=True)

    # 处理职位详情页面
    def parse_detail(self, response):
        job_detail = {'job_name': response.meta['job_name'], 'company_name': response.meta['company_name'],
                      'position_detail': response.xpath('//*[@id="j-job-desc"]/div[1]/p[2]'),
                      'company_detail': response.xpath('//*[@id="j-job-desc"]/div[1]/p[4]'),
                      'contact_address': response.css('p.company_address::text')}
        yield job_detail
