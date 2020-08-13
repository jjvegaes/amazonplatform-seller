import scrap.amazon.scrap_productos as f
import pandas as pd

#f.spider_crawler("mesa", 5, "es")
palabras_clave=['ropa de montaña', 'pantalon de montaña', 'pantalon de trekking', 'pantalon de senderismo', 'forro polar', 'zapatillas de montaña', 'botas de montaña', 'camisetas de manga corta para deporte', 'camiseta termica para hombre y mujer', 'chaquetas de montaña']
#for p in palabras_clave:
i=10
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

