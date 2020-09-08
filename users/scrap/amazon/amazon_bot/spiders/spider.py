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
    item_count=0 #Lo usaremos para saber cuantos productos llevamos scrapeados
    fecha_label={'es':'Producto en Amazon.es desde:', 'it':'Disponibile su Amazon.it a partire dal:', 'co.uk':'Date first available at Amazon.co.uk:', 'fr':'Date de mise en ligne sur Amazon.fr', 'nl':'Datum eerste beschikbaarheid op Amazon.nl:', 'de':'Im Angebot von Amazon.de seit:', 'com':'no disponible', 'ca':'Date first available at Amazon.ca:'} #Diccionario que se usará para sacar la fecha de cuando se subió el producto

    #Estas son las reglas que se seguirán para moverse dentro de la página
    rules={
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="a-last"]/a'))), #Esta regla nos permite pasar de página dentro de amazon (cuando se obtengan todos los productos de una página se pasará a la siguiente)
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a')), callback='parse_item', follow=False),#Esta regla nos permite ir seleccionando productos (cada vez que entre en un producto se llamará a la función parse_item)
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')), callback='parse_item', follow=False)#Esta regla permite seleccionar otro tipo de productos (cada vez que entre en un producto se llamará a la función parse_item)
        #Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="reviews-medley-footer"]/div[2]/a')), callback='parse_item', follow=False)#Esta regla permite seleccionar otro tipo de productos
    }

    #Al constructor le pasamos el término de búsqueda de amazon, el número máximo de items que vamos a scrapear y el marketplace en concreto (amazon.es, amazon.com, amazon.fr, amazon.it, ...)
    def __init__(self, busqueda, num_items, marketplace,  *args, **kwargs):
        self.start_urls=[ 'https://www.amazon.'+marketplace+'/s?k='+busqueda]#URL donde empieza la araña
        self.allowed_domain=['www.amazon.'+marketplace]
        self.num_items=num_items#Número de items para analizar
        self.busqueda=busqueda#Término de búsqueda
        self.marketplace=marketplace
        super(AmazonBotSpider, self).__init__(*args, **kwargs)#Llamamos al constructor del padre

    #Por cada producto se ejecuta esta función para obtener la información
    def parse_item(self, response):
        ml_item=AmazonBotItem()#Creamos un objeto tipo item (el producto en concreto)
        
        
        #Obtenemos el nombre del producto:
        ml_item['name']=response.xpath('//*[@id="productTitle"]/text()').extract()
        try:
            ml_item['name']=ml_item['name'][0][8:-7]#Eliminamos tabuladores
        except:
            pass
        #Obtenemos el precio del producto (el precio se puede encontrar en tres xpath distintos según el producto, por lo que comprobamos todas las posibilidades):
        ml_item['price']=response.xpath('//*[@id="priceblock_ourprice"]/text()').extract()
        if ml_item['price']==[]:
            ml_item['price']=response.xpath('//*[@id="priceblock_dealprice"]/text()').extract()
        if ml_item['price']==[]:
            ml_item['price']=response.xpath('//*[@id="priceblock_saleprice"]/text()').extract()
        #Puede ser que el precio no aparezca
        if len(ml_item['price'])>0:
            ml_item['price']=ml_item['price'][0]

        #A continuación sacamos toda la información que aparece en "Información adicional" o "detalles del producto" (según el producto la sección se llama de una forma u otra, por lo que se han contemplado todas posibilidades):
        Link = response.xpath('//*[@id="prodDetails"]/div').extract()#si la sección se llama información adicional, esta información se guardará en la variable
        if Link==[]:
            Link = response.xpath('//*[@id="detail_bullets_id"]').extract()#Como Link es vacío, la sección no es "información adicional" y tenemos que ver si es "detalles del producto"
            if Link!=[]:#Sección "detalles del productos
                #Link es un código HTML que se le pasa a las funciones get_details, get_details2 o get_details3 (según en la situación donde estemos) y te devuelve la información separada
                ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details(Link[0])
            else:#No existe esta sección, no podemos obtener estos datos, comprobamos más posibilidades
                if Link!=[]:
                    ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details3(Link[0])
                else:
                    Link = response.xpath('//*[@id="detail-bullets"]').extract()
                    if Link!=[]:
                        ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details(Link[0])
                    else:
                        Link=response.xpath('//*[@id="detailBullets"]').extract()
                        if Link!=[]:
                            ml_item['asin'], ml_item['rank'], ml_item['categoria'], ml_item['valoracion_media'], ml_item['start_date']=self.get_details3(Link[0])
                        else:#Si después de haber intentado sacar los detalles del producto mediante distintos xpath no se ha encontrado, lo asignamos a vacío
                            ml_item['categoria']=''
                            ml_item['asin']=''
                            ml_item['rank']=''
                            ml_item['valoracion_media']=''
        else:#Sección "Información adicional"
            if len(Link)>1:
                Link[0]=Link[1]
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


    #A continuación aparecen distintas funciones que permiten sacar los datos del html de la sección de detalles de producto, hay tres distintas porque existen varias opciones de que aparezcan estos datos:

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
        inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de dos espacios en blanco empieza la categoría
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
    def get_details2(self, details):#Esta función es parecida a antes pero cambiado algúnos parámeros
        #Obtenemos asin de la misma forma que antes, pero le sumamos un valor más a indice porque aquí aparecen comillas:
        indice=details.find('asin=')
        if(self.marketplace=='com'):#En amazon.com sale distinto que en los demás marketplaces
            asin=details[indice+6:indice+16]
        else:
            asin=details[indice+5:indice+15]
        indice=details.find('SalesRank')
        if indice==-1:#Si no está puesto con 'SalesRank' está escrito con 'Best Sellers Rank'
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
        inicio=clasificacion[inicio1:].find(' ')+inicio1+1#A partir de dos espacios en blanco empieza la categoria
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
        asin=details[indice+6:indice+16]#El Asin estará a 6 posiciones de indice (porque len('asin=')==5+1 posición de una comilla) y tiene un tamaño de 10 (10+6=16)
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

    #La fecha del producto la sacamos aparte:
    def get_date(self, details):
        date=details.find("date-first-available")
        if date != -1:#Si la fecha se llama 'date-first-available' en el HTML la obtenemos así:
            inicio=details[date:].find("value")+date+7#Después de value y 7 posiciones tenemos la fecha
            final=details[inicio:].find('<')+inicio#Antes de < termina la fecha
            start_date=details[inicio:final]
        else:
            date=details.find("Date First Available")
            if date != -1:# Sino, la fecha se puede llamar 'Date First Available' en el HTML
                inicio=details[date:].find('<span>')+date+6#Encontramos la fecha entre las etiquetas <span>
                final=details[inicio:].find('</span>')+inicio
                start_date=details[inicio:final]
            else:#Si la fecha no tiene id podemos encontrarla por el texto que aparece antes, usaremos el diccionario fecha_label para saber como aparece ese texto en cada país
                date=details.find(self.fecha_label[self.marketplace])
                if date==-1 and self.marketplace=='nl':#En nl se puede llamar de dos maneras
                    date=details.find('Oorspronkelijke publicatiedatum:')
                if date !=-1:#La fecha la encontramos después de la etiqueta </B>
                    inicio=details[date:].find('</b>')+date+5
                    final=details[date:].find('</li>')+date
                    start_date=details[inicio:final]
                else:
                    start_date=''
        return start_date

