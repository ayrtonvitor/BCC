from ._get_cookies import get_gdrive_cookies
import scrapy
import os

class ClassesSpider(scrapy.Spider):
    name = "classes"

    def start_requests(self):
        URLS_PATH = os.path.join(os.path.dirname(__file__), "URLS")
        urls = []
        with open(URLS_PATH, 'r') as f:
            urls.append(f.readline().strip())

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
