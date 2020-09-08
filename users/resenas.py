from scrapear import scrap_resenas
from scrapear import scrap_amazon
import pandas as pd
import time
import os
import datetime

#Función que dado un dataframe de reseñas devuelve otro dataframe con palabras positivas y negativas y la frecuencia. El umbral es la frecuencia con la cual quieres que aparezca la palabra en el dataframe
def palabras_clave(df, umbral):
    #Palabras que le pueden seguir 1 o más palabras importantes
    conectores=['bastante', 'tengo', 'hasta', 'llegó', 'llego', 'desde', 'gran', 'está', 'nada', 'buen', 'algo', 'ninguna', 'ningún', 'ningun', 'primera', 'primer',  'casi', 'problema',   'este', 'siguiente', 'unos', 'unas', 'cada', 'otro', 'otra', 'otros', 'otras', 'mucho', 'ahora',  'bien', 'daba',   'demasiado', 'bien', 'como', 'hace', 'porque', 'parece', 'otra']
    #Palabras que le pueden seguir 2 o más palabras importantes
    conectores2=['pero', 'aunque',  'aun que', 'para', 'además', 'ademas', 'también', 'tambien','creo', 'pensar', 'tiene', 'tenía', 'hay', 'había', 'sobre', 'puede', 'todo', 'toda', 'durante']
    
    #separamos el dataframe en comentarios positivas y negativas
    palabras_positivas={}
    palabras_negativas={}
    df=df.fillna(1)
    df_negativos = df.drop(df[df['estrellas']>3].index)
    df_positivos = df.drop(df[df['estrellas']<4].index)
    comentarios_positivos=list(df_positivos['descripcion'])
    comentarios_negativos=list(df_negativos['descripcion'])

    #Creamos listas con todas las palabras:
    palabras_positivas=list()
    for c in comentarios_positivos:
        palabras_positivas.extend(str(c).split())
    palabras_negativas=list()
    for c in comentarios_negativos:
        palabras_negativas.extend(str(c).split())
    

    #Las palabras que esten en conectores le añadimos 1, 2, 3, 4 y 5 palabras más y las que estén en conectores2 le añadimos 2, 3, 4 y 5
    for i in range(len(palabras_positivas)):
        if palabras_positivas[i] in conectores:
            try:
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2]+' '+palabras_positivas[i+3])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2]+' '+palabras_positivas[i+3]+' '+palabras_positivas[i+4])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2]+' '+palabras_positivas[i+3]+' '+palabras_positivas[i+4]+' '+palabras_positivas[i+5])
            except:
                pass
        elif palabras_positivas[i] in conectores2:
            try:
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2]+' '+palabras_positivas[i+3])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2]+' '+palabras_positivas[i+3]+' '+palabras_positivas[i+4])
                palabras_positivas.append(palabras_positivas[i]+' '+palabras_positivas[i+1]+' '+palabras_positivas[i+2]+' '+palabras_positivas[i+3]+' '+palabras_positivas[i+4]+' '+palabras_positivas[i+5])
            except:
                pass
    #Con negativas
    for i in range(len(palabras_negativas)):
        if palabras_negativas[i] in conectores:
            try:
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2]+' '+palabras_negativas[i+3])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2]+' '+palabras_negativas[i+3]+' '+palabras_negativas[i+4])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2]+' '+palabras_negativas[i+3]+' '+palabras_negativas[i+4]+' '+palabras_negativas[i+5])
            except:
                pass
        elif palabras_negativas[i] in conectores2:
            try:
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2]+' '+palabras_negativas[i+3])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2]+' '+palabras_negativas[i+3]+' '+palabras_negativas[i+4])
                palabras_negativas.append(palabras_negativas[i]+' '+palabras_negativas[i+1]+' '+palabras_negativas[i+2]+' '+palabras_negativas[i+3]+' '+palabras_negativas[i+4]+' '+palabras_negativas[i+5])
            except:
                pass

    #Sacamos la frecuencia de cada palabra en las listas y las ponemos en un diccionario
    frecuencia_positiva={}
    frecuencia_negativa={}
    for p in palabras_positivas:
        p=p.replace(".","").replace(",","").replace(";", "")
        p=p.lower()
        if len(p)>3 and p not in conectores and p not in conectores2:
            if p in frecuencia_positiva.keys():
                frecuencia_positiva[p]+=1
            else:
                frecuencia_positiva[p]=1
    for p in palabras_negativas:
        p=p.replace(".","").replace(",","").replace(";", "")
        p=p.lower()
        if len(p)>3 and p not in conectores and p not in conectores2:
            if p in frecuencia_negativa.keys():
                frecuencia_negativa[p]+=1
            else:
                frecuencia_negativa[p]=1

    #Creamos los dataframes y solo añadimos las palabras que superan el umbral:
    positivas = pd.DataFrame({'Palabra': [], 'Frecuencia': []})
    for key, value in frecuencia_positiva.items():
        if value>=umbral:
            positivas=positivas.append({'Palabra' : key , 'Frecuencia' : value} , ignore_index=True)
    positivas['valoracion']='Positiva'
    negativas = pd.DataFrame({'Palabra': [], 'Frecuencia': []})
    for key, value in frecuencia_negativa.items():
        if value>=umbral:
            negativas=negativas.append({'Palabra' : key , 'Frecuencia' : value} , ignore_index=True)
    negativas['valoracion']='Negativa'

    return positivas.append(negativas, ignore_index = True)

#Función que pasa de una fecha de formato string (ejemplo: 8 de febrero de 2019) y lo pasa a datetime
def cambio_a_fecha(fecha, marketplace):
    #EN estos marketplaces tenemos que hacer estos cambios
    if marketplace=='de':
        fecha=fecha.replace('.', '')
    if marketplace=='com' or marketplace=='ca':
        fecha=fecha.replace(',', '')
    #El año es el segundo número que tenemos, el día ponemos con uno porque lo que nos importa es el mes y el año
    numeros=[int(s) for s in fecha.split() if s.isdigit()]
    ano=numeros[1]
    dia=1
    #Según el marketplace se calcula el mes de una manera(hay que tener en cuenta el idioma)
    if marketplace=='es':
        meses={'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
        mes=fecha[fecha.find('de')+3:]
        mes=meses[mes[:mes.find('de')-1]]
    elif marketplace=='it':
        meses={'gennaio':1, 'febbraio':2, 'marzo':3, 'aprile':4, 'maggio':5, 'giugno':6, 'luglio':7, 'agosto':8, 'settembre':9, 'ottobre':10, 'novembre':11, 'dicembre':12}
        fecha=fecha[1:]
        mes=fecha[fecha.find(' ')+1:]
        mes=meses[mes[:mes.find(' ')]]
    elif marketplace=='fr':
        meses={'janvier':1, 'février':2, 'mars':3, 'avril':4, 'mai':5, 'juin':6, 'juillet':7, 'août':8, 'septembre':9, 'octobre':10, 'novembre':11, 'décembre':12}
        mes=fecha[fecha.find(' ')+1:]
        mes=meses[mes[:mes.find(' ')]]
    elif marketplace=='co.uk':
        meses={'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        fecha=fecha[12:]
        mes=fecha[fecha.find(' ')+1:]
        mes=meses[mes[:mes.find(' ')]]
    elif marketplace=='de':
        meses={'Januar':1, 'Februar':2, 'März':3, 'April':4, 'Mai':5, 'Juni':6, 'Juli':7, 'August':8, 'September':9, 'Oktober':10, 'November':11, 'Dezember':12}
        fecha=fecha[8:]
        mes=fecha[fecha.find(' ')+1:]
        mes=meses[mes[:mes.find(' ')]]
    elif marketplace=='com':
        meses={'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        fecha=fecha[10:]
        mes=fecha[fecha.find(' ')+1:]
        mes=meses[mes[:mes.find(' ')]]
    elif marketplace=='ca':
        meses={'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        mes=meses[fecha[:fecha.find(' ')]]

    #Devolvemos la fecha
    return datetime.datetime(year=ano, month=mes, day=dia)

    #Januar, Februar, März, April, Mai, Juni, Juli, August, September, Oktober, November und Dezember

from pandas import ExcelWriter
'''asins=['B07PY3GM9P', 'B083WM3XQC', 'B07DKPHTRH', 'B081ZCZGTT', 'B07V5BXRMD']
writer = ExcelWriter('top5resenas.xlsx')
for a in asins:
    scrap_resenas(a, 500, 'es')
    try:
        df=pd.read_csv(os.path.dirname(__file__)+'/scrap/resenas/rresenas_bot_items.csv')
        print(a)
        df.to_excel(writer, sheet_name=a)
    except:
        pass
writer.save()'''
#nombres=['B07PY3GM9P', 'B07DKPHTRH', 'B081ZCZGTT', 'B07V5BXRMD']
def otro():

    writer = ExcelWriter('palabras_clave_top5.xlsx')
    for n in nombres:
        df=pd.read_excel('top5resenas.xlsx', sheet_name=n)
        print(n)
        df2=palabras_clave(df, 4)
        df2.to_excel(writer, sheet_name=n)
    writer.save()

#df2=palabras_clave(df, 4)
#df2.to_excel('palabras_clave.xlsx')

'''competidores=['Colchón']
i=0
for i in range(len(competidores)):
    if i==0:
        scrap_amazon(competidores[i], 5, 'es')
        time.sleep(5)
        df=pd.read_csv(os.path.dirname(__file__)+"/scrap/amazon/amazon_bot_items.csv", encoding= 'utf-8')
        df.to_csv('scrap3.csv')
    else:
        scrap_amazon(competidores[i], 20, 'co.uk')
        time.sleep(5)
        df=pd.read_csv(os.path.dirname(__file__)+"/scrap/amazon/amazon_bot_items.csv", encoding= 'utf-8')
        df2=pd.read_csv("scrap.csv", encoding= 'utf-8')
        df=df.append(df2, ignore_index = True)
        df.to_csv('scrap.csv')'''

def hola():
    df=pd.read_csv("scrap.csv", encoding= 'utf-8')[['name', 'price','asin', 'seller', 'valoracion_media','busqueda', 'marketplace', 'start_date']]
    df = df.drop(df[df['asin']==''].index)
    df = df.drop(df[df['asin']=='class="a-r'].index)
    df['columna']=df['asin']+df['marketplace']
    df = df.drop_duplicates('columna')
    df=df[['name', 'price','asin', 'seller', 'valoracion_media','busqueda', 'marketplace', 'start_date']]
    df.to_excel('scrap2.xlsx')



def distintos():
    df=pd.read_excel("scrap2.xlsx", encoding= 'utf-8')
    df=df.fillna('')
    writer = ExcelWriter('competidores.xlsx')
    df['vendedores marketplace']=df['seller']+'*'+df['marketplace']
    all_sellers=list(set(list(df['vendedores marketplace'])))
    print(all_sellers)
    for s in all_sellers:
        indice=s.find('*')
        seller=s[:indice]
        seller=seller.replace("/", "")
        marketplace=s[indice+1:]
        dfaux=df.drop(df[df['seller']!=seller].index)
        dfaux=dfaux.drop(dfaux[dfaux['marketplace']!=marketplace].index)
        try:
            dfaux.to_excel(writer, sheet_name=seller+' '+marketplace)
        except:
            pass
        obten_resenas(list(dfaux['asin']), s[0], s[1])
    print(len(all_sellers))
    writer.save()
#distintos()
def obten_resenas():
    otra_vez=True
    df=pd.read_excel('productos_a_resenas.xlsx')
    writer = ExcelWriter('resenas.xlsx')
    all_sellers=list(set(list(df['vendedores marketplace'])))
    cont=0
    for s in all_sellers:
        
        indice=s.find('*')
        seller=s[:indice]
        seller=seller.replace("/", "")
        marketplace=s[indice+1:]
        dfaux=df.drop(df[df['vendedores marketplace']!=s].index)
        asins=list(dfaux['asin'])
        for i in range(len(asins)):
            print('-------------------------------------'+str(cont))
            cont+=1
            scrap_resenas(asins[i], 100, marketplace[7:])
            if otra_vez:
                try:
                    df2=pd.read_csv(os.path.dirname(__file__)+'/scrap/resenas/rresenas_bot_items.csv')
                    df2['asin']=asins[i]
                    print(df2)
                    otra_vez=False
                except:
                    print('******************************************************************************************')
                    pass
                
            else:
                try:
                    dfaux2=pd.read_csv(os.path.dirname(__file__)+'/scrap/resenas/rresenas_bot_items.csv')
                    dfaux2['asin']=asins[i]
                    df2=df2.append(dfaux2, ignore_index = True)
                    print(df2)
                except:
                    print('******************************************************************************************')
                    pass

        df2.to_excel(writer, sheet_name=s.replace('*', ''))
        otra_vez=True
        #except:
            #print('******************************************************************************************')
            #pass
    writer.save()
#obten_resenas()
#nombres=['Simba Sleepamazon.co.uk', 'bedzonlineamazon.co.uk', 'Molblly Home EUamazon.co.uk', 'Duermexamazon.es', 'VENTA-STOCKamazon.fr', 'ABeddingamazon.es', 'Grupo Simpuramazon.fr', 'Farmarelaxamazon.it', 'Dormideoamazon.es', 'CHANG XU DONG SHOPamazon.es', 'Buy Gifts, S.Lamazon.es', 'OUTLET-SOFA-DIRECTamazon.it', 'Materassiedogheamazon.it', 'Grupo Simpuramazon.es', 'NOFFA-WJamazon.fr', 'RS tradingamazon.it', 'Starlight Beds Ltdamazon.co.uk', 'ty56fdfamazon.co.uk',  'SETL GmbHamazon.it', 'Träumegut24amazon.de', 'literie-moins-cheramazon.fr', 'Kamahaus Storeamazon.es', 'xinhaowangamazon.fr', 'PROXELamazon.co.uk', 'ABUSINESSDCamazon.es', 'VISCOSOFTamazon.fr']
nombres=['PIKOLINamazon.es']
def otro():

    writer = ExcelWriter('palabras_clave_resenas.xlsx')
    for n in nombres:
        if n!='Träumegut24amazon.de' and n!='literie-moins-cheramazon.fr':
            df=pd.read_excel('resenas.xlsx', sheet_name=n)
            print(n)
            df2=palabras_clave(df, 6)
            df2.to_excel(writer, sheet_name=n)
    writer.save()
otro()
