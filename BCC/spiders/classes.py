from BCC.items import ClassMainPage, Section
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
        section = Section(title = "", url = "", content = {},
                          is_placeholder = False)
        if not self.parse_started:
            new_section = Section(title = "", url = "", content = {},
                              is_placeholder = True)
            self.parse_started = True
        for a in response.css('#region-main').css('a'):
            if not new_section.get('is_placeholder', 
                                  len(new_section.get('url', "")) != 0):
                section = new_section
                new_section = Section(title = "", url = "", content = {},
                                  is_placeholder = True)

            spans = a.css('span')
            if len(spans) == 0:
                if section["url"] == "":
                    section["title"] = a.css("::text").get()
                    section["url"] = a.attrib["href"]
                else:
                    new_section = Section(
                        title = a.css("::text").get(),
                        url = a.attrib["href"],
                        content = {},
                        is_placeholder = False
                    )
                    yield section
            for s in spans:
                if s.attrib['class'] == 'instancename':
                    section["content"][s.css("::text").get()] = a.attrib['href']
                    break
        yield section
