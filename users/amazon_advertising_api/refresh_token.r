library(httr)

headers = c( ContentType = 'application/x-www-form-urlencoded;charset=UTF-8')

data = list( grant_type= 'authorization_code', code= 'ANPdSFgGQojtSJxzXaPC', redirect_uri= 'http://localhost', client_id= 'amzn1.application-oa2-client.a8fd6816f08d46569dfd2362198fc4d1', client_secret= 'a743f8e758089168f35bfbc5bc3399567ae8e8e95dbeddc5fc17ecf7de2532de' )

response = POST(url = 'https://api.amazon.com/auth/o2/token', add_headers(.headers=headers), body = data , encode = "form")

content(response)$access_token

content(response)$refresh_token