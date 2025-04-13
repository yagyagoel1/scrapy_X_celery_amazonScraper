from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import os
import sys
from twisted.internet.defer import inlineCallbacks, Deferred

def run_spider(spider_name, item, pages, output_file="results.json"):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    settings = get_project_settings()
    
    settings.set('FEEDS', {
        output_file: {
            'format': 'json',
            'encoding': 'utf-8',
            'overwrite': True,
        }
    })
    
    print(f"Spider will write results to: {os.path.abspath(output_file)}")
    
    runner = CrawlerRunner(settings)
    
    @inlineCallbacks
    def crawl():
        if spider_name == 'amazonspider':
            from amazon_scraper.amazon_scraper.spiders.amazonspider import AmazonSpiderSpider
            yield runner.crawl(AmazonSpiderSpider, keyword=item, pages=pages)
        else:
            raise ValueError(f"Unknown spider: {spider_name}")
        
        if not reactor.running:
            reactor.stop()
    
    crawl()
    
    if not reactor.running:
        reactor.run()

    return {"status": "completed", "item": item, "pages": pages}

def run_spider_celery(spider_name, item, pages, output_file="results.json"):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    settings = get_project_settings()
    
    settings.set('FEEDS', {
        output_file: {
            'format': 'json',
            'encoding': 'utf-8',
            'overwrite': True,
        }
    })
    
    print(f"Spider will write results to: {os.path.abspath(output_file)}")
    
    runner = CrawlerRunner(settings)
    
    if spider_name == 'amazonspider':
        from amazon_scraper.amazon_scraper.spiders.amazonspider import AmazonSpiderSpider
        deferred = runner.crawl(AmazonSpiderSpider, keyword=item, pages=pages)
        return deferred
    else:
        raise ValueError(f"Unknown spider: {spider_name}")