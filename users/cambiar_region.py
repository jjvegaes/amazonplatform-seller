import numpy as np 
import pandas as pd
import pgeocode as pg
pd.options.display.max_columns = None
import os
import matplotlib.pyplot as plt
import sys

class cambiar_region():

    def __init__(self, archivo):
        self.archivo = archivo
        pass

    def accion(self):

        d_data_old = pd.read_excel(self.archivo)
        d_data_old = d_data_old.rename(columns = {"Región" : "Region"})
        codigos = []
        for i in range(1, 10):
            codigos.append("0" + str(i))
        for i in range(10, 53):
            codigos.append(str(i))

        provincias = ["Alava", "Albacete", "Alicante", "Almería", "Avila", "Badajoz", "Islas Baleares", "Barcelona", "Burgos", "Caceres", "Cadiz",
                        "Castellon", "Ciudad Real", "Cordoba", "La Coruña", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipuzcoa", "Huelva",
                        "Huesca", "Jaen", "Leon", "Lerida", "La Rioja", "Lugo", "Madrid", "Malaga", "Murcia", "Navarra", "Orense", "Asturias",
                        "Palencia", "Las Palmas", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Cantabria", "Segovia", "Sevilla", "Soria",
                        "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza", "Ceuta", "Melilla"]

        d_region = pd.DataFrame({"Codigo" : codigos, "Region" : provincias})
        d_data_old = d_data_old.astype({"Código postal": str})
        aux = d_data_old["Código postal"].apply(lambda x: x[0:2])

        nomenc = pg.Nominatim("es")

        for _, row in d_region.iterrows():
            mascara = row["Codigo"] == aux
            d_data_old["Region"].mask(mascara, row["Region"], inplace=True)

        d_data_old["Latitud"] = nomenc.query_postal_code(d_data_old["Código postal"].tolist())["latitude"]
        d_data_old["Longitud"] = nomenc.query_postal_code(d_data_old["Código postal"].tolist())["longitude"]

        d_data_old["Region"] = d_data_old.Region.str.lower()
        return d_data_old