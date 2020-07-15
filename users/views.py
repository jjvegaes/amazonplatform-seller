from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
from django.urls import path


def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "index.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


def graphics(request):
    return render(request, "graphics.html")


def products(request):
    return render(request, "products.html")


def customers(request):
    return render(request, "customers.html")


def refunds(request):
    return render(request, "refunds.html")


def sales(request):
    return render(request, "sales.html")


def settings(request):
    return render(request, "settings.html")


def shipments(request):
    return render(request, "shipments.html")


def storage_fees(request):
    return render(request, "storage_fees.html")


def support(request):
    return render(request, "support.html")


def reports(request):
    return render(request, "reports.html")


def register(request):
    return render(request, "register.html")

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
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/login')