import pandas as pd

#Para cada vendedor, tiene una serie de Hojas
from users.informes import Informe


class Seller():
    #Al crearse un vendedor se crean sus hojas
    def __init__(self, access_key, merchant_id, secret_key, region, marketplaces, ids_hoja):
        self.access_key=access_key
        self.merchant_id=merchant_id
        self.secret_key=secret_key
        self.region=region
        self.marketplaces=marketplaces
        self.hojas=[]
        for (key, value) in ids_hoja.items():
            self.hojas.append(Hoja(key, value))
        for h in self.hojas:
            h.create_report(None, None, self.marketplaces, self)
    
    #Para actualizar los datos de las hojas
    def update_reports(self, last_update):
        for h in self.hojas:
            h.update_report(seller=self, last_update=last_update, marketplaces=self.marketplaces)
        
#Cada hoja es un informe (con datos limpios y cruzados para represanterse en un dashboard)
class Hoja():
    def __init__(self, id_hoja, ids_informes_implicados):
        self.id_hoja=id_hoja #El id será con el nombre del dashboard al que representa
        self.ids_informes_implicados=ids_informes_implicados#Todos los informes obtenidos de mws por los que se crea la hoja (informe final con datos cruzados)

    def get_reports(self,start_date, end_date, marketplace,  seller):#Obtenemos todos los informes de mws
        i=Informe(seller.access_key, seller.merchant_id, seller.secret_key, seller.region)
        if start_date!=None:
            start_date=start_date.isoformat()
        if end_date!=None:
            end_date=end_date.isoformat()
        self.informes=i.get_reports(self.ids_informes_implicados, start_date=start_date, end_date=end_date, marketplace=marketplace)

    def get_merged_report(self):#Cruza los datos de los informes (y los limpia) para obtener el informe final(hoja)
        #llamar al script que hemos ido haciendo cada uno según el id_hoja y devolverlo
        return pd.DataFrame({'numbers': [1, 2, 3], 'colors': ['red', 'white', 'blue']})

    def save_report(self):#Guarda la hoja en un excel (en la ruta por defecto y con nombre id_hoja)
        self.informe.to_excel(self.id_hoja+'.xlsx', sheet_name=self.id_hoja)#Tenemos que mirar si hacerlo con bbdd, excel o csv.

    def update_report(self, marketplaces, seller, last_update):#Descarga de mws los nuevos datos y los añade a la hoja
        self.get_reports( start_date=last_update, marketplace=marketplaces, seller=seller)
        self.informe=pd.read_excel(self.id_hoja + '.xlsx')
        update=self.get_merged_report()
        self.informe=self.informe.append(update, ignore_index = True)
        self.save_report()

    def create_report(self, start_date, end_date, marketplaces, seller):#Crea una nueva hoja con los informes obtenidos de mws.
        self.get_reports( start_date=start_date, end_date=end_date, marketplace=marketplaces, seller=seller)
        self.informe=self.get_merged_report()
        self.save_report()
    

if __name__ == "__main__":

    access_key='AKIAIRF2R7EOJFNTGBEA'
    merchant_id='A2GU67S0S60AC1'
    secret_key='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'
    vendedor=Seller(access_key, merchant_id, secret_key, 'ES', ['ES', 'IT'], {'informe':['_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_', '_GET_SELLER_FEEDBACK_DATA_'], 'informe2':['_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_', '_GET_SELLER_FEEDBACK_DATA_']})