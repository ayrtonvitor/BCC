import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'edis'
    download_delay = 2
    allowed_domains = ['edisciplinas.usp.br']
    start_urls = ['https://edisciplinas.usp.br/course/view.php?id=86963',]

    rules = (
        Rule(LinkExtractor(deny=["/mod/forum",
                                "/mod/dialogue",
                                 "/mod/feedback",
                                "/mod/quiz",
                                "forceview"], restrict_css="#region-main"),
             callback='parse_item', follow = False),
    )

    def parse_item(self, response : scrapy.http.Response):
        print(">"*80, response.url)
