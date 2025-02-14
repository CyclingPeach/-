from itertools import product
from math import prod
from scrapy import Spider, Request
from urllib.parse import quote
from scrapyseleniumtest.items import ProductItem

class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.comm']
    base_url = ['http://s.taobao.com/search?q=']

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE')+1):
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page':page}, dont_filter=True)
    
    def parse(self, response):
        products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
        for product in products:
            item = ProductItem()
            item['price']    = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title']    = ''.join(product.xpaht('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop']     = ''.join(product.xpaht('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image']    = ''.join(product.xpaht('.//div[contains(@class="pic")]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal']     = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            yield item
