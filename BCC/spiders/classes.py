from ._get_cookies import get_gdrive_cookies
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import os
import scrapy

class ClassesSpider(scrapy.Spider):
    name = "classes"
    allowed_domains = ['edisciplinas.ups.br']

    def start_requests(self):
        URLS_PATH = os.path.join(os.path.dirname(__file__), "URLS")
        urls = []
        with open(URLS_PATH, 'r') as f:
            urls.append(f.readline().strip())

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for a in response.css('#region-main').css('a'):
            for s in a.css('span'):
                if s.attrib['class'] == 'instancename':
                    print(a.css('span::text').get())
            print(a.attrib['href'])
            print()

