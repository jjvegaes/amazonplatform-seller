from users.vendor import productos, customers2, ventas, resenas, competidores
from users.seller import productos_seller, customers_seller, ventas_seller, resenas_seller, competidores_seller

keys={'izas':{'access_key':'AKIAIRF2R7EOJFNTGBEA', 'merchant_id':'A2GU67S0S60AC1', 'secret_key':'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'}}
vendor=['miquelrius']
seller=['izas']

def get_products(vendedor, search_asin=None, search_titulo=None, n_weeks_ago=None):
    if vendedor in vendor:
        return productos(vendedor, search_asin=search_asin, search_titulo=search_titulo)
    else:
        return productos_seller(vendedor, keys[vendedor]['access_key'], keys[vendedor]['merchant_id'], keys[vendedor]['secret_key'], n_weeks_ago, search_asin=search_asin, search_titulo=search_titulo)

def get_ventas(vendedor, search_asin=None, search_titulo=None, n_weeks_ago=None):
    if vendedor in vendor:
        return ventas(vendedor, search_asin=search_asin, search_titulo=search_titulo)
    else:
        return ventas_seller(vendedor, keys[vendedor]['access_key'], keys[vendedor]['merchant_id'], keys[vendedor]['secret_key'], n_weeks_ago, search_asin=search_asin, search_titulo=search_titulo)
        

def get_customers(vendedor, search_asin=None, search_titulo=None, n_weeks_ago=None):
    if vendedor in vendor:
        return customers2(vendedor, search_asin=search_asin, search_titulo=search_titulo)
    else:
        return customers_seller(vendedor, keys[vendedor]['access_key'], keys[vendedor]['merchant_id'], keys[vendedor]['secret_key'], n_weeks_ago, search_asin=search_asin, search_titulo=search_titulo)
        

def get_competidores(vendedor, termino=None, num_items=None, marketplace=None):
    if vendedor in vendor:
        return competidores(termino, num_items, marketplace)
    else:
        return competidores_seller(termino, num_items, marketplace)
        

def get_resenas(vendedor, asin=None, num_items=None, marketplace=None):
    if vendedor in vendor:
        return resenas(asin, num_items, marketplace)
    else:
        return resenas_seller(asin, num_items, marketplace)
        
        