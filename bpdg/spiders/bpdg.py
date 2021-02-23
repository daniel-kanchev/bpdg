import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bpdg.items import Article


class BpdgSpider(scrapy.Spider):
    name = 'bpdg'
    start_urls = ['https://www.bpdg.ch/fr/news']

    def parse(self, response):
        links = response.xpath('//a[@class="news_more_info btn_standard"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//h4/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//p[@align="justify"]//text()').getall() or response.xpath('//p//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
