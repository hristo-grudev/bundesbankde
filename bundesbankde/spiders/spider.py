import scrapy

from scrapy.loader import ItemLoader

from ..items import BundesbankdeItem
from itemloaders.processors import TakeFirst


class BundesbankdeSpider(scrapy.Spider):
	name = 'bundesbankde'
	start_urls = ['https://www.bundesbank.de/action/de/724000/bbksearch?query=*&hitsPerPageString=9999999&sort=bbksortdate+desc']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="resultlist"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		if response.url[-3:] == 'pdf':
			return
		title = response.xpath('//h1[@class="main__headline mb-4"]/text()').get()
		description = response.xpath('//main[@class="main"]/div[@class="richtext"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="metadata__date"]/text()').get()

		item = ItemLoader(item=BundesbankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
