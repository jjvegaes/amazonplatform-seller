import mws
import time
import numpy as np
import pandas as pd
from python_dict_wrapper import wrap, unwrap
from datetime import datetime, timedelta

class Pedidos():
    def __init__(self, access_key, merchant_id, secret_key, region='ES'):
        self.marketplaces={'BR':'A2Q3Y263D00KWC', 'CA':'A2EUQ1WTGCTBG2', 'MX':'A1AM78C64UM0Y8', 'US':'ATVPDKIKX0DER', 'AE':'A2VIGQ35RCS4UG', 'DE':'A1PA6795UKMFR9', 'EG':'ARBP9OOSHTCHU', 'ES':'A1RKKUPIHCS9HS', 'FR':'A13V1IB3VIYZZH', 'UK':'A1F83G8C2ARO7P', 'IN':'A21TJRUUN4KGV', 'IT':'APJ6JRA9NG5V4', 'NL':'A1805IZSGTT6HS', 'SA':'A17E79C6D8DWNP', 'TR':'A33AVAJ2PDY3EV', 'SG':'A19VAU5U5O7RUS', 'AU':'A39IBJ37TRP1C6', 'JP':'A1VC38T7YXB528'}
        self.mws_orders = mws.Orders(access_key=access_key, secret_key=secret_key, account_id=merchant_id, region=region)
        self.region = region
        pd.set_option("display.max_rows", None, "display.max_columns", None)

    def all_orders(self):
        data = self.mws_orders.list_orders(marketplaceids=self.marketplaces[self.region], created_after = (datetime.today() - timedelta(days=3)).isoformat())
        return data.parsed['Orders']['Order']

    def into_dataframe(self):   
        # TO-DO
        # Transforma los datos obtenidos por amazon en un dataframe.

        # *********** SIN TERMINAR *************

        orders_list = self.all_orders()
        columns = orders_list[0].keys()
        data=[]
        keys = []
        for order in orders_list:
            aux = []
            for c in columns:
                try:
                    if not isinstance(order[c], str):
                        if (len(order[c].keys()) == 1):
                            aux.append(list(order[c].values())[0])
                            if c not in keys:
                                keys.append(c)
                        else:
                            for k in order[c].keys():
                                if not isinstance(order[c][k], str):
                                    if k not in keys:
                                        keys.append(k)
                                    aux.append(list(order[c][k].values())[0])
                except KeyError:
                    if c == "OrderTotal":
                        aux.append('Unknown')
                        aux.append('Unknown')
                    elif c == "ShippingAddress":
                        aux.append('Unknown')
                        aux.append('Unknown')
                        aux.append('Unknown')
                        aux.append('Unknown')
                    else:
                        aux.append('Unknown')
                    continue
            data.append(aux)

        df = pd.DataFrame(data = data, columns= keys)
        return df
        

if __name__ == "__main__":
    access_key='AKIAIRF2R7EOJFNTGBEA'
    merchant_id='A2GU67S0S60AC1'
    secret_key='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'
    pedidos = Pedidos(access_key, merchant_id, secret_key)

    df = pedidos.into_dataframe()
    print(df)