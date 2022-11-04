# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import Section, ClassMainPage


class BccPipeline:
    def __init__(self):
        #self.connect_to_db()
        pass

    def connect_to_db(self):
        self.connection = sqlite3.connect('db.sqlite3')
        self.cursor = connection.cursor()

    def save_page(self, code, item, url):
        self.cursor.execute("""insert into pages values (?, ?, ?)"""(
            code,
            item,
            url
        ))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def process_item(self, item, spider):
        if isinstance(item, ClassMainPage):
            self.process_page_content(item)

    def process_page_content(self, item):
        code = item['title'].split()[0]
        self.save_page(code, item['title'], item['url'])
        self.process_sections(code, item['content'])

    def process_sections(self, class_code,  section_list):
        raise NotImplementedError("Need to process section sublinks, texts, and
                                  downloads")
        for section in section_list:
            if self.is_download_link(section['url']):
                self.process_download_link()

    def is_download_link(self, url):
        raise NotImplementedError()

    def process_download_link(self):
        raise NotImplementedError()
