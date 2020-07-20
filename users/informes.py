import mws
import time
from datetime import datetime


class Informe():
    
    #Creamos el objeto tipo Reports
    def __init__(self, access_key, merchant_id, secret_key, region='ES'):
        self.amazon_mws=(mws.Reports(access_key=access_key, secret_key=secret_key, account_id=merchant_id, region=region))
        #IDs de los marketplaces disponibles para pedir informes:
        self.marketplaces={'BR':'A2Q3Y263D00KWC', 'CA':'A2EUQ1WTGCTBG2', 'MX':'A1AM78C64UM0Y8', 'US':'ATVPDKIKX0DER', 'AE':'A2VIGQ35RCS4UG', 'DE':'A1PA6795UKMFR9', 'EG':'ARBP9OOSHTCHU', 'ES':'A1RKKUPIHCS9HS', 'FR':'A13V1IB3VIYZZH', 'UK':'A1F83G8C2ARO7P', 'IN':'A21TJRUUN4KGV', 'IT':'APJ6JRA9NG5V4', 'NL':'A1805IZSGTT6HS', 'SA':'A17E79C6D8DWNP', 'TR':'A33AVAJ2PDY3EV', 'SG':'A19VAU5U5O7RUS', 'AU':'A39IBJ37TRP1C6', 'JP':'A1VC38T7YXB528'}
    
    #Devuelve un informe en concreto dados los parámetros necesarios para un informe
    def report(self, report, start_date=None, end_date=None, marketplace=None):
        marketplaces=[]
        if marketplace!=None:#Especificamos los ids de los marketplaces
            for i in range(len(marketplace)):
                marketplaces.append(self.marketplaces[marketplace[i]])
        request_id=self.amazon_mws.request_report(report_type=report, start_date=start_date, end_date=end_date, marketplaceids=marketplaces)#Pedimos el informe
        time.sleep(10)
        info=self.amazon_mws.get_report_request_list(request_id.parsed['ReportRequestInfo']['ReportRequestId']['value'])#Comprobamos su estado
        while info.parsed['ReportRequestInfo']['ReportProcessingStatus']['value']=='_SUBMITTED_' or info.parsed['ReportRequestInfo']['ReportProcessingStatus']['value']=='_IN_PROGRESS_':#Si aún se esta generando seguimos comprobando su estado
            time.sleep(45)#Tiempo mínimo de espera entre dos "get_report_request_list"
            info=self.amazon_mws.get_report_request_list(request_id.parsed['ReportRequestInfo']['ReportRequestId']['value'])
        if info.parsed['ReportRequestInfo']['ReportProcessingStatus']['value']=='_DONE_':#Si se ha completado el informe lo devolvemos
            return self.amazon_mws.get_report(info.parsed['ReportRequestInfo']['GeneratedReportId']['value']).parsed
        return None
    
    #Devuelve un diccionario de varios informes a la vez
    def get_reports(self, reports, start_date=None, end_date=None, marketplace=None):
        marketplaces=[]
        if marketplace!=None:#Especificamos los ids de los marketplaces
            for i in range(len(marketplace)):
                marketplaces.append(self.marketplaces[marketplace[i]])
        informes={}
        for rep in reports:#Obtenemos informes y los devolvemos
            informes[rep]=self.report(rep, start_date, end_date, marketplaces)
        return informes



#register=mws.Subscriptions(access_key=access_key, secret_key=secret_key, account_id=merchant_id, region=ES)
#register.register_destination(marketplace_id='A1RKKUPIHCS9HS', attributes={'sqsQueueUrl': 'url sqs'}, delivery_channel="SQS")
#register.create_subscription(marketplace_id='A1RKKUPIHCS9HS', attributes={'sqsQueueUrl': 'url sqs'}, notification_type='ReportProcessingFinished', is_enabled=True, delivery_channel="SQS")
#Crear URL sqs: https://aws.amazon.com/es/sqs/
#access_key='AKIAIRF2R7EOJFNTGBEA'
#merchant_id='A2GU67S0S60AC1'
#secret_key='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'
#report_id=['_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_']
#i=Informe(access_key, merchant_id, secret_key, 'ES')

#new_date = datetime(2020, 6, 30, 10, 15, 00, 00000)

#print(i.get_reports(report_id, start_date=new_date.isoformat(), marketplace=['ES', 'IT']))