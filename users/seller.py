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

mutex=threading.Lock()

class crearGraficasSeller():
    def __init__(self, vendedor, access_key, merchant_id, secret_key):
        self.gr=graficas({})
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)
        self.access_key=access_key
        self.merchant_id=merchant_id
        self.secret_key=secret_key
        self.dict_reports={'envios amazon':'_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_', 'exceso inventario':'_GET_EXCESS_INVENTORY_DATA_'}

    def filtra_x_asin(self, df, asin):
        if asin!=None:
            return df[df.ASIN.isin(asin)]
        else:
            return df

    def filtra_x_search_asin(self, df, asin):
        if asin!=None:
            return df[df['ASIN'].str.contains(asin, case=False)]
        else:
            return df

    def filtra_x_titulo(self, df, titulo):
        if titulo!=None:
            return df[df['Título del producto'].isin(titulo)]
        else:
            return df

    def filtra_x_search_titulo(self, df, titulo):
        if titulo!=None:
            return df[df['Título del producto'].str.contains(titulo, case=False)]
        else:
            return df

    def filtra(self, df, asin, asin_search, titulo, titulo_search):
        return self.filtra_x_asin(self.filtra_x_search_asin(self.filtra_x_titulo(self.filtra_x_search_titulo(df, titulo_search),titulo), asin_search), asin)

    def mws_csv(self, id, n_weeks_ago):
        mutex.acquire()
        l=Limpieza()
        df=l.limpieza(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], n_weeks_ago)
        if df.__str__() != "None": 
            df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+str(n_weeks_ago)+'.csv')
            print('Cargado el informe '+id)
        mutex.release()



    def get_envios_amazon(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+str(n_weeks_ago)+'.csv')
        except:
            self.mws_csv('envios amazon', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+str(n_weeks_ago)+'.csv')
                self.gr.add_df('envios gestionados por amazon', self.filtra(df, asin, search_asin, titulo, search_titulo))
            except:
                pass
        
        #df.to_excel(self.myRute+'/informes_seller/'+self.vendedor+'/envios_amazon/envios_gestionados_por_amazon.xlsx')
    
    def graph_envios_amazon(self):
        return self.gr.get_html(self.gr.circular('envios gestionados por amazon', ['sales-channel', 'sku'], 'quantity-shipped', 'prueba'))

    def graph_envios_amazon2(self):
        pass


    def get_exceso_inventario(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.csv')
        except:
            self.mws_csv('exceso inventario', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.csv')
                self.gr.add_df('excedente de inventario', self.filtra(df, asin, search_asin, titulo, search_titulo))
            except:
                pass


    def graph_exceso_inventario(self):
        try:
            return self.gr.get_html(self.gr.tam(self.gr.barras('excedente de inventario',etiquetas=['Asin'], valores=['Total Quantity (Sellable)', 'Estimated Excess'], titulo='Cantidad total y excesa', orientacion='v', hovertext=['Product Name']), h=700))
        except:
            return 'No se ha podido cargar el gráfico'
    
    def graph_exceso_inventario2(self):
        try:
            gr1={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['Asin', 'Marketplace'], 'valores':['Units Sold - Last 7 Days'], 'orientacion':'v', 'hovertext':['Product Name'], 'row':0, 'col':0, 'titulo':'Unidades vendidas últimos 7 días', 'colores':False}
            gr2={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['Asin', 'Marketplace'], 'valores':['Units Sold - Last 30 Days'], 'orientacion':'v', 'hovertext':['Product Name'], 'row':0, 'col':1, 'titulo':'Unidades vendidas últimos 30 días', 'colores':False}
            gr3={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['Asin', 'Marketplace'], 'valores':['Units Sold - Last 60 Days'], 'orientacion':'v', 'hovertext':['Product Name'], 'row':1, 'col':0, 'titulo':'Unidades vendidas últimos 60 días', 'colores':False}
            gr4={'id':'barras', 'id_df':'excedente de inventario', 'etiquetas':['Asin', 'Marketplace'], 'valores':['Units Sold - Last 90 Days'], 'orientacion':'v', 'hovertext':['Product Name'], 'row':1, 'col':1, 'titulo':'Unidades vendidas últimos 90 días', 'colores':False}
            return self.gr.get_html(self.gr.tam(self.gr.varios([gr1, gr2, gr3, gr4], 'Unidades vendidas', 2, 2), h=500, color='lightblue'))
            #return self.gr.get_html(self.gr.tam(self.gr.barras('excedente de inventario',etiquetas=['Asin'], valores=['Units Sold - Last 7 Days', 'Units Sold - Last 30 Days', 'Units Sold - Last 60 Days', 'Units Sold - Last 90 Days'], titulo='Unidades vendidas de los productos excesos', orientacion='v', hovertext=['Product Name']), h=700))
        except:
            return 'No se ha podido cargar el gráfico'

access_key='AKIAIRF2R7EOJFNTGBEA'
merchant_id='A2GU67S0S60AC1'
secret_key='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'


def ventas(vendedor, access_key, merchant_id, secret_key, n_weeks_ago, asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    cgs.get_envios_amazon(n_weeks_ago, asin, search_asin, titulo, search_titulo)
    if len(threading.enumerate())<15:
        hilo=Thread(target=cgs.mws_csv, args=['envios amazon', n_weeks_ago])
        hilo.start()
    return cgs.graph_envios_amazon()

def excedente_inventario(vendedor, access_key, merchant_id, secret_key, n_weeks_ago,  asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    cgs.get_exceso_inventario(n_weeks_ago, asin, search_asin, titulo, search_titulo)
    if len(threading.enumerate())<15 and False:
        hilo=Thread(target=cgs.mws_csv, args=['exceso inventario', n_weeks_ago])
        hilo.start()
    graph= cgs.graph_exceso_inventario()
    graph+=cgs.graph_exceso_inventario2()
    return graph

#print(excedente_inventario('izas', access_key, merchant_id, secret_key, 1))
#print(ventas('nose', access_key, merchant_id, secret_key, 1))
#hilo=Thread(target=hola, args=['envios amazon'], name='mws')
#hilo.start()
#list=[x.getName() for x in threading.enumerate()]
#print(list)
#cgs=crearGraficasSeller('nose', access_key, merchant_id, secret_key)
#cgs.mws_csv('exceso inventario',2)