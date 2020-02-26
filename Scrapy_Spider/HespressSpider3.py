# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:17:48 2019

@author: Mohammed EL KHOU
"""
import scrapy, csv
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess

import matplotlib.pyplot as plt
from textpros import textPros as tp

class HespressSpider(scrapy.Spider):
    name = 'hespress'
    allowed_domains = ['hespress.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likev Gecko) Chrome/74.0.3729.169 Safari/537.36'
    # itemlist = []
            
    def start_requests(self):
        print("----------------------------------------------")
        with open("D:/WISD/S3/Web_Mining/Scrapy_Spider/outputfile.csv","w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames = ['title', 'type', 'link', 'date', 'comments', 'comments_2'])
            writer.writeheader()
            
        # articles du mois septembre et octobre
        url = "https://www.hespress.com/archive/"
        date = datetime.today()
        for _ in range(60):
            date = date - timedelta(days=1)
            for i in range(1,11):
                url = url +str(date.year)+"/"+str(date.month)+"/"+str(date.day)+ "/index."+ str(i) +".html"
                yield scrapy.Request(url = url, callback = self.getUrls)
            break
        
    def getUrls(self, response):
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        urls = response.xpath('//div[@id="box_center_holder"]//div[@class="short"]//h2[@class="section_title"]//a/@href').extract()
        titres = response.xpath('//div[@id="box_center_holder"]//div[@class="short"]//h2[@class="section_title"]//a/text()').extract()
        for url,titre in zip(urls,titres):
            yield scrapy.Request(response.urljoin(url), self.parse)
        with open(r'D:/WISD/S3/Web_Mining/Scrapy_Spider/URLs.txt', 'a', encoding="utf-8") as f:
            f.write("\n".join(urls))
          
    def parse(self, response):
        print("***********************************************")
        items = {}
        items["title"] = response.xpath('//div[@id="article_holder"]//h1[@class="page_title"]/text()').extract()[0]
        # items["date"]  = response.xpath('//div[@id="article_body"]//div[@class="story_stamp"]//spam/text()').extract()
        items["date"]  = response.xpath('//div[@id="comment_list"]//div[@class="comment_holder"]//div[@class="irow_1"]//div[@class="comment_body_in"]//div[@class="comment_body"]//div[@class="comment_header"]//spam/text()').extract()
        items["link"]  = response.xpath('//head//link/@href').extract()[0]
        items["type"]  = items["link"].split("/")[-2]
        comments = response.xpath('//div[@id="comment_list"]//div[@class="comment_text"]/text()').extract()
        
        with open("D:/WISD/S3/Web_Mining/Scrapy_Spider/outputfile.csv","a", newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames = ['title', 'type', 'link', 'date', 'comments', 'comments_2'])
            for c in comments:
                items["comments"] = c
                if c:
                    items["comments_2"] = str(tp().text_pros(c))
                else:
                    items["comments_2"] = ""
                writer.writerow(items)
                # self.itemlist.append(items)
                yield items
            
        # with open(r'D:/WISD/S3/Web_Mining/Scrapy_Spider/comments.txt', 'a', encoding="utf-8") as f:
        #     f.write("\n".join(comments))        

'''
 scrapy runspider "D:/WISD/S3/Web_Mining/Scrapy_Spider/HespressSpider3.py" -o "D:/WISD/S3/Web_Mining/Scrapy_Spider/m.json"
 scrapy runspider "D:/WISD/S3/Web_Mining/Scrapy_Spider/HespressSpider3.py" -o "D:/WISD/S3/Web_Mining/Scrapy_Spider/m.csv" -t csv
'''