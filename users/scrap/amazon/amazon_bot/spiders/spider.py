import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap.amazon.amazon_bot.items import AmazonBotItem
from scrapy.exceptions import CloseSpider
from scrapy.http.request import Request
import re
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AmazonBotSpider(CrawlSpider):

    name="amazon_bot"
    item_count=0
    fecha_label={'es':'Producto en Amazon.es desde:', 'it':'Disponibile su Amazon.it a partire dal:', 'co.uk':'Date first available at Amazon.co.uk:', 'fr':'Date de mise en ligne sur Amazon.fr', 'nl':'Datum eerste beschikbaarheid op Amazon.nl:', 'de':'Im Angebot von Amazon.de seit:', 'com':'no disponible', 'ca':'Date first available at Amazon.ca:'}

    rules={
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="a-last"]/a'))), #Esta regla nos permite pasar de página dentro de amazon
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a')), callback='parse_item', follow=False),#Esta regla nos permite ir seleccionando productos
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')), callback='parse_item', follow=False)#Esta regla permite seleccionar otro tipo de productos
        
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="reviews-medley-footer"]/div[2]/a')), callback='parse_item', follow=False)#Esta regla permite seleccionar otro tipo de productos
    
        
    }

    def __init__(self, busqueda, num_items, marketplace,  *args, **kwargs):
        self.start_urls=[ 'https://www.amazon.'+marketplace+'/s?k='+busqueda]#URL donde empieza la araña
        self.allowed_domain=['www.amazon.'+marketplace]
        self.num_items=num_items#Número de items para analizar
        self.busqueda=busqueda#Término de búsqueda
        self.marketplace=marketplace
        super(AmazonBotSpider, self).__init__(*args, **kwargs)#Llamamos al constructor del padre

    #Por cada producto se ejecuta esta función para obtener la información
    def parse_item(self, response):
        ml_item=AmazonBotItem()#Creamos un objeto tipo item
        #Inicializamos estos valores porque cabe la posibilidad de que no sean asignados:
        
        
        #Obtenemos el nombre del producto:
        ml_item['name']=response.xpath('//*[@id="productTitle"]/text()').extract()
        try:
            ml_item['name']=ml_item['name'][0][8:-7]#Eliminamos tabuladores
        except:
            pass
        #Obtenemos el precio del producto (el precio pse puede encpntrar en tres xpath distintos según el producto, por lo que comprobamos todas las posibilidades):
        ml_item['price']=response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()
        if ml_item['price']==[]:
            ml_item['price']=response.xpath('//*[@id="priceblock_dealprice"]/text()').extract()
        if ml_item['price']==[]:
            ml_item['price']=response.xpath('//*[@id="priceblock_saleprice"]/text()').extract()
        #Puede ser que el precio no aparezca
        if len(ml_item['price'])>0:
            ml_item['price']=ml_item['price'][0]

        #A continuación sacamos toda la información que aparece en "Información adicional" o "detalles del producto" (según el producto la sección se llama de una forma u otra, por lo que se han contemplado las dos posibilidades):
        Link = response.xpath('//*[@id="prodDetails"]/div').extract()#si la sección se llama información adicional, esta información se guardará en la variable
        if Link==[]:
            Link = response.xpath('//*[@id="detail_bullets_id"]').extract()#Como Link es vacío, la sección no es "información adicional" y tenemos que ver si es "detalles del producto"
                
            if Link!=[]:#Sección "detalles del producto"
                #Obtenemos ASIN:
                '''
                indice=Link[0].find('asin=')#Buscamos en Link el asin
                ml_item['asin']=Link[0][indice+5:indice+15]#El Asin estará a 5 posiciones de indice (porque len('asin=')==5) y tiene un tamaño de 10 (10+5=15)
                #Obtenemos categoria y rank:
                indice=Link[0].find('SalesRank')#Esta información se encuentra despues de esta etiqueta
                clasificacion=Link[0][indice:]#Nos quedamos con lo que hay a partir de esta información
                try:
                    ml_item['rank']=int(re.findall(r'\b\d+\b', clasificacion.replace(".", "").replace(",", "").replace("nº", "nº "))[0])#El rank es un número que está despueés de nº 
                except:
                    pass
                indice=clasificacion.find('</b>')+19
                clasificacion=clasificacion[indice:]
                inicio1=clasificacion.find(' ')+1
                inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de el "en " empieza la categoria
                final=clasificacion.find("(")-1#Antes de "(" termina la categoría
                ml_item['categoria']=clasificacion[inicio:final]
                
                #Obtenemos la valoración media:
                indice=Link[0].find('a-icon-alt')#A partir de 'a-icon-alt' tenemos la valoración
                valoracion=Link[0][indice:]
                final=valoracion.find(" ")
                ml_item['valoracion_media']=valoracion[12:final]#El principio de la valoración está a partir de el índice 12 y acaba cuando hay un espacio
                '''
                #print('1')
                #print(Link)
                ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details(Link[0])
            else:#No existe esta sección, no podemos obtener estos datos
                
                if Link!=[]:
                    #print('2')
                    ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details3(Link[0])
                else:
                    Link = response.xpath('//*[@id="detail-bullets"]').extract()
                    if Link!=[]:
                        #print('3')
                        #print(Link)
                        ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details(Link[0])
                        
                    else:
                        Link=response.xpath('//*[@id="detailBullets"]').extract()
                        if Link!=[]:
                            #print(Link)
                            ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details3(Link[0])
                        else:
                            ml_item['categoria']=''
                            ml_item['asin']=''
                            ml_item['rank']=''
                            ml_item['valoracion_media']=''

        else:#Sección "Información adicional"
            if len(Link)>1:
                Link[0]=Link[1]
            '''
            #Obtenemos asin de la misma forma que antes, pero le sumamos un valor más a indice porque aquí aparecen comillas:
            indice=Link[0].find('asin=')
            ml_item['asin']=Link[0][indice+5:indice+15]
            indice=Link[0].find('SalesRank')
            #Obtenemos categoría y rank de la misma forma que antes pero en este caso 'vendidos de Amazon' no lleva ':'
            clasificacion=Link[0][indice:]
            try:
                ml_item['rank']=int(re.findall(r'\b\d+\b', clasificacion.replace(".", "").replace(",", "").replace("nº", "nº "))[0])#El rank es un número que está despueés de nº 
            except:
                pass
            
            indice=clasificacion.find('<td class="value">')+19
            clasificacion=clasificacion[indice:]
            inicio1=clasificacion.find(' ')+1
            inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de el "en " empieza la categoria
            final=clasificacion.find("(")-1#Antes de "(" termina la categoría
            ml_item['categoria']=clasificacion[inicio:final]
            #Obtenemos valoración como antes:
            indice=Link[0].find('a-icon-alt')
            valoracion=Link[0][indice:]
            final=valoracion.find(" ")
            ml_item['valoracion_media']=valoracion[12:final]
            '''
            #print('4')
            #print(Link)
            ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details2(Link[0])
        if (self.marketplace=='it' or self.marketplace=='de') and ml_item['categoria'] != '':
            ml_item['categoria']=ml_item['categoria'][3:]

        #Obtenemos el vendedor:
        ml_item['seller']=response.xpath('//*[@id="merchant-info"]/a[1]/text()').extract()
        if len(ml_item['seller'])>0:#Si se ha encontrado vendedor lo guardamos
            ml_item['seller']=ml_item['seller'][0]
        else:
            ml_item['seller']=''

        #El término de búsqueda será el que hemos usado:
        ml_item['busqueda']=self.busqueda

        #Asignamos marketplace
        ml_item['marketplace']='amazon.'+self.marketplace

        
        #Por último, si hemos superado el número de items acabamos.
        self.item_count+=1
        if self.item_count>self.num_items:
            raise CloseSpider("item_exceded")
        yield ml_item

    #Ejemplo de estos productos: busca camiseta en amazon.es y selecciona uno
    def get_details(self, details):
        #Obtenemos ASIN:
        indice=details.find('asin=')#Buscamos en Link el asin
        asin=details[indice+5:indice+15]#El Asin estará a 5 posiciones de indice (porque len('asin=')==5) y tiene un tamaño de 10 (10+5=15)
        #Obtenemos categoria y rank:
        indice=details.find('SalesRank')#Esta información se encuentra despues de esta etiqueta
        clasificacion=details[indice:]#Nos quedamos con lo que hay a partir de esta información
        rank=''
        try:
            rank=int(re.findall(r'\b\d+\b', clasificacion.replace(".", "").replace(",", "").replace("nº", "nº "))[0])#El rank es un número que está despueés de nº 
        except:
            pass
        indice=clasificacion.find('</b>')+19
        clasificacion=clasificacion[indice:]
        inicio1=clasificacion.find(' ')+1
        inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de el "en " empieza la categoria
        final=clasificacion.find("(")-1#Antes de "(" termina la categoría
        categoria=clasificacion[inicio:final]
        if(len(categoria)>50):
            categoria=''
            rank=''
        #Obtenemos la valoración media:
        indice=details.find('a-icon-alt')#A partir de 'a-icon-alt' tenemos la valoración
        valoracion=details[indice:]
        final=valoracion.find(" ")
        valoracion_media=valoracion[12:final]#El principio de la valoración está a partir de el índice 12 y acaba cuando hay un espacio
        
        return asin, rank, categoria, valoracion_media, self.get_date(details)

    #Ejemplo de estos productos: busca calculadora en amazon.es y selecciona uno
    def get_details2(self, details):
        #Obtenemos asin de la misma forma que antes, pero le sumamos un valor más a indice porque aquí aparecen comillas:
        indice=details.find('asin=')
        if(self.marketplace=='com'):
            asin=details[indice+6:indice+16]
        else:
            asin=details[indice+5:indice+15]
        indice=details.find('SalesRank')
        if indice==-1:
            indice=details.find('Best Sellers Rank')
        #Obtenemos categoría y rank de la misma forma que antes pero en este caso 'vendidos de Amazon' no lleva ':'
        clasificacion=details[indice:]
        rank=''
        try:
            rank=int(re.findall(r'\b\d+\b', clasificacion.replace(".", "").replace(",", "").replace("nº", "nº "))[0])#El rank es un número que está despueés de nº 
        except:
            pass
        indice=clasificacion.find('<td class="value">')+19
        clasificacion=clasificacion[indice:]
        inicio1=clasificacion.find(' ')+1
        inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de el "en " empieza la categoria
        final=clasificacion.find("(")-1#Antes de "(" termina la categoría
        categoria=clasificacion[inicio:final]
        if(len(categoria)>50):
            categoria=''
            rank=''
        #Obtenemos valoración como antes:
        indice=details.find('a-icon-alt')
        valoracion=details[indice:]
        final=valoracion.find(" ")
        valoracion_media=valoracion[12:final]

 
        return asin, rank, categoria, valoracion_media, self.get_date(details)

    #Ejemplo de estos productos: busca shirt en amazon.com y selecciona uno
    def get_details3(self, details):
        
        #Obtenemos ASIN:
        indice=details.find('asin=')#Buscamos en Link el asin
        asin=details[indice+6:indice+16]#El Asin estará a 5 posiciones de indice (porque len('asin=')==5) y tiene un tamaño de 10 (10+5=15)
        #Obtenemos categoria y rank:
        indice=details.find('SalesRank')#Esta información se encuentra despues de esta etiqueta
        clasificacion=details[indice:]#Nos quedamos con lo que hay a partir de esta información
        rank=''
        try:
            rank=int(re.findall(r'\b\d+\b', clasificacion.replace(".", "").replace(",", "").replace("nº", "nº "))[0])#El rank es un número que está despueés de nº 
        except:
            pass
        indice=clasificacion.find('</b>')+5
        clasificacion=clasificacion[indice:]
        inicio1=clasificacion.find(' ')+1
        inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de el "en " empieza la categoria
        final=clasificacion.find("(")-1#Antes de "(" termina la categoría
        categoria=clasificacion[inicio:final]
        if(len(categoria)>50):
            categoria=''
            rank=''
        #Obtenemos la valoración media:
        indice=details.find('a-icon-alt')#A partir de 'a-icon-alt' tenemos la valoración
        valoracion=details[indice:]
        final=valoracion.find(" ")
        valoracion_media=valoracion[12:final]#El principio de la valoración está a partir de el índice 12 y acaba cuando hay un espacio
        
        return asin, rank, categoria, valoracion_media, self.get_date(details)

    def get_date(self, details):
        date=details.find("date-first-available")
        if date != -1:
            inicio=details[date:].find("value")+date+7
            final=details[inicio:].find('<')+inicio
            start_date=details[inicio:final]
        else:
            date=details.find("Date First Available")
            if date != -1:
                inicio=details[date:].find('<span>')+date+6
                final=details[inicio:].find('</span>')+inicio
                start_date=details[inicio:final]
            else:
                date=details.find(self.fecha_label[self.marketplace])
                if date==-1 and self.marketplace=='nl':
                    date=details.find('Oorspronkelijke publicatiedatum:')
                if date !=-1:
                    inicio=details[date:].find('</b>')+date+5
                    final=details[date:].find('</li>')+date
                    start_date=details[inicio:final]
                else:
                    start_date=''
        return start_date

