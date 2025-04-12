import scrapy
from amazon_scraper.items import AmazonScraperItem
class AmazonspiderSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["amazon.in"]
    start_urls = ["https://www.amazon.in"]

    def start_requests(self):
        keywords = ["pendrive"]
        for word in keywords:
            url = f"https://www.amazon.in/s?k={word}"
            yield scrapy.Request(url=url)

    def parse(self, response):
        products = response.css('a.a-link-normal.s-link-style.a-text-normal::attr(href)').getall()
        for prt in products:
            prt_url = response.urljoin(prt)
            yield scrapy.Request(url=prt_url, callback=self.parse_prt)

    def parse_prt(self, response):
        object  = AmazonScraperItem()
        table = response.css('table.a-normal.a-spacing-micro tr')
        object['name'] = response.css('span#productTitle::text').get()
        object['price'] = response.css('span.a-price-whole ::text').get()
        object['brand'] = table[0].css('td.a-span9 span ::text').get()
        object['memory'] = table[1].css('td.a-span9 span ::text').get()
        object['h_interface'] = table[2].css('td.a-span9 span ::text').get()
        object['special_features'] = table[3].css('td.a-span9 span ::text').get()
        object['speed'] = table[0].css('td.a-span9 span ::text').get()

        yield object
        