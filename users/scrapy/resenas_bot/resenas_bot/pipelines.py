# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import csv
from scrapy.exporters import JsonItemExporter
import pandas as pd

class ResenasBotPipeline:
    def __init__(self):
        self.files={}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline =cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    #Al abrir la araña se ejecuta esta función
    def spider_opened(self, spider):
        file = open('%s_items.csv' % spider.name, 'wb')#Se crea el fichero
        self.files[spider]=file
        self.exporter= CsvItemExporter(file, encoding = 'utf-8')
        self.exporter.fields_to_export = ['comprador', 'enlace_perfil', 'fecha', 'estrellas', 'titulo', 'descripcion']#Estos son los campos que vamos a usar para guardar los datos
        self.exporter.start_exporting()

    #Al cerrar la araña se ejecuta esta función
    def spider_closed(self,spider):
        self.exporter.finish_exporting()
        file=self.files.pop(spider)
        file.close()

    #Para ir guardando cada uno de los items
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
