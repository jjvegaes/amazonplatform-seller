import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap.resenas.resenas_bot.items import ResenasBotItem
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from scrap.resenas.resenas_bot.spiders.spider import ResenasBotSpider
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import pandas as pd
import os

#Llama a esta función con una palabra clave y un número de items y te devuelve el df con la información
def spider_crawler(busqueda, num_items, marketplace, version=1):
    settings = Settings()
    settings['USER_AGENT']='Mozilla / '+str(version)+'.0'
    settings['BOT_NAME'] = 'resenas_bot'
    settings['SPIDER_MODULES'] = ['scrap.resenas.resenas_bot.spiders']
    settings['NEWSPIDER_MODULE'] = 'scrap.resenas.resenas_bot.spiders'
    settings['DOWNLOAD_DELAY'] = 1

    #CSV import:
    settings['ITEM_PIPELINES']={'scrap.resenas.resenas_bot.pipelines.ResenasBotPipeline':200}

    settings['ROBOTSTXT_OBEY'] = True

    settings['FEED_EXPORT_ENCODING'] = 'utf-8'
    settings['COOKIES_ENABLED'] = False
    process = CrawlerProcess(settings)

    process.crawl(ResenasBotSpider, asin=busqueda, num_items=num_items, marketplace=marketplace)
    process.start()

    try:
        pd.read_csv(os.path.dirname(__file__)+"/resenas_bot_items.csv", encoding= 'utf-8')
    except:
        if version==5:
            pass
        else:
            spider_crawler(busqueda, num_items, marketplace, version+1)
    



