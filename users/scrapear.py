import scrap.resenas.scrap_productos as r
import scrap.amazon.scrap_productos as a
import time
import pandas as pd
import os
from random import randrange

#f.spider_crawler("mesa", 5, "es")
#palabras_clave=['ropa de montaña', 'pantalon de montaña', 'pantalon de trekking', 'pantalon de senderismo', 'forro polar', 'zapatillas de montaña', 'botas de montaña', 'camisetas de manga corta para deporte', 'camiseta termica para hombre y mujer', 'chaquetas de montaña']
#for p in palabras_clave:
def scrap_amazon(palabra, num, market):
    version=1
    mensaje='vuelve'
    while mensaje=='vuelve':
        mensaje=execute(palabra, num, market, version, False)
        version+=1

def scrap_resenas(palabra, num, market):
    version=1
    mensaje='vuelve'
    while mensaje=='vuelve':
        mensaje=execute(palabra, num, market, version, True)
        version+=1

def execute(palabra, num, market, version, resenas):
    if resenas:
        m=r.spider_crawler(palabra, num, market, version)
        time.sleep(5+num/20)
    else:
        m=a.spider_crawler(palabra, num, market, version)
        time.sleep(20+num*1.5)
    try:
        if resenas:
            df=pd.read_csv(os.path.dirname(__file__)+"/scrap/resenas/rresenas_bot_items.csv", encoding= 'utf-8')
        else:
            df=pd.read_csv(os.path.dirname(__file__)+"/scrap/amazon/amazon_bot_items.csv", encoding= 'utf-8')
    except:
        if version==5:
            return 'error' 
        else:
            return 'vuelve'
    if df.empty:
        if version==15:
            return 'error' 
        else:
            return 'vuelve'
    return m

'''i=10
if i!=0:
    df=pd.read_excel('C:/Users/mg_4_/OneDrive/Documentos/GitHub/amazonplatform-seller/users/scrap/amazon/amazon_bot_items.xlsx')
    df = df.drop(['Unnamed: 0'], axis=1)
    f.spider_crawler(palabras_clave[i], 10, 'es')
    df2=pd.read_csv('C:/Users/mg_4_/OneDrive/Documentos/GitHub/amazonplatform-seller/users/scrap/amazon/amazon_bot_items.csv')
    print(df2)
    
    df=df.append(df2, ignore_index = True)
    print(df)
    df.to_excel('C:/Users/mg_4_/OneDrive/Documentos/GitHub/amazonplatform-seller/users/scrap/amazon/amazon_bot_items.xlsx')
    
else:
    f.spider_crawler(palabras_clave[i], 10, 'es')
    df=pd.read_csv('C:/Users/mg_4_/OneDrive/Documentos/GitHub/amazonplatform-seller/users/scrap/amazon/amazon_bot_items.csv')
    df.to_excel('C:/Users/mg_4_/OneDrive/Documentos/GitHub/amazonplatform-seller/users/scrap/amazon/amazon_bot_items.xlsx')

'''