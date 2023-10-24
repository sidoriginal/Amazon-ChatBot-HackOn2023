import scrapy
import urllib
import re
import json
import csv
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.exceptions import CloseSpider
import pandas as pd
queries=[]

class AmazonSpider(scrapy.Spider):
    # count=0
    name = 'amazon'
    def __init__(self, search_query='', *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.search_query = search_query
        # self.count=0
        # dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
    def start_requests(self):
        queries.append(self.search_query)
        for query in queries:
            url = 'https://www.amazon.in/s?' + urllib.parse.urlencode({'k': query})
            API = '45f968b58f72cde1357ad00b73dfc5f7'
            payload = {'api_key': API, 'url': url, 'country_code': 'in'}
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
            yield scrapy.Request(proxy_url, callback=self.parse_keyword_response)
    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.in/dp/{asin}"
            API = '45f968b58f72cde1357ad00b73dfc5f7'
            payload = {'api_key': API, 'url': product_url, 'country_code': 'in'}
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
            yield scrapy.Request(proxy_url, callback=self.parse_product_page, meta={'asin': asin})
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urllib.parse.urljoin("https://www.amazon.in",next_page)
            API = '45f968b58f72cde1357ad00b73dfc5f7'
            payload = {'api_key': API, 'url': url, 'country_code': 'in'}
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
            yield scrapy.Request(proxy_url, callback=self.parse_keyword_response)
    def parse_product_page(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"',response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[1]/text()').extract_first()
        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        temp = response.xpath('//*[@id="twister"]')
        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])
        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        seller_rank = response.xpath('//*[text()="Amazon Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        yield {'asin': asin, 'Title': title, 'MainImage': image, 'Rating': rating, 'NumberOfReviews': number_of_reviews,
               'Price': price, 'AvailableSizes': sizes, 'AvailableColors': colors, 'BulletPoints': bullet_points,
               'SellerRank': seller_rank}
            # self.count+=1
        df = pd.read_csv('test.csv')
        if len(df) >= 6:
            raise CloseSpider('Reached 6 rows in test.csv')
        # with open('test.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     row_count = sum(1 for row in reader)
        # if row_count >= 7:
        #     self.crawler.engine.close_spider(self, '')
