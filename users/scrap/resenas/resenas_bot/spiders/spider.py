import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap.resenas.resenas_bot.items import ResenasBotItem
from scrapy.exceptions import CloseSpider
from scrapy.http.request import Request
import re
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ResenasBotSpider(CrawlSpider):

    name="resenas_bot"
    item_count=0
    

    rules={
        
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="reviews-medley-footer"]/div[2]/a')), callback='parse_item', follow=True), #Esta regla nos permite pasar de página dentro de amazon
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a')), callback='parse_item', follow=False),#Esta regla nos permite ir seleccionando productos
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')), callback='parse_item', follow=False)#Esta regla permite seleccionar otro tipo de productos
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="reviews-medley-footer"]/div[2]/a')), callback='parse_item', follow=False)#Esta regla permite seleccionar otro tipo de productos
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="a-last"]/a')), callback='parse_item', follow=True),
        
    }

    def __init__(self, asin, num_items, marketplace,  *args, **kwargs):
        self.start_urls=[ 'https://www.amazon.'+marketplace+'/dp/'+asin]#URL donde empieza la araña
        self.allowed_domain=['www.amazon.'+marketplace]
        self.num_items=num_items#Número de items para analizar
        self.asin=asin#Término de búsqueda
        self.marketplace=marketplace
        super(ResenasBotSpider, self).__init__(*args, **kwargs)#Llamamos al constructor del padre

    #Por cada producto se ejecuta esta función para obtener la información
    def parse_item(self, response):
        resenas=response.xpath('//*[@id="cm_cr-review_list"]').extract()
        
        
        profiles_names=[a.end() for a in list(re.finditer('a-profile-name', resenas[0]))]
        enlace_perfil=[a.end() for a in list(re.finditer('a-row a-spacing-mini"><a href="', resenas[0]))]
        fecha=[a.end() for a in list(re.finditer('a-size-base a-color-secondary review-date', resenas[0]))]
        estrellas=[a.end() for a in list(re.finditer('<span class="a-icon-alt">', resenas[0]))]
        titulo=[a.end() for a in list(re.finditer('a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold', resenas[0]))]
        descripcion=[a.end() for a in list(re.finditer('a-size-base review-text review-text-content', resenas[0]))]
        
        for i in range(len(descripcion)):
            
            ml_item=ResenasBotItem()
            finalPN=resenas[0][profiles_names[i]:].find('<')+profiles_names[i]
            ml_item['comprador']=resenas[0][profiles_names[i]+2:finalPN]

            finalEP=resenas[0][enlace_perfil[i]:].find('" class=')+enlace_perfil[i]
            ml_item['enlace_perfil']=self.allowed_domain[0]+resenas[0][enlace_perfil[i]:finalEP]

            finalPN=resenas[0][fecha[i]:].find('<')+fecha[i]
            ml_item['fecha']=resenas[0][fecha[i]+24:finalPN]

            ml_item['estrellas']=resenas[0][estrellas[i]:estrellas[i]+1]

            inicioT=resenas[0][titulo[i]:].find('<span>')+titulo[i]+6
            finalT=resenas[0][titulo[i]:].find('</span>')+titulo[i]
            ml_item['titulo']=resenas[0][inicioT:finalT]
            inicioD=resenas[0][descripcion[i]:].find('<span>')+descripcion[i]+8
            finalD=resenas[0][descripcion[i]:].find('</span>')+descripcion[i]
            ml_item['descripcion']=resenas[0][inicioD:finalD]
            self.item_count+=1
            if self.item_count>self.num_items:
                raise CloseSpider("item_exceded")
            yield ml_item