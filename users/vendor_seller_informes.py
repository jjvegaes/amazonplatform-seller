from informes_plantlla.informes_plantilla import informe_semanal
from informes_plantlla.graficas_informe import graficas_informe
from seller import crearGraficasSeller
import os
import pandas as pd

class informe_seller():
    def __init__(self, vendedor, access_key, merchant_id, secret_key):
        self.seller_graficas=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
        self.gi=graficas_informe(os.path.dirname(__file__)+'/informes_plantlla/imagenes')
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)#Ruta de este archivo
        #Credenciales de la cuenta:
        #IDs de los informes a usar:
        self.dict_df={}
        self.dict_reports={'datos inventario':'_GET_AFN_INVENTORY_DATA_', 'comentarios negativos':'_GET_SELLER_FEEDBACK_DATA_', 'estado inventario':'_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_','envios amazon':'_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_', 'exceso inventario':'_GET_EXCESS_INVENTORY_DATA_'}

    def get_envios_amazon(self):
        #self.seller_graficas.mws_csv('envios amazon', 1)
        df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'1'+'.csv')
        df["Ingresos"]=df["item-price"]+df["shipping-price"]+df["item-tax"]+df["shipping-tax"]+df["gift-wrap-price"]+df["item-promotion-discount"]+df["ship-promotion-discount"]
        ingresos_totales=sum(list(df['Ingresos']))
        ventas_totales=sum(list(df['quantity-shipped']))
        df1=df.groupby(by="product-name", as_index=False).sum()
        df1=df1.sort_values('Ingresos').iloc[::-1]
        df2 =df1.nlargest(1, 'Ingresos')#Obtenemos los 20 ASIN con más ingresos
        dfmasingresos =df1.nlargest(20, 'Ingresos')#Obtenemos los 20 ASIN con más ingresos
        producto_mas_ingresos=list(df2['product-name'])[0]
        df1=df1.sort_values('quantity-shipped').iloc[::-1]
        df3 =df1.nlargest(1, 'quantity-shipped')
        dfmasventas =df1.nlargest(20, 'quantity-shipped')
        producto_mas_vendido=list(df3['product-name'])[0]
        self.gi.add_df('envios amazon', df)
        self.gi.add_df('envios amazon top ingresos', dfmasingresos)
        self.gi.add_df('envios amazon top vendidos', dfmasventas)
        return ingresos_totales, ventas_totales, producto_mas_ingresos, producto_mas_vendido

    def graph_envios_amazon(self):
        self.gi.barra('envios amazon top ingresos', ['Ingresos'], ['product-name'])
        self.gi.barra('envios amazon top vendidos', ['quantity-shipped'], ['product-name'])
        self.gi.quesito('envios amazon top ingresos', 'Ingresos', 'product-name')
        self.gi.quesito('envios amazon top vendidos', 'quantity-shipped', 'product-name')


def gen_informe_seller(vendedor, access_key, merchant_id, secret_key):
    i_seller=informe_seller(vendedor, access_key, merchant_id, secret_key)
    ingresos_totales, ventas_totales, producto_mas_ingresos, producto_mas_vendido=i_seller.get_envios_amazon()
    i_seller.graph_envios_amazon()
    informe_sem=informe_semanal(vendedor)
    informe_sem.portada()
    informe_sem.pag1(ingresos_totales, ventas_totales, 'Esto es un texto para editar', ['envios amazon top ingresos_barras.png', 'envios amazon top vendidos_barras.png'])
    informe_sem.pag2(16284.87, 100, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag3(405, 110.25, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag4('Esto es un texto para editar',['ingresos.png', 'ventas.png'], exceso_inventario=10, reabastecer=20)
    informe_sem.pag5(98, 95.2, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag6(producto_mas_ingresos, producto_mas_vendido, 'Esto es un texto para editar', ['envios amazon top ingresos_quesitos.png', 'envios amazon top vendidos_quesitos.png'])
    informe_sem.pag7(['Campaña 1', 'Campaña 2', 'Campaña 3', 'Campaña 4'], 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag8(1000, 950, 100, 99, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag9(1800, 1000, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag10(54645, 9504, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag11(126, 15, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag12(1000, 950, 50, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.finaliza_doc()

access_key='AKIAIRF2R7EOJFNTGBEA'
merchant_id='A2GU67S0S60AC1'
secret_key='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'

gen_informe_seller('izas', access_key, merchant_id, secret_key)
    

    