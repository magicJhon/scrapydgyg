# scrapydgyg
scrapy采集测试项目，方便以后忘了参考

采集http://wz.sun0769.com/html/top/report.shtml页面，
获取列表，分析详情页，并下载图片后修改内容中的图片相对地址；
ScrapydgygPipeline：处理非图片部分的内容；并以json格式写到文件dgyg.json中。
ScrapydgygImgPipeline：处理图片，将图片转移到指定目录；替换内容中的图片路径为新路径。

在settings.py中配置权重，先处理ScrapydgygImgPipeline，后转ScrapydgygPipeline，再将结果保存。
执行命令：
scrapy crawl dgyg

安装插件
scrapy
pillow
