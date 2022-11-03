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

        self.parse_started = False
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        section = {'title': "", 'link': "", 'content': {}}
        if not self.parse_started:
            new_section = {}
            self.parse_started = True
        for a in response.css('#region-main').css('a'):
            if len(new_section) != 0:
                section = new_section
                new_section = {}

            spans = a.css('span')
            if len(spans) == 0:
                if section["link"] == "":
                    section["title"] = a.css("::text").get()
                    section["link"] = a.attrib["href"]
                else:
                    new_section = {
                        'title': a.css("::text").get(),
                        'link': a.attrib["href"],
                        'content': {}
                    }
                    yield section
            for s in spans:
                if s.attrib['class'] == 'instancename':
                    section["content"][s.css("::text").get()] = a.attrib['href']
                    break
        yield section
