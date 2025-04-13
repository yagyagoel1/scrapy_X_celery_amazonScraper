from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

def run_spider(spider_name):
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Import the spider class correctly
    if spider_name == 'amazonspider':
        from amazon_scraper.amazon_scraper.spiders.amazonspider import AmazonSpiderSpider
        
        # Create process with project settings
        process = CrawlerProcess(get_project_settings())
        
        # Crawl using the spider class, not the module
        process.crawl(AmazonSpiderSpider)
        process.start()
    else:
        raise ValueError(f"Unknown spider: {spider_name}")