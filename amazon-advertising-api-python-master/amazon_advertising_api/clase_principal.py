from advertising_api import AdvertisingApi
import json
import pandas as pd
import time
pd.set_option('display.max_columns', 500)


class Advertising():
    def __init__(self, client_id, client_secret, region, refresh_token):
        self.ad = AdvertisingApi(client_id, client_secret, region, refresh_token)
        self.ad._access_token = "Atza|IwEBIFdbmmUQ9nLFge3VJ_dg5zSPqf9IyyWv3Na-BFAeOYw344yw9mJ2KJzN86Ve4EaNbLTWLQMyyWm2z-2I0rNuQ8vhj74g1P58nkqUs3pU2-BUcKHkDLDD9gTuHcWwTGC_cc9zmcRxtzC0ItBaALBnbjKuF9V5IaxbUvQyKzwXIPF8c0rxUq946uRC3j0KjazLXexaFf81sIUI89eH6h91LLGVmdyB3Oq2Z8bbzfH5ynwmHnOmPCGG_X-biMeBAKJ7OFrdjrlagw_Be5nsubrPP3rJ-oHFXReCmCtUCdgCWCosB6T1WLmpLHo4M-2B50--vyv07hhU2_MIvIUsBg0BoAIJtQpSo35rnhZ93wy68H_Jy6Di8wN3O3RRTzSd6leubFzLMYUMF0dtxJSRPYRIOJwxC4VObga4S8Nomp6AxRG-KQ"
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
    refresh_token = "Atzr|IwEBIOtnNkfgRJInrjMG3ng7-FnpFW_4XQscmqLWJ7SX71lUD3bye47PgUiDSiFji8VHl5pdK7h5-5-udSYzZEFmtDcB3U8mzRIUyclebLdTrk9rErYzj6wIanmnMZQACDQXiatUUsjNdCBB08XdmhzrHIkuZ-hb6eps8uBjQKGRl-fW8aemnDJ4sytN278l3zizuEoJF4S07uu6_ekucmgUDniSlGdGNWiBb9gMl9QOHad5k3-QPzrO2n5BHBLna9nMpc0kGhfhzsPdTQvVIsB_YqPrrV7KMOWA3J6Nx-vBbLbPkZKt6dMXpitR0AZNEQczxygXjAdJcJ1nu2A6lr_AlLhuCedyhxryUkGt4SITtZrhTnFFPwTuSO6xLAUIztj11aw_q0co-APpv9WmrGov6I8HaND4A5e-fCVd43yQY_BkxoE1dXi6A8wgBzbs-cvxXBQ"
    
    ad = Advertising(client_id, client_secret, region, refresh_token= refresh_token)
    
    profile_id = 1654375404703644

    df = ad.get_informe("campaigns", profile_id)
    print(df)

    