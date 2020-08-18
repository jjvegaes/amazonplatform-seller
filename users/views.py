from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django import forms


# Create your views here.
from django.urls import path

from users import limpieza
from users.limpieza import Limpieza
from users.vendor import productos, customers2, ventas

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)





def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/products.html')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})



def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "products.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

def index(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "index.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

#def testingDf(request):
#    df = limpieza("_GET_MERCHANT_LISTINGS_DATA_LITE_")
#    return render(request, 'testingDf.html', {'df': df})


def testingDf(request):
    df = Limpieza("_GET_MERCHANT_LISTINGS_DATA_LITE_")
    html_table = df.to_html()
    return render(request, 'testingDf.html', {'html_table': html_table})

def graphics(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "graphics.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def customers(request):
    grap_customers = customers2()
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "customers.html", {'graficos': grap_customers})
    # En otro caso redireccionamos al login
    return redirect('/login')


def products(request):
    search_asin=None
    asins_picked=None
    if request.POST.get('edad'):
        search_asin = int(request.POST.get('edad'))
        form = yourForm(request.POST)
        asins_picked=form.cleaned_data.get('picked')
    grap_products, asins, b = productos(asin=asins_picked, search_asin=search_asin)
    form=yourForm(asins)
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "products.html", {'graficos': grap_products, 'form':form})
    # En otro caso redireccionamos al login
    return redirect('/login')



def refunds(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "refunds.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def sales(request):
    grap_sales = ventas()
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "sales.html", {'graficos': grap_sales})
    # En otro caso redireccionamos al login
    return redirect('/login')


def settings(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "settings.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def shipments(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "shipments.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def storage_fees(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "storage_fees.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

def support(request):
    return render(request, "support.html")


def reports(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "reports.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def register(request):
    return render(request, "register.html")


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/login')

from django import forms

class yourForm(forms.Form):
    def __init__(self, o):
        OPTIONS=list()
        for i in range(len(o)):
            OPTIONS.append((o[i], o[i]))
        self.options = forms.MultipleChoiceField( choices=OPTIONS, widget=forms.CheckboxSelectMultiple(),label="ASIN", required=True, error_messages={'required': 'D'})