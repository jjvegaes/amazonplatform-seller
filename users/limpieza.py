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

    def limpieza(self, access_key, merchant_id, secret_key, report_id, n_weeks_ago):
        
        i=Informe(access_key, merchant_id, secret_key, 'ES')
        # new_date = datetime(2020, 6, 30, 10, 15, 00, 00000)
        date_month = (datetime.today() - timedelta(weeks=n_weeks_ago))

        rep = i.report(report_id, start_date=date_month.isoformat(), marketplace=['ES'])
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
                data.append(e.split(sep="&"))                                               # Y dividimos por columna
            
            del data[-1]                                        # Borramos la ultima fila porque da problemas al hacer la conversion
            matriz = np.array(data)

            df_no_headers = pd.DataFrame(data = matriz)         # Creamos un primer dataframe con todos los datos
            headers = df_no_headers.iloc[0]                     # Sacamos la primera fila como titulos de columna y creamos el siguiente dataframe definitivo con esos titulos
            df_headers = pd.DataFrame(df_no_headers.values[1:], columns=headers)

            name = report_id + ".csv"                        # Descomentar estas dos lineas si queremos que se guarde en un excel
            df_headers.to_csv(name)
            return df_headers

if __name__ == "__main__":
    access_key='AKIAIRF2R7EOJFNTGBEA'
    merchant_id='A2GU67S0S60AC1'
    secret_key='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'
    seller_account = Seller(access_key, merchant_id, secret_key, 'ES', ['ES'], {})

    report_id = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_'                            #'_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_',
    n=0
    i=Informe(access_key, merchant_id, secret_key, 'ES')
    new_date = datetime(2020, 6, 30, 10, 15, 00, 00000)
    l = Limpieza()

    # Realizamos el proceso de limpieza por cada uno de los reports que creamos

    df = l.limpieza(report_id, 4)
    print(df)
    








    
""" string = re.sub(r"\b(\\t)+\b", "", i.get_reports(report_id, start_date=new_date.isoformat(), marketplace=['ES', 'IT']).__str__()).replace("\\r\\n", ";").replace("\\t", ",")
print(string) """

