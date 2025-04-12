# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmazonScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        for field in fields:
            if field =="name":
                value = adapter.get(field)
                adapter[field]=value.strip()
        return item
