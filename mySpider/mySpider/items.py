import scrapy
import datetime
import re
from .models.es_types import JobType
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from scrapy.loader.processors import Identity, Join, TakeFirst, MapCompose
from elasticsearch_dsl.connections import connections
es = connections.create_connection(host="127.0.0.1")
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


def clean_xa0(value):
    return value.replace('\xa0', '')


def date_convert(value):
    value = value.replace('\\xa0', '').replace('发布', '')
    try:
        # create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        create_date = datetime.datetime.strptime(value, "%m-%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def number_of_people_process(value):
    match_obj = re.match('.*招(\d*)人.*', value)
    if match_obj:
        return int(match_obj.group(1))
    else:
        return 0


def location_process(value):
    match_obj = re.match('.*\'(((https:|http:|ftp:|rtsp:|mms:)?\/\/)[^\s]+)\'.*', value)
    if match_obj:
        return match_obj.group(1)
    else:
        return ''


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


class JobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = Identity()


class JobItem(scrapy.Item):
    # 职位链接
    url = scrapy.Field(output_processor=TakeFirst())
    # 职位名称
    job_name = scrapy.Field(output_processor=TakeFirst())
    # 薪资
    salary = scrapy.Field(output_processor=TakeFirst())
    # 公司名称
    company_name = scrapy.Field(output_processor=TakeFirst())
    workplace = scrapy.Field(input_processor=MapCompose(clean_xa0), output_processor=TakeFirst())
    experience = scrapy.Field(input_processor=MapCompose(clean_xa0), output_processor=TakeFirst())
    education = scrapy.Field(input_processor=MapCompose(clean_xa0), output_processor=TakeFirst())
    # 招聘人数
    number_of_people = scrapy.Field(input_processor=MapCompose(number_of_people_process), output_processor=TakeFirst())
    # 发布时间
    published_time = scrapy.Field(input_processor=MapCompose(date_convert), output_processor=TakeFirst())
    # 职位详情
    position_detail = scrapy.Field(input_processor=MapCompose(remove_tags),
                                   output_processor=Join("\n"))  # 有的detail可能内容可能含有各种html标签，就可以用w3lib.html.remove_tags去除
    # 职位类型
    position_type = scrapy.Field()
    # 工作地点
    location = scrapy.Field(input_processor=MapCompose(location_process), output_processor=TakeFirst())
    # 公司详情
    company_detail = scrapy.Field(input_processor=MapCompose(clean_xa0), output_processor=Join("\n"))

    def gen_suggests(self, info_tuple):
        # 根据字符串生成搜索建议数组
        used_words = set()  # set为去重功能
        suggests = []
        for text, weight in info_tuple:
            if text:
                # 字符串不为空时，调用elasticsearch的analyze接口分析字符串（分词、大小写转换）
                words = es.indices.analyze(body={'text': text, 'analyzer': "ik_max_word"})
                anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
                new_words = anylyzed_words - used_words
            else:
                new_words = set()
            if new_words:
                suggests.append({'input': list(new_words), 'weight': weight})
        return suggests

    def fill_item(self):
        keys = ['url', 'job_name', 'salary', 'company_name', 'workplace',  'experience', 'education', 'number_of_people',
                'published_time', 'position_detail', 'position_type', 'location', 'company_detail']
        for key in keys:
            try:
                self[key]
            except:
                self[key] = ''

    def save_to_es(self):
        self.fill_item()

        job = JobType()
        job.url = self['url']
        job.job_name = self['job_name']
        job.location = self['location']
        job.salary = self['salary']
        job.company_name = self['company_name']
        job.experience = self['experience']
        job.education = self['education']
        job.number_of_people = self['number_of_people']
        job.published_time = self['published_time']
        job.position_detail = self['position_detail']
        job.position_type = self['position_type']
        job.workplace = self['workplace']
        job.company_detail = self['company_detail']

        job.suggest = self.gen_suggests(((job.job_name, 10), (job.company_name, 3), (job.position_type, 7)))  # 生成搜索建议词

        job.save()

        return
