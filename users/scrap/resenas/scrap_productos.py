import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap.resenas.resenas_bot.items import ResenasBotItem
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from scrap.resenas.resenas_bot.spiders.spider import ResenasBotSpider
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import os
from multiprocessing.context import Process
from twisted.internet import reactor
from crochet import setup, retrieve_result
import time
setup()

#Llama a esta función con una palabra clave y un número de items y te devuelve el df con la información
def spider_crawler(busqueda, num_items, marketplace, version):
    settings = Settings()
    settings['USER_AGENT']='Mozilla / '+str(version)+'.0'
    settings['BOT_NAME'] = 'resenas_bot'
    settings['SPIDER_MODULES'] = ['scrap.resenas.resenas_bot.spiders']
    settings['NEWSPIDER_MODULE'] = 'scrap.resenas.resenas_bot.spiders'
    #settings['DOWNLOAD_DELAY'] = 1

    #CSV import:
    settings['ITEM_PIPELINES']={'scrap.resenas.resenas_bot.pipelines.ResenasBotPipeline':200}

    settings['ROBOTSTXT_OBEY'] = True

    settings['FEED_EXPORT_ENCODING'] = 'utf-8'
    settings['COOKIES_ENABLED'] = False
    print(settings)
    try:
        process = CrawlerProcess(settings)

        process.crawl(AmazonBotSpider, busqueda=busqueda, num_items=num_items, marketplace=marketplace)
    #process.start()
    #reactor.stop()

    
        
    except:
        if version==5:
            return 'error'
            
        else:
            return 'vuelve'
            #spider_crawler(busqueda, num_items, marketplace, version+1)
    return 'correcto'


