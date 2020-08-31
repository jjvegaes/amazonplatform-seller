import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pandas.plotting as plotting
sns.set()
sns.set_style('dark')
sns.set_palette("pastel")

# generate df
#df = pd.DataFrame({'asin':['a', 'b', 'c'], 'esin':['c', 'd', 'e'], 'ventas':[1,2,3], 'gastos':[2,3,4]})
class graficos_informes():
    def __init__(self):
        self.dict_df={}

    def add_df(self, id, df):
        self.dict_df[id]=df

#dict_df={'hola':pd.DataFrame({'asin':['a', 'b', 'c', 'd'], 'esin':['rojo', 'azul', 'rojo', 'azul'], 'ventas':[1,2,3, 8], 'gastos':[2,10,1, 9]})}
    def varios(self, id, param):
        fig, axes = plt.subplots(1, 5)
        sns.despine(left=True)
        fig.set_size_inches(18.5, 10.5, forward=True)
        cont=0
        for i in param:
            if(i['tipo']=='barras'):
                barra(id, i['valores'], i['etiquetas'], ax=axes[cont], subplot=True)
                print('barra')
            elif(i['tipo']=='tabla'):
                tabla(id, ax=axes[cont], subplot=True)
                print('tabla', cont)
            elif(i['tipo']=='quesito'):
                quesito(id, i['valor'], i['etiqueta'], ax=axes[cont], subplot=True)
                print('queso', cont)
            elif(i['tipo']=='linea'):
                linea(id, i['x'], i['y'], ax=axes[cont], subplot=True)
            elif(i['tipo']=='linea_barra'):
                linea_barra(id, i['x'], i['y1'], i['y2'], ax=axes[cont], subplot=True)
            cont+=1
        plt.tight_layout()
        
        plt.savefig(id+'.png')


    #varios('hola', [{'tipo':'barras','valores':['ventas', 'gastos'], 'etiquetas':['asin']}, {'tipo':'barras', 'valores':['ventas'], 'etiquetas':['esin']}, {'tipo':'tabla'}, {'tipo':'quesito', 'valor':'ventas', 'etiqueta':'esin'}])






    def barra(self, id, valores, etiquetas, ax=None, subplot=False):
        if len(valores)==1 and len(etiquetas)==1:
            sns.barplot(x=etiquetas[0], y=valores[0], data=self.dict_df[id], ax=ax)
        else:
            if len(valores)==1:
                sns.barplot(x=etiquetas[0], y=valores[0], hue=etiquetas[1], data=self.dict_df[id], ax=ax)
            else:
                df_aux=dict_df[id].melt(id_vars=etiquetas, value_vars=valores)
                sns.barplot(x=etiquetas[0], y='value', hue='variable', data=self.dict_df[id], ax=ax)
        if not subplot:
            plt.savefig(id+'_barras.png')
            plt.close(ax)



    def quesito(self, id, valor, etiqueta, ax=None, subplot=False):
        dict_df[id].plot.pie(subplots=True, labels=self.dict_df[id][etiqueta], y=valor, figsize=(6, 3), ax=ax)
        if not subplot:
            plt.savefig(id+'_quesitos.png')
            plt.close(ax)


    def tabla(self, id, ax=None, subplot=False):
        if ax==None:
            plt.axis('off')
            plt.axis('tight')
            plt.table(cellText=self.dict_df[id].values, rowLabels=self.dict_df[id].index, colLabels=self.dict_df[id].columns, loc='center')
        else:
            ax.axis('off')
            ax.axis('tight')
            ax.table(cellText=self.dict_df[id].values, rowLabels=self.dict_df[id].index, colLabels=self.dict_df[id].columns, loc='center')
        if not subplot:
            plt.savefig(id+'_tabla.png')
            plt.close()
        
    def linea(self, id, x, y, ax=None, subplot=False):
        if ax==None:
            plt.plot(self.dict_df[id][x], self.dict_df[id][y])
        else:
            ax.plot(self.dict_df[id][x], self.dict_df[id][y])
        if not subplot:
            plt.savefig(id+'_linea.png')
            plt.close()

    def linea_barra(self, id, x, y1, y2, ax=None, subplot=False):
        if ax==None:
            sns.barplot(x=x, y=y1, data=self.dict_df[id], color='c')
            plt.twinx()
            plt.plot(self.dict_df[id][x], self.dict_df[id][y2], color='r', marker='o')
            plt.ylabel(y2)
        else:
            sns.barplot(x=x, y=y1, data=self.dict_df[id], ax=ax, color='c')
            ax.twinx()
            ax.plot(self.dict_df[id][x], self.dict_df[id][y2], color='r', marker='o')
            plt.ylabel(y2)
        if not subplot:
            plt.savefig(id+'_linea_barra.png')
            plt.close()


#tabla('hola')
#linea('hola', 'asin', 'gastos')
#barra('hola', ['ventas', 'gastos'], ['asin'])
#quesito('hola','ventas', 'asin')
#linea_barra('hola', 'asin', 'gastos', 'ventas')

#varios('hola', [{'tipo':'linea_barra', 'x':'asin', 'y1':'gastos', 'y2':'ventas'},{'tipo':'barras','valores':['ventas', 'gastos'], 'etiquetas':['asin']}, {'tipo':'linea', 'x':'asin', 'y':'gastos'}, {'tipo':'quesito', 'valor':'ventas', 'etiqueta':'esin'}, {'tipo':'tabla'}])

#plt.figure(figsize=(10,8)
'''


#pip install plotly==2.7 cufflinks
#pip install plotly.express
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = px.line(dict_df['hola'], x="asin", y="ventas", title='Life expectancy in Canada')
#Esto crea el archivo
#plotly.offline.plot(fig, filename='file.html')
#Esto devuelve una cadena div:
#Si lo haces con div, añadir en el head del html: <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
print(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'))





import plotly.graph_objects as go

x = np.arange(10)

fig = go.Figure(data=go.Scatter(x=x, y=x**2))
fig.show()


#Clase para crear gráficas interactivas
class graficas():

    #Diccionario con los tipos de gráficos (para luego usar en los subplots de la función 'varios')
    tipos={'barras':'bar', 'barras_apiladas':'bar', 'circular':'pie', 'lineal':'scatter', 'temporal':'scatter', 'embudo':'funnel'}
    colors=['blue', 'green', 'red', 'orange', 'yellow', 'cyan', 'black', 'magenta', 'brown', 'aliceblue', 'gray', 'greenyellow', 'antiquewhite', 'violet', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'silver', 'blueviolet', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'grey', 'aqua', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rosybrown', 'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'wheat', 'white', 'whitesmoke', 'yellowgreen']
    #La clase tendrá un diccionario de dataframes con clave id del dataframe y valor el dataframe
    def __init__(self, dict_df):
        self.dict_df=dict_df.copy()

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
                        return px.bar(dict_df[id], x=etiquetas[0], y=valores[0], color=etiquetas[1], barmode='group', title=titulo, orientation=orientacion)
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
                        return px.bar(dict_df[id], x=valores[0], y=etiquetas[0], color=etiquetas[1], barmode='group', title=titulo, orientation=orientacion)
                    else:
                        df_aux=self.dict_df[id].melt(id_vars=etiquetas, value_vars=valores)
                        return px.bar(df_aux, x="value", y=etiquetas[0], color='variable', barmode='group', title=titulo, orientation=orientacion)


    #Gráfico de barras apiladas, tiene los mismos parámetros que barras normal (sin colores)
    def barras_apiladas(self, id, etiquetas, valores, titulo=None, orientation='v'):
        if orientation=='v':
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
        fig = go.Figure(data=go.Scatter(x=self.dict_df[id][x], y=self.dift_df[id][y], mode='lines', name=y))
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
            return px.funnel(dict_df['hola'], x=valor, y=etiquetas[0], title=titulo)
        else:
            return px.funnel(dict_df['hola'], x=valor, y=etiquetas[0], color=etiquetas[1], title=titulo)

    #Esta función es capaz de integrar varios gráficos en los mismos ejes, los distintos gráficos se pasan en param como una lista de diccionarios.
    #Por ejemplo:
    #gr=graficas(dict_df)
    #g1={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False}
    #g2={'id':'barras', 'etiquetas':['asin'], 'valores':['gastos'], 'colores':False, 'orientacion':'v'}
    #gr.multiple('df1', [g1,g2], 'prueba')
    def multiple(self, id, param, titulo):
        color=0
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
                data=self.temporal(id, p['x'], p['y'], titulo)
            else:
                data=self.embudo(id, p['x'], p['y'], p['color'], titulo)
            for d in data:
                d.marker.color=self.colors[color]
                color+=1
                fig.add_trace(d)
        return fig

    #Crea una cuadricula para introducir varios gráficos en el mismo div, funciona como el anterior pero en este caso en param se debe de introducir la posición de cada gráfico y además pasar ncols y nrows.
    #Ejemplo:
    #gr=graficas(dict_df)
    #g1={'id':'embudo', 'valor':'gastos', 'etiquetas':['asin'],  'row':0, 'col':0}
    #g2={'id':'circular', 'etiquetas':['asin'], 'valor':'gastos', 'row':0, 'col':1}
    #g3={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False, 'row':1, 'col':0}
    #g4={'id':'barras', 'etiquetas':['asin'], 'valores':['ventas','gastos'], 'colores':False, 'orientacion':'h', 'row':1, 'col':1}
    #gr.varios('df1', [g1,g2,g3,g4], 'prueba', 2, 2)
    def varios(self, id, param, titulo, ncols, nrows):
        color=0
        cuadricula=list(list())
        for i in range(nrows):
            aux=[]
            for j in range(ncols):
                aux.append('')
            cuadricula.append(aux)
        for p in param:
            cuadricula[p['row']][p['col']]={"type":self.tipos[p['id']]}
        fig = make_subplots(
            rows=nrows, cols=ncols,
            shared_xaxes=True,
            vertical_spacing=0.03,
            specs=cuadricula
        )
        fig.update_layout(title_text=titulo)
        for p in param:
            if(p['id']=='barras'):
                data=self.barras(id,p['etiquetas'], p['valores'], p['colores'], titulo, p['orientacion']).data
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
                data=self.embudo(id, p['etiquetas'], p['valor'], titulo).data
            for d in data:
                if p['id']!='circular':
                    d.marker.color=self.colors[color]
                    color+=1
                fig.add_trace(d, row=p['row']+1, col=p['col']+1)
            print("hola")
        return fig
        
    #Devuelve el html de fig pasada como parámetro.
    #Como todas las anteriores funciones devuelven fig, llamar a esta para obtener el html.
    def get_html(self, fig):
        return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')

#fig =px.sunburst( dict_df['hola'], names='asin', parents='esin', values='gastos')

gr=graficas(dict_df)
g1={'id':'embudo', 'valor':'gastos', 'etiquetas':['asin'],  'row':0, 'col':0}
g2={'id':'circular', 'etiquetas':['esin','asin'], 'valor':'gastos', 'row':0, 'col':1}
g3={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False, 'row':1, 'col':0}
g4={'id':'barras', 'etiquetas':['asin'], 'valores':['ventas','gastos'], 'colores':False, 'orientacion':'h', 'row':1, 'col':1}

#gr=graficas(dict_df)
#g1={'id':'lineal', 'x':'asin', 'y':'ventas', 'rectas':True, 'puntos':False}
#g2={'id':'barras', 'etiquetas':['asin'], 'valores':['gastos', 'ventas'], 'colores':False, 'orientacion':'v'}
#print(gr.get_html(gr.multiple('hola', [g1,g2], 'prueba')))
print(gr.get_html(gr.varios('hola', [g1,g2,g3,g4], 'prueba', 2, 2)))
fig1 = px.funnel(dict_df['hola'], x='gastos', y='asin', color='esin')
fig2=px.pie(dict_df['hola'], values='gastos', names='asin')
fig3 = px.funnel(dict_df['hola'], x='ventas', y='asin')
fig4 = go.Figure(data=go.Scatter(x=dict_df['hola']['asin'], y=dict_df['hola']['ventas'], mode='lines+markers', name='hola'))
fig = go.Figure()
fig.add_traces([fig1.data[0], fig2.data[0]])

# initialize xaxis2 and yaxis2
fig['layout']['xaxis2'] = {}
fig['layout']['yaxis2'] = {}

# Edit layout for subplots
fig.layout.xaxis.update({'domain': [0, .5]})
fig.layout.xaxis2.update({'domain': [0.6, 1.]})

# The graph's yaxis MUST BE anchored to the graph's xaxis
fig.layout.yaxis2.update({'anchor': 'x2'})
fig.layout.yaxis2.update({'title': 'Goals'})

# Update the margins to add a title and see graph x-labels.
fig.layout.margin.update({'t':50, 'b':100})
fig.layout.update({'title': '2016 Hockey Stats'})

fig.show()

#barras_apiladas('hola', ['asin'], ['gastos', 'ventas']).show()
#multiple('hola', [{'id':'barras_apiladas', 'etiquetas':['asin'], 'valores':['gastos', 'ventas']}, {'id':'lineal', 'x':'asin', 'y':'gastos', 'rectas':True, 'puntos':True}], 'prueba').show()





fig = make_subplots(
    rows=2, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "funnel"}, {"type":"pie"}],
           [{"type": "funnel"}, {"type":"scatter"}]]
)
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)
fig.add_trace(fig3.data[0], row=2, col=1)
fig.add_trace(fig4.data[0], row=2, col=2)
fig.show()'''