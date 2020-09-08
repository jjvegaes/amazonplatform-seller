import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

#Clase para crear gráficas interactivas
class graficas():

    #Diccionario con los tipos de gráficos (para luego usar en los subplots de la función 'varios')
    tipos={'barras':'bar', 'barras_apiladas':'bar', 'circular':'pie', 'lineal':'scatter','word_cloud':'scatter', 'temporal':'scatter', 'embudo':'funnel', 'indicador':'Indicator'}
    colors=['blue', 'green', 'red', 'orange', 'yellow', 'cyan', 'black', 'magenta', 'brown', 'aliceblue', 'gray', 'greenyellow', 'antiquewhite', 'violet', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'silver', 'blueviolet', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'grey', 'aqua', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rosybrown', 'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'wheat', 'white', 'whitesmoke', 'yellowgreen']
    #La clase tendrá un diccionario de dataframes con clave id del dataframe y valor el dataframe
    def __init__(self, dict_df):
        self.dict_df=dict_df.copy()

    #Para añadir un nuevo dataframe al diccionario
    def add_df(self, id, df):
        self.dict_df[id]=df

    #Se le pasa el id del dataframe a usar, etiquetas para las barras, valores para la algura de las barras, colores se pondrá a true si queremos tener un degradado de colores para cada valor de 'valores', título del gráfico y orientación de las barras
    #Etiquetas es una lista de uno o dos valores, si lleva dos el primero será para cada columna y el segundo para el color de columna, valores es una lista sin limite por cada valor se usará un color de columna según etiqueta.
    def barras(self, id, etiquetas, valores, colores=False, titulo=None, orientacion='v', hovertext=None):
        if orientacion=='v': 
            if colores==True:#Si usamos colores, la etiqueta valor es la que tenga los colores
                return px.bar(self.dict_df[id], x=etiquetas[0], y=valores[0], hover_data=hovertext, color=valores[0], title=titulo, orientation=orientacion)
            else:
                if len(valores)==1 and len(etiquetas)==1:#Con una etiqueta y un valor es un diagrama de barras simple
                    return px.bar(self.dict_df[id], x=etiquetas[0], y=valores[0], barmode='group',hover_data=hovertext, title=titulo, orientation=orientacion)
                else:
                    if len(valores)==1:#tenemos un valor y dos etiquetass
                        return px.bar(self.dict_df[id], x=etiquetas[0], y=valores[0], color=etiquetas[1],hover_data=hovertext, barmode='group', title=titulo, orientation=orientacion)     
                    else:#tenemos mas de un valor y una etiqueta
                        for h in hovertext:#Para que cuando hagamos el melt no se pierdan las etiquetas
                            etiquetas.append(h)
                        df_aux=self.dict_df[id].melt(id_vars=etiquetas, value_vars=valores)#Para poder crear un diagrama con más de un valor por etiqueta
                        return px.bar(df_aux, x=etiquetas[0], y="value", color='variable', barmode='group',hover_data=hovertext, title=titulo, orientation=orientacion)
        else:#es igual que el vertical
            if colores==True:
                return px.bar(self.dict_df[id], x=valores[0], y=etiquetas[0], hover_data=hovertext, color=valores[0], title=titulo, orientation=orientacion)
            else:
                if len(valores)==1 and len(etiquetas)==1:
                    return px.bar(self.dict_df[id], x=valores[0], y=etiquetas[0], barmode='group',hover_data=hovertext, title=titulo, orientation=orientacion)
                else:
                    if len(valores)==1:
                        return px.bar(self.dict_df[id], x=valores[0], y=etiquetas[0], color=etiquetas[1],hover_data=hovertext, barmode='group', title=titulo, orientation=orientacion)
                    else:
                        df_aux=self.dict_df[id].melt(id_vars=etiquetas, value_vars=valores)
                        return px.bar(df_aux, x="value", y=etiquetas[0], color='variable', barmode='group',hover_data=hovertext, title=titulo, orientation=orientacion)


    #Gráfico de barras apiladas, tiene los mismos parámetros que barras normal (sin colores)
    def barras_apiladas(self, id, etiquetas, valores, titulo=None, orientacion='v', hovertext=None):
        if orientacion=='v':
            if(len(etiquetas)==1):#Una etiqueta y varios valores
                return px.bar(self.dict_df[id], x=etiquetas[0], y=valores, title=titulo, hover_data=hovertext, orientation=orientacion)
            else:#Dos etiquetas y varios valores
                return px.bar(self.dict_df[id], x=etiquetas[0], y=valores, color=etiquetas[1], title=titulo, hover_data=hovertext, orientation=orientacion)
        else:
            if(len(etiquetas)==1):
                return px.bar(self.dict_df[id], x=valores, y=etiquetas[0], title=titulo, hover_data=hovertext, orientation=orientacion)
            else:
                return px.bar(self.dict_df[id], x=valores, y=etiquetas[0], color=etiquetas[1], hover_data=hovertext, title=titulo, orientation=orientacion)

    #Crea un gráfico circular donde etiquetas puede ser una lista, si es una lista se creará un gráfico circular con pisos, si no uno normal. Valor no es una lista
    def circular(self, id, etiquetas, valor, titulo=None, hovertext=None):
        if len(etiquetas)==1:
            return px.pie(self.dict_df[id], values=valor, names=etiquetas[0], title=titulo, hover_data=hovertext)
        else:
            return px.sunburst(self.dict_df[id], path=etiquetas, values=valor, title=titulo, hover_data=hovertext)
 
    #Crea un gráfico de una recta y/o puntos (según se marquen los parámetros rectas y puntos) con los valores x e y.
    #x e y no son listas, son strings con las variables del df a usar
    def lineal(self, id, x, y, rectas=True, puntos=True, titulo=None, hovertext=None):
        if rectas and puntos:#Rectas y puntos
            fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='lines+markers', name=y, hovertext=hovertext))
        elif rectas:#Solo la recta
            fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='lines', name=y, hovertext=hovertext))
        else:#Solo los puntos
            fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='markers', name=y, hovertext=hovertext))
        fig.update_layout(title=titulo)#Añadimos el título
        return fig

    #Crea un gráfico lineal como el anterior pero en este caso x debe de ser datos del tipo DateTime (se añaden filtros temporales)
    def temporal(self, id, x, y, titulo, hovertext=None):
        fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='lines', name=y, hovertext=hovertext))
        #Para los filtros temporales:
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.update_layout(title=titulo)
        return fig

    #Crea un gráfico de embudo etiquetas es una lista de 1 o 2 valores, si etiquetas tiene un valor se crea un gráfico de embudo normal, si tiene 2 el primero se usará para el eje 'y' y el segundo para el color
    def embudo(self, id, etiquetas, valor, titulo=None, hovertext=None):
        if(len(etiquetas)==1):#Una etiqueta
            return px.funnel(self.dict_df[id], x=valor, y=etiquetas[0], title=titulo, hover_data=hovertext)
        else:#Más de una etiqueta
            return px.funnel(self.dict_df[id], x=valor, y=etiquetas[0], color=etiquetas[1], title=titulo, hover_data=hovertext,)

    #Indicador dada una etiqueta del dataframe, si mean es True se hace la media de todos los valores de esa etiqueta, si es False se hace la suma, formato es lo que se debe de poner después de la etiqueta
    def indicador(self, id, etiqueta, mean=False, titulo=None, formato={'suffix': "€"}):
        total = self.dict_df[id][etiqueta].sum()#Creamos el indicador
        if mean:
            total=total/self.dict_df[id].shape[0]#Creamos el indicadorr
        fig= go.Figure(go.Indicator( mode = "number", value = total, number = formato, domain = {'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout(title=titulo)
        return fig

    #Creamos un Mapa de calor (etiqueta es el valor por el que un punto en el mapa es intenso o no), antes de llamar a esta función llamar a la del archivo cambiar_region para obtener latitud y longitud
    def mapa_calor(self, id, etiqueta, hovertext=None):
        return px.density_mapbox(self.dict_df[id], lat='Latitud', lon='Longitud', z=etiqueta, radius=20,
                        center=dict(lat=40.4167, lon=-3.70325), zoom=5,
                        mapbox_style="stamen-terrain", hover_data=hovertext)
    
    #Crea una tabla dadas unas etiquetas del dataframe que se quiere que aparezcan en la tabla, columnwidth es una lista de tamaños de cada columna
    def tabla(self, id, etiquetas, titulo, columnwidth=None):
        fig= go.Figure(data=go.Table(columnwidth = columnwidth, header=dict(values=etiquetas, font=dict(size=10), align="left"), cells=dict( values=[self.dict_df[id][k].tolist() for k in etiquetas],align = "left")))
        fig.update_layout(title=titulo)
        return fig

    #Nos permite crear una nube de palabras, etiqueta es la columna del df donde aparecen las palabras y valor es el tamaño de estas palabras
    def word_cloud(self, id, etiqueta, valor, titulo):
        tam=self.dict_df[id].shape[0]
        colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(tam)] #Cogemos los 10 colores de python
        #Creamos los valores x con una lista desordenada:
        x=list(range(tam))
        random.shuffle(x)
        #Creamos los valores y con una lista desordenada:
        y=list(range(tam))
        random.shuffle(y)
        #Según el tamaño tenemos un multiplicador u otro, esto es porque según el número de palabras deben de ser más grandes o pequeñas para que se vea bien
        if tam<8:
            multiplicador=0.2
        elif tam<15:
            multiplicador=0.5
        elif tam<25:
            multiplicador=1
        elif tam<100:
            multiplicador=1.5
        else:
            multiplicador=2
        #Obtenemos el gráfico y lo devolvemos:
        data = go.Scatter(x=x, y=y, mode='text', text=list(self.dict_df[id][etiqueta]), marker={'opacity': 1}, textfont={'size': [(float(x)*multiplicador+5)/(tam*0.01) for x in list(self.dict_df[id][valor])], 'color':colors})
        l = go.Layout({'xaxis': {'range':[tam-tam*1.3, tam*1.2], 'showgrid': False, 'showticklabels': False, 'zeroline': False, 'visible': False}, 'yaxis': {'range':[tam-tam*1.1, tam*1.1], 'showgrid': False, 'showticklabels': False, 'zeroline': False, 'visible': False}})
        fig= go.Figure(data=[data], layout=l)
        fig.update_layout(title=titulo)
        return fig
        
    #Para un filtro
    #https://stackoverflow.com/questions/56671386/create-dropdown-button-to-filter-based-on-a-categorical-column
    
    #Esta función es capaz de integrar varios gráficos en los mismos ejes, los distintos gráficos se pasan en param como una lista de diccionarios.
    #Por ejemplo:
    #gr=graficas(dict_df)
    #g1={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False, 'secondary_y':False}
    #g2={'id':'barras', 'etiquetas':['asin'], 'valores':['gastos'], 'colores':False, 'orientacion':'v', 'secondary_y':True}
    #gr.multiple('df1', [g1,g2], 'prueba', doble_eje=True, etiqueta1='ventas', etiqueta2='gastos')
    def multiple(self, id, param, titulo, doble_eje=False, etiqueta1=None, etiqueta2=None):
        color=0
        #Creamos el doble eje:
        if doble_eje==True:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.update_yaxes(title_text=etiqueta1, secondary_y=False)
            fig.update_yaxes(title_text=etiqueta2, secondary_y=True)
        else:
            fig=go.Figure()
        fig.update_layout(title_text=titulo)#Asignamos el título
        #Vamos dibujando todos los gráficos, según el tipo llamamos a uno u otro
        for p in param:
            if(p['id']=='barras'):
                data=self.barras(id,p['etiquetas'], p['valores'], p['colores'], titulo, 'v', p['hovertext']).data
                fig.update_layout(barmode='group')
            elif(p['id']=='barras_apiladas'):
                data=self.barras_apiladas(id,p['etiquetas'], p['valores'], titulo, p['hovertext']).data
                fig.update_layout(barmode='stack')
            elif(p['id']=='circular'):
                data=self.circular(id,p['etiquetas'], p['valor'], titulo, p['hovertext']).data
            elif(p['id']=='lineal'):
                data=self.lineal(id,p['x'], p['y'], p['rectas'], p['puntos'], titulo, p['hovertext']).data
            elif(p['id']=='temporal'):
                data=self.temporal(id, p['x'], p['y'], titulo, p['hovertext']).data
            else:
                data=self.embudo(id, p['x'], p['y'],  titulo, p['hovertext']).data
            for d in data:#Vamos añadiendo todos los gráficos al nuestro
                d.marker.color=self.colors[color]
                color+=1#Para que el siguiente tenga otro color
                if doble_eje:
                    if p['secondary_y']:
                        fig.add_trace(d, secondary_y=True)
                    else:
                        fig.add_trace(d, secondary_y=False)
                else:
                    fig.add_trace(d)
            if (p['id']=='temporal'):#Si añadimos un temporal tenemos que ponerle los filtros
                fig.update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                    )
                )
        return fig

    #Crea una cuadricula para introducir varios gráficos en el mismo div, funciona como el anterior pero en este caso en param se debe de introducir la posición de cada gráfico y además pasar ncols y nrows.
    #Ejemplo:
    #gr=graficas(dict_df)
    #g1={'id':'embudo', 'valor':'gastos', 'etiquetas':['asin'],  'row':0, 'col':0}
    #g2={'id':'circular', 'etiquetas':['asin'], 'valor':'gastos', 'row':0, 'col':1}
    #g3={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False, 'row':1, 'col':0}
    #g4={'id':'barras', 'etiquetas':['asin'], 'valores':['ventas','gastos'], 'colores':False, 'orientacion':'h', 'row':1, 'col':1}
    #gr.varios('df1', [g1,g2,g3,g4], 'prueba', 2, 2)
    def varios(self, param, titulo, ncols, nrows):
        color=0
        #Creamos una matriz con la cuadricula que vamos a usar:
        cuadricula=list(list())
        for i in range(nrows):
            aux=[]
            for j in range(ncols):
                aux.append('')
            cuadricula.append(aux)
        titulos=[]
        #Creamos la cuadricula
        for p in param:
            cuadricula[p['row']][p['col']]={"type":self.tipos[p['id']]}
            titulos.append(p['titulo'])
        fig = make_subplots(
            rows=nrows, cols=ncols,
            shared_xaxes=True,
            #vertical_spacing=0.03,
            specs=cuadricula,
            subplot_titles = titulos
        )
        fig.update_layout(title_text=titulo)
        #Vamos dibujando todos los gráficos, según el tipo llamamos a uno u otro
        for p in param:
            if(p['id']=='barras'):
                data=self.barras(p['id_df'] ,p['etiquetas'], p['valores'], p['colores'], titulo, p['orientacion'], p['hovertext']).data
                fig.update_layout(barmode='group')
            elif(p['id']=='barras_apiladas'):
                data=self.barras_apiladas(p['id_df'],p['etiquetas'], p['valores'], titulo, p['hovertext']).data
                fig.update_layout(barmode='stack')
            elif(p['id']=='circular'):
                data=self.circular(p['id_df'],p['etiquetas'], p['valor'], titulo, p['hovertext']).data
            elif(p['id']=='lineal'):
                data=self.lineal(p['id_df'],p['x'], p['y'], p['rectas'], p['puntos'], titulo,p['hovertext']).data
            elif(p['id']=='temporal'):
                data=self.temporal(p['id_df'], p['x'], p['y'], titulo, p['hovertext']).data
            elif(p['id']=='indicador'):
                data=self.indicador(p['id_df'], p['etiqueta'], p['mean'], titulo, p['formato']).data
            elif(p['id']=='word_cloud'):
                data=self.word_cloud(p['id_df'], p['etiqueta'], p['valor'], titulo).data
            else:
                data=self.embudo(p['id_df'], p['etiquetas'], p['valor'], titulo, p['hovertext']).data
            for d in data:
                if p['id']!='circular' and p['id']!= 'indicador':
                    d.marker.color=self.colors[color]
                    color+=1
                fig.add_trace(d, row=p['row']+1, col=p['col']+1)

        #if titulo=='Unidades vendidas de inventario exceso':
        #    fig.update_layout(showlegend=False)
        return fig
        
    #Devuelve el html de fig pasada como parámetro.
    #Como todas las anteriores funciones devuelven fig, llamar a esta para obtener el html.
    def get_html(self, fig):
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    #Para cambiar el tamaño de una figura y el color
    def tam(self, fig, w=None, h=None, color=None):
        return fig.update_layout( autosize=True, width=w, height=h, margin=dict( l=50, r=50, b=100, t=100, pad=4 ), paper_bgcolor=color)


