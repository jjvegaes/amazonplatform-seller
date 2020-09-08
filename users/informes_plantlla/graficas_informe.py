import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pandas.plotting as plotting
import matplotlib as mpl
sns.set()
sns.set_style('dark')
sns.set_palette("pastel")

#Clase que crea gráficas que se añaden en el informe
class graficas_informe():
    #La ruta es donde quieres que se guarden las gráficas
    def __init__(self, ruta):
        self.ruta=ruta
        self.dict_df={}#Diccionario con todos los dataframes (con clave un id)

    #Para introducir un nuevo dataframe
    def add_df(self, id, df):
        self.dict_df[id]=df

    #Para poner varias gráficas una seguida de otra (no se usa de momento), param es una lista de diccionarios con los parámetros de los distintos gráficos
    def varios(self, id, param):
        fig, axes = plt.subplots(1, 5)#Permitimos 5 gráficos seguidos
        sns.despine(left=True)
        fig.set_size_inches(18.5, 10.5, forward=True)
        cont=0
        for i in param:#Recorremos todos los gráficos y según el tipo creamos un sublplot con los parámetros necesarios
            if(i['tipo']=='barras'):
                self.barra(id, i['valores'], i['etiquetas'], ax=axes[cont], subplot=True)
                print('barra')
            elif(i['tipo']=='tabla'):
                self.tabla(id, ax=axes[cont], subplot=True)
                print('tabla', cont)
            elif(i['tipo']=='quesito'):
                self.quesito(id, i['valor'], i['etiqueta'], ax=axes[cont], subplot=True)
                print('queso', cont)
            elif(i['tipo']=='linea'):
                self.linea(id, i['x'], i['y'], ax=axes[cont], subplot=True)
            elif(i['tipo']=='linea_barra'):
                self.linea_barra(id, i['x'], i['y1'], i['y2'], ax=axes[cont], subplot=True)
            cont+=1
        plt.tight_layout()
        
        plt.savefig(id+'.png')


    #varios('hola', [{'tipo':'barras','valores':['ventas', 'gastos'], 'etiquetas':['asin']}, {'tipo':'barras', 'valores':['ventas'], 'etiquetas':['esin']}, {'tipo':'tabla'}, {'tipo':'quesito', 'valor':'ventas', 'etiqueta':'esin'}])





    #Dibujamos el gráfico de barras, se le pasa el id del dataframe a usar, los valores del eje y, las etiquetas del eje x. ax y subplot debe dejarse por defecto.
    def barra(self, id, valores, etiquetas, ax=None, subplot=False):
        if len(valores)==1 and len(etiquetas)==1:
            sns.barplot(x=etiquetas[0], y=valores[0], data=self.dict_df[id], ax=ax)
        else:
            if len(valores)==1:
                sns.barplot(x=etiquetas[0], y=valores[0], hue=etiquetas[1], data=self.dict_df[id], ax=ax)#hue genera gráficos con dos etiquetas
            else:
                df_aux=self.dict_df[id].melt(id_vars=etiquetas, value_vars=valores)#Genera un nuevo dataframe con una nueva columna variable
                sns.barplot(x=etiquetas[0], y='value', hue='variable', data=df_aux, ax=ax)
        if not subplot:
            plt.rcParams.update({'font.size': 40})#Tamaño del texto
            fig = plt.gcf()
            fig.set_size_inches(10.5, 6.5)#Tamaño de la figura
            plt.xticks(rotation=90)#Texto puesto vertical
            fig.savefig(self.ruta+'/'+id+'_barras.png', bbox_inches = "tight")#Guardamos figura
            plt.close(ax)


    #Genera un diagrama circular de la misma forma que el de barras. ax y sublplot dejarlo por defecto
    def quesito(self, id, valor, etiqueta, ax=None, subplot=False):
        if ax != None:
            self.dict_df[id].plot.pie(subplots=True, labels=self.dict_df[id][etiqueta], y=valor, figsize=(6, 3), ax=ax, textprops={'fontsize': 14})
            if not subplot:
                mpl.rcParams['font.size'] = 1000
                plt.rcParams.update({'font.size': 1000})
                plt.legend('')
                fig = plt.gcf()
                fig.set_size_inches(40.5, 40.5)
                fig.savefig(self.ruta+'/'+id+'_quesitos.png', bbox_inches = "tight")
                plt.close(ax)
        else:
            fig, ax = plt.subplots()
            ax.pie(list(self.dict_df[id][valor]),labels=self.dict_df[id][etiqueta], wedgeprops=dict(width=.7))
            if not subplot:
                plt.legend('')
                fig.set_size_inches(10, 10)
                fig.savefig(self.ruta+'/'+id+'_quesitos.png', bbox_inches = "tight")
            plt.close(fig)

    #Genera una tabla. ax y subplot dejarlo por defecto
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
        
    #Genera un gráfico lineal
    def linea(self, id, x, y, ax=None, subplot=False):
        if ax==None:
            plt.plot(self.dict_df[id][x], self.dict_df[id][y])
        else:
            ax.plot(self.dict_df[id][x], self.dict_df[id][y])
        if not subplot:
            plt.rcParams.update({'font.size': 40})
            fig = plt.gcf()
            fig.set_size_inches(10.5, 6.5)
            plt.xticks(rotation=90)
            plt.savefig(self.ruta+'/'+id+'_linea.png', bbox_inches = "tight")
            plt.close()

    #Genera un gráfico lineal junto a uno de barras
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
