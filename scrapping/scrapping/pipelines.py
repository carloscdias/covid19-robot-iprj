# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class ScrappingPipeline(object):
    def process_item(self, item, spider):
        try:
            item.save()
            return item
        except Exception as err:
            raise DropItem(err)
