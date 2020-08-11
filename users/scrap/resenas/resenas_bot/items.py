# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ResenasBotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comprador=scrapy.Field()
    enlace_perfil=scrapy.Field()
    fecha=scrapy.Field()
    estrellas=scrapy.Field()
    titulo=scrapy.Field()
    descripcion=scrapy.Field()
    
