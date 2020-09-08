from advertising_api import AdvertisingApi
import json
import pandas as pd
import time
pd.set_option('display.max_columns', 500)


class Advertising():
    def __init__(self, client_id, client_secret, region, refresh_token):
        self.ad = AdvertisingApi(client_id, client_secret, region, refresh_token)
        self.ad._access_token = "Atza|IwEBIE-wYRMTKKsO3Dql7twOsDnLRZZyL8K8IW0_ASAQCg53dAcYCjSdFkbO7qL7jDdRumt79ii5Q84Uw8rtGyAXviPW2NV8bA6t4M-cXQcGAFQF6Bd430GnFoN_bajJzdwaFUkhF9-q75kwS6-sneLaU7blnfqwLWvAMPgt4tEpljOoBJhnuMDlw-xsb98TW6-RJLOwgjAB-VZ_TSUi1r6Qrg77WFU66S0L75l4Y8LKVRn8fw6xnrrH6eN9B5znMqQeSzqlKVuckp8nYjSsNWoGvAUwoxcepy93rQVXQYW410fZbQhO0rfnVz6W22ta803anshM7VgP4Fs2Zly_jtC5wTk5IkZCO4xd84UVtbq1qhAEZMJkNjnJfk3NjPZDuf308_2BpqeRGgodfxvs2mwIqSu8X-wVeVYGSAli2htgC8HRz36GVYn7aPr1RguxySMmq9sCBjrQligbkPtCKHSYSIm9DH0lBKMNyQn0tBZbFnOJJqskDITPdp2BMUhv3Qby2tc"
        self.ad.do_refresh_token()

    def df_all_campaigns(self):
        df_dict = {}
        json_data = json.loads(self.ad.get_profiles()['response'])

        for prof in json_data:
            self.ad.profile_id=prof["profileId"]
            if self.ad.list_campaigns()['response'] != "[]":
                df = pd.read_json(self.ad.list_campaigns()['response'])
                columns = df['bidding'].tolist()
                columns = str(columns).replace("\'", "\"")
                df_columns = pd.read_json(str(columns))
                df.drop(['bidding'], axis ='columns', inplace = True)
                df = pd.concat([df, df_columns], axis = 1)
                df_dict.setdefault(self.ad.profile_id , df)
        return df_dict

    def crear_campaña(self, profile_id, name, campaignType, targetingType, state, dailyBudget, startDate):
        self.ad.profile_id = profile_id
        self.ad.do_refresh_token()
        dicc = {"name" : name, "campaignType" : campaignType, "targetingType" : targetingType, "state" : state, "dailyBudget" : dailyBudget, "startDate" : startDate}
        list_campaigns = []
        list_campaigns.append(dicc)
        resp = self.ad.create_campaigns(list_campaigns)
        return resp
    
    def habilitar_campaña(self, profile_id, campaignId, state = False):
        self.ad.profile_id = profile_id
        list_campaigns = []
        if state:
            dicc = {"campaignId" : campaignId, "state" : "enabled"}
        else:
            dicc = {"campaignId" : campaignId, "state" : "paused"}

        list_campaigns.append(dicc)
        resp = self.ad.update_campaigns(list_campaigns)
        return resp

    def get_campañas_perfil(self, profile_id):
        self.ad.profile_id = profile_id
        if self.ad.list_campaigns()['response'] != "[]":
            df = pd.read_json(self.ad.list_campaigns()['response'])
            columns = df['bidding'].tolist()
            columns = str(columns).replace("\'", "\"")
            df_columns = pd.read_json(str(columns))
            df.drop(['bidding'], axis ='columns', inplace = True)
            df = pd.concat([df, df_columns], axis = 1)
        return df

    def get_perfiles(self):
        if self.ad.get_profiles()['response'] != "[]":
            json_data = json.loads(self.ad.get_profiles()['response'])
            df_result = pd.DataFrame(columns = list(json_data[0].keys()))

            df = pd.read_json(self.ad.get_profiles()['response'])
            columns = df['accountInfo'].tolist()
            columns = str(columns).replace("\'", "\"")
            df_columns = pd.read_json(str(columns))
            df.drop(['accountInfo'], axis ='columns', inplace = True)
            df = pd.concat([df, df_columns], axis = 1)
            df_result = pd.concat([df_result, df])
            
            return df_result
        else: 
            return "[]"

    def get_informe(self, typeInforme, profile_id):
        self.ad.profile_id = profile_id
        dicc_aux = {"campaignType" : "sponsoredProducts", "segment" : "placement", "reportDate" : "20200826", "metrics" : "campaignName,impressions,cost,attributedSales30d,clicks"}
        resp = self.ad.request_report(record_type=typeInforme, data=dicc_aux)
        print(resp)

        time.sleep(5)
        if resp['code'] == 202:
            json_data = json.loads(resp['response'])
            informe = ad.ad.get_report(report_id=json_data["reportId"])
        else:
            return resp

        df_bueno = pd.read_json(str(informe['response']).replace("\'", "\""))

        return df_bueno



if __name__ == "__main__":
    client_id = "amzn1.application-oa2-client.a8fd6816f08d46569dfd2362198fc4d1"
    client_secret = "a743f8e758089168f35bfbc5bc3399567ae8e8e95dbeddc5fc17ecf7de2532de"
    region = 'eu'
    refresh_token = "Atzr|IwEBIO5zIbn3reyXTkV3daVaXVPbS4pqUQt5xiDIyZglZY4ejAmwwpXP241favZsccPoEdUugEKQIOANngXwLrRWWKlbHB9hr7CYdtouEWHbezcobKIW6UnvA4x-Sjz5LsCMq4LZEMgwWNpsuLYN5ztFrTkttJK5Dz8tCpvQKhYK3KEqMvOJtDdWd04pD87BLxdda-ChGK4H8qxTOXKAcsL7SceyCAG2B4wU4_uUMdflxv-GQgm5ho8NwYk841KaoyybfjAFGMmJ3pUkemmaUUhCAXPGt3xu8_EdCns7NHAK-cJvt5hcf301mBx-DghHrNW6pgaHBxzeTDzl2ufxhZVfRgm70eJmsKyMvEuyzvFM8hL6e5RRqmc9fjkuEuoKeQ5cuIrCs8vG_tSKiAMJY9viX3UGjAttFR1gFxRviDtq1SoVbEvSxN-GVS8GXmRx_ZBKGL77P1o9lMO29G9BC1uKhgYUVMiOeE1peF_1YofJg1qmYiyFw3LT6Cp2lij1F7Q8J08"
    
    ad = Advertising(client_id, client_secret, region, refresh_token= refresh_token)
    
    profile_id = 1654375404703644

    df = ad.get_informe("campaigns", profile_id)
    print(df)

    