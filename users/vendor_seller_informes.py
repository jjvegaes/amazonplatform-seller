from informes_plantlla.informes_plantilla import informe_semanal
from informes_plantlla.graficas_informe import graficas_informe
from seller import crearGraficasSeller
import os
import pandas as pd
from datetime import datetime

#Clase para crear los informes de seller
class informe_seller():
    #Constructor con las claves necesarias:
    def __init__(self, vendedor, access_key, merchant_id, secret_key):
        self.seller_graficas=crearGraficasSeller(vendedor, access_key, merchant_id, secret_key)
        self.gi=graficas_informe(os.path.dirname(__file__)+'/informes_plantlla/imagenes')
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)#Ruta de este archivo
        self.dict_df={}
        self.dict_reports={'datos inventario':'_GET_AFN_INVENTORY_DATA_', 'comentarios negativos':'_GET_SELLER_FEEDBACK_DATA_', 'estado inventario':'_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_','envios amazon':'_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_', 'exceso inventario':'_GET_EXCESS_INVENTORY_DATA_'}

    #Obtenemos el informe envios de amazon semanal y creamos los dataframes concretos:
    def get_envios_amazon_semanal(self):
        self.seller_graficas.mws_csv('envios amazon', 1)
        df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'1'+'.csv')#Leemos el dataframe
        df["Ingresos"]=df["item-price"]+df["shipping-price"]+df["item-tax"]+df["shipping-tax"]+df["gift-wrap-price"]+df["item-promotion-discount"]+df["ship-promotion-discount"]#Añadimos al dataframe la columna ingresos
        #Calculamos las dos variables de ingresos totales y ventas totales:
        ingresos_totales=sum(list(df['Ingresos']))
        ventas_totales=sum(list(df['quantity-shipped']))
        #Obtenemos el top 20 de productos con más ingresos
        df1=df.groupby(by="product-name", as_index=False).sum()
        df1=df1.sort_values('Ingresos').iloc[::-1]
        df2 =df1.nlargest(1, 'Ingresos')#Obtenemos los 20 ASIN con más ingresos
        dfmasingresos =df1.nlargest(20, 'Ingresos')#Obtenemos los 20 ASIN con más ingresos
        producto_mas_ingresos=list(df2['product-name'])[0]#Producto con más ingresos
        #Obtenemos el top 20 de los productos con más ventas:
        df1=df1.sort_values('quantity-shipped').iloc[::-1]
        df3 =df1.nlargest(1, 'quantity-shipped')
        dfmasventas =df1.nlargest(20, 'quantity-shipped')
        producto_mas_vendido=list(df3['product-name'])[0]
        #Guardamos los dataframes:
        self.gi.add_df('envios amazon', df)
        self.gi.add_df('envios amazon top ingresos', dfmasingresos)
        self.gi.add_df('envios amazon top vendidos', dfmasventas)

        #CALCULAMOS TICKET MEDIO:
        df['Num-compras']=1
        df_mismaCompra=df.groupby(by='shipment-id').sum().reset_index()
        ticket_medio_compra=ingresos_totales/df_mismaCompra.shape[0]#Fórmula del ticket medio
        #Ticket medio por asin:
        df_asin = df.groupby(by='product-name').sum().reset_index()
        df_asin['ticket_medio']=df_asin['Ingresos']/df_asin['Num-compras']#Fómula del ticket medio
        df_asin_mayores=df_asin.sort_values('ticket_medio').iloc[::-1].nlargest(20, 'ticket_medio')#Productos con mayor ticket medio
        df_asin_menores=df_asin.sort_values('ticket_medio').nsmallest(20, 'ticket_medio').iloc[::-1]#Productos con menor ticket medio
        self.gi.add_df('Ticket medio por asin mayores', df_asin_mayores)
        self.gi.add_df('Ticket medio por asin menores', df_asin_menores)
        #Ticket medio por ciudad:
        df_ciudad=df.copy()
        df_mismaCompra['Num-compras']=1
        df_ciudad['ciudad']=[x.lower() for x in list(df_ciudad['ship-city'])]#Lo ponemos en minúsculas
        df_ciudad = df_ciudad.groupby(by='ciudad').sum().reset_index()
        df_ciudad['ticket_medio']=df_ciudad['Ingresos']/df_ciudad['Num-compras']#Fórmula del ticket medio
        df_ciudad_mayores=df_ciudad.sort_values('ticket_medio').iloc[::-1].nlargest(20, 'ticket_medio')#Productos con mayor ticket medio
        df_ciudad_menores=df_ciudad.sort_values('ticket_medio').nsmallest(20, 'ticket_medio').iloc[::-1]#Productos con menor ticket medio
        self.gi.add_df('Ticket medio por ciudad mayores', df_ciudad_mayores)
        self.gi.add_df('Ticket medio por ciudad menores', df_ciudad_menores)

        
        
        return ingresos_totales, ventas_totales, producto_mas_ingresos, producto_mas_vendido, ticket_medio_compra

    def graph_envios_amazon_semanal(self):
        #Generamos los gráficos necesarios:
        self.gi.barra('envios amazon top ingresos', ['Ingresos'], ['product-name'])
        self.gi.barra('envios amazon top vendidos', ['quantity-shipped'], ['product-name'])
        self.gi.quesito('envios amazon top ingresos', 'Ingresos', 'product-name')
        self.gi.quesito('envios amazon top vendidos', 'quantity-shipped', 'product-name')
        self.gi.linea('Ticket medio por asin mayores', 'product-name', 'ticket_medio')
        self.gi.linea('Ticket medio por asin menores', 'product-name', 'ticket_medio')
        self.gi.linea('Ticket medio por ciudad mayores', 'ciudad', 'ticket_medio')
        self.gi.linea('Ticket medio por ciudad menores', 'ciudad', 'ticket_medio')

    def get_envios_amazon_mensual(self):
        #primero obtenemos los días del mes anterior
        meses={1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9: 30, 10:31, 11:30, 12:31}#Número de días cada mes
        hoy=datetime.now()
        mes_hoy=hoy.month
        dia_hoy=hoy.day
        año_hoy=hoy.year
        if dia_hoy==meses[mes_hoy]:#Si estamos en el último día del mes pedimos el dataframe de este mes
            self.seller_graficas.mws_csv('envios amazon', 1, datetime(year=año_hoy, month=mes_hoy, day=1), hoy)
        else:#Si no pues pedimos el dataframe del mes pasado
            if mes_hoy==1:
                self.seller_graficas.mws_csv('envios amazon', 1, datetime(year=año_hoy-1, month=12, day=1), datetime(year=año_hoy-1, month=12, day=31))
            else:
                self.seller_graficas.mws_csv('envios amazon', 1, datetime(year=año_hoy, month=mes_hoy-1, day=1), datetime(year=año_hoy, month=mes_hoy-1, day=31))
        #Seguimos el mismo procedimiento que el informe semanal:
        df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/envios amazon/envios amazon'+'aux'+'.csv')
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
        self.gi.add_df('envios amazon mensual', df)
        self.gi.add_df('envios amazon top ingresos mensual', dfmasingresos)
        self.gi.add_df('envios amazon top vendidos mensual', dfmasventas)
        return ingresos_totales, ventas_totales, producto_mas_ingresos, producto_mas_vendido

    #Dibujamos los gráficos
    def graph_envios_amazon_mensual(self):
        self.gi.barra('envios amazon top ingresos mensual', ['Ingresos'], ['product-name'])
        self.gi.barra('envios amazon top vendidos mensual', ['quantity-shipped'], ['product-name'])
        self.gi.quesito('envios amazon top ingresos mensual', 'Ingresos', 'product-name')
        self.gi.quesito('envios amazon top vendidos mensual', 'quantity-shipped', 'product-name')

    #Obtenemos el dataframe de reabastecer inventario y exceso de inventario
    def get_exceso_reabastecer_inventario(self):
        #Obtenemos exceso y reabastecer inventario:
        self.seller_graficas.mws_csv('exceso inventario', 1)
        self.seller_graficas.mws_csv('reabastecer inventario', 1)
        df_exceso=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/exceso inventario/exceso inventario'+'1'+'.csv')
        df_reabastecer=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/reabastecer inventario/reabastecer inventario'+'1'+'.csv')
        #Obtenemos los valores de items out of stock, low stock y unidades excesas:
        items_out_of_stock = df_reabastecer.drop(df_reabastecer[df_reabastecer['Alert']!='out_of_stock'].index).shape[0]
        items_low_stock = df_reabastecer.drop(df_reabastecer[df_reabastecer['Alert']!='low_stock'].index).shape[0]
        unidades_excesas=sum(list(df_exceso['Estimated Excess']))
        #Obtenemos el top 20 de ambos datafames:
        df_exceso=df_exceso.sort_values('Estimated Excess').iloc[::-1]
        df_exceso=df_exceso.nlargest(20, 'Estimated Excess')
        df_reabastecer=df_reabastecer.drop(df_reabastecer[df_reabastecer['Recommended replenishment qty']=='out_of_stock'].index)
        df_reabastecer=df_reabastecer.drop(df_reabastecer[df_reabastecer['Recommended replenishment qty']=='low_stock'].index)
        df_reabastecer['Recommended replenishment qty'] = df_reabastecer['Recommended replenishment qty'].apply(pd.to_numeric)
        df_reabastecer=df_reabastecer.sort_values('Recommended replenishment qty').iloc[::-1]
        df_reabastecer=df_reabastecer.nlargest(20, 'Recommended replenishment qty')
        #Guardamos los dataframes:
        self.gi.add_df('exceso inventario', df_exceso)
        self.gi.add_df('reabastecer inventario', df_reabastecer)
        return items_out_of_stock, items_low_stock, unidades_excesas

    #Dibujamos los gráficos
    def graph_exceso_reabastecer_inventario(self):
        self.gi.barra('exceso inventario', ['Estimated Excess', 'Total Quantity (Sellable)'], ['Product Name'])
        self.gi.barra('reabastecer inventario', ['Recommended replenishment qty', 'Total Units'], ['Product Name'])

    #Obtenemos la información de todos los pedidos y los dataframes:
    def get_informacion_pedidos(self):
        #Obtenemos el dataframe:
        self.seller_graficas.mws_csv('informacion pedidos', 1)
        df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/informacion pedidos/informacion pedidos'+'1'+'.csv', encoding='utf-8-sig')
        #Obtenemos la cantidad de pedidos totales, pendientes, enviados, enviando y cancelados:
        df['n_pedidos']=1
        n_totales=df.shape[0]
        n_pendientes=df.drop(df[df['order-status']!='Pending'].index).shape[0]
        n_enviados=df.drop(df[df['order-status']!='Shipped'].index).shape[0]
        n_enviando=df.drop(df[df['order-status']!='Shipping'].index).shape[0]
        n_cancelados=df.drop(df[df['order-status']!='Cancelled'].index).shape[0]
        df = df.groupby(by="order-status").sum().reset_index()
        self.gi.add_df('informacion pedidos', df)

        return n_totales, n_pendientes, n_enviando, n_enviados, n_cancelados

    #Dibujamos la información de pedidos
    def graph_informacion_pedidos(self):
        self.gi.quesito('informacion pedidos', 'n_pedidos', 'order-status')

    def get_estado_inventario(self):
        self.seller_graficas.mws_csv('estado inventario', 1)
        df=pd.read_csv(self.myRute+'/informes_seller/'+self.vendedor+'/estado inventario/estado inventario'+'1'+'.csv', encoding='utf-8-sig')
        total_quantity=sum(list(df['total-quantity']))
        sellable_quantity=sum(list(df['sellable-quantity']))
        df1=df.sort_values('total-quantity').iloc[::-1]
        df1 =df1.nlargest(20, 'total-quantity')
        self.gi.add_df('estado inventario', df1)
        return total_quantity, sellable_quantity

    def graph_estado_inventario(self):
        self.gi.barra('estado inventario', ['total-quantity', 'sellable-quantity'], ['product-name'])





#Función que crea el informe
def gen_informe_seller(vendedor, access_key, merchant_id, secret_key):
    i_seller=informe_seller(vendedor, access_key, merchant_id, secret_key)
    #Obtenemos todos los dataframes y datos concretos:
    ingresos_totales, ventas_totales, producto_mas_ingresos, producto_mas_vendido, ticket_medio_compra=i_seller.get_envios_amazon_semanal()
    ingresos_totales_mensual, ventas_totales_mensual, producto_mas_ingresos_mensual, producto_mas_vendido_mensual=i_seller.get_envios_amazon_mensual()
    items_out_of_stock, items_low_stock, unidades_excesas=i_seller.get_exceso_reabastecer_inventario()
    n_totales, n_pendientes, n_enviando, n_enviados, n_cancelados=i_seller.get_informacion_pedidos()
    total_quantity, sellable_quantity =i_seller.get_estado_inventario()
    #Creamos todas las gráficas
    i_seller.graph_envios_amazon_semanal()
    i_seller.graph_envios_amazon_mensual()
    i_seller.graph_exceso_reabastecer_inventario()
    i_seller.graph_informacion_pedidos()
    i_seller.graph_estado_inventario()
    #Creamos el informe pasando todos los datos como parámetro
    informe_sem=informe_semanal(vendedor)
    informe_sem.portada()
    informe_sem.pag1(ingresos_totales, ventas_totales, 'Esto es un texto para editar', ['envios amazon top ingresos_barras.png', 'envios amazon top vendidos_barras.png'])
    informe_sem.pag2(ingresos_totales_mensual, ventas_totales_mensual, 'Esto es un texto para editar', ['envios amazon top ingresos mensual_barras.png', 'envios amazon top vendidos mensual_barras.png'])
    informe_sem.pag2_2(ticket_medio_compra, 'Esto es un texto para editar', ['Ticket medio por asin mayores_linea.png', 'Ticket medio por asin menores_linea.png', 'Ticket medio por ciudad mayores_linea.png', 'Ticket medio por ciudad menores_linea.png'])
    #informe_sem.pag3(405, 110.25, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png']) Esto en seller no va
    informe_sem.pag3_2(total_quantity, sellable_quantity, 'Esto es un texto para editar', ['estado inventario_barras.png'])
    informe_sem.pag4('Esto es un texto para editar',['exceso inventario_barras.png', 'reabastecer inventario_barras.png'], exceso_inventario=unidades_excesas, numero_low_stock=items_low_stock, numero_out_of_stock=items_out_of_stock)
    informe_sem.pag5(98, 95.2, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag6(producto_mas_ingresos, producto_mas_vendido, 'Esto es un texto para editar', ['envios amazon top ingresos_quesitos.png', 'envios amazon top vendidos_quesitos.png'])
    informe_sem.pag6_2(producto_mas_ingresos_mensual, producto_mas_vendido_mensual, 'Esto es un texto para editar', ['envios amazon top ingresos mensual_quesitos.png', 'envios amazon top vendidos mensual_quesitos.png'])
    informe_sem.pag7(['Campaña 1', 'Campaña 2', 'Campaña 3', 'Campaña 4'], 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag8(1000, 950, 100, 99, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag9(1800, 1000, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag10(54645, 9504, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag11(126, 15, 'Esto es un texto para editar', ['ingresos.png', 'ventas.png'])
    informe_sem.pag12(n_totales, n_pendientes, n_enviando, n_enviados, n_cancelados, 'Esto es un texto para editar', ['informacion pedidos_quesitos.png'])
    informe_sem.finaliza_doc()

access_key='AKIAIRF2R7EOJFNTGBEA'
merchant_id='A2GU67S0S60AC1'
secret_key='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'

gen_informe_seller('izas', access_key, merchant_id, secret_key)
    

    