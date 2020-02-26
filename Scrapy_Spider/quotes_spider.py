import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.xpath('span/small/text()').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
'''
scrapy runspider quotes_spider.py -o quotes.json
'''
#from scrapy import cmdline
#cmdline.execute("scrapy crawl QuotesSpider".split())
#
#import os
#os.system("scrapy crawl yourspider")

#pool = Pool(processes=len(QuotesSpider))
#pool.map(_crawl, QuotesSpider)

#--------------------------------------------------------------------------
#from scrapy.crawler import CrawlerProcess
##from project.spiders.test_spider import SpiderName
#
#process = CrawlerProcess()
#process.crawl(QuotesSpider)
#process.start()
'''
In your code sample you are making calls to twisted.reactor starting it on every function call. 
This is not working because there is only one reactor per process and you cannot start it twice.

There are two ways to solve your problem, both described in documentation here. 
Either stick with CrawlerRunner but move reactor.run() outside your search() function to ensure 
it is only called once. Or use CrawlerProcess and simply call crawler_process.start(). 
Second approach is easier, your code would look like this:
'''
from scrapy.crawler import CrawlerProcess

def search(runner, keyword):
    return runner.crawl(QuotesSpider, keyword)

runner = CrawlerProcess()
search(runner, "alfa")
search(runner, "beta")
runner.start()