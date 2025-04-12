from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

def run_spider(amazonspider):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from amazon_scraper.amazon_scraper.spiders import amazonspider

    process = CrawlerProcess(get_project_settings())
    process.crawl(amazonspider)
    process.start()
