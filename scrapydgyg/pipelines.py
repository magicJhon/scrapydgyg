import os
import re
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline

from scrapydgyg.settings import IMAGES_STORE as images_store
from scrapydgyg.settings import IMAGES_PATH as images_path
from scrapydgyg.items import ScrapydgygItem

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapydgygPipeline(object):

    def __init__(self):
        self.f = open("dgyg.json", "wb")
        self.f.write("[".encode("utf-8"))

    '''
        处理文字部分
    '''
    def process_item(self, item, spider):

        if item['contenttxt'] is not None:
            item['contenttxt'] = self.process_content(item['contenttxt'])

        jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\r\n"
        jsontext = jsontext.encode("utf-8")
        self.f.write(jsontext)
        return item

    def process_content(self, content):
        # 替换内容中的\xa0
        content = [re.sub(r"\xa0|\s","",i) for i in content]
        return content

    def close_spider(self, spider):
        self.f.write("]".encode("utf-8"))
        self.f.close()


class ScrapydgygImgPipeline(ImagesPipeline):
    '''
        处理图片下载
    '''
    # 重写方法    
    def get_media_requests(self, item, info):
        
        if isinstance(item, ScrapydgygItem):
            # 没有图片，无需处理

            if len(item['image_urls'])<=0:
                return super().get_media_requests(item, info)

            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)
    
        return super().get_media_requests(item, info)

    
    def item_completed(self, results, item, info):
        
        # 列表推导式，获取图片保存路径
        image_url = [{"url":x["url"],"local":x['path']} for ok, x in results if ok]

        # 重命名，保存到指定位置；并替换内容中的图片
        images = []
        i = 1
        for img in image_url:
            # 获取后缀名
            subfix = img['local'].split(".")[-1]
            tmp_filename = item['codeId'] + "_" + str(i) + "." + subfix
            if not os.path.isfile(images_store + images_path + tmp_filename):
                os.rename(images_store+img['local'], images_store + images_path + tmp_filename)
            images.append( images_path + tmp_filename)
            item['contenttxt'] = [str(c).replace(img['url'].replace('http://wz.sun0769.com',""), images_path + tmp_filename) for c in item['contenttxt']]
            i += 1
        
        item['web_images'] = images

        return super().item_completed(results, item, info)