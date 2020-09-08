# encoding: utf-8

import pandas as pd
import numpy as np
import mws
import re
import os
from datetime import datetime, timedelta
from informes import Informe
#from users import informes as Informe


class Limpieza():
    def __init__(self):
        self.result = None

    def limpieza(self, access_key, merchant_id, secret_key, report_id, start_date, end_date):
        
        i=Informe(access_key, merchant_id, secret_key, 'ES')
        # new_date = datetime(2020, 6, 30, 10, 15, 00, 00000)
        #date_month = (datetime.today() - timedelta(weeks=n_weeks_ago))
        try:
            rep = i.report(report_id, start_date=start_date, end_date=end_date, marketplace=['ES'])
        except:
            rep = None
        string_rep = rep.__str__()
        if string_rep == "None":
            print("Informe vacío, prueba con otro informe o con otro rango de fechas.")
        else:
            data = [] 
            aux = string_rep.find("\\n")                                                        # variable que se usara para tratar los informes en el que los saltos de linea se hacen con \r o con \r\n

            if string_rep[aux-2:aux] == "\\r":
                new_string = string_rep.replace("\\r\\n", ";").replace("\\t", "&")              # Reemplazamos con un solo caracter para no tener fallos en la funcion split
            else:
                new_string = string_rep.replace("\\n", ";").replace("\\t", "&")   

            elements = new_string.split(sep=";")                                            # Dividimos primero por producto
            
            for e in elements:
                data.append(e.split(sep="&")) 
                                                         # Y dividimos por columna
            del data[-1]    
                                                # Borramos la ultima fila porque da problemas al hacer la conversion
            if report_id!='_GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT_': 
                matriz = np.array(data)
            else:
                matriz=data
            print(matriz)
            df_no_headers = pd.DataFrame(data = matriz)         # Creamos un primer dataframe con todos los datos
            headers = df_no_headers.iloc[0]                     # Sacamos la primera fila como titulos de columna y creamos el siguiente dataframe definitivo con esos titulos
            df_headers = pd.DataFrame(df_no_headers.values[1:], columns=headers)

            #name = report_id + ".csv"                        # Descomentar estas dos lineas si queremos que se guarde en un excel
            #df_headers.to_csv(name)
            return df_headers


    def limpieza2(self, access_key, merchant_id, secret_key, report_id, n_weeks_ago):
        if n_weeks_ago<4:
            date_month = (datetime.today() - timedelta(weeks=n_weeks_ago))
            return self.limpieza(access_key, merchant_id, secret_key, report_id, date_month.isoformat(), None)
        else:
            start_date=(datetime.today() - timedelta(weeks=1))
            end_date=datetime.today()
            df = self.limpieza(access_key, merchant_id, secret_key, report_id, start_date.isoformat(), end_date.isoformat())
            for i in range(1, n_weeks_ago):
                end_date=start_date
                start_date=(start_date - timedelta(weeks=1))
                df2=self.limpieza(access_key, merchant_id, secret_key, report_id, start_date.isoformat(), end_date.isoformat())
                df=df.append(df2, ignore_index = True)
                #df2.to_excel(str(i)+'.xlsx')
            return df




if __name__ == "__main__":
    access_key='AKIAIRF2R7EOJFNTGBEA'
    merchant_id='A2GU67S0S60AC1'
    secret_key='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'
    #seller_account = Seller(access_key, merchant_id, secret_key, 'ES', ['ES'], {})

    report_id = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_'                            #'_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_',
    n=0
    i=Informe(access_key, merchant_id, secret_key, 'ES')
    new_date = datetime(2020, 6, 30, 10, 15, 00, 00000)
    l = Limpieza()

    # Realizamos el proceso de limpieza por cada uno de los reports que creamos

    df = l.limpieza2(access_key, merchant_id, secret_key, report_id, 1)
    print(df)
    








    
""" string = re.sub(r"\b(\\t)+\b", "", i.get_reports(report_id, start_date=new_date.isoformat(), marketplace=['ES', 'IT']).__str__()).replace("\\r\\n", ";").replace("\\t", ",")
print(string) """

