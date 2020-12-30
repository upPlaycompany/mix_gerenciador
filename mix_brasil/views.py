import pyrebase
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import psycopg2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connections
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
import pprint

firebaseConfig = {
    'apiKey' : "AIzaSyBh-DC_fXWzzcHV6XYhFQ1Ya6MWG5OjH_w",
    'authDomain' : "mix-brasil.firebaseapp.com",
    'databaseURL': "https://mix-brasil.firebaseio.com",
    'projectId': "mix-brasil",
    'storageBucket': "mix-brasil.appspot.com",
    'messagingSenderId': "132448934641",
    'appId': "1:132448934641:web:0843ac2954464054822750",
    'measurementId': "G-VH0XXQFXES"
}

pyrebase = pyrebase.initialize_app(firebaseConfig)
auth = pyrebase.auth()

cred = credentials.Certificate("/app/mix_brasil/credencial.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def logar(request):
    next = request.GET.get('next', '/index/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
    return render(request, 'login.html', {'redirect_to': next})

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def deslogar(request):
    logout(request)
    return HttpResponseRedirect("/")



@login_required
def categoria_listagem(request):
    categorias = db.collection('categorias').stream()
    doz = [x.id for x in categorias]
    ident = db.collection('categorias').stream()
    docs = [x.to_dict() for x in ident]
    return render(request,'categoria_listagem.html', {'lista': docs, 'lista': doz})

@login_required
def lojas_listagem(request, id):
    lojas = db.collection(f'categorias/{id}/lojas').stream()
    docs = [x.to_dict() for x in lojas]
    return render(request, 'lojas_listagem.html', {'lista': docs})





