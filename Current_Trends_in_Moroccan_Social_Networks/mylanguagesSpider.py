# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:17:48 2019

@author: Mohammed EL KHOU
"""
import scrapy, csv, sys, os
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess
from tqdm import tqdm

class MyLangSpider(scrapy.Spider):
    name = 'mylanguages'
    allowed_domains = ['mylanguages.org']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

    def clear(self):
        # sys.stderr.flush()
        sys.stdout.flush()
        # os.system('cls' if os.name=='nt' else 'clear')
        f = open('log', "w")
        f.close()

    def start_requests(self):
        with open("mylanguages.csv","w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames = ['en', 'ar', 'mafr'])
            writer.writeheader()
        
        self.bar = tqdm(1e+15, desc= "nb comment")#, file = sys.stdout)

        urls = ["http://mylanguages.org/moroccan_adjectives.php",
                'http://mylanguages.org/moroccan_vocabulary.php',
                'http://mylanguages.org/moroccan_numbers.php',
                'http://mylanguages.org/moroccan_phrases.php',
                'http://mylanguages.org/moroccan_articles.php'
                ]
        # url = "http://mylanguages.org/learn_moroccan.php"
        for url in urls:
            # yield scrapy.Request(url = url, callback = self.get_urls)
            yield scrapy.Request(url = url, callback = self.parse)

        
    def get_urls(self, response):
        urls = response.xpath('//div[@id="sidebar-wrapper"]//ul[@class="sidebar-nav"]//li//a/@href').extract()
        # with open("log.txt", "a", newline="", encoding="utf-8") as f:
        #     f.write(str(urls))
        for url in zip(urls):
            yield scrapy.Request(response.urljoin(str(url)), self.parse)
            # yield scrapy.Request(url = url, callback = self.parse)
          
    def parse(self, response):
        print('\n\n\nDON\'T GIVE UP\n\n\n')

        trs = response.xpath('//table[@id="example2"]//tbody//tr')#.getall()#extract()

        for tr in trs:
            tds = tr.xpath('.//td')#.getall()
            items = {}
            items["en"] = tds[0].xpath('.//b/text()').extract_first()
            # if items["en"] is None:
            #     items["en"] =''
            mafr = tds[1].xpath('./text()').extract_first()
            if mafr is not None and mafr != " - ":
                items["mafr"] = mafr.replace(" - ","")
            else :
                continue
            items["ar"] = tds[1].xpath('.//b/text()').extract_first()
            # if items["ar"] is None:
            #     items["ar"] =''
   
            with open("mylanguages.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames = ['en', 'ar', 'mafr'])
                writer.writerow(items)
            self.bar.update(1)

            yield items
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0 (compatible; Windows NT 10.0; Win64; x64)'
# })

# process.crawl(HespressSpider)
# process.start() # the script will block here until the crawling is finished
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
 
 scrapy runspider "mylanguagesSpider.py" 
'''