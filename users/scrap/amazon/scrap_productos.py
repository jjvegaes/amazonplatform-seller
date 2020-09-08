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
from multiprocessing.context import Process
from twisted.internet import reactor
from crochet import setup, retrieve_result
import time
setup()
#Llama a esta función con una palabra clave y un número de items y ejecuta el scrapy
def spider_crawler(busqueda, num_items, marketplace, version):
    #SETTINGS DEL SCRAPY
    settings = Settings()
    settings['USER_AGENT']='Mozilla / '+str(version)+'.0'
    settings['BOT_NAME'] = 'amazon_bot'
    settings['SPIDER_MODULES'] = ['scrap.amazon.amazon_bot.spiders']#IMPORTANTE, SI SE SUBE A LA PLATAFORMA PONER: 'users.scrap.amazon.amazon_bot.spiders'
    settings['NEWSPIDER_MODULE'] = 'scrap.amazon.amazon_bot.spiders'#IMPORTANTE, SI SE SUBE A LA PLATAFORMA PONER: 'users.scrap.amazon.amazon_bot.spiders'
    settings['DOWNLOAD_DELAY'] = 1

    #CSV import:
    settings['ITEM_PIPELINES']={'scrap.amazon.amazon_bot.pipelines.AmazonBotPipeline':200}#IMPORTANTE, SI SE SUBE A LA PLATAFORMA PONER: 'users.scrap.amazon.amazon_bot.pipelines.AmazonBotPipeline'

    settings['ROBOTSTXT_OBEY'] = True

    settings['FEED_EXPORT_ENCODING'] = 'utf-8'
    settings['COOKIES_ENABLED'] = False
    try:
        process = CrawlerProcess(settings)

        process.crawl(AmazonBotSpider, busqueda=busqueda, num_items=num_items, marketplace=marketplace)
    #process.start()
    #reactor.stop()

    
        
    except:
        if version==15:#Si devuelve error, el scrapy nunca se va a poder ejecutar
            return 'error'
            
        else:#Si devuelve 'vuelve' es que ha dado error y se debe probar con otra versión
            return 'vuelve'
    return 'correcto'#Se ha ejecutado correctamente


#spider_crawler("raton", 5, "es")

