import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from amazon_bot.items import AmazonBotItem
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from amazon_bot.spiders.spider import AmazonBotSpider
from scrapy.utils.project import get_project_settings
import pandas as pd

#Llama a esta función con una palabra clave y un número de items y te devuelve el df con la información
def spider_crawler(busqueda, num_items, marketplace):
    process = CrawlerProcess(get_project_settings())

    process.crawl(AmazonBotSpider, busqueda=busqueda, num_items=num_items, marketplace=marketplace)
    process.start()

    return pd.read_csv("amazon_bot_items.csv", encoding= 'utf-8')
    

print(spider_crawler("Maglietta", 5, "fr"))
