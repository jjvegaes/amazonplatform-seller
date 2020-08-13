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

mutex=threading.Lock()

class crearGraficasSeller():
    def __init__(self, vendedor, access_key, merchant_id, secret_key):
        self.gr=graficas({})
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)
        self.access_key=access_key
        self.merchant_id=merchant_id
        self.secret_key=secret_key
        self.dict_reports={'comentarios negativos':'_GET_SELLER_FEEDBACK_DATA_', 'estado inventario':'_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_','envios amazon':'_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_', 'exceso inventario':'_GET_EXCESS_INVENTORY_DATA_'}

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
        df=l.limpieza2(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], n_weeks_ago)
        if df.__str__() != "None": 
            df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+str(n_weeks_ago)+'.csv')
            print('Cargado el informe '+id)
        mutex.release()

    def mws_csv_historico(self, id, n_weeks_ago):
        mutex.acquire()
        try:
            l=Limpieza()
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.csv')
            df = df.drop(['Unnamed: 0'], axis=1)
            df2=l.limpieza2(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], 1)
            if df2.__str__() != "None": 
                df=df.append(df2, ignore_index = True)
                df = df.drop_duplicates('b"amazon-order-id')
                df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.csv')
                print('Cargado el informe '+id)
                df.to_excel(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.xlsx')
        except:
            print('ha habido exceptcion')
            l=Limpieza()
            df=l.limpieza2(self.access_key, self.merchant_id, self.secret_key, self.dict_reports[id], n_weeks_ago)
            if df.__str__() != "None": 
                df.to_csv(self.myRute+'/informes_seller/'+self.vendedor+'/'+id+'/'+id+'historico'+'.csv')
                print('Cargado el informe '+id)
        mutex.release()


    def get_envios_amazon_historico(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.csv')
        except:
            self.mws_csv_historico('envios amazon', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.csv')
            except:
                return
        variables_ingresos=['item-price', 'shipping-price', 'item-tax', 'shipping-tax', "gift-wrap-price", "item-promotion-discount", "ship-promotion-discount"]
        for v in variables_ingresos:
            for i in range(len(df[v])):
                if df[v][i] != df[v][i]:
                    df[v][i]=0
        df["Ingresos"]=df["item-price"]+df["shipping-price"]+df["item-tax"]+df["shipping-tax"]+df["gift-wrap-price"]+df["item-promotion-discount"]+df["ship-promotion-discount"]
        df1=df.groupby(by="sku", as_index=False).sum()
        df1=df1.sort_values('Ingresos').iloc[::-1]
        df2 =df1.nlargest(20, 'Ingresos')#Obtenemos los 20 ASIN con más ingresos
        df3 =df1.nlargest(20, 'quantity-shipped')#Obtenemos los 20 asin con más unidades enviadas
        df4=df.copy()
        df4['ingresos por día']=''
        for i in range(len(df4['payments-date'])):
            df4['ingresos por día'][i]=df4['payments-date'][i][:10]
        
        df4=df4.groupby(by="ingresos por día", as_index=False).sum()
        df4=df4.sort_values('ingresos por día').iloc[::-1]
        print(list(df4['quantity-shipped']))
        df4['Precio medio de venta']=df4['Ingresos']/df4['quantity-shipped']

        o=cambiar_region(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'historico'+'.csv')
        df5=o.accion()
        variables_ingresos=['item-price', 'shipping-price', 'item-tax', 'shipping-tax', "gift-wrap-price", "item-promotion-discount", "ship-promotion-discount"]
        for v in variables_ingresos:
            for i in range(len(df[v])):
                if df5[v][i] != df5[v][i]:
                    df5[v][i]=0
        df5["Ingresos"]=df5["item-price"]+df5["shipping-price"]+df5["item-tax"]+df5["shipping-tax"]+df5["gift-wrap-price"]+df5["item-promotion-discount"]+df5["ship-promotion-discount"]
        #df["Ingresos por envíos"] = df["Ingresos por envíos"].apply(pd.to_numeric)


        self.gr.add_df('envios gestionados por amazon', self.filtra(df1, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon 20 ingresos', self.filtra(df2, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon 20 cantidad', self.filtra(df3, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon historico', self.filtra(df4, asin, search_asin, titulo, search_titulo))
        self.gr.add_df('envios gestionados por amazon mapa', self.filtra(df5, asin, search_asin, titulo, search_titulo))
        #df.to_excel(self.myRute+'/informes_seller/'+self.vendedor+'/envios_amazon/envios_gestionados_por_amazon.xlsx')
    
    #def get_envios_amazon_historico(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):

    def graph_envios_amazon(self):
        #return self.gr.get_html(self.gr.circular('envios gestionados por amazon', ['sales-channel', 'sku'], 'quantity-shipped', 'prueba'))
        return self.gr.get_html(self.gr.tam(self.gr.barras('envios gestionados por amazon',etiquetas=['sku'], valores=['Ingresos'], titulo='Ingresos por ASIN', colores=True, orientacion='v', hovertext=['sku']), h=700))
    
    def graph_envios_amazon2(self):
        gr1={'id':'circular', 'id_df':'envios gestionados por amazon 20 ingresos', 'etiquetas':['sku'], 'valor':'Ingresos', 'titulo':'Ingresos', 'row':0, 'col':0, 'hovertext':[]}
        gr2={'id':'circular','id_df':'envios gestionados por amazon 20 cantidad', 'etiquetas':['sku'], 'valor':'quantity-shipped', 'titulo':'Unidades','row':0, 'col':1, 'hovertext':[]}
        return self.gr.get_html(self.gr.tam(self.gr.varios([gr1, gr2], 'Top 20 ingresos', 2, 1),h=600, color='lightblue'))

    def graph_envios_amazon3(self):
        gr1={'id':'temporal', 'x':'ingresos por día', 'y':'Ingresos', 'secondary_y':False, 'hovertext':None}
        gr2={'id':'temporal', 'x':'ingresos por día', 'y':'Precio medio de venta', 'secondary_y':True, 'hovertext':None}
        return self.gr.get_html(self.gr.multiple('envios gestionados por amazon historico', [gr1, gr2], 'Tendencias de rendimiento de ventas', True, 'Ingresos por envíos', 'Precio medio de venta'))

    def graph_envios_amazon4(self):
        return self.gr.get_html(self.gr.mapa_calor('envios gestionados por amazon mapa', 'Ingresos', hovertext=[]))

    def get_estado_inventario(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+str(n_weeks_ago)+'.csv')
        except:
            self.mws_csv('estado inventario', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+str(n_weeks_ago)+'.csv')
                self.gr.add_df('estado inventario', self.filtra(df, asin, search_asin, titulo, search_titulo))
            except:
                return
        df=df.sort_values('total-quantity').iloc[::-1]
        self.gr.add_df('estado inventario', self.filtra(df, asin, search_asin, titulo, search_titulo))


    def graph_estado_inventario(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('estado inventario',etiquetas=['asin'], valores=['total-quantity','sellable-quantity'], titulo='Inventario disponible', colores=False, orientacion='v', hovertext=['product-name']), h=700))

    def get_comentarios_negativos(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/comentarios negativos/comentarios negativos'+'historico'+'.csv')
        except:
            self.mws_csv_historico('comentarios negativos', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/comentarios negativos/comentarios negativos'+'historico'+'.csv')
            except:
                return
        


    def get_exceso_inventario(self, n_weeks_ago, asin, search_asin, titulo, search_titulo):
        try:
            df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.csv')
        except:
            self.mws_csv('exceso inventario', n_weeks_ago)
            try:
                df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+str(n_weeks_ago)+'.csv')
                self.gr.add_df('excedente de inventario', self.filtra(df, asin, search_asin, titulo, search_titulo))
            except:
                return


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


def ventas(vendedor, access_key, merchant_id, secret_key, n_weeks_ago=None, asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    cgs.get_envios_amazon_historico(n_weeks_ago=5, asin=asin, search_asin=search_asin, titulo=titulo, search_titulo=search_titulo)
    cgs.get_estado_inventario(n_weeks_ago=n_weeks_ago, asin=asin, search_asin=search_asin, titulo=titulo, search_titulo=search_titulo)
    if len(threading.enumerate())<15:
        hilo=Thread(target=cgs.mws_csv_historico, args=['envios amazon', 5])
        hilo2=Thread(target=cgs.mws_csv, args=['estado inventario', n_weeks_ago])
        hilo.start()
        hilo2.start()
    graph= cgs.graph_envios_amazon()
    graph+=cgs.graph_envios_amazon2()
    graph+=cgs.graph_envios_amazon3()
    graph+=cgs.graph_envios_amazon4()
    graph+=cgs.graph_estado_inventario()
    return graph


def excedente_inventario(vendedor, access_key, merchant_id, secret_key, n_weeks_ago,  asin=None, search_asin=None, titulo=None, search_titulo=None):
    cgs=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
    cgs.get_exceso_inventario(n_weeks_ago, asin, search_asin, titulo, search_titulo)
    if len(threading.enumerate())<15 and False:
        hilo=Thread(target=cgs.mws_csv, args=['exceso inventario', n_weeks_ago])
        hilo.start()
    graph= cgs.graph_exceso_inventario()
    graph+=cgs.graph_exceso_inventario2()
    return graph

print(ventas('izas', access_key, merchant_id, secret_key, 2))
#print(ventas('nose', access_key, merchant_id, secret_key, 1))
#hilo=Thread(target=hola, args=['envios amazon'], name='mws')
#hilo.start()
#list=[x.getName() for x in threading.enumerate()]
#print(list)
#cgs=crearGraficasSeller('nose', access_key, merchant_id, secret_key)
#cgs.mws_csv('exceso inventario',2)