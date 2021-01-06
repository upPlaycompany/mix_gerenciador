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
def criar_loja(request, id):
    dados = db.collection(f'categorias/{id}/lojas').document()
    if request.method == 'POST':
        name = request.POST['name']
        descricao = request.POST['descricao']
        price = request.POST['price']
        destaque = 'false'
        dados.set({
            'name':f'{name}',
            'descricao':f'{descricao}',
            'price':{price},
            'destaque':f'{destaque}',
            'promocao': "",
            'img': firestore.ArrayUnion([""])
        })
        info = db.collection(f'categorias/{id}/lojas').where('name','==',f'{name}').stream()
        ff = [{'id':x.id} for x in info]
        info2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
        gg = [x.to_dict() for x in info2]
        a = len(ff)
        categoria = {'categoria': f'{id}'}
        [ff[x].update(gg[x]) for x in range(a)]
        [ff[x].update(categoria) for x in range(a)]
        for n in ff:
            des = db.collection('destaques_home').document()
            des.set({
                'cid':f"{n['categoria']}",
                'cupons': firestore.ArrayUnion([""]),
                'img': firestore.ArrauUnion([""]),
                'lid': f"{n['id']}",
                'name':f"{n['name']}",
                'ofertas': firestore.ArrayUnion([""]),
                'ofertas_destaque': firestore.ArrayUnion([""]),
                'price': f"{n['price']}"
            })
        return redirect('criar_loja_sucesso')
    return render(request, 'criar_loja.html')

@login_required
def criar_loja_sucesso(request):
    return render(request,'criar_loja_sucesso.html')


@login_required
def categoria_listagem(request):
    categorias = db.collection('categorias').stream()
    doz = [x.id for x in categorias]
    ident = db.collection('categorias').stream()
    docs = [x.to_dict() for x in ident]
    return render(request, 'categoria_listagem.html', {'lista': docs, 'lista_id': doz})

@login_required
def lojas_listagem(request, id):
    lojas = db.collection(f'categorias/{id}/lojas').stream()
    docs = [{'id':x.id} for x in lojas]
    lojas2 = db.collection(f'categorias/{id}/lojas').stream()
    docs2 = [y.to_dict() for y in lojas2]
    a = len(docs)
    categoria = {'categoria':f'{id}'}
    [docs[x].update(docs2[x]) for x in range(a)]
    [docs[x].update(categoria) for x in range(a)]
    return render(request, 'lojas_listagem.html', {'lista': docs})

@login_required
def lojas_dados(request, id, nome, cod):
    dados = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    abc = [x.to_dict() for x in dados]
    dados2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    dec = [{'id':x.id} for x in dados2]
    a = len(dec)
    categoria = {'categoria': f'{id}'}
    [dec[x].update(abc[x]) for x in range(a)]
    [dec[x].update(categoria) for x in range(a)]
    if request.method == 'POST':
        name = request.POST['name']
        descricao = request.POST['descricao']
        price = request.POST['price']
        destaque = request.POST['destaque']
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        att = formform.update(
            {
                'name':f'{name}',
                'descricao':f'{descricao}',
                'price':f'{price}',
                'destaque':f'{destaque}'
            }
        )
        return redirect('atualizar_loja_sucesso')
    return render(request,'lojas_dados.html', {'lista':dec})

@login_required
def atualizar_loja_sucesso(request):
    return render(request, 'atualizar_loja_sucesso.html')

@login_required
def adicionar_imagens_loja(request, id, cod):
    if request.method == 'POST':
        img = request.POST['img']
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        att = formform.update({
            'img': firestore.ArrayUnion([f'{img}'])
        })
        return redirect('adicionar_imagens_loja_sucesso')
    return render(request, 'adicionar_imagens_loja.html')

@login_required
def adicionar_imagens_loja_sucesso(request):
    return render(request, 'adicionar_imagens_loja_sucesso.html')

@login_required
def remover_imagens_loja(request, id, name, cod):
    dados = db.collection(f'categorias/{id}/lojas').where('name','==',f'{name}').stream()
    docs = [x.to_dict() for x in dados]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        att = formform.update({
            'img':firestore.ArrayRemove([f'{imagem}'])
        })
        return redirect('remover_imagens_loja_sucesso')
    return render(request, 'remover_imagens_loja.html', {'lista': docs})

@login_required
def remover_imagens_loja_sucesso(request):
    return render(request, 'remover_imagens_loja_sucesso.html')

@login_required
def remover_loja(request, id, cod):
    if request.method == 'POST':
        dados = db.collection(f'categorias/{id}/lojas').document(f'{cod}').delete()
        return redirect('remover_loja_sucesso')
    return render(request,'remover_loja.html')

@login_required
def remover_loja_sucesso(request):
    return render(request,'remover_loja_sucesso.html')

