# -*- coding: utf-8 -*-
from elasticsearch_dsl import Document, Date, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer
ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class JobType(Document):
    class Meta:  # 设置index名称和document名称
        index = "spider_data"
        doc_type = "java"

    class Index:
        name = "spider_data"
        doc_type = "java"

    url = Keyword()  # 不分词，默认保留256个字符
    job_name = Text(analyzer="ik_max_word")   # “中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合；
    salary = Text(analyzer="ik_smart")  # 将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”
    company_name = Text(analyzer="ik_max_word")
    workplace = Text(analyzer="ik_max_word")
    experience = Text(analyzer="ik_max_word")
    education = Text(analyzer="ik_max_word")
    number_of_people = Integer()
    published_time = Date()
    position_detail = Text(analyzer="ik_smart")
    position_type = Text(analyzer="ik_max_word")
    company_detail = Text(analyzer="ik_max_word")
    location = Text(analyzer="ik_max_word")

    suggest = Completion(analyzer=ik_analyzer)  # 搜索建议


