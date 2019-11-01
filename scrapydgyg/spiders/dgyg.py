# -*- coding: utf-8 -*-
import scrapy
import re
from scrapydgyg.items import ScrapydgygItem


class DgygSpider(scrapy.Spider):
    name = 'dgyg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/html/top/report.shtml']

    def parse(self, response):
        # 获取列表
        tr_list = response.xpath("//div[@class='newsHead clearfix']/table[2]/tr")


        # 拼item，那详情内容
        for tr in tr_list:
            item = ScrapydgygItem()
            
            item['title'] = tr.xpath("./td[3]/a[1]/text()").extract_first()
            item['link'] = tr.xpath("./td[3]/a[1]/@href").extract_first()
            item['user'] = tr.xpath("./td[5]/text()").extract_first()
            item['time'] = tr.xpath("./td[6]/text()").extract_first()
            item['codeId'] = tr.xpath("./td[1]/text()").extract_first()
            print(type(item['link']))
            if type(item['link']) == str:
                yield scrapy.Request(item['link'], callback=self.parse_detail, meta = {"item":item})


        #下一页
        # next_url = response.xpath('//a[text()=">"]/@href').extract()

        # if next_url is not None:
        #     yield scrapy.Request(next_url, callback=self.parse)


    def parse_detail(self, response):
        item = response.meta['item']

        #获取详情页的内容、图片
        item['contenttxt'] = response.xpath("//div[@class='wzy1']/table[2]/tr[1]/td").extract()
        item['contenttxt'] = [re.sub(r"\xa0", "", i) for i in item['contenttxt']]
        item['contenttxt'] = [re.sub(r"</?td\s*.*?>", "", i) for i in item['contenttxt']]
        
        item['image_urls'] = response.xpath("//div[@class='wzy1']/table[2]/tr[1]/td//img/@src").extract()
        item['image_urls'] = ['http://wz.sun0769.com'+ i for i in item['image_urls']]



        yield item