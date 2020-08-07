# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy

#Clase de un item
class AmazonBotItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price =scrapy.Field()
    asin = scrapy.Field()
    seller=scrapy.Field()
    categoria=scrapy.Field()
    rank=scrapy.Field()
    valoracion_media=scrapy.Field()
    busqueda=scrapy.Field()
    marketplace=scrapy.Field()
    resena=scrapy.Field()
    pass
