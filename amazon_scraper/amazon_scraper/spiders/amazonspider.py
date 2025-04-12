from typing import Iterable
import scrapy
from amazon_scraper.items import AmazonScraperItem
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

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
        n_pages = 10

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

        