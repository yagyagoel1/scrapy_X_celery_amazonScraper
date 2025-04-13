from typing import Iterable
import scrapy
import os
import time 
from  amazon_scraper.amazon_scraper.items import AmazonScraperItem
from urllib.parse import urlencode
from .configs import (API_KEY,client)

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazonspider"
    # allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in"]

    def start_requests(self):
        keyword = ['pendrive']
        n_pages = 1

        for word in keyword:
            for page in range(n_pages):
                url = f'https://www.amazon.in/s?k={word}&page={page +1}'
                yield scrapy.Request(get_scrapeops_url(url))
        


    def parse(self, response):
        products = response.css('a.a-link-normal.s-link-style.a-text-normal::attr(href)').getall()
        for prt in products:
            prt_url = "https://www.amazon.in" + prt
            yield response.follow(get_scrapeops_url(prt_url), callback=self.parse_prt)

    def parse_prt(self, response):
        object = AmazonScraperItem()
        table = response.css('table.a-normal.a-spacing-micro tr')
        object['name'] = response.css('span#productTitle ::text').get()
        object['price'] = response.css('span.a-price-whole ::text').get()
        object['brand'] = table[0].css('td.a-span9 span ::text').get()
        object['memory'] = table[1].css('td.a-span9 span ::text').get()
        object['h_interface'] = table[2].css('td.a-span9 span ::text').get()
        object['special_features'] = table[3].css('td.a-span9 span ::text').get()
        object['speed'] = table[4].css('td.a-span9 span ::text').get()
        
        yield object

    def closed(self, reason):
        self.logger.info("Spider closed: %s", reason)
        try:
            # Get current directory
            current_dir = os.getcwd()
            self.logger.info(f"Current working directory: {current_dir}")
            
            # Try many different possible file paths
            potential_paths = [
                "results.json",                 # Current directory
                "./results.json",               # Relative to current
                f"{current_dir}/results.json",  # Absolute to current
                "/app/results.json",            # Docker common path
                "/app/amazon_scraper/results.json",  # Subdirectory
                "/app/amazon_scraper/amazon_scraper/results.json",  # Deeper subdirectory
                # Recursive search for results.json in current directory
            ]
            
            # Also search recursively for the file
            for root, dirs, files in os.walk(current_dir):
                if 'results.json' in files:
                    potential_paths.append(os.path.join(root, 'results.json'))
            
            # Find first file that exists
            file_path = None
            for path in potential_paths:
                if os.path.exists(path):
                    file_path = path
                    self.logger.info(f"Found results file at: {path}")
                    break
                    
            if not file_path:
                # List all files in current directory to help debug
                self.logger.error(f"Results file not found. Tried: {potential_paths}")
                self.logger.info(f"Files in current directory: {os.listdir(current_dir)}")
                
                # Try to find any .json files
                json_files = []
                for root, dirs, files in os.walk(current_dir):
                    for file in files:
                        if file.endswith('.json'):
                            json_files.append(os.path.join(root, file))
                
                if json_files:
                    self.logger.info(f"Found these JSON files: {json_files}")
                    # Use the first JSON file found as fallback
                    file_path = json_files[0]
                    self.logger.info(f"Using {file_path} as fallback")
                else:
                    self.logger.error("No JSON files found anywhere in the directory tree")
                    return
                    
            # Upload file to S3
            bucket = os.getenv('AWS_BUCKET')
            if not bucket:
                self.logger.error("AWS_BUCKET environment variable not set")
                return
                
            filename = f"result_{time.strftime('%Y%m%d_%H%M%S')}.json"
            self.logger.info(f"Uploading {file_path} to S3 bucket {bucket} as {filename}")
            
            client.upload_file(
                Filename=file_path,
                Bucket=bucket,
                Key=filename
            )
            self.logger.info(f"Successfully uploaded file to S3: {filename}")
            
        except Exception as e:
            self.logger.error(f"Error uploading to S3: {str(e)}")
            # Print full stack trace for better debugging
            import traceback
            self.logger.error(traceback.format_exc())