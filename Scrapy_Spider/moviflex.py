# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:17:48 2019

@author: Mohammed EL KHOU
"""

import scrapy, csv,re
from datetime import datetime,timedelta
from scrapy.crawler import CrawlerProcess



class HespressSpider(scrapy.Spider):
    name = 'moviflex'
    allowed_domains = ['moviflex.net']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    
    def start_requests(self):
        print("----------------------------------------------")
            
        # articles du mois septembre et octobre
        urls = ["https://www.moviflex.net/"]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
                    
    def parse(self, response):
        print("***********************************************")

        comments= response.xpath('//div[@id="contenedor"]//div[@class="module"]//div[@class="content"]//div[@class="items"]//article//div[@class="data"]//h3//a/@href').extract()
                        
        with open(r'D:/WISD/S3/Web_Mining/Scrapy_Spider/comments.txt', 'a', encoding="utf-8") as f:
            f.write("\n".join(comments))

        yield {'comments' : comments}
                
        
'''
 scrapy runspider "D:/WISD/S3/Web_Mining/Scrapy_Spider/kooora.py" -o "D:/WISD/S3/Web_Mining/Scrapy_Spider/m.json"
'''