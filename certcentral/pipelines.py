# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class JsonWriterPipeline:

    def __init__(self):
        self.urls_seen = set()

    def open_spider(self, spider):
        self.file = open('cc_crawl.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.urls_seen:
            raise DropItem(f"Duplicate url found: {item!r}")
        else:
            self.urls_seen.add(adapter['url'])
            line = json.dumps(adapter.asdict()) + "\n"
            self.file.write(line)
            return item

