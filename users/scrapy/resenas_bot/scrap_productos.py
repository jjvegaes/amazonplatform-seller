import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from resenas_bot.items import ResenasBotItem
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from resenas_bot.spiders.spider import ResenasBotSpider
from scrapy.utils.project import get_project_settings
import pandas as pd

#Llama a esta función con una palabra clave y un número de items y te devuelve el df con la información
def spider_crawler(busqueda, num_items, marketplace):
    process = CrawlerProcess(get_project_settings())

    process.crawl(ResenasBotSpider, asin=busqueda, num_items=num_items, marketplace=marketplace)
    process.start()

    return pd.read_csv("resenas_bot_items.csv", encoding= 'utf-8')
    

print(spider_crawler("B01G5HYQJC", 15, "es"))