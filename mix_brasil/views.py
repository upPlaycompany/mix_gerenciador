import pyrebase
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
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

cred = credentials.Certificate("/app/mix_brasil/credencial.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
sto = storage.bucket('mix-brasil.appspot.com')


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
        destaque = request.POST['destaque']
        if destaque == 'true':
            dex = True
        else:
            dex = False
        price = float(price)
        dados.set({
            'name': f'{name}',
            'descricao': f'{descricao}',
            'price': price,
            'destaque': dex,
            'promocao': "",
            'img': firestore.ArrayUnion([""])
        })
        info = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
        ff = [{'id': x.id} for x in info]
        info2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
        gg = [x.to_dict() for x in info2]
        a = len(ff)
        categoria = {'categoria': f'{id}'}
        [ff[x].update(gg[x]) for x in range(a)]
        [ff[x].update(categoria) for x in range(a)]
        for n in ff:
            if destaque == 'true':
                des = db.collection('destaques_home').document()
                des.set({
                    'cid': f"{n['categoria']}",
                    'cupons': firestore.ArrayUnion([""]),
                    'img': firestore.ArrayUnion([""]),
                    'lid': f"{n['id']}",
                    'name': f"{n['name']}",
                    'ofertas': firestore.ArrayUnion([""]),
                    'ofertas_destaque': firestore.ArrayUnion([""]),
                    'price': n['price']
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
    docs = [{'id': x.id} for x in lojas]
    lojas2 = db.collection(f'categorias/{id}/lojas').stream()
    docs2 = [y.to_dict() for y in lojas2]
    a = len(docs)
    dzz = [{'categoria': f'{id}'}]
    categoria = {'categoria': f'{id}'}
    [docs[x].update(docs2[x]) for x in range(a)]
    [docs[x].update(categoria) for x in range(a)]
    return render(request, 'lojas_listagem.html', {'lista': docs, 'order': dzz})

@login_required
def lojas_dados(request, id, nome, cod):
    dados = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    abc = [x.to_dict() for x in dados]
    dados2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    dec = [{'id': x.id} for x in dados2]
    a = len(dec)
    categoria = {'categoria': f'{id}'}
    [dec[x].update(abc[x]) for x in range(a)]
    [dec[x].update(categoria) for x in range(a)]
    if request.method == 'POST':
        name = request.POST['name']
        descricao = request.POST['descricao']
        price = request.POST['price']
        destaque = request.POST['destaque']
        promocao = request.POST['promocao']
        price = float(price)
        if destaque == 'true':
            des = True
        else:
            des = False
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')

        formform.update(
            {
                'name':f'{name}',
                'descricao': f'{descricao}',
                'price': price,
                'destaque': des,
                'promocao': f'{promocao}'
            }
        )
        if des == True:
            desdes = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            categoria = {'categoria': f'{id}'}
            [da[x].update(dw[x]) for x in range(a)]
            [da[x].update(categoria) for x in range(a)]
            didi = db.collection('destaques_home').document()
            for n in da:
                didi.set({
                    'cid': f"{n['categoria']}",
                    'cupons': firestore.ArrayUnion([""]),
                    'img': firestore.ArrayUnion([""]),
                    'lid': f"{n['id']}",
                    'name': f"{n['name']}",
                    'ofertas': firestore.ArrayUnion([""]),
                    'ofertas_destaque': firestore.ArrayUnion([""]),
                    'price': n['price']
                })
        elif des == False:
            desdes = db.collection(f'destaques_home').where('lid', '==', f'{cod}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'destaques_home').where('lid', '==', f'{cod}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            [da[x].update(dw[x]) for x in range(a)]
            for n in da:
                db.collection('destaques_home').document(f"{n['id']}").delete()
        return redirect('atualizar_loja_sucesso')
    return render(request,'lojas_dados.html', {'lista':dec})

@login_required
def atualizar_loja_sucesso(request):
    return render(request, 'atualizar_loja_sucesso.html')

@login_required
def adicionar_imagens_loja(request, id, cod):
    if request.method == 'POST':
        img = request.POST['img']
        arquivo = sto.blob(img)
        arquivo.upload_from_filename(img)
        url = arquivo.generate_signed_url(
            version="v0", method="GET",
        )
        url = str(url)
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        formform.update({
            'img': firestore.ArrayUnion([f'{url}'])
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
        formform.update({
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
        db.collection(f'categorias/{id}/lojas').document(f'{cod}').delete()
        return redirect('remover_loja_sucesso')
    return render(request,'remover_loja.html')

@login_required
def remover_loja_sucesso(request):
    return render(request,'remover_loja_sucesso.html')

