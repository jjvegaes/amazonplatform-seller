import pandas as pd
from datetime import datetime
import os
import plotly.express as px
import plotly

from users.cambiar_region import cambiar_region
from users.graficos import graficas


class crearGraficasVendor():
    def __init__(self, vendedor):
        self.gr=graficas({})
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)

    def get_tendencias_ventas(self):
        
        meses_dict={'dic':'12', 'nov':'11', 'ene':'01', 'feb':'02', 'mar':'03', 'abr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'ago':'08', 'sep':'09', 'oct':'10'}
        dataframes=[]
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/miquelrius/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES.xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/miquelrius/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (1).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/miquelrius/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (2).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/miquelrius/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (3).xlsx'))
        for i in range(1,4):
            dataframes[0]=dataframes[0].append(dataframes[i], ignore_index = True)
        
        for i in range(len(dataframes[0]['Fecha'])):
            mes=dataframes[0]['Fecha'][i][3:6]
            dataframes[0]['Fecha'][i]=dataframes[0]['Fecha'][i].replace(mes, meses_dict[mes])
            dataframes[0]['Fecha'][i]=datetime.strptime(dataframes[0]['Fecha'][i], '%d-%m-%Y')
        reversed_df = dataframes[0].iloc[::-1]
        self.gr.add_df('tendencias de ventas', reversed_df)

    def gen_tendencias_ventas(self):
        gr1={'id':'temporal', 'x':'Fecha', 'y':'Ingresos por envíos', 'secondary_y':False}
        gr2={'id':'temporal', 'x':'Fecha', 'y':'Precio medio de venta', 'secondary_y':True}
        return self.gr.get_html(self.gr.multiple('tendencias de ventas', [gr1,gr2], 'Tendencias de rendimiento de ventas', True, 'Ingresos por envíos', 'Precio medio de venta'))

    def get_diagnostico_ventas(self):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de ventas/Diagnóstico de ventas_Vista de detalles_ES.xlsx')
        df2 = df.drop(df[df['Ingresos por envíos']==0].index)
        df3 =df2.nlargest(20, 'Ingresos por envíos')
        df4 =df2.nlargest(20, 'Unidades enviadas')
        df5=df.drop(df[df['Buy box perdida (Precio)']==0].index)
        df5=df5.drop(df5[df5['Buy box perdida (Precio)']=='—'].index)
        df5['Buy box perdida (Precio)']=df5['Buy box perdida (Precio)']*100
        df5=df5.sort_values(by='Buy box perdida (Precio)').iloc[::-1]
        self.gr.add_df('diagnostico de ventas top 20 ingresos', df3)
        self.gr.add_df('diagnostico de ventas top 20 unidades', df4)
        self.gr.add_df('diagnostico de ventas', df)
        self.gr.add_df('diagnostico de ventas sin 0', df2)
        self.gr.add_df('diagnostico de ventas buy box', df5)

    def gen_diagnostico_ventas(self):
        gr1={'id':'barras', 'id_df':'diagnostico de ventas sin 0', 'etiquetas':['ASIN'], 'valores':['Ingresos por envíos'], 'colores': False, 'orientacion':'h', 'row':0, 'col':0}
        gr2={'id':'circular','id_df':'diagnostico de ventas sin 0', 'etiquetas':['ASIN'], 'valor':'Unidades enviadas','row':0, 'col':1}
        return self.gr.get_html(self.gr.varios([gr1, gr2], 'Ventas por producto', 2, 1))

    def gen_diagnostico_ventas2(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('diagnostico de ventas sin 0',etiquetas=['ASIN'], valores=['Ingresos por envíos'], titulo='Ingresos por ASIN', colores=True, orientacion='v'), h=700))

    def gen_diagnostico_ventas3(self):
        gr1={'id':'circular', 'id_df':'diagnostico de ventas top 20 ingresos', 'etiquetas':['ASIN'], 'valor':'Ingresos por envíos', 'titulo':'Ingresos', 'row':0, 'col':0}
        gr2={'id':'circular','id_df':'diagnostico de ventas top 20 unidades', 'etiquetas':['ASIN'], 'valor':'Unidades enviadas', 'titulo':'Unidades','row':0, 'col':1}
        return self.gr.get_html(self.gr.tam(self.gr.varios([gr1, gr2], 'Top 20 ingresos', 2, 1),h=600, color='lightblue'))
    
    def gen_diagnostico_ventas4(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('diagnostico de ventas buy box',etiquetas=['ASIN'], valores=['Buy box perdida (Precio)'], titulo='Buy box perdida (%)', colores=False, orientacion='v'), h=600, ))

    def get_diagnostico_trafico(self):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de trafico/Diagnóstico de tráfico_Detalles_ES.xlsx')
        df2=df.drop(df[df['% de visitas totales']=='—'].index)
        #df3==df.drop(df[df['Visitas de Envío 1 día']=='—'].index)
        #df3=df3.replace({"—": 0}
        self.gr.add_df('diagnostico de trafico', df2)
        #self.gr.add_df('visitas de Envío 1 día',)

    def gen_diagnostico_trafico(self):
        return self.gr.get_html(self.gr.tam(self.gr.circular('diagnostico de trafico', etiquetas=['Subcategoría', 'ASIN'], valor='% de visitas totales', titulo='Visitas a cada producto'), h=800))

    def get_resenas(self):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/resenas/Reseñas de clientes_ES.xlsx')
        df1=df.sort_values(by='Valoración media del cliente').iloc[::-1]
        df2=df.sort_values(by='Número de reseñas de clientes').iloc[::-1]
        self.gr.add_df('resenas', df1)
        self.gr.add_df('resenas numero', df2)

    def gen_resenas(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('resenas',etiquetas=['ASIN'], valores=['Valoración media del cliente'], titulo='valoracion media', colores=True, orientacion='v'), h=700))
    def gen_resenas2(self):
        gr1={'id':'indicador', 'id_df':'resenas', 'etiqueta':'Valoración media del cliente', 'mean':True, 'formato':{'suffix': " estrellas"}, 'titulo': 'Valoración media', 'row':0, 'col':0}
        gr2={'id':'indicador', 'id_df':'resenas', 'etiqueta':'5 estrellas', 'mean':False, 'formato':{'suffix': " estrellas"}, 'titulo': '5 estrellas', 'row':0, 'col':1}
        gr3={'id':'indicador', 'id_df':'resenas', 'etiqueta':'4 estrellas', 'mean':False, 'formato':{'suffix': " estrellas"}, 'titulo': '4 estrellas', 'row':0, 'col':2}
        gr4={'id':'indicador', 'id_df':'resenas', 'etiqueta':'3 estrellas', 'mean':False, 'formato':{'suffix': " estrellas"}, 'titulo': '3 estrellas', 'row':1, 'col':0}
        gr5={'id':'indicador', 'id_df':'resenas', 'etiqueta':'2 estrellas', 'mean':False, 'formato':{'suffix': " estrellas"}, 'titulo': '2 estrellas', 'row':1, 'col':1}
        gr6={'id':'indicador', 'id_df':'resenas', 'etiqueta':'1 estrella', 'mean':False, 'formato':{'suffix': " estrellas"}, 'titulo': '1 estrella', 'row':1, 'col':2}
        return self.gr.get_html(self.gr.tam(self.gr.varios([gr1, gr2, gr3, gr4, gr5, gr6], 'Resumen de la valoración', 3, 2), h=500, color='lightblue'))
        #gr1={'id':'circular', 'id_df':'diagnostico de trafico', 'etiquetas':['Subcategoría', 'ASIN'], 'valor':'% de visitas totales', 'titulo':'visitas', 'row':0, 'col':0}
        #gr2={'id':'barras', 'id_df':'diagnostico de trafico 1 día', 'etiquetas':['ASIN'], 'valores':['Visitas de Envío 1 día', 'Visitas de Envío 1 día - Periodo anterior'], 'colores':False,  'titulo':'visitas', 'orientacion':'v', 'row':0, 'col':1}
        #return self.gr.get_html(self.gr.varios([gr1, gr2], 'Diagnostico de tráfico', 2, 1))
    
    def gen_resenas3(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('resenas numero',etiquetas=['ASIN'], valores=['Número de reseñas de clientes'], titulo='Número de reseñas por ASIN', colores=True, orientacion='v'), h=700))

    def get_estado_inventario(self):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/estado inventario/Estado del inventario_ES.xlsx')
        df2 = df.drop(df[df['Unidades disponibles no aptas para venta']==0].index)
        df2=df2.sort_values(by='Unidades disponibles no aptas para venta').iloc[::-1]
        self.gr.add_df('estado inventario', df)
        self.gr.add_df('estado inventario no aptas', df2)

    def gen_estado_inventario(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('estado inventario',etiquetas=['ASIN'], valores=['Unidades disponibles aptas para venta'], titulo='Unidades disponibles aptas para venta', colores=True, orientacion='v'), h=700, color='lightblue'))


    def gen_estado_inventario2(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('estado inventario no aptas',etiquetas=['ASIN'], valores=['Unidades disponibles no aptas para venta'], titulo='Unidades disponibles no aptas para venta', colores=True, orientacion='v'), h=700))

    def get_informacion_geografica(self):
        o=cambiar_region(self.myRute+'/informes_vendor/'+self.vendedor+'/informacion geografica/Información geográfica sobre ventas_Detalles_ES.xlsx')
        df=o.accion()
        df["Ingresos por envíos"] = df["Ingresos por envíos"].apply(pd.to_numeric)
        self.gr.add_df('informacion geografica', df)

    def gen_informacion_geografica(self):
        
        fig = px.density_mapbox(self.gr.dict_df['informacion geografica'], lat='Latitud', lon='Longitud', z='Ingresos por envíos', radius=20,
                        center=dict(lat=40.4167, lon=-3.70325), zoom=5,
                        mapbox_style="stamen-terrain")
                        
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
'''
def gen_graficos():
    v=crearGraficasVendor('miquelrius')
    v.get_tendencias_ventas()
    graph=v.gen_tendencias_ventas()
    v.get_diagnostico_ventas()

    graph=graph+v.gen_diagnostico_ventas2()
    graph=graph+v.gen_diagnostico_ventas3()
    graph=graph+v.gen_diagnostico_ventas4()
    v.get_diagnostico_trafico()
    graph=graph+v.gen_diagnostico_trafico()
    v.get_resenas()
    graph=graph+v.gen_resenas()
    graph=graph+v.gen_resenas2()
    graph=graph+v.gen_resenas3()
    return graph
'''
def productos():
    v=crearGraficasVendor('miquelrius')
    v.get_diagnostico_ventas()
    graph=v.gen_diagnostico_ventas2()
    graph=graph+v.gen_diagnostico_ventas3()
    graph=graph+v.gen_diagnostico_ventas4()
    v.get_diagnostico_trafico()
    graph=graph+v.gen_diagnostico_trafico()
    v.get_estado_inventario()
    graph=graph+v.gen_estado_inventario()
    graph=graph+v.gen_estado_inventario2()
    return graph

def ventas():
    
    v=crearGraficasVendor('miquelrius')
    v.get_tendencias_ventas()
    graph=v.gen_tendencias_ventas()
    v.get_informacion_geografica()
    graph=graph+v.gen_informacion_geografica()
    return graph

def customers2():
    v=crearGraficasVendor('miquelrius')
    v.get_resenas()
    graph=v.gen_resenas()
    graph=graph+v.gen_resenas2()
    graph=graph+v.gen_resenas3()
    return graph

