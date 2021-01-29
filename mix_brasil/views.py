import pyrebase
import os
import datetime
import requests
from .models import *
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from firebase_admin import auth
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
    next_user = request.GET.get('next_user', '/user_index/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        options = request.POST['options']
        user = authenticate(username=username, password=password)
        if options == 'admin' and user.is_superuser == True and user.is_staff == True:
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next)
        elif options == 'user' and user.is_superuser == False and user.is_staff == False:
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_user)
        else:
            return redirect('login_erro')
    return render(request, 'login.html', {'redirect_to': next})


def login_erro(request):
    return render(request, 'login_erro.html')

@login_required
def index(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'index.html')

@login_required
def user_index(request):
    if request.user.is_superuser == True or request.user.is_staff == True:
        return redirect('index')
    return render(request, 'user_index.html')


@login_required
def deslogar(request):
    logout(request)
    return HttpResponseRedirect("/")

def criar_usuario(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cep = request.POST['cep']
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
        link = requests.get(url, headers=headers, verify=False)
        cde = link.json()
        auth.create_user(
                email=f'{email}', password=f'{password}')
        ussu = auth.get_user_by_email(f'{email}')
        dados = db.collection('users').document(ussu.uid)
        dados.set({
            'name': f'{name}',
            'phone': f'{phone}',
            'email': f'{email}',
            'img': None,
            'address': {
                'city': f"{cde['cidade']['nome']}",
                'district': f"{cde['bairro']}",
                'lat': f"{cde['latitude']}",
                'long': f"{cde['longitude']}",
                'state': f"{cde['estado']['sigla']}",
                'street': f"{cde['logradouro']}",
                'zipCode': f"{cde['cep']}"
            }

        })
        user = User.objects.create_user(username, email, password)
        user.first_name = name
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return redirect('criar_usuario_sucesso')
    return render(request, 'criar_usuario.html')

def criar_usuario_sucesso(request):
    return render(request, 'criar_usuario_sucesso.html')

@login_required
def usuario_listagem(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    usuarios = db.collection('users').stream()
    doz = [x.id for x in usuarios]
    ident = db.collection('users').stream()
    docs = [x.to_dict() for x in ident]
    return render(request, 'usuario_listagem.html', {'lista': docs, 'lista_id': doz})

@login_required
def usuario_dados(request, id):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    cep = request.GET.get("cep")
    url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
    headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
    link = requests.get(url, headers=headers, verify=False)
    cde = link.json()
    dados = db.collection(f'users').document(f'{id}')
    dad = dados.get()
    abc = dad.to_dict()
    ident = {'id': f'{id}'}
    abc.update(ident)
    abc.update(cde)
    abc = [abc]
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        city = request.POST['city']
        district = request.POST['district']
        lat = request.POST['lat']
        long = request.POST['long']
        state = request.POST['state']
        street = request.POST['street']
        zipCode = request.POST['zipCode']
        formform = db.collection(f'users').document(f'{id}')
        formform.update(
            {
                'name': f'{name}',
                'phone': f"{phone}",
                'email': f'{email}',
                'address': {
                    'city': f"{city}",
                    'district': f"{district}",
                    'lat': f"{lat}",
                    'long': f"{long}",
                    'state': f"{state}",
                    'street': f"{street}",
                    'zipCode': f"{zipCode}"
                }
            }
        )
        return redirect('atualizar_usuario_sucesso')
    return render(request, 'usuario_dados.html', {'lista': abc})


@login_required
def atualizar_usuario_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'atualizar_usuario_sucesso.html')

@login_required
def remover_usuario(request, id, e):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        user = User.objects.get(email=e)
        user.delete()
        db.collection(f'users').document(f'{id}').delete()
        auth.delete_user(uid=id)
        return redirect('remover_usuario_sucesso')
    return render(request, 'remover_usuario.html')

@login_required
def remover_usuario_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'remover_usuario_sucesso.html')

@login_required
def adicionar_imagem_perfil(request, id):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        arquivo = sto.blob(f'userImg/{id}/{img}')
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        formform = db.collection(f'users').document(f'{id}')
        formform.update({
            'img': url
        })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('adicionar_imagem_perfil_sucesso')
    return render(request, 'adicionar_imagem_perfil.html')

@login_required
def criar_loja(request, id):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        name = request.POST['name']
        whatsapp = request.POST['whatsapp']
        trabalhe_conosco = request.POST['trabalhe_conosco']
        price = request.POST['price']
        destaque = request.POST['destaque']
        cep = request.POST['cep']
        if destaque == 'true':
            dex = True
        else:
            dex = False
        price = price.replace(',', '.')
        price = float(price)
        dados = db.collection(f'categorias/{id}/lojas').document()
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
        link = requests.get(url, headers=headers, verify=False)
        cde = link.json()
        dados.set({
            'name': f'{name}',
            'whatsapp': f'{whatsapp}',
            'trabalhe_conosco': f'{trabalhe_conosco}',
            'price': price,
            'destaque': dex,
            'promocao': "",
            'img': firestore.ArrayUnion([""]),
            'img_destacados': firestore.ArrayUnion([""]),
            'img_ofertas': firestore.ArrayUnion([""]),
            'img_cupons': firestore.ArrayUnion([""]),
            'cidade': f"{cde['cidade']['nome']}",
            'estado': f"{cde['estado']['sigla']}",
        })
        info = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
        ff = [{'id': x.id} for x in info]
        info2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
        gg = [x.to_dict() for x in info2]
        a = len(ff)
        categoria = {'categoria': f'{id}'}
        [ff[x].update(gg[x]) for x in range(a)]
        [ff[x].update(categoria) for x in range(a)]
        [ff[x].update(cde) for x in range(a)]
        for n in ff:
            if destaque == 'true':
                des = db.collection('destaque_home').document()
                des.set({
                    'cid': f"{n['categoria']}",
                    'cupons': firestore.ArrayUnion([""]),
                    'img': firestore.ArrayUnion([""]),
                    'lid': f"{n['id']}",
                    'name': f"{n['name']}",
                    'ofertas': firestore.ArrayUnion([""]),
                    'ofertas_destaque': firestore.ArrayUnion([""]),
                    'price': n['price'],
                    'cidade': f"{n['cidade']['nome']}",
                    'estado': f"{n['estado']['sigla']}"
                })
        return redirect('criar_loja_sucesso')
    return render(request, 'criar_loja.html')

@login_required
def criar_loja_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'criar_loja_sucesso.html')

@login_required
def categoria_listagem(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    categorias = db.collection('categorias').stream()
    doz = [x.id for x in categorias]
    ident = db.collection('categorias').stream()
    docs = [x.to_dict() for x in ident]
    return render(request, 'categoria_listagem.html', {'lista': docs, 'lista_id': doz})

@login_required
def lojas_listagem(request, id):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
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
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    cep = request.GET.get("cep")
    url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
    headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
    link = requests.get(url, headers=headers, verify=False)
    cde = link.json()
    dados = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    abc = [x.to_dict() for x in dados]
    dados2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    dec = [{'id': x.id} for x in dados2]
    a = len(dec)
    categoria = {'categoria': f'{id}'}
    [dec[x].update(abc[x]) for x in range(a)]
    [dec[x].update(categoria) for x in range(a)]
    [dec[x].update(cde) for x in range(a)]
    if request.method == 'POST':
        name = request.POST['name']
        whatsapp = request.POST['whatsapp']
        trabalhe_conosco = request.POST['trabalhe_conosco']
        price = request.POST['price']
        destaque = request.POST['destaque']
        promocao = request.POST['promocao']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        price = price.replace(',', '.')
        price = float(price)
        if destaque == 'true':
            des = True
        else:
            des = False
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        formform.update(
            {
                'name': f'{name}',
                'whatsapp': f'{whatsapp}',
                'trabalhe_conosco': f'{trabalhe_conosco}',
                'price': price,
                'destaque': des,
                'promocao': f'{promocao}',
                'cidade': f'{cidade}',
                'estado': f'{estado}'
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
            [da[x].update(cde) for x in range(a)]
            didi = db.collection('destaque_home').document()
            for n in da:
                didi.set({
                    'cid': f"{n['categoria']}",
                    'cupons': firestore.ArrayUnion([""]),
                    'img': firestore.ArrayUnion([""]),
                    'lid': f"{n['id']}",
                    'name': f"{n['name']}",
                    'ofertas': firestore.ArrayUnion([""]),
                    'ofertas_destaque': firestore.ArrayUnion([""]),
                    'price': n['price'],
                    'cidade': n['cidade']['nome'],
                    'estado': n['estado']['sigla']
                })
        elif des == False:
            desdes = db.collection(f'destaque_home').where('lid', '==', f'{cod}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'destaque_home').where('lid', '==', f'{cod}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            [da[x].update(dw[x]) for x in range(a)]
            for n in da:
                db.collection('destaque_home').document(f"{n['id']}").delete()
        else:
            desdes = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            categoria = {'categoria': f'{id}'}
            [da[x].update(dw[x]) for x in range(a)]
            [da[x].update(categoria) for x in range(a)]
            [da[x].update(cde[x]) for x in range(a)]
        return redirect('atualizar_loja_sucesso')
    return render(request, 'lojas_dados.html', {'lista': dec})

@login_required
def atualizar_loja_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'atualizar_loja_sucesso.html')

@login_required
def adicionar_imagens_loja(request, id, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        arquivo = sto.blob(f'categorias/{id}/{cod}/{img}')
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        formform.update({
            'img': firestore.ArrayUnion([f'{url}'])
        })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('adicionar_imagens_loja_sucesso')
    return render(request, 'adicionar_imagens_loja.html')

@login_required
def adicionar_imagens_loja_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'adicionar_imagens_loja_sucesso.html')

@login_required
def remover_imagens_loja(request, id, name, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    dados = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
    docs = [x.to_dict() for x in dados]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        formform.update({
            'img': firestore.ArrayRemove([f'{imagem}'])
        })
        return redirect('remover_imagens_loja_sucesso')
    return render(request, 'remover_imagens_loja.html', {'lista': docs})

@login_required
def remover_imagens_loja_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'remover_imagens_loja_sucesso.html')

@login_required
def remover_loja(request, id, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        db.collection(f'categorias/{id}/lojas').document(f'{cod}').delete()
        db.collection('destaque_home').where('lid', '==', f'{cod}').delete()
        return redirect('remover_loja_sucesso')
    return render(request, 'remover_loja.html')

@login_required
def remover_loja_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'remover_loja_sucesso.html')

@login_required
def criar_desapego(request, id):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        anunciante = request.POST['anunciante']
        descricao = request.POST['descricao']
        name = request.POST['name']
        number = request.POST['number']
        price = request.POST['price']
        promocao = request.POST['promocao']
        destaque = request.POST['destaque']
        cep = request.POST['cep']
        if destaque == 'true':
            dex = True
        else:
            dex = False
        price = price.replace(',', '.')
        price = float(price)
        count = db.collection(f'desapego/{id}/desapegos').stream()
        xxx = len([x.id for x in count])
        dados = db.collection(f'desapego/{id}/desapegos').document()
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
        link = requests.get(url, headers=headers, verify=False)
        cde = link.json()
        dados.set({
            'anunciante': f'{anunciante}',
            'descricao': f'{descricao}',
            'name': f'{name}',
            'number': f'{number}',
            'price': price,
            'promocao': f'{promocao}',
            'destaque': dex,
            'cidade': f"{cde['cidade']['nome']}",
            'estado': f"{cde['estado']['sigla']}",
            'pos': int(xxx + 1),
            'img': firestore.ArrayUnion([""])
        })
        info = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
        ff = [{'id': x.id} for x in info]
        info2 = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
        gg = [x.to_dict() for x in info2]
        a = len(ff)
        categoria = {'categoria': f'{id}'}
        [ff[x].update(gg[x]) for x in range(a)]
        [ff[x].update(categoria) for x in range(a)]
        [ff[x].update(cde) for x in range(a)]
        for n in ff:
            if destaque == 'true':
                des = db.collection('destaque_desapego').document()
                des.set({
                    'cid': f"{n['categoria']}",
                    'img': firestore.ArrayUnion([""]),
                    'did': f"{n['id']}",
                    'name': f"{n['name']}",
                    'price': n['price'],
                    'number': f"{n['number']}",
                    'cidade': f"{n['cidade']['nome']}",
                    'estado': f"{n['estado']['sigla']}",
                })
        return redirect('criar_loja_sucesso')
    return render(request, 'criar_desapego.html')

@login_required
def criar_desapego_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'criar_desapego_sucesso.html')

@login_required
def categoria_desapego_listagem(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    desapegos = db.collection('desapego').stream()
    doz = [x.id for x in desapegos]
    ident = db.collection('desapego').stream()
    docs = [x.to_dict() for x in ident]
    return render(request, 'categoria_desapego_listagem.html', {'lista': docs, 'lista_id': doz})

@login_required
def desapegos_listagem(request, id):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    desapegos = db.collection(f'desapego/{id}/desapegos').stream()
    docs = [{'id': x.id} for x in desapegos]
    lojas2 = db.collection(f'desapego/{id}/desapegos').stream()
    docs2 = [y.to_dict() for y in lojas2]
    a = len(docs)
    dzz = [{'categoria': f'{id}'}]
    categoria = {'categoria': f'{id}'}
    [docs[x].update(docs2[x]) for x in range(a)]
    [docs[x].update(categoria) for x in range(a)]
    return render(request, 'desapegos_listagem.html', {'lista': docs, 'order': dzz})

@login_required
def desapegos_dados(request, id, nome, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    cep = request.GET.get("cep")
    url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
    headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
    link = requests.get(url, headers=headers, verify=False)
    cde = link.json()
    dados = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{nome}').stream()
    abc = [x.to_dict() for x in dados]
    dados2 = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{nome}').stream()
    dec = [{'id': x.id} for x in dados2]
    a = len(dec)
    categoria = {'categoria': f'{id}'}
    [dec[x].update(abc[x]) for x in range(a)]
    [dec[x].update(categoria) for x in range(a)]
    [dec[x].update(cde) for x in range(a)]
    if request.method == 'POST':
        name = request.POST['name']
        descricao = request.POST['descricao']
        price = request.POST['price']
        destaque = request.POST['destaque']
        promocao = request.POST['promocao']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        anunciante = request.POST['estado']
        number = request.POST['number']
        price = price.replace(',', '.')
        price = float(price)
        if destaque == 'true':
            des = True
        else:
            des = False
        formform = db.collection(f'desapego/{id}/desapegos').document(f'{cod}')
        formform.update(
            {
                'name': f'{name}',
                'descricao': f'{descricao}',
                'price': price,
                'destaque': des,
                'promocao': f'{promocao}',
                'cidade': f'{cidade}',
                'estado': f'{estado}',
                'anunciante': f'{anunciante}',
                'number': f'{number}'
            }
        )
        if des == True:
            desdes = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            categoria = {'categoria': f'{id}'}
            [da[x].update(dw[x]) for x in range(a)]
            [da[x].update(categoria) for x in range(a)]
            [da[x].update(cde) for x in range(a)]
            didi = db.collection('destaque_desapego').document()
            for n in da:
                didi.set({
                    'cid': f"{n['categoria']}",
                    'img': firestore.ArrayUnion([""]),
                    'did': f"{n['id']}",
                    'name': f"{n['name']}",
                    'price': n['price'],
                    'cidade': n['cidade']['nome'],
                    'estado': n['estado']['sigla'],
                    'anunciante': f"{n['anunciante']}",
                    'number': f"{n['number']}"
                })
        elif des == False:
            desdes = db.collection(f'destaque_desapego').where('lid', '==', f'{cod}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'destaque_desapego').where('lid', '==', f'{cod}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            [da[x].update(dw[x]) for x in range(a)]
            for n in da:
                db.collection('destaque_desapego').document(f"{n['id']}").delete()
        else:
            desdes = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            categoria = {'categoria': f'{id}'}
            [da[x].update(dw[x]) for x in range(a)]
            [da[x].update(categoria) for x in range(a)]
            [da[x].update(cde[x]) for x in range(a)]
        return redirect('atualizar_desapego_sucesso')
    return render(request, 'desapegos_dados.html', {'lista': dec})

@login_required
def atualizar_desapego_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'atualizar_desapego_sucesso.html')

@login_required
def adicionar_imagens_desapego(request, id, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        arquivo = sto.blob(f'desapego/{id}/{cod}/{img}')
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        formform = db.collection(f'desapego/{id}/desapegos').document(f'{cod}')
        formform.update({
            'img': firestore.ArrayUnion([f'{url}'])
        })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('adicionar_imagens_desapego_sucesso')
    return render(request, 'adicionar_imagens_desapego.html')


@login_required
def adicionar_imagens_desapego_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'adicionar_imagens_desapego_sucesso.html')

@login_required
def remover_imagens_desapego(request, id, name, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    dados = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
    docs = [x.to_dict() for x in dados]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        formform = db.collection(f'desapego/{id}/desapegos').document(f'{cod}')
        formform.update({
            'img': firestore.ArrayRemove([f'{imagem}'])
        })
        return redirect('remover_imagens_desapego_sucesso')
    return render(request, 'remover_imagens_desapego.html', {'lista': docs})

@login_required
def remover_imagens_desapego_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'remover_imagens_desapego_sucesso.html')

@login_required
def remover_desapego(request, id, cod):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    if request.method == 'POST':
        db.collection(f'desapego/{id}/desapegos').document(f'{cod}').delete()
        db.collection('destaque_desapego').where('did', '==', f'{cod}').delete()
        return redirect('remover_desapego_sucesso')
    return render(request, 'remover_desapego.html')

@login_required
def remover_desapego_sucesso(request):
    if request.user.is_superuser == False or request.user.is_staff == False:
        return redirect('user_index')
    return render(request, 'remover_desapego_sucesso.html')


#PARTE DE USUARIO
@login_required
def user_criar_loja(request):
    if request.user.is_superuser == True or request.user.is_staff == True:
        return redirect('index')
    if request.method == 'POST':
        email = request.user.email
        name = request.POST['name']
        categoria = request.POST['categoria']
        whatsapp = request.POST['whatsapp']
        trabalhe_conosco = request.POST['trabalhe_conosco']
        price = request.POST['price']
        cep = request.POST['cep']
        dex = False
        price = price.replace(',', '.')
        price = float(price)
        dados = db.collection(f'categorias/{categoria}/lojas').document()
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
        link = requests.get(url, headers=headers, verify=False)
        cde = link.json()
        dados.set({
            'name': f'{name}',
            'categoria': f'{categoria}',
            'whatsapp': f'{whatsapp}',
            'trabalhe_conosco': f'{trabalhe_conosco}',
            'price': price,
            'destaque': dex,
            'promocao': "",
            'img': firestore.ArrayUnion([""]),
            'img_destacados': firestore.ArrayUnion([""]),
            'img_ofertas': firestore.ArrayUnion([""]),
            'img_cupons': firestore.ArrayUnion([""]),
            'cidade': f"{cde['cidade']['nome']}",
            'estado': f"{cde['estado']['sigla']}",
            'uemail': f"{email}"
        })
        info = db.collection(f'categorias/{categoria}/lojas').where('name', '==', f'{name}').stream()
        ff = [{'id': x.id} for x in info]
        info2 = db.collection(f'categorias/{categoria}/lojas').where('name', '==', f'{name}').stream()
        gg = [x.to_dict() for x in info2]
        a = len(ff)
        category = {'categoria': f'{categoria}'}
        [ff[x].update(gg[x]) for x in range(a)]
        [ff[x].update(category) for x in range(a)]
        [ff[x].update(cde) for x in range(a)]
        des = db.collection(f'users').where('email','==',f'{email}').stream()
        pka = [{'id': x.id} for x in des]
        for y in pka:
            fad = db.collection(f"users/{y['id']}/loja").document(f"{y['id']}")
            fad.set({
                    'name': f'{name}',
                    'categoria': f'{categoria}',
                    'whatsapp': f'{whatsapp}',
                    'trabalhe_conosco': f'{trabalhe_conosco}',
                    'price': price,
                    'destaque': dex,
                    'promocao': "",
                    'img': firestore.ArrayUnion([""]),
                    'img_destacados': firestore.ArrayUnion([""]),
                    'img_ofertas': firestore.ArrayUnion([""]),
                    'img_cupons': firestore.ArrayUnion([""]),
                    'cidade': f"{cde['cidade']['nome']}",
                    'estado': f"{cde['estado']['sigla']}",
                    'uemail': f"{email}"
            })
        return redirect('user_criar_loja_sucesso')
    return render(request, 'user_criar_loja.html')

@login_required
def user_criar_loja_sucesso(request):
    if request.user.is_superuser == True or request.user.is_staff == True:
        return redirect('index')
    return render(request,'user_criar_loja_sucesso.html')

@login_required
def user_loja_dados(request):
    cep = request.GET.get("cep")
    url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
    headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
    link = requests.get(url, headers=headers, verify=False)
    cde = link.json()
    email = request.user.email
    dados = db.collection('users').where('email', '==', f'{email}').stream()
    y = [{'id': x.id} for x in dados]
    con = db.collection(f"users/{y[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
    abc = [{'id': x.id} for x in con]
    cen = db.collection(f"users/{y[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
    xyz = [x.to_dict() for x in cen]
    la = len(abc)
    [abc[x].update(xyz[x]) for x in range(la)]
    [abc[x].update(cde) for x in range(la)]
    if request.method == 'POST':
        name = request.POST['name']
        whatsapp = request.POST['whatsapp']
        trabalheconosco = request.POST['trabalheconosco']
        price = request.POST['price']
        promocao = request.POST['promocao']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        price = price.replace(',', '.')
        price = float(price)
        can = db.collection(f"users/{abc[0]['id']}/loja").document(f"{abc[0]['id']}")
        can.update({
                'name': f'{name}',
                'whatsapp': f'{whatsapp}',
                'trabalhe_conosco': f'{trabalheconosco}',
                'price': price,
                'promocao': f"{promocao}",
                'cidade': f"{cidade}",
                'estado': f"{estado}",
        })
        return redirect('user_loja_dados_sucesso')
    return render(request, 'user_loja_dados.html', {'lista': abc})

@login_required
def user_loja_dados_sucesso(request):
    return render(request, 'user_loja_dados_sucesso.html')

@login_required
def user_adicionar_imagem(request, cat, id):
    if request.user.is_superuser == True or request.user.is_staff == True:
        return redirect('index')
    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        arquivo = sto.blob(f'categorias/{cat}/{id}/{img}')
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        formform = db.collection(f'categorias/{cat}/lojas').document(f'{id}')
        formform.update({
            'img': firestore.ArrayUnion([f'{url}'])
        })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('user_adicionar_imagem_sucesso')
    return render(request, 'user_adicionar_imagem_sucesso.html')

@login_required
def user_adicionar_imagem_sucesso(request):
    return render(request, 'user_adicionar_imagem_sucesso.html')
