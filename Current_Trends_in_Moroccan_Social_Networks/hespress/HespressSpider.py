# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:17:48 2019

@author: Mohammed EL KHOU
"""
import scrapy, csv, sys, os
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm
 
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
# comment_date = ''

d = datetime.today()
comment_date = d.strftime("%Y/%m/%d")

class HespressSpider(scrapy.Spider):
    name = 'hespress'
    allowed_domains = ['hespress.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

    def __init__(self, name=None, comment_date='', **kwargs):
        super().__init__(name=name, **kwargs)
        self.comment_date = comment_date

    def clear(self):
        # sys.stderr.flush()
        # sys.stdout.flush()
        # os.system('cls' if os.name=='nt' else 'clear')
        # f = open('log', "w")
        # f.close()
        pass

    def start_requests(self):
        self.clear()
        # self.comment_date = comment_date
        self.bar = tqdm(1e+6, desc= self.comment_date)#, file = sys.stdout)
        # articles du mois septembre et octobre
        url = "https://www.hespress.com/archive/"

        for i in range(1,11):
            url = url +self.comment_date+ "/index."+ str(i) +".html"
            yield scrapy.Request(url = url, callback = self.getUrls)
        
    def getUrls(self, response):
        urls = response.xpath('//div[@id="box_center_holder"]//div[@class="short"]//h2[@class="section_title"]//a/@href').extract()
        # for url,titre in zip(urls,titres):
        #     yield scrapy.Request(response.urljoin(url), self.parse)
        # with open(r'D:/WISD/S3/Web_Mining/Scrapy_Spider/URLs.txt', 'a', encoding="utf-8") as f:
        #     f.write("\n".join(urls))
        for url in zip(urls):
            yield scrapy.Request(response.urljoin(str(url)), self.parse)
          
    def parse(self, response):
        items = {}
        items["title"] = response.xpath('//div[@id="article_holder"]//h1[@class="page_title"]/text()').extract()[0]
        items["date"]  = self.comment_date
        items["link"]  = response.xpath('//head//link/@href').extract()[0]
        items["type"]  = items["link"].split("/")[-2]
        comments = response.xpath('//div[@id="comment_list"]//div[@class="comment_text"]/text()').extract()
                
        with open("HespressComments.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames = ['title', 'type', 'link', 'date', 'comments'])
            for comment in comments:
                items["comments"] = str(comment)
                writer.writerow(items)
                self.bar.update(1)
                # yield items     

    def closed(self, reason):
        #Called when the spider closes. This method provides a shortcut to signals.connect() for the spider_closed signal.
        # process = CrawlerProcess({
        #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        # })

        # d = datetime.strptime(self.comment_date, "%Y/%m/%d") - timedelta(days=1)
        # comment_date = d.strftime("%Y/%m/%d")
        # process.crawl(HespressSpider, comment_date = comment_date)
        # process.start()
        pass

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(HespressSpider, comment_date = comment_date)
process.start()

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# date = datetime.today()
# for _ in range(10):
#     date -= timedelta(days=1)
#     comment_date = str(date.year)+"/"+str(date.month)+"/"+str(date.day)
#     process.crawl(HespressSpider, comment_date = comment_date)

# process.start() # the script will block here until the crawling is finished


# configure_logging()
# runner = CrawlerRunner()

# @defer.inlineCallbacks
# def crawl(cdate):
#     hs = HespressSpider(comment_date = cdate)
#     yield runner.crawl(hs)
#     reactor.stop()

# date = datetime.today()
# for _ in range(10):
#     date -= timedelta(days=1)
#     comment_date = str(date.year)+"/"+str(date.month)+"/"+str(date.day)
#     crawl(comment_date)
# reactor.run()

'''
=====
  scrapy runspider [options] <spider_file>

Run the spider defined in the given file

Options
=======
--help, -h              show this help message and exit
-a NAME=VALUE           set spider argument (may be repeated)
--output=FILE, -o FILE  dump scraped items into FILE (use - for stdout)
--output-format=FORMAT, -t FORMAT
                        format to use for dumping items with -o

Global Options
--------------
--logfile=FILE          log file. if omitted stderr will be used
--loglevel=LEVEL, -L LEVEL
                        log level (default: DEBUG)
--nolog                 disable logging completely
--profile=FILE          write python cProfile stats to FILE
--pidfile=FILE          write process ID to FILE
--set=NAME=VALUE, -s NAME=VALUE
                        set/override setting (may be repeated)
--pdb                   enable pdb on failure


 scrapy runspider "D:/WISD/S3/Web_Mining/Scrapy_Spider/HespressSpider.py" -o "D:/WISD/S3/Web_Mining/Scrapy_Spider/m.json"
 scrapy runspider "D:/WISD/S3/Web_Mining/Scrapy_Spider/HespressSpider.py" -o "D:/WISD/S3/Web_Mining/Scrapy_Spider/m.csv" -t csv
 scrapy runspider "HespressSpider.py"
 python3 -m scrapy runspider "HespressSpider.py" --nolog --logfile=log
 python -m scrapy runspider "HespressSpider.py" >> log
 python -u "HespressSpider.py" >> log
 
'''
print('\n\n\n\n[DONE]')