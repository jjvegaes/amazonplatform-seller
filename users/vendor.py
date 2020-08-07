import pandas as pd
from datetime import datetime
import os
import plotly.express as px
import plotly

from users.graficos import graficas
from users.cambiar_region import cambiar_region

#Esta clase obtendrá los dataframes y el html de todas las gráficas, dentro hay dos tipos de funciones, las que empiezan por 'get' se encargan de obtener los dataframes y guardarlos en la clase Graficas, las que empiezan por 'gen' se encargan de obtener el html de los gráficos usando funciones de la clase Graficas
class crearGraficasVendor():

    def __init__(self, vendedor):
        self.gr=graficas({})
        self.vendedor=vendedor
        self.myRute=os.path.dirname(__file__)

    def filtra_x_asin(self, df, asin):
        if asin!=None:
            return df[df.ASIN.isin(asin)]
        else:
            return df
    #TENDENCIAS DE VENTAS:
    #obtenemos el dataframe de tendencias de ventas:
    def get_tendencias_ventas(self):
        meses_dict={'dic':'12', 'nov':'11', 'ene':'01', 'feb':'02', 'mar':'03', 'abr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'ago':'08', 'sep':'09', 'oct':'10'}
        dataframes=[]
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES.xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (1).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (2).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (3).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (4).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (5).xlsx'))
        dataframes.append(pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/tendencias de rendimiento/Tendencias de rendimiento de ventas_ES (6).xlsx'))
        #Unimos los 4:
        for i in range(1,7):
            dataframes[0]=dataframes[0].append(dataframes[i], ignore_index = True)
        #Formateamos la fecha para ponerla como un datetime:
        for i in range(len(dataframes[0]['Fecha'])):
            mes=dataframes[0]['Fecha'][i][3:6]
            dataframes[0]['Fecha'][i]=dataframes[0]['Fecha'][i].replace(mes, meses_dict[mes])
            dataframes[0]['Fecha'][i]=datetime.strptime(dataframes[0]['Fecha'][i], '%d-%m-%Y')
        #Ordenamos por fecha:
        reversed_df = dataframes[0].iloc[::-1]
        self.gr.add_df('tendencias de ventas', reversed_df)

    #Generamos el primer diagrama de tendencias de ventas usando la clase graficos
    def gen_tendencias_ventas(self):
        gr1={'id':'temporal', 'x':'Fecha', 'y':'Ingresos por envíos', 'secondary_y':False, 'hovertext':None}
        gr2={'id':'temporal', 'x':'Fecha', 'y':'Precio medio de venta', 'secondary_y':True, 'hovertext':None}
        return self.gr.get_html(self.gr.multiple('tendencias de ventas', [gr1,gr2], 'Tendencias de rendimiento de ventas', True, 'Ingresos por envíos', 'Precio medio de venta'))

    #DIAGNOSTICO DE VENTAS:
    #Obtenemos el dataframe diagnostico de ventas:
    def get_diagnostico_ventas(self, asin):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de ventas/Diagnóstico de ventas_Vista de detalles_ES.xlsx')
        df5=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de ventas/Diagnóstico de ventas_Vista de detalles_ESbuybox.xlsx')
        #Obtenemos distintas versiones del dataframe para generar mejores gráficos
        df2 = df.drop(df[df['Ingresos por envíos']==0].index)#Se eliminan los ASIN sin ingresos
        df3 =df2.nlargest(20, 'Ingresos por envíos')#Obtenemos los 20 ASIN con más ingresos
        df4 =df2.nlargest(20, 'Unidades enviadas')#Obtenemos los 20 asin con más unidades enviadas
        df5=df5.drop(df5[df5['Buy box perdida (Precio)']=='—'].index)#Eliminamos guiones
        df5=df5.drop(df5[df5['Buy box perdida (Precio)']==0].index)#Eliminamos ASIN con buy box perdida 0
        
        df5['Buy box perdida (Precio)']=df5['Buy box perdida (Precio)']*100
        df5=df5.sort_values(by='Buy box perdida (Precio)').iloc[::-1]#Lo ordenamos decreciente
        

        self.gr.add_df('diagnostico de ventas top 20 ingresos', self.filtra_x_asin(df3, asin))
        self.gr.add_df('diagnostico de ventas top 20 unidades', self.filtra_x_asin(df4, asin))
        self.gr.add_df('diagnostico de ventas', self.filtra_x_asin(df, asin))
        self.gr.add_df('diagnostico de ventas sin 0', self.filtra_x_asin(df2, asin))
        self.gr.add_df('diagnostico de ventas buy box', self.filtra_x_asin(df5, asin))

    #Dibujamos las gráficas de diagnostico de ventas:
    def gen_diagnostico_ventas(self):
        gr1={'id':'barras', 'id_df':'diagnostico de ventas sin 0', 'etiquetas':['ASIN'], 'valores':['Ingresos por envíos'], 'colores': False, 'orientacion':'h', 'row':0, 'col':0, 'hovertext':['Título del producto']}
        gr2={'id':'circular','id_df':'diagnostico de ventas sin 0', 'etiquetas':['ASIN'], 'valor':'Unidades enviadas','row':0, 'col':1, 'hovertext':['Título del producto']}
        return self.gr.get_html(self.gr.varios([gr1, gr2], 'Ventas por producto', 2, 1))

    def gen_diagnostico_ventas2(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('diagnostico de ventas sin 0',etiquetas=['ASIN'], valores=['Ingresos por envíos'], titulo='Ingresos por ASIN', colores=True, orientacion='v', hovertext=['Título del producto']), h=700))

    def gen_diagnostico_ventas3(self):
        gr1={'id':'circular', 'id_df':'diagnostico de ventas top 20 ingresos', 'etiquetas':['ASIN'], 'valor':'Ingresos por envíos', 'titulo':'Ingresos', 'row':0, 'col':0, 'hovertext':['Título del producto']}
        gr2={'id':'circular','id_df':'diagnostico de ventas top 20 unidades', 'etiquetas':['ASIN'], 'valor':'Unidades enviadas', 'titulo':'Unidades','row':0, 'col':1, 'hovertext':['Título del producto']}
        return self.gr.get_html(self.gr.tam(self.gr.varios([gr1, gr2], 'Top 20 ingresos', 2, 1),h=600, color='lightblue'))
    
    def gen_diagnostico_ventas4(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('diagnostico de ventas buy box',etiquetas=['ASIN'], valores=['Buy box perdida (Precio)'], titulo='Buy box perdida (%)', colores=False, orientacion='v', hovertext=['Título del producto']), h=600, ))

    #DIAGNOSTICO DE TRÁFICO:
    #Obtenemos el dataframe
    def get_diagnostico_trafico(self, asin):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de trafico/Diagnóstico de tráfico_Detalles_ES.xlsx')
        df2=df.drop(df[df['% de visitas totales']=='—'].index)#Eliminamos ASIN sin visitas
        #df3==df.drop(df[df['Visitas de Envío 1 día']=='—'].index)
        #df3=df3.replace({"—": 0}
        self.gr.add_df('diagnostico de trafico', self.filtra_x_asin(df2, asin))
        #self.gr.add_df('visitas de Envío 1 día',)
    #Generamos el gráfico
    def gen_diagnostico_trafico(self):
        #return self.gr.get_html(self.gr.tam(self.gr.circular('diagnostico de trafico', etiquetas=['Subcategoría', 'ASIN'], valor='% de visitas totales', titulo='Visitas a cada producto'), h=800))
        return self.gr.get_html(self.gr.tam(self.gr.circular('diagnostico de trafico', etiquetas=[ 'Subcategoría', 'ASIN'], valor='% de visitas totales', titulo='Visitas a cada producto', hovertext=['Título del producto']), h=800))
        
    #RESEÑAS DE CLIENTES:
    #Obtenemos el dataframe:
    def get_resenas(self):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/resenas/Reseñas de clientes_ES.xlsx')
        df1=df.sort_values(by='Valoración media del cliente').iloc[::-1]#Ordenado por valoración media
        df2=df.sort_values(by='Número de reseñas de clientes').iloc[::-1]#Ordenado por número de reseñas
        self.gr.add_df('resenas', df1)
        self.gr.add_df('resenas numero', df2)

    #Dibujamos las gráficas:
    def gen_resenas(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('resenas',etiquetas=['ASIN'], valores=['Valoración media del cliente'], titulo='valoracion media', colores=True, orientacion='v', hovertext=['Título del producto']), h=700))
    
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
        return self.gr.get_html(self.gr.tam(self.gr.barras('resenas numero',etiquetas=['ASIN'], valores=['Número de reseñas de clientes'], titulo='Número de reseñas por ASIN', colores=True, orientacion='v', hovertext=['Título del producto']), h=700))

    #ESTADO DEL INVENTARIO
    #Obtenemos el dataframe
    def get_estado_inventario(self, asin):
        df=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/estado inventario/Estado del inventario_ES.xlsx')
        df2 = df.drop(df[df['Unidades disponibles no aptas para venta']==0].index)
        df2=df2.sort_values(by='Unidades disponibles no aptas para venta').iloc[::-1]
        self.gr.add_df('estado inventario', self.filtra_x_asin(df, asin))
        self.gr.add_df('estado inventario no aptas', self.filtra_x_asin(df2, asin))

    #Dibujamos:
    def gen_estado_inventario(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('estado inventario',etiquetas=['ASIN'], valores=['Unidades disponibles aptas para venta'], titulo='Unidades disponibles aptas para venta', colores=True, orientacion='v', hovertext=['Título del producto']), h=700, color='lightblue'))


    def gen_estado_inventario2(self):
        return self.gr.get_html(self.gr.tam(self.gr.barras('estado inventario no aptas',etiquetas=['ASIN'], valores=['Unidades disponibles no aptas para venta'], titulo='Unidades disponibles no aptas para venta', colores=True, orientacion='v', hovertext=['Título del producto']), h=700))

    def get_informacion_geografica(self):
        o=cambiar_region(self.myRute+'/informes_vendor/'+self.vendedor+'/informacion geografica/Información geográfica sobre ventas_Detalles_ES.xlsx')
        df=o.accion()
        df["Ingresos por envíos"] = df["Ingresos por envíos"].apply(pd.to_numeric)
        self.gr.add_df('informacion geografica', df)

    def gen_informacion_geografica(self):
        return self.gr.get_html(self.gr.mapa_calor('informacion geografica', 'Ingresos por envíos', hovertext=['Título del producto']))

    def get_todo(self):
        ventas=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de ventas/Diagnóstico de ventas_Vista de detalles_ES3.xlsx')
        ventas = ventas.groupby(by="ASIN").sum()
        trafico=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/diagnostico de trafico/Diagnóstico de tráfico_Detalles_ES3.xlsx')
        trafico=trafico.drop(trafico[trafico['% de visitas totales']=='—'].index)
        trafico['% de visitas totales']=trafico['% de visitas totales'].apply(pd.to_numeric)
        trafico = trafico.groupby(by="ASIN").sum()
        publicidad=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/publicidad/Producto_anunciado_3meses3.xlsx')
        publicidad=publicidad.rename(columns = {'ASIN anunciados' : 'ASIN'})
        publicidad = publicidad.groupby(by="ASIN").sum()
        inventario=pd.read_excel(self.myRute+'/informes_vendor/'+self.vendedor+'/estado inventario/Estado del inventario_ES3.xlsx')
        #inventario = inventario.groupby(by="ASIN").sum()
        df=pd.merge(ventas, trafico, on='ASIN')
        df=pd.merge(df, publicidad, on='ASIN')
        df=pd.merge(df, inventario, on='ASIN')
        df_ordenadoUnidades = df.sort_values('Unidades disponibles aptas para venta').iloc[::-1]
        df_ordenadoVisitas = df.fillna(0).sort_values('% de visitas totales').iloc[::-1]
        self.gr.add_df('estrategia', df)
        self.gr.add_df('estratefia ordenado unidades', df_ordenadoUnidades)
        self.gr.add_df('estratefia ordenado visitas', df_ordenadoVisitas)
        

    def gen_inventario_ventas(self):
        gr1={'id':'barras', 'etiquetas':['ASIN'], 'valores':['Unidades disponibles aptas para venta'], 'colores':False, 'secondary_y':False, 'hovertext':['Título del producto']}
        gr2={'id':'lineal', 'x':'ASIN', 'y':'Ingresos por envíos', 'rectas':True, 'puntos':False, 'secondary_y':True, 'hovertext':['Título del producto']}
        return self.gr.get_html(self.gr.multiple('estratefia ordenado unidades', [gr1, gr2], 'Unidades disponibles y ventas', True, 'Unidades disponibles aptas para venta', 'Ingresos por envíos'))

    def gen_visitas_ventas_publicidad(self):
        gr1={'id':'barras', 'etiquetas':['ASIN'], 'valores':['% de visitas totales', 'Ingresos por envíos: % del total'], 'colores':False, 'secondary_y':False, 'hovertext':['Título del producto']}
        gr2={'id':'lineal', 'x':'ASIN', 'y':'Gasto', 'rectas':True, 'puntos':False, 'secondary_y':True, 'hovertext':['Título del producto']}
        return self.gr.get_html(self.gr.multiple('estratefia ordenado visitas', [gr1, gr2], 'Visitas, ventas y gasto en publicidad', True, '% de visitas y ventas', 'Gasto publicidad'))
    
    def gen_inventario_publicidad(self):
        gr1={'id':'barras', 'etiquetas':['ASIN'], 'valores':['Unidades disponibles aptas para venta'], 'colores':False, 'secondary_y':False, 'hovertext':['Título del producto']}
        gr2={'id':'lineal', 'x':'ASIN', 'y':'Gasto', 'rectas':True, 'puntos':False, 'secondary_y':True, 'hovertext':['Título del producto']}
        return self.gr.get_html(self.gr.multiple('estratefia ordenado unidades', [gr1, gr2], 'Unidades disponibles y gasto en publicidad', True, 'Unidades disponibles aptas para ventas', 'Gasto publicidad'))

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

#A continuación se facilitan funciones que usan funciones de crearGraficasVendor para crear el html de una serie de gráficas en concreto:
def productos(vendedor='miquelrius', asin=None):
    v=crearGraficasVendor(vendedor)
    v.get_diagnostico_ventas(asin)
    graph=v.gen_diagnostico_ventas2()
    graph=graph+v.gen_diagnostico_ventas3()
    graph=graph+v.gen_diagnostico_ventas4()
    v.get_diagnostico_trafico(asin)
    graph=graph+v.gen_diagnostico_trafico()
    v.get_estado_inventario(asin)
    graph=graph+v.gen_estado_inventario()
    graph=graph+v.gen_estado_inventario2()
    return graph

def ventas(vendedor='miquelrius'):
    
    v=crearGraficasVendor(vendedor)
    v.get_tendencias_ventas()
    graph=v.gen_tendencias_ventas()
    v.get_informacion_geografica()
    graph=graph+v.gen_informacion_geografica()
    v.get_todo()
    graph+=v.gen_inventario_ventas()
    graph+=v.gen_visitas_ventas_publicidad()
    graph+=v.gen_inventario_publicidad()
    return graph

def customers2(vendedor='miquelrius'):
    v=crearGraficasVendor(vendedor)
    v.get_resenas()
    graph=v.gen_resenas()
    graph=graph+v.gen_resenas2()
    graph=graph+v.gen_resenas3()
    return graph

def index1(vendedor):
    v=crearGraficasVendor(vendedor)
    v.get_tendencias_ventas()
    graph=v.gen_tendencias_ventas()
    return graph

def index2(vendedor):
    v=crearGraficasVendor(vendedor)
    v.get_diagnostico_ventas()
    graph=v.gen_diagnostico_ventas2()
    return graph

def index3(vendedor):
    v=crearGraficasVendor(vendedor)
    v.get_resenas()
    graph=v.gen_resenas()
    return graph

def todo(vendedor):
    graph=index1(vendedor)
    graph=graph+index2(vendedor)
    return graph+index3(vendedor)






#pip install -U kaleido
#pip install psutil