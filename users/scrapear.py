import scrap.resenas.scrap_productos as r
import scrap.amazon.scrap_productos as a
import time
import pandas as pd
import os
from random import randrange
import threading

#Para ejecutar el scraping dentro del proyecto hay que llamar a las dos funciones siguientes:

def scrap_amazon(palabra, num, market):
    try:
        version=1
        mensaje='vuelve'
        while mensaje=='vuelve':
            mensaje=execute(palabra, num, market, version, False)
            version+=1
    except:
        pass

def scrap_resenas(palabra, num, market):
    try:
        version=randrange(1,15)
        mensaje='vuelve'
        #while mensaje=='vuelve':
        mensaje=execute(palabra, num, market, version, True)
        version+=1
    except:
        pass

def execute(palabra, num, market, version, resenas):#Llama a las funciones de scrap_productos.py
    if resenas:
        m=r.spider_crawler(palabra, num, market, version)#Se ejecuta el scraping y se espera un tiempo
        time.sleep(5+num/10)
    else:
        m=a.spider_crawler(palabra, num, market, version)
        time.sleep(20+num*1.5)
    try:
        #Probamos a ver si existen los csv:
        if resenas:
            df=pd.read_csv(os.path.dirname(__file__)+"/scrap/resenas/rresenas_bot_items.csv", encoding= 'utf-8')
        else:
            df=pd.read_csv(os.path.dirname(__file__)+"/scrap/amazon/amazon_bot_items.csv", encoding= 'utf-8')
    except:
        if version==15:
            return 'error' #No se puede ejecutar el scrap
        else:
            return 'vuelve' #Hay que volver a intentaro con otro número de versión
    if df.empty:
        if version==15:
            return 'error' #No se puede ejecutar el scrap
        else:
            return 'vuelve' #Hay que volver a intentaro con otro número de versión
    return m

