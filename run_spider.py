from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

def run_spider(spider_name,item,pages):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    if spider_name == 'amazonspider':
        from amazon_scraper.amazon_scraper.spiders.amazonspider import AmazonSpiderSpider
        
        process = CrawlerProcess(get_project_settings())
        
        process.crawl(AmazonSpiderSpider, keyword=item, pages=pages)
        process.start()
    else:
        raise ValueError(f"Unknown spider: {spider_name}")