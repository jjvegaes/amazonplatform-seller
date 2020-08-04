"""mcreif URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('', views.welcome),
    path('index.html', views.welcome),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),



    path('graphics.html', views.graphics),
    path('customers.html', views.customers),
    path('products.html', views.products),
    path('refunds.html', views.refunds),
    path('reports.html', views.reports),
    path('sales.html', views.sales),
    path('settings.html', views.settings),
    path('shipments.html', views.shipments),
    path('storage_fees.html', views.storage_fees),
    path('support.html', views.support),
    path('testingDf.html', views.testingDf),




    path('admin/', admin.site.urls),
]
