import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Clase para crear gráficas interactivas
class graficas():

    #Diccionario con los tipos de gráficos (para luego usar en los subplots de la función 'varios')
    tipos={'barras':'bar', 'barras_apiladas':'bar', 'circular':'pie', 'lineal':'scatter', 'temporal':'scatter', 'embudo':'funnel', 'indicador':'Indicator'}
    colors=['blue', 'green', 'red', 'orange', 'yellow', 'cyan', 'black', 'magenta', 'brown', 'aliceblue', 'gray', 'greenyellow', 'antiquewhite', 'violet', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'silver', 'blueviolet', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'grey', 'aqua', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rosybrown', 'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'wheat', 'white', 'whitesmoke', 'yellowgreen']
    #La clase tendrá un diccionario de dataframes con clave id del dataframe y valor el dataframe
    def __init__(self, dict_df):
        self.dict_df=dict_df.copy()

    def add_df(self, id, df):
        self.dict_df[id]=df

    #Se le pasa el id del dataframe a usar, etiquetas para las barras, valores para la algura de las barras, colores se pondrá a true si queremos tener un degradado de colores para cada valor de 'valores', título del gráfico y orientación de las barras
    #Etiquetas es una lista de uno o dos valores, si lleva dos el primero será para cada columna y el segundo para el color de columna, valores es una lista sin limite por cada valor se usará un color de columna según etiqueta.
    def barras(self, id, etiquetas, valores, colores=False, titulo=None, orientacion='v'):
        if orientacion=='v': 
            if colores==True:
                return px.bar(self.dict_df[id], x=etiquetas[0], y=valores[0], hover_data=[valores[0]], color=valores[0], title=titulo, orientation=orientacion)
            else:
                if len(valores)==1 and len(etiquetas)==1:
                    return px.bar(self.dict_df[id], x=etiquetas[0], y=valores[0], barmode='group', title=titulo, orientation=orientacion, labels={'y':valores[0]})
                else:
                    if len(valores)==1:
                        return px.bar(self.dict_df[id], x=etiquetas[0], y=valores[0], color=etiquetas[1], barmode='group', title=titulo, orientation=orientacion)
                    else:
                        df_aux=self.dict_df[id].melt(id_vars=etiquetas, value_vars=valores)
                        return px.bar(df_aux, x=etiquetas[0], y="value", color='variable', barmode='group', title=titulo, orientation=orientacion)
        else:
            if colores==True:
                return px.bar(self.dict_df[id], x=valores[0], y=etiquetas[0], hover_data=[valores[0]], color=valores[0], title=titulo, orientation=orientacion)
            else:
                if len(valores)==1 and len(etiquetas)==1:
                    return px.bar(self.dict_df[id], x=valores[0], y=etiquetas[0], barmode='group', title=titulo, orientation=orientacion)
                else:
                    if len(valores)==1:
                        return px.bar(self.dict_df[id], x=valores[0], y=etiquetas[0], color=etiquetas[1], barmode='group', title=titulo, orientation=orientacion)
                    else:
                        df_aux=self.dict_df[id].melt(id_vars=etiquetas, value_vars=valores)
                        return px.bar(df_aux, x="value", y=etiquetas[0], color='variable', barmode='group', title=titulo, orientation=orientacion)


    #Gráfico de barras apiladas, tiene los mismos parámetros que barras normal (sin colores)
    def barras_apiladas(self, id, etiquetas, valores, titulo=None, orientacion='v'):
        if orientacion=='v':
            if(len(etiquetas)==1):
                return px.bar(self.dict_df[id], x=etiquetas[0], y=valores, title=titulo, orientation=orientacion)
            else:
                return px.bar(self.dict_df[id], x=etiquetas[0], y=valores, color=etiquetas[1], title=titulo, orientation=orientacion)
        else:
            if(len(etiquetas)==1):
                return px.bar(self.dict_df[id], x=valores, y=etiquetas[0], title=titulo, orientation=orientacion)
            else:
                return px.bar(self.dict_df[id], x=valores, y=etiquetas[0], color=etiquetas[1], title=titulo, orientation=orientacion)

    #Crea un gráfico circular donde etiquetas puede ser una lista, si es una lista se creará un gráfico circular con pisos, si no uno normal. Valor no es una lista
    def circular(self, id, etiquetas, valor, titulo=None):
        if len(etiquetas)==1:
            return px.pie(self.dict_df[id], values=valor, names=etiquetas[0], title=titulo)
        else:
            return px.sunburst(self.dict_df[id], path=etiquetas, values=valor, title=titulo)
 
    #Crea un gráfico de una recta y/o puntos (según se marquen los parámetros rectas y puntos) con los valores x e y.
    #x e y no son listas, son strings con las variables del df a usar
    def lineal(self, id, x, y, rectas=True, puntos=True, titulo=None):
        if rectas and puntos:
            fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='lines+markers', name=y))
        elif rectas:
            fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='lines', name=y))
        else:
            fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='markers', name=y))
        fig.update_layout(title=titulo)
        return fig

    #lineal('hola', 'asin', 'gastos', rectas=False)
    #Crea un gráfico lineal como el anterior pero en este caso x debe de ser datos del tipo DateTime
    def temporal(self, id, x, y, titulo):
        fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dict_df[id][y], mode='lines', name=y))
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
    def embudo(self, id, etiquetas, valor, titulo=None):
        if(len(etiquetas)==1):
            return px.funnel(self.dict_df[id], x=valor, y=etiquetas[0], title=titulo)
        else:
            return px.funnel(self.dict_df[id], x=valor, y=etiquetas[0], color=etiquetas[1], title=titulo)


    def indicador(self, id, etiqueta, mean=False, titulo=None, formato={'suffix': "€"}):
        total = self.dict_df[id][etiqueta].sum()
        if mean:
            total=total/self.dict_df[id].shape[0]
        fig= go.Figure(go.Indicator( mode = "number", value = total, number = formato, domain = {'x': [0, 1], 'y': [0, 1]}))
        fig.update_layout(title=titulo)
        return fig
    #Esta función es capaz de integrar varios gráficos en los mismos ejes, los distintos gráficos se pasan en param como una lista de diccionarios.
    #Por ejemplo:
    #gr=graficas(dict_df)
    #g1={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False}
    #g2={'id':'barras', 'etiquetas':['asin'], 'valores':['gastos'], 'colores':False, 'orientacion':'v'}
    #gr.multiple('df1', [g1,g2], 'prueba')
    def multiple(self, id, param, titulo, doble_eje=False, etiqueta1=None, etiqueta2=None):
        color=0
        if doble_eje==True:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.update_yaxes(title_text=etiqueta1, secondary_y=False)
            fig.update_yaxes(title_text=etiqueta2, secondary_y=True)
        else:
            fig=go.Figure()
        fig.update_layout(title_text=titulo)
        for p in param:
            if(p['id']=='barras'):
                data=self.barras(id,p['etiquetas'], p['valores'], p['colores'], titulo).data
                fig.update_layout(barmode='group')
            elif(p['id']=='barras_apiladas'):
                data=self.barras_apiladas(id,p['etiquetas'], p['valores'], titulo).data
                fig.update_layout(barmode='stack')
            elif(p['id']=='circular'):
                data=self.circular(id,p['etiquetas'], p['valor'], titulo).data
            elif(p['id']=='lineal'):
                data=self.lineal(id,p['x'], p['y'], p['rectas'], p['puntos'], titulo).data
            elif(p['id']=='temporal'):
                data=self.temporal(id, p['x'], p['y'], titulo).data
            else:
                data=self.embudo(id, p['x'], p['y'],  titulo).data
            for d in data:
                d.marker.color=self.colors[color]
                color+=1
                if doble_eje:
                    if p['secondary_y']:
                        fig.add_trace(d, secondary_y=True)
                    else:
                        fig.add_trace(d, secondary_y=False)
                else:
                    fig.add_trace(d)
            if (p['id']=='temporal'):
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
        cuadricula=list(list())
        for i in range(nrows):
            aux=[]
            for j in range(ncols):
                aux.append('')
            cuadricula.append(aux)
        titulos=[]
        for p in param:
            cuadricula[p['row']][p['col']]={"type":self.tipos[p['id']]}
            titulos.append(p['titulo'])
        fig = make_subplots(
            rows=nrows, cols=ncols,
            shared_xaxes=True,
            vertical_spacing=0.03,
            specs=cuadricula,
            subplot_titles = titulos
        )
        fig.update_layout(title_text=titulo)
        for p in param:
            if(p['id']=='barras'):
                data=self.barras(p['id_df'] ,p['etiquetas'], p['valores'], p['colores'], titulo, p['orientacion']).data
                fig.update_layout(barmode='group')
            elif(p['id']=='barras_apiladas'):
                data=self.barras_apiladas(p['id_df'],p['etiquetas'], p['valores'], titulo).data
                fig.update_layout(barmode='stack')
            elif(p['id']=='circular'):
                data=self.circular(p['id_df'],p['etiquetas'], p['valor'], titulo).data
            elif(p['id']=='lineal'):
                data=self.lineal(p['id_df'],p['x'], p['y'], p['rectas'], p['puntos'], titulo).data
            elif(p['id']=='temporal'):
                data=self.temporal(p['id_df'], p['x'], p['y'], titulo).data
            elif(p['id']=='indicador'):
                data=self.indicador(p['id_df'], p['etiqueta'], p['mean'], titulo, p['formato']).data
            else:
                data=self.embudo(p['id_df'], p['etiquetas'], p['valor'], titulo).data
            for d in data:
                if p['id']!='circular' and p['id']!= 'indicador':
                    d.marker.color=self.colors[color]
                    color+=1
                fig.add_trace(d, row=p['row']+1, col=p['col']+1)
        return fig
        
    #Devuelve el html de fig pasada como parámetro.
    #Como todas las anteriores funciones devuelven fig, llamar a esta para obtener el html.
    def get_html(self, fig):
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

    def tam(self, fig, w=None, h=None, color=None):
        return fig.update_layout( autosize=True, width=w, height=h, margin=dict( l=50, r=50, b=100, t=100, pad=4 ), paper_bgcolor=color)