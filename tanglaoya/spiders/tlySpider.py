import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import requests
import re

class QuotesSpider(CrawlSpider):
    name = "tanglaoya"

    allowed_domains = ['58pic.com']

    start_urls = [
        'http://www.58pic.com/tupian/tanglaoya-0-0-1.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=(r'http://www\.58pic\.com/tupian/tanglaoya.*\.html', )), callback='parse_item'),
        #Rule(LinkExtractor(allow=(r'http://www\.58pic\.com/tupian/tanglaoya-0-0-1\.html', )), callback='parse_item'),
    )

    picSet = set()

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        picList = response.xpath('//*[@id="listBox"]/div/div/a/img/@data-original').extract()
        for pic in picList:
            if pic in self.picSet:
                continue
            self.picSet.add(pic)


    #download
    def closed(self,reason):
        self.logger.info("This game gg, pic count %d, begin download..."  % len(self.picSet))
        i = 0
        for each in self.picSet:
            try:
                pic = requests.get(each, timeout=10)
            except requests.exceptions.ConnectionError:
                print 'download faild'
                continue
            tail = re.match(r".*(?=!.*)", each).group(0).split(".")[-1]
            string = 'pictures/'+str(i) + '.' + tail
            fp = open(string,'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
