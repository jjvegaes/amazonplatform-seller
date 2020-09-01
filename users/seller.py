from graficos import graficas
from cambiar_region import cambiar_region
import pandas as pd
from datetime import datetime
import os
import plotly.express as px
import plotly
from limpieza import Limpieza
from threading import Thread
import threading
import time
import math
import re
#from users.scrapear import scrap_amazon
#from users.scrapear import scrap_resenas
from datetime import datetime
#from users.resenas import palabras_clave, cambio_a_fecha

mutex=threading.Lock()

class crearGraficasSeller():
    def __init__(self, vendedor, access_key, merchant_id, secret_key):
        self.gr=graficas({})#Guardaremos los df y crearemos las gráficas
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)#Ruta de este archivo
        #Credenciales de la cuenta:
        self.access_key=access_key
        self.merchant_id=merchant_id
        self.secret_key=secret_key
        #IDs de los informes a usar:
        self.dict_reports={'datos inventario':'_GET_AFN_INVENTORY_DATA_', 'comentarios negativos':'_GET_SELLER_FEEDBACK_DATA_', 'estado inventario':'_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_','envios amazon':'_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_', 'exceso inventario':'_GET_EXCESS_INVENTORY_DATA_'}

    #FILTROS

    def filtra_x_asin(self, df, asin):
        if asin!=None:
            return df[df.asin.isin(asin)]
        else:
            return df

    def filtra_x_search_asin(self, df, asin):
        if asin!=None:
            return df[df['asin'].str.contains(asin, case=False)]
        else:
            return df

    def filtra_x_titulo(self, df, titulo):
        if titulo!=None:
            return df[df['product-name'].isin(titulo)]
        else:
            return df

    def filtra_x_search_titulo(self, df, titulo):
        if titulo!=None:
            return df[df['product-name'].str.contains(titulo, case=False)]
        else:
            return df

    #Filtro general (llama a todos los demás)
    def filtra(self, df, asin, asin_search, titulo, titulo_search):
        return self.filtra_x_asin(self.filtra_x_search_asin(self.filtra_x_titulo(self.filtra_x_search_titulo(df, titulo_search),titulo), asin_search), asin)

    #Obtención de informes usando mws:

    #Informes que no son históricos (el nuevo sustituye al viejo y si no existe se crea)
    def mws_csv(self, id, n_weeks_ago):
        mutex.acquire()
        try:
            l=Limpieza()
            df=l.limpieza2(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], n_weeks_ago)
            if df.__str__() != "None": 
                df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+str(n_weeks_ago)+'.csv')
                print('Cargado el informe '+id)
            f=open(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+str(n_weeks_ago)+'.txt', 'w')
            f.write(str(datetime.now()))
            f.close()
            mutex.release()
        except:
            mutex.release()

    #Informes históricos (si no existe se crea y si existe se obtiene el informe de la última semana y se actualiza el actual)
    def mws_csv_historico(self, id, n_weeks_ago):
        mutex.acquire()
        try:
            l=Limpieza()
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.csv')
            df = df.drop(['Unnamed: 0'], axis=1)
            df2=l.limpieza2(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], 1)
            if df2.__str__() != "None": 
                df=df.append(df2, ignore_index = True)
                if id=='envios amazon':
                    df = df.drop_duplicates('b"amazon-order-id')
                elif id=='comentarios negativos':
                    df= df.drop_duplicates('Comentarios')
                df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.csv', encoding="utf-8")
                print('Cargado el informe '+id)
            f=open(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.txt', 'w')
            f.write(str(datetime.now()))
            f.close()
            mutex.release()
        except:
            try:
                l=Limpieza()
                df=l.limpieza2(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], n_weeks_ago)
                if df.__str__() != "None": 
                    df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.csv')
                    print('Cargado el informe '+id)
                f=open(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.txt', 'w')
                f.write(str(datetime.now()))
                f.close()
                mutex.release()
            except:
                mutex.release()
        

    #INFORME: ENVÍOS AMAZON


    #Obtiene el histórico de envíos:
    def get_envios_amazon_historico(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        #Si no existe lo crea:
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.csv')
            f = open (self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.txt','r')
            ult_fecha = f.read()
            f.close()
        except:
            self.mws_csv_historico('envios amazon', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.csv')
                f = open (self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.txt','r')
                ult_fecha = f.read()
                f.close()
            except:
                return
        #Obtiene equivalencia entre asin y sku porque 'envios amazon' no tiene asin:
        try:
            inventario=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/datos inventario/datos inventario'+'1'+'.csv')
            f = open (self.myRute+'/informes_seller/'+self.vendedor+'/datos inventario/datos inventario'+'1'+'.txt','r')
            ult_fecha2 = f.read()
            f.close()
        except:
            self.mws_csv('datos inventario', 1)
            try:
                inventario=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/datos inventario/datos inventario'+'1'+'.csv')
                f = open (self.myRute+'/informes_seller/'+self.vendedor+'/datos inventario/datos inventario'+'1'+'.txt','r')
                ult_fecha2 = f.read()
                f.close()
            except:
                return
        #Cruzamos invenario con df para que aparezca asin:
        inventario=inventario[["b'seller-sku",'asin']] 
        inventario = inventario.rename(columns = {"b'seller-sku" : "sku"})
        inventario = inventario.drop_duplicates('sku')
        df=pd.merge(df, inventario, on='sku')
        #Limpiamos las variables con las que vamos a calcular los ingresos:
        variables_ingresos=['item-price', 'shipping-price', 'item-tax', 'shipping-tax', "gift-wrap-price", "item-promotion-discount", "ship-promotion-discount"]
        for v in variables_ingresos:
            for i in range(len(df[v])):
                if df[v][i] != df[v][i]:
                    df[v][i]=0
        df["Ingresos"]=df["item-price"]+df["shipping-price"]+df["item-tax"]+df["shipping-tax"]+df["gift-wrap-price"]+df["item-promotion-discount"]+df["ship-promotion-discount"]
        dfaux=df[['asin', 'product-name']]
        dfaux=dfaux.drop_duplicates('asin')
        todos_asin=list(dfaux['asin'])
        todos_titulos=list(dfaux['product-name'])
        df1=df.groupby(by="asin", as_index=False).sum()
        df1=pd.merge(df1, dfaux, on='asin')
        df1=df1.sort_values('Ingresos').iloc[::-1]
        df2 =df1.nlargest(20, 'Ingresos')#Obtenemos los 20 ASIN con más ingresos
        df3 =df1.nlargest(20, 'quantity-shipped')#Obtenemos los 20 asin con más unidades enviadas
        #Para el precio medio de venta:
        df4=df.copy()
        df4['ingresos por día']=''
        for i in range(len(df4['payments-date'])):
            df4['ingresos por día'][i]=df4['payments-date'][i][:10]
        df4=df4.groupby(by="ingresos por día", as_index=False).sum()
        df4=df4.sort_values('ingresos por día').iloc[::-1]
        df4['Precio medio de venta']=df4['Ingresos']/df4['quantity-shipped']
        #Para el mapa de calor:
        o=cambiar_region(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.csv')
        df5=o.accion()
        variables_ingresos=['item-price', 'shipping-price', 'item-tax', 'shipping-tax', "gift-wrap-price", "item-promotion-discount", "ship-promotion-discount"]
        for v in variables_ingresos:
            for i in range(len(df5[v])):
                if df5[v][i] != df5[v][i]:
                    df5[v][i]=0
        df5["Ingresos"]=df5["item-price"]+df5["shipping-price"]+df5["item-tax"]+df5["shipping-tax"]+df5["gift-wrap-price"]+df5["item-promotion-discount"]+df5["ship-promotion-discount"]
        #df["Ingresos por envíos"] = df["Ingresos por envíos"].apply(pd.to_numeric)
        #Guardamos los dataframes:
        self.gr.add_df('envios gestionados por amazon', self.filtra(df1, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon 20 ingresos', self.filtra(df2, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon 20 cantidad', self.filtra(df3, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon historico', self.filtra(df4, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon mapa', self.filtra(df5, asin, search_asin, titulo, search_titulo))
        #df.to_excel(self.myRute+'/informes_seller/'+self.vendedor+'/envios_amazon/envios_gestionados_por_amazon.xlsx')
        return todos_asin, todos_titulos, ult_fecha, ult_fecha2
    #Creamos todas las gráficas

    def graph_envios_amazon(self):
        try:
        #return self.gr.get_html(self.gr.circular('envios gestionados por amazon', ['sales-channel', 'sku'], 'quantity-shipped', 'prueba'))
            return self.gr.get_html(self.gr.tam(self.gr.barras('envios gestionados por amazon',etiquetas=['asin'], valores=['Ingresos'], titulo='Ingresos por ASIN', colores=True, orientacion='v', hovertext=['product-name']), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Ingresos por ASIN"\n\n'
    
    def graph_envios_amazon2(self):
        try:
            gr1={'id':'circular', 'id_df':'envios gestionados por amazon 20 ingresos', 'etiquetas':['asin'], 'valor':'Ingresos', 'titulo':'Ingresos', 'row':0, 'col':0, 'hovertext':['product-name']}
            gr2={'id':'circular','id_df':'envios gestionados por amazon 20 cantidad', 'etiquetas':['asin'], 'valor':'quantity-shipped', 'titulo':'Unidades','row':0, 'col':1, 'hovertext':['product-name']}
            return self.gr.get_html(self.gr.tam(self.gr.varios([gr1, gr2], 'Top 20 productos', 2, 1),h=600, color='lightblue'))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Top 20 productos"\n\n'


    def graph_envios_amazon3(self):
        try:
            gr1={'id':'temporal', 'x':'ingresos por día', 'y':'Ingresos', 'secondary_y':False, 'hovertext':None}
            gr2={'id':'temporal', 'x':'ingresos por día', 'y':'Precio medio de venta', 'secondary_y':True, 'hovertext':None}
            return self.gr.get_html(self.gr.multiple('envios gestionados por amazon historico', [gr1, gr2], 'Tendencias de rendimiento de ventas', True, 'Ingresos por envíos', 'Precio medio de venta'))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Ingresos por ASIN"\n\n'

    def graph_envios_amazon4(self):
        try:
            return self.gr.get_html(self.gr.mapa_calor('envios gestionados por amazon mapa', 'Ingresos', hovertext=[]))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Mapa de calor de ingresos"\n\n'

    #INFORME: ESTADO DEL INVENTARIO

    def get_estado_inventario(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+str(n_weeks_ago)+'.csv', encoding='cp1252')
            f = open (self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+str(n_weeks_ago)+'.txt','r')
            ult_fecha = f.read()
            f.close()
        except:
            self.mws_csv('estado inventario', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+str(n_weeks_ago)+'.csv')
                f = open (self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+str(n_weeks_ago)+'.txt','r')
                ult_fecha = f.read()
                f.close()
            except:
                return
        df=df.sort_values('total-quantity').iloc[::-1]
        todos_asin=list(df['asin'])
        todos_titulo=list(df['product-name'])
        self.gr.add_df('estado inventario', self.filtra(df, asin, search_asin, titulo, search_titulo))
        return todos_asin, todos_titulo, ult_fecha


    def graph_estado_inventario(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.barras('estado inventario',etiquetas=['asin'], valores=['total-quantity','sellable-quantity'], titulo='Inventario disponible', colores=False, orientacion='v', hovertext=['product-name']), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "INventario disponible"\n\n'

    #INFORME: COMENTARIOS NEGATIVOS

    def get_comentarios_negativos(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/comentarios negativos/comentarios negativos'+'historico'+'.csv', encoding='utf-8')
            f = open (self.myRute+'/informes_seller/'+self.vendedor+'/comentarios negativos/comentarios negativos'+'historico'+'.txt','r')
            ult_fecha = f.read()
            f.close()        
        except:
            self.mws_csv_historico('comentarios negativos', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/comentarios negativos/comentarios negativos'+'historico'+'.csv')
                f = open (self.myRute+'/informes_seller/'+self.vendedor+'/comentarios negativos/comentarios negativos'+'historico'+'.txt','r')
                ult_fecha = f.read()
                f.close() 
            except:
                return
        #df["Comentarios"]=df["Comentarios"].astype(str)
        #df["Comentarios"]=[x.encode("utf-8") for x in list(df['Comentarios'])]
        df = df.rename(columns = {"Clasificaci\\xc3\\xb3n" : "Clasificación"})
        self.gr.add_df('comentarios negativos', df)
        return ult_fecha

    #INFORME EXCESO DE INVENTARIO

    def graph_comentarios_negativos(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.tabla('comentarios negativos',etiquetas=["b'Fecha", "Clasificación", 'Comentarios', 'Tu respuesta', 'E-mail del cliente'], titulo='Comentarios negativos'), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Comentarios negativos"\n\n'

    def get_exceso_inventario(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.csv')
            f = open (self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.txt','r')
            ult_fecha = f.read()
            f.close() 
        except:
            self.mws_csv('exceso inventario', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.csv')
                f = open (self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.txt','r')
                ult_fecha = f.read()
                f.close() 
            except:
                return
        df["a"]=1
        df =df.rename(columns = {'Asin' : 'asin', 'Product Name':'product-name'})
        df['Your Price']=[float(re.findall("\d+\.\d+", x)[0]) for x in list(df['Your Price'])]
        marketplaces=set(list(df['Marketplace']))
        for m in marketplaces:
            dfaux=df[df.Marketplace.isin([m])]
            self.gr.add_df('excedente de inventario '+m, self.filtra(dfaux, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('excedente de inventario', self.filtra(df, asin, search_asin, titulo, search_titulo))
        return ult_fecha

    def graph_exceso_inventario(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.barras('excedente de inventario',etiquetas=['asin'], valores=['Total Quantity (Sellable)', 'Estimated Excess'], titulo='Cantidad total y excesa', orientacion='v', hovertext=['product-name']), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Cantidad total y excesa de inventario"\n\n'
    
    def graph_exceso_inventario2(self):
        try:
            gr1={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['asin', 'Marketplace'], 'valores':['Units Sold - Last 7 Days'], 'orientacion':'v', 'hovertext':['Marketplace'], 'row':0, 'col':0, 'titulo':'Unidades vendidas últimos 7 días', 'colores':False}
            gr2={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['asin', 'Marketplace'], 'valores':['Units Sold - Last 30 Days'], 'orientacion':'v', 'hovertext':['Marketplace'], 'row':0, 'col':1, 'titulo':'Unidades vendidas últimos 30 días', 'colores':False}
            gr3={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['asin', 'Marketplace'], 'valores':['Units Sold - Last 60 Days'], 'orientacion':'v', 'hovertext':['Marketplace'], 'row':1, 'col':0, 'titulo':'Unidades vendidas últimos 60 días', 'colores':False}
            gr4={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['asin', 'Marketplace'], 'valores':['Units Sold - Last 90 Days'], 'orientacion':'v', 'hovertext':['Marketplace'], 'row':1, 'col':1, 'titulo':'Unidades vendidas últimos 90 días', 'colores':False}
            fig = self.gr.tam(self.gr.varios([gr1, gr2, gr3, gr4], 'Unidades vendidas de inventario exceso', 2, 2), h=800, color='lightblue')
            fig.update_layout(showlegend=False)
            return self.gr.get_html(fig)
            #return self.gr.get_html(self.gr.tam(self.gr.barras('excedente de inventario',etiquetas=['Asin'], valores=['Units Sold - Last 7 Days', 'Units Sold - Last 30 Days', 'Units Sold - Last 60 Days', 'Units Sold - Last 90 Days'], titulo='Unidades vendidas de los productos excesos', orientacion='v', hovertext=['Product Name']), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Unidades vendidas de inventario exceso"\n\n'   
    
    def graph_exceso_inventario3(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.circular('excedente de inventario', etiquetas=[ 'Alert', 'Marketplace', 'asin'], valor='a', titulo='Alertas', hovertext=['product-name']), h=800))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Ingresos por ASIN"\n\n'

    def graph_exceso_inventario4(self):
        #try:
        marketplaces=set(list(self.gr.dict_df['excedente de inventario']['Marketplace']))
        grs=""
        for m in marketplaces:
            gr1={'id':'lineal', 'x':'asin', 'y':'Your Price', 'rectas':True, 'puntos':False, 'hovertext':None, 'secondary_y':True}
            gr2={'id':'lineal', 'x':'asin', 'y':'Recommended sales price', 'rectas':True, 'puntos':False, 'hovertext':None, 'secondary_y':True}
            gr3={'id':'barras', 'etiquetas':['asin'], 'valores':['Recommended sale duration (days)'], 'colores':False, 'hovertext':['product-name'], 'secondary_y':False}
            grs+= self.gr.get_html(self.gr.tam(self.gr.multiple('excedente de inventario '+m, [gr3, gr1, gr2], 'Precio de venta y recomendado '+m, True, 'Días', 'Precio'), h=450, color='aquamarine'))
        return grs
        #except:
        #    return '\n\nNo se ha podido cargar el gráfico "Precio de venta y recomendado"\n\n'

    def get_competidores(self, termino, num_items, marketplace):
        try:
            scrap_amazon(termino, num_items, marketplace)
            df=pd.read_csv(self.myRute+'/scrap/amazon/amazon_bot_items.csv')
            self.gr.add_df('competidores', df)
        except:
            pass

    def graph_competidores(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.tabla('competidores',etiquetas=(self.gr.dict_df['competidores'].columns), titulo='Palabra clave'), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Competidores"\n\n'

    def get_resenas(self, asin, num_items, marketplace):
        try:
            scrap_resenas(asin, num_items, marketplace)
            df=pd.read_csv(self.myRute+'/scrap/resenas/rresenas_bot_items.csv')
            df["Valoración"] = df.apply(lambda x: "Positivo" if int(x["estrellas"]) > 3 else "Negativo", axis=1)
            df["Cantidad"]=1
            self.gr.add_df('resenas', df)
            df2=palabras_clave(df, 4)
            print(df2)
            pos = df2.drop(df2[df2['valoracion']=='Negativa'].index)
            neg = df2.drop(df2[df2['valoracion']=='Positiva'].index)
            self.gr.add_df('palabras clave pos', pos)
            self.gr.add_df('palabras clave neg', neg)
            dfaux=df.copy()
            #dfaux['fecha']=dfaux.apply(lambda x: cambio_a_fecha(dfaux['fecha'], marketplace), axis=1)
            dfaux['fecha']=[cambio_a_fecha(x, marketplace) for x in list(dfaux['fecha'])]
            dfaux = dfaux.groupby(by="fecha", as_index=False).sum()
            print(dfaux.columns)
            self.gr.add_df('resenas tiempo', dfaux)
        except:
            pass

    def graph_resenas(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.tabla('resenas',etiquetas= ['comprador', 'fecha', 'estrellas', 'titulo', 'descripcion'], titulo='Reseñas', columnwidth=[50, 50, 20, 50, 200]), h=700))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Reseñas"\n\n'

    def graph_resenas2(self):
        try:
            gr1={'id':'circular', 'id_df':'resenas', 'etiquetas':['Valoración'], 'valor':'Cantidad', 'hovertext':[], 'row':0, 'col':1, 'titulo':'Cantidad de comentarios positivos y negativos'}
            gr2={'id':'indicador', 'id_df':'resenas', 'etiqueta':'estrellas', 'mean':True, 'formato':{'suffix': "estrellas"}, 'row':0, 'col':0, 'titulo':'Valoración media'}
            return self.gr.get_html(self.gr.tam(self.gr.varios([gr2, gr1], 'Valoración del producto:', 2, 1), h=500, color='lightblue'))
        except:
            return '\n\nNo se ha podido cargar el gráfico "Valoración del producto"\n\n'

    def graph_resenas3(self):
        try:
            return self.gr.get_html(self.gr.word_cloud('palabras clave pos', 'Palabra', 'Frecuencia', 'Palabras más repetidas en reseñas positivas'))
        except:
            return'\n\nNo se ha podido cargar el gráfico "Palabras más repetidas en reseñas positivas"\n\n'

    def graph_resenas4(self):
        try:
            return self.gr.get_html(self.gr.word_cloud('palabras clave neg', 'Palabra', 'Frecuencia', 'Palabras más repetidas en reseñas negativas'))
        except:
            return'\n\nNo se ha podido cargar el gráfico "Palabras más repetidas en reseñas negativas"\n\n'

    def graph_resenas5(self):
        try:
            return self.gr.get_html(self.gr.temporal('resenas tiempo', 'fecha', 'Cantidad', 'Número de reseñas por día'))
        except:
            return'\n\nNo se ha podido cargar el gráfico "Palabras más repetidas en reseñas negativas"\n\n'


access_key='AKIAIRF2R7EOJFNTGBEA'
merchant_id='A2GU67S0S60AC1'
secret_key='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'


def ventas_seller(vendedor, access_key, merchant_id, secret_key, n_weeks_ago=None, asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    todos_asin, todos_titulos, ult_fecha, ult_fecha2=cgs.get_envios_amazon_historico(n_weeks_ago=5, asin=asin, search_asin=search_asin, titulo=titulo, search_titulo=search_titulo)
    graph='<div class="caption v-middle text-center">Última hora actualización envios amazon:'+ult_fecha+'</div>'
    graph+='<div class="caption v-middle text-center">Última hora actualización datos inventario:'+ult_fecha2+'</div>'
    if len(threading.enumerate())<15:
        hilo=Thread(target=cgs.mws_csv_historico, args=['envios amazon', 20])
        hilo3=Thread(target=cgs.mws_csv, args=['datos inventario', 1])
        try:
            hilo.start()
            hilo3.start()
            graph+='Se actualizan los gráficos'
        except:
            graph+='No se actualizan los gráficos'
    graph+= cgs.graph_envios_amazon()
    graph+=cgs.graph_envios_amazon2()
    graph+=cgs.graph_envios_amazon3()
    graph+=cgs.graph_envios_amazon4()
    return graph

def productos_seller(vendedor, access_key, merchant_id, secret_key, n_weeks_ago=None, asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    todos_asin, todos_titulo, ult_fecha=cgs.get_estado_inventario(n_weeks_ago=n_weeks_ago, asin=asin, search_asin=search_asin, titulo=titulo, search_titulo=search_titulo)
    ult_fecha2=cgs.get_exceso_inventario(n_weeks_ago, asin, search_asin, titulo, search_titulo)
    graph='<div class="caption v-middle text-center">Última hora actualización estado inventario:'+ult_fecha+'</div>'
    graph+='<div class="caption v-middle text-center">Última hora actualización exceso inventario:'+ult_fecha2+'</div>'
    if len(threading.enumerate())<15:
        hilo=Thread(target=cgs.mws_csv, args=['estado inventario', 1])
        hilo2=Thread(target=cgs.mws_csv, args=['exceso inventario', 1])
        try:
            hilo.start()
            hilo2.start()
            graph+='Se actualizan los gráficos'
        except:
            graph+='No se actualizan los gráficos'
    graph+=cgs.graph_estado_inventario()
    graph+=cgs.graph_exceso_inventario()
    graph+=cgs.graph_exceso_inventario2()
    graph+=cgs.graph_exceso_inventario3()
    graph+=cgs.graph_exceso_inventario4()
    return graph

def customers_seller(vendedor, access_key, merchant_id, secret_key, n_weeks_ago=None, asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    ult_fecha=cgs.get_comentarios_negativos(n_weeks_ago=5, asin=asin, search_asin=search_asin, titulo=titulo, search_titulo=search_titulo)
    graph='<div class="caption v-middle text-center">Última hora actualización comentarios negativos:'+ult_fecha+'</div>'
    if len(threading.enumerate())<15:
        hilo=Thread(target=cgs.mws_csv_historico, args=['comentarios negativos', 20])
        try:
            hilo.start()
            graph+='Se actualizan los gráficos'
        except:
            graph+='No se actualizan los gráficos'
    graph+=cgs.graph_comentarios_negativos()
    return graph

def competidores_seller(termino=None, num_items=None, marketplace=None):
    '''if termino!= None and num_items != None and marketplace != None and termino != '' and num_items != '' and marketplace != '':
        cgs=crearGraficasSeller('', '', '', '')
        cgs.get_competidores(termino, num_items, marketplace)
        return cgs.graph_competidores()
    else:'''
    return '<div class="caption v-middle text-center">Seleccione término de búsqueda, número de itmes y marketplace para ver los competidores:</div>'

def resenas_seller(asin=None, num_items=None, marketplace=None):
    '''if asin!=None and num_items != None and marketplace!= None and asin!='' and num_items!='' and marketplace !='':
        cgs=crearGraficasSeller('', '', '', '')
        cgs.get_resenas(asin, int(num_items), marketplace)
        graph= cgs.graph_resenas()
        graph+=cgs.graph_resenas2()
        graph+=cgs.graph_resenas3()
        graph+=cgs.graph_resenas4()
        graph+=cgs.graph_resenas5()
        return graph
    else:'''
    return '<div class="caption v-middle text-center">Seleccione ASIN, número de itmes y marketplace para ver las reseñas:</div>'


#print(resenas_seller('B01NH0XWNU', 100, 'ca'))


#print(ventas_seller('izas', access_key, merchant_id, secret_key, 1))
#print(datetime.now())
#hilo=Thread(target=hola, args=['envios amazon'], name='mws')
#hilo.start()
#list=[x.getName() for x in threading.enumerate()]
#print(list)
#cgs=crearGraficasSeller('nose', access_key, merchant_id, secret_key)
#cgs.mws_csv('exceso inventario',2)