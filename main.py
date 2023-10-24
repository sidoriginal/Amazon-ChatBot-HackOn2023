import sys
from scrapy.crawler import CrawlerProcess
from amazon_scraper.amazon_scraper.spiders.amazon import AmazonSpider
import pandas as pd


# Get search query from command-line arguments
user_query = sys.argv[1] if len(sys.argv) > 1 else input("Enter the search query: ")

process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'test.csv'
})

process.crawl(AmazonSpider, search_query=user_query)
process.start()
# df = pd.read_csv('test.csv')
# top_asins = df['asin'].head(5)
# top_links = [f"https://www.amazon.in/dp/{asin}" for asin in top_asins]
# print(f"Here are the top 5 links:\n{' '.join(top_links)}")

