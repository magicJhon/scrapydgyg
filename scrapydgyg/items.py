# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydgygItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 标题
    title = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 网友
    user = scrapy.Field()
    # 时间
    time = scrapy.Field()
    # 编号
    codeId = scrapy.Field()
    # 内容
    contenttxt = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    web_images = scrapy.Field()
