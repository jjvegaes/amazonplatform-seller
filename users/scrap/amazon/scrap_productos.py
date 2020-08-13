import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap.amazon.amazon_bot.items import AmazonBotItem
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from scrap.amazon.amazon_bot.spiders.spider import AmazonBotSpider
from scrapy.utils.project import get_project_settings
import pandas as pd
from scrapy.settings import Settings
import os

#Llama a esta función con una palabra clave y un número de items y te devuelve el df con la información
def spider_crawler(busqueda, num_items, marketplace, version=1):
    
    settings = Settings()
    settings['USER_AGENT']='Mozilla / '+'2'+'.0'
    settings['BOT_NAME'] = 'amazon_bot'
    settings['SPIDER_MODULES'] = ['scrap.amazon.amazon_bot.spiders']
    settings['NEWSPIDER_MODULE'] = 'scrap.amazon.amazon_bot.spiders'
    #settings['DOWNLOAD_DELAY'] = 1

    #CSV import:
    settings['ITEM_PIPELINES']={'scrap.amazon.amazon_bot.pipelines.AmazonBotPipeline':200}

    settings['ROBOTSTXT_OBEY'] = True

    settings['FEED_EXPORT_ENCODING'] = 'utf-8'
    settings['COOKIES_ENABLED'] = False
    print(settings)

    process = CrawlerProcess(settings)

    process.crawl(AmazonBotSpider, busqueda=busqueda, num_items=num_items, marketplace=marketplace)
    process.start()

    try:
        pd.read_csv(os.path.dirname(__file__)+"/amazon_bot_items.csv", encoding= 'utf-8')
    except:
        if version==5:
            pass
        else:
            spider_crawler(busqueda, num_items, marketplace, version+1)

#spider_crawler("raton", 5, "es")

