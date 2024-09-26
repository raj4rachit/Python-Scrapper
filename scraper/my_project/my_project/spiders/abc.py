import scrapy

class AbcSpider(scrapy.Spider):
    name = "abc"
    allowed_domains = ['abc.com']
    start_urls = [
        'https://abc.com/',
    ]

    def parse(self, response):
        titles = response.css('h2.article-title::text').getall()
        yield {'titles': titles}
