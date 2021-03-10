import pyrebase
import locale
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
from firebase_admin import messaging
import psycopg2
from django.contrib import auth as autent
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

config = {
    'apiKey': "AIzaSyBh-DC_fXWzzcHV6XYhFQ1Ya6MWG5OjH_w",
    'authDomain': "mix-brasil.firebaseapp.com",
    'databaseURL': "https://mix-brasil.firebaseio.com",
    'projectId': "mix-brasil",
    'storageBucket': "mix-brasil.appspot.com",
    'messagingSenderId': "132448934641",
    'appId': "1:132448934641:web:f22d872cbc228c8d822750",
    'measurementId': "G-NPE7ECX901"
}

cred = credentials.Certificate("/app/mix_brasil/credencial.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
sto = storage.bucket('mix-brasil.appspot.com')
firebase = pyrebase.initialize_app(config)
authent = firebase.auth()


def logar(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authent.sign_in_with_email_and_password(email, password)
        key = str(user['localId'])
        consulta = db.collection('admin').where('email', '==', f'{email}').stream()
        con = [{'id': x.id} for x in consulta]
        for x in con:
            if str(x['id']) == user['localId']:
                return redirect('index', token=key)
            else:
                return redirect('login_erro')
        # if options == 'admin':
        #   consulta = db.collection('admin').where('email', '==', f'{email}').stream()
        #    con = [{'id': x.id} for x in consulta]
        #    for x in con:
        #        if str(x['id']) == user['localId']:
        #
        #           return redirect('index', token=key)
        #       else:
        #           return redirect('login_erro')
        # elif options == 'user':
        #    consulta = db.collection('users').where('email', '==', f'{email}').stream()
        #   con = [{'id': x.id} for x in consulta]
        #    for x in con:
        #        if str(x['id']) == user['localId']:
        #
        #          return redirect('user_index', token=user['localId'])
        #       else:
        #           return HttpResponseRedirect('login_erro')
        # else:
        #   return redirect('login_erro')
    return render(request, 'login.html')


def login_erro(request):
    return render(request, 'login_erro.html')


def index(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    a = db.collection('users').stream()
    b = [{'id': x.id} for x in a]
    contagem_user = len(b)
    c = db.collection('categorias/academia_sumplementos/lojas').stream()
    d = [{'id': x.id} for x in c]
    e = db.collection('categorias/agencia_viagens/lojas').stream()
    f = [{'id': x.id} for x in e]
    g = db.collection('categorias/automoveis/lojas').stream()
    h = [{'id': x.id} for x in g]
    i = db.collection('categorias/brinquedos/lojas').stream()
    j = [{'id': x.id} for x in i]
    k = db.collection('categorias/cama_mesa_banho/lojas').stream()
    l = [{'id': x.id} for x in k]
    m = db.collection('categorias/cosmetico_beleza/lojas').stream()
    n = [{'id': x.id} for x in m]
    o = db.collection('categorias/decoracao/lojas').stream()
    p = [{'id': x.id} for x in o]
    q = db.collection('categorias/drogarias/lojas').stream()
    r = [{'id': x.id} for x in q]
    s = db.collection('categorias/eletronicos/lojas').stream()
    t = [{'id': x.id} for x in s]
    u = db.collection('categorias/fornecedores/lojas').stream()
    v = [{'id': x.id} for x in u]
    w = db.collection('categorias/materias_construcao/lojas').stream()
    x = [{'id': x.id} for x in w]
    y = db.collection('categorias/modulados/lojas').stream()
    z = [{'id': x.id} for x in y]
    aa = db.collection('categorias/musica_hobbies/lojas').stream()
    bb = [{'id': x.id} for x in aa]
    cc = db.collection('categorias/oticas/lojas').stream()
    dd = [{'id': x.id} for x in cc]
    contagem_lojas = len(d) + len(f) + len(h) + len(j) + len(l) + len(n) + len(p) + len(r) + len(t) + len(v) + len(
        x) + len(z) + len(bb) + len(dd)

    aaa = db.collection('desapego/agro_industria/desapegos').stream()
    bbb = [{'id': x.id} for x in aaa]
    ccc = db.collection('desapego/animais_estimacao/desapegos').stream()
    ddd = [{'id': x.id} for x in ccc]
    eee = db.collection('desapego/artigos_infantis/desapegos').stream()
    fff = [{'id': x.id} for x in eee]
    ggg = db.collection('desapego/autos_e_pecas/desapegos').stream()
    hhh = [{'id': x.id} for x in ggg]
    iii = db.collection('desapego/comercio_escritorio/desapegos').stream()
    jjj = [{'id': x.id} for x in iii]
    kkk = db.collection('desapego/eletronicos_celulares/desapegos').stream()
    lll = [{'id': x.id} for x in kkk]
    mmm = db.collection('desapego/esporte_lazer/desapegos').stream()
    nnn = [{'id': x.id} for x in mmm]
    ooo = db.collection('desapego/imoveis/desapegos').stream()
    ppp = [{'id': x.id} for x in ooo]
    qqq = db.collection('desapego/moda_beleza/desapegos').stream()
    rrr = [{'id': x.id} for x in qqq]
    sss = db.collection('desapego/musicas_hobbies/desapegos').stream()
    ttt = [{'id': x.id} for x in sss]
    uuu = db.collection('desapego/para_sua_casa/desapegos').stream()
    vvv = [{'id': x.id} for x in uuu]
    www = db.collection('desapego/servicos/desapegos').stream()
    xxx = [{'id': x.id} for x in www]
    yyy = db.collection('desapego/vagas_empregos/desapegos').stream()
    zzz = [{'id': x.id} for x in yyy]
    contagem_desapego = len(bbb) + len(ddd) + len(fff) + len(hhh) + len(jjj) + len(lll) + len(nnn) + len(ppp) + len(
        rrr) + len(ttt) + len(vvv) + len(xxx) + len(zzz)
    coa = db.collection('destaque_home').stream()
    coe = [{'id': x.id} for x in coa]
    contagem_destaque_lojas = len(coe)
    cap = db.collection('destaque_desapego').stream()
    cip = [{'id': x.id} for x in cap]
    contagem_destaque_desapegos = len(cip)
    numeros = [{'usuarios': int(contagem_user), 'lojas': int(contagem_lojas), 'desapegos': int(contagem_desapego), 'destaque_lojas': int(contagem_destaque_lojas), 'destaque_desapegos': int(contagem_destaque_desapegos)}]
    estado = request.GET.get('estado')
    municipio = request.GET.get('municipio')
    estados_link = requests.get('http://servicodados.ibge.gov.br/api/v1/localidades/estados')
    estados = estados_link.json()
    if estado:
        municipios_link = requests.get(
            f"http://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/municipios")
        municipios = municipios_link.json()
    else:
        municipios = {'null': 0}
    if municipio and estado:
        ccccc = db.collection('categorias/academia_sumplementos/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        ddddd = [{'id': x.id} for x in ccccc]
        eeee = db.collection('categorias/agencia_viagens/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        ffff = [{'id': x.id} for x in eeee]
        gggg = db.collection('categorias/automoveis/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        hhhh = [{'id': x.id} for x in gggg]
        iiii = db.collection('categorias/brinquedos/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        jjjj = [{'id': x.id} for x in iiii]
        kkkk = db.collection('categorias/cama_mesa_banho/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        llll = [{'id': x.id} for x in kkkk]
        mmmm = db.collection('categorias/cosmetico_beleza/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        nnnn = [{'id': x.id} for x in mmmm]
        oooo = db.collection('categorias/decoracao/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        pppp = [{'id': x.id} for x in oooo]
        qqqq = db.collection('categorias/drogarias/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        rrrr = [{'id': x.id} for x in qqqq]
        ssss = db.collection('categorias/eletronicos/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        tttt = [{'id': x.id} for x in ssss]
        uuuu = db.collection('categorias/fornecedores/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        vvvv = [{'id': x.id} for x in uuuu]
        wwww = db.collection('categorias/materias_construcao/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        xxxx = [{'id': x.id} for x in wwww]
        yyyy = db.collection('categorias/modulados/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        zzzz = [{'id': x.id} for x in yyyy]
        aaaa = db.collection('categorias/musica_hobbies/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        bbbb = [{'id': x.id} for x in aaaa]
        cccc = db.collection('categorias/oticas/lojas').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        dddd = [{'id': x.id} for x in cccc]
        contagem_lojas_pesq = len(ddddd) + len(ffff) + len(hhhh) + len(jjjj) + len(llll) + len(nnnn) + len(pppp) + len(rrrr) + len(tttt) + len(vvvv) + len(
            xxxx) + len(zzzz) + len(bbbb) + len(dddd)
        aax = db.collection('desapego/agro_industria/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        bbx = [{'id': x.id} for x in aax]
        ccx = db.collection('desapego/animais_estimacao/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        ddx = [{'id': x.id} for x in ccx]
        eex = db.collection('desapego/artigos_infantis/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        ffx = [{'id': x.id} for x in eex]
        ggx = db.collection('desapego/autos_e_pecas/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        hhx = [{'id': x.id} for x in ggx]
        iix = db.collection('desapego/comercio_escritorio/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        jjx = [{'id': x.id} for x in iix]
        kkx = db.collection('desapego/eletronicos_celulares/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        llx = [{'id': x.id} for x in kkx]
        mmx = db.collection('desapego/esporte_lazer/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        nnx = [{'id': x.id} for x in mmx]
        oox = db.collection('desapego/imoveis/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        ppx = [{'id': x.id} for x in oox]
        qqx = db.collection('desapego/moda_beleza/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        rrx = [{'id': x.id} for x in qqx]
        ssx = db.collection('desapego/musicas_hobbies/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        ttx = [{'id': x.id} for x in ssx]
        uux = db.collection('desapego/para_sua_casa/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        vvx = [{'id': x.id} for x in uux]
        wwx = db.collection('desapego/servicos/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        xxy = [{'id': x.id} for x in wwx]
        yyx = db.collection('desapego/vagas_empregos/desapegos').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        zzx = [{'id': x.id} for x in yyx]
        contagem_desapego_pesq = len(bbx) + len(ddx) + len(ffx) + len(hhx) + len(jjx) + len(llx) + len(nnx) + len(ppx) + len(
            rrx) + len(ttx) + len(vvx) + len(xxy) + len(zzx)
        coaa = db.collection('destaque_home').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        coee = [{'id': x.id} for x in coaa]
        contagem_destaque_lojas_pesq = len(coee)
        capp = db.collection('destaque_desapego').where('cidade','==',f'{municipio}').where('estado','==',f'{estado}').stream()
        cipp = [{'id': x.id} for x in capp]
        contagem_destaque_desapegos_pesq = len(cipp)
        numeros_pesq = numeros = [{'lojas': int(contagem_lojas_pesq), 'desapegos': int(contagem_desapego_pesq), 'destaque_lojas': int(contagem_destaque_lojas_pesq), 'destaque_desapegos': int(contagem_destaque_desapegos_pesq)}]
    elif municipio:
        ccccc = db.collection('categorias/academia_sumplementos/lojas').where('cidade','==',f'{municipio}').stream()
        ddddd = [{'id': x.id} for x in ccccc]
        eeee = db.collection('categorias/agencia_viagens/lojas').where('cidade','==',f'{municipio}').stream()
        ffff = [{'id': x.id} for x in eeee]
        gggg = db.collection('categorias/automoveis/lojas').where('cidade','==',f'{municipio}').stream()
        hhhh = [{'id': x.id} for x in gggg]
        iiii = db.collection('categorias/brinquedos/lojas').where('cidade','==',f'{municipio}').stream()
        jjjj = [{'id': x.id} for x in iiii]
        kkkk = db.collection('categorias/cama_mesa_banho/lojas').where('cidade','==',f'{municipio}').stream()
        llll = [{'id': x.id} for x in kkkk]
        mmmm = db.collection('categorias/cosmetico_beleza/lojas').where('cidade','==',f'{municipio}').stream()
        nnnn = [{'id': x.id} for x in mmmm]
        oooo = db.collection('categorias/decoracao/lojas').where('cidade','==',f'{municipio}').stream()
        pppp = [{'id': x.id} for x in oooo]
        qqqq = db.collection('categorias/drogarias/lojas').where('cidade','==',f'{municipio}').stream()
        rrrr = [{'id': x.id} for x in qqqq]
        ssss = db.collection('categorias/eletronicos/lojas').where('cidade','==',f'{municipio}').stream()
        tttt = [{'id': x.id} for x in ssss]
        uuuu = db.collection('categorias/fornecedores/lojas').where('cidade','==',f'{municipio}').stream()
        vvvv = [{'id': x.id} for x in uuuu]
        wwww = db.collection('categorias/materias_construcao/lojas').where('cidade','==',f'{municipio}').stream()
        xxxx = [{'id': x.id} for x in wwww]
        yyyy = db.collection('categorias/modulados/lojas').where('cidade','==',f'{municipio}').stream()
        zzzz = [{'id': x.id} for x in yyyy]
        aaaa = db.collection('categorias/musica_hobbies/lojas').where('cidade','==',f'{municipio}').stream()
        bbbb = [{'id': x.id} for x in aaaa]
        cccc = db.collection('categorias/oticas/lojas').where('cidade','==',f'{municipio}').stream()
        dddd = [{'id': x.id} for x in cccc]
        contagem_lojas_pesq = len(ddddd) + len(ffff) + len(hhhh) + len(jjjj) + len(llll) + len(nnnn) + len(pppp) + len(
            rrrr) + len(tttt) + len(vvvv) + len(
            xxxx) + len(zzzz) + len(bbbb) + len(dddd)
        aax = db.collection('desapego/agro_industria/desapegos').where('cidade','==',f'{municipio}').stream()
        bbx = [{'id': x.id} for x in aax]
        ccx = db.collection('desapego/animais_estimacao/desapegos').where('cidade','==',f'{municipio}').stream()
        ddx = [{'id': x.id} for x in ccx]
        eex = db.collection('desapego/artigos_infantis/desapegos').where('cidade','==',f'{municipio}').stream()
        ffx = [{'id': x.id} for x in eex]
        ggx = db.collection('desapego/autos_e_pecas/desapegos').where('cidade','==',f'{municipio}').stream()
        hhx = [{'id': x.id} for x in ggx]
        iix = db.collection('desapego/comercio_escritorio/desapegos').where('cidade','==',f'{municipio}').stream()
        jjx = [{'id': x.id} for x in iix]
        kkx = db.collection('desapego/eletronicos_celulares/desapegos').where('cidade','==',f'{municipio}').stream()
        llx = [{'id': x.id} for x in kkx]
        mmx = db.collection('desapego/esporte_lazer/desapegos').where('cidade','==',f'{municipio}').stream()
        nnx = [{'id': x.id} for x in mmx]
        oox = db.collection('desapego/imoveis/desapegos').where('cidade','==',f'{municipio}').stream()
        ppx = [{'id': x.id} for x in oox]
        qqx = db.collection('desapego/moda_beleza/desapegos').where('cidade','==',f'{municipio}').stream()
        rrx = [{'id': x.id} for x in qqx]
        ssx = db.collection('desapego/musicas_hobbies/desapegos').where('cidade','==',f'{municipio}').stream()
        ttx = [{'id': x.id} for x in ssx]
        uux = db.collection('desapego/para_sua_casa/desapegos').where('cidade','==',f'{municipio}').stream()
        vvx = [{'id': x.id} for x in uux]
        wwx = db.collection('desapego/servicos/desapegos').where('cidade','==',f'{municipio}').stream()
        xxy = [{'id': x.id} for x in wwx]
        yyx = db.collection('desapego/vagas_empregos/desapegos').where('cidade','==',f'{municipio}').stream()
        zzx = [{'id': x.id} for x in yyx]
        contagem_desapego_pesq = len(bbx) + len(ddx) + len(ffx) + len(hhx) + len(jjx) + len(llx) + len(nnx) + len(
            ppx) + len(
            rrx) + len(ttx) + len(vvx) + len(xxy) + len(zzx)
        coaa = db.collection('destaque_home').where('cidade','==',f'{municipio}').stream()
        coee = [{'id': x.id} for x in coaa]
        contagem_destaque_lojas_pesq = len(coee)
        capp = db.collection('destaque_desapego').where('cidade','==',f'{municipio}').stream()
        cipp = [{'id': x.id} for x in capp]
        contagem_destaque_desapegos_pesq = len(cipp)
        numeros_pesq = numeros = [{'lojas': int(contagem_lojas_pesq), 'desapegos': int(contagem_desapego_pesq),
                                   'destaque_lojas': int(contagem_destaque_lojas_pesq),
                                   'destaque_desapegos': int(contagem_destaque_desapegos_pesq)}]
    elif estado:
        ccccc = db.collection('categorias/academia_sumplementos/lojas').where('estado','==',f'{estado}').stream()
        ddddd = [{'id': x.id} for x in ccccc]
        eeee = db.collection('categorias/agencia_viagens/lojas').where('estado','==',f'{estado}').stream()
        ffff = [{'id': x.id} for x in eeee]
        gggg = db.collection('categorias/automoveis/lojas').where('estado','==',f'{estado}').stream()
        hhhh = [{'id': x.id} for x in gggg]
        iiii = db.collection('categorias/brinquedos/lojas').where('estado','==',f'{estado}').stream()
        jjjj = [{'id': x.id} for x in iiii]
        kkkk = db.collection('categorias/cama_mesa_banho/lojas').where('estado','==',f'{estado}').stream()
        llll = [{'id': x.id} for x in kkkk]
        mmmm = db.collection('categorias/cosmetico_beleza/lojas').where('estado','==',f'{estado}').stream()
        nnnn = [{'id': x.id} for x in mmmm]
        oooo = db.collection('categorias/decoracao/lojas').where('estado','==',f'{estado}').stream()
        pppp = [{'id': x.id} for x in oooo]
        qqqq = db.collection('categorias/drogarias/lojas').where('estado','==',f'{estado}').stream()
        rrrr = [{'id': x.id} for x in qqqq]
        ssss = db.collection('categorias/eletronicos/lojas').where('estado','==',f'{estado}').stream()
        tttt = [{'id': x.id} for x in ssss]
        uuuu = db.collection('categorias/fornecedores/lojas').where('estado','==',f'{estado}').stream()
        vvvv = [{'id': x.id} for x in uuuu]
        wwww = db.collection('categorias/materias_construcao/lojas').where('estado','==',f'{estado}').stream()
        xxxx = [{'id': x.id} for x in wwww]
        yyyy = db.collection('categorias/modulados/lojas').where('estado','==',f'{estado}').stream()
        zzzz = [{'id': x.id} for x in yyyy]
        aaaa = db.collection('categorias/musica_hobbies/lojas').where('estado','==',f'{estado}').stream()
        bbbb = [{'id': x.id} for x in aaaa]
        cccc = db.collection('categorias/oticas/lojas').where('estado','==',f'{estado}').stream()
        dddd = [{'id': x.id} for x in cccc]
        contagem_lojas_pesq = len(ddddd) + len(ffff) + len(hhhh) + len(jjjj) + len(llll) + len(nnnn) + len(pppp) + len(
            rrrr) + len(tttt) + len(vvvv) + len(
            xxxx) + len(zzzz) + len(bbbb) + len(dddd)
        aax = db.collection('desapego/agro_industria/desapegos').where('estado','==',f'{estado}').stream()
        bbx = [{'id': x.id} for x in aax]
        ccx = db.collection('desapego/animais_estimacao/desapegos').where('estado','==',f'{estado}').stream()
        ddx = [{'id': x.id} for x in ccx]
        eex = db.collection('desapego/artigos_infantis/desapegos').where('estado','==',f'{estado}').stream()
        ffx = [{'id': x.id} for x in eex]
        ggx = db.collection('desapego/autos_e_pecas/desapegos').where('estado','==',f'{estado}').stream()
        hhx = [{'id': x.id} for x in ggx]
        iix = db.collection('desapego/comercio_escritorio/desapegos').where('estado','==',f'{estado}').stream()
        jjx = [{'id': x.id} for x in iix]
        kkx = db.collection('desapego/eletronicos_celulares/desapegos').where('estado','==',f'{estado}').stream()
        llx = [{'id': x.id} for x in kkx]
        mmx = db.collection('desapego/esporte_lazer/desapegos').where('estado','==',f'{estado}').stream()
        nnx = [{'id': x.id} for x in mmx]
        oox = db.collection('desapego/imoveis/desapegos').where('estado','==',f'{estado}').stream()
        ppx = [{'id': x.id} for x in oox]
        qqx = db.collection('desapego/moda_beleza/desapegos').where('estado','==',f'{estado}').stream()
        rrx = [{'id': x.id} for x in qqx]
        ssx = db.collection('desapego/musicas_hobbies/desapegos').where('estado','==',f'{estado}').stream()
        ttx = [{'id': x.id} for x in ssx]
        uux = db.collection('desapego/para_sua_casa/desapegos').where('estado','==',f'{estado}').stream()
        vvx = [{'id': x.id} for x in uux]
        wwx = db.collection('desapego/servicos/desapegos').where('estado','==',f'{estado}').stream()
        xxy = [{'id': x.id} for x in wwx]
        yyx = db.collection('desapego/vagas_empregos/desapegos').where('estado','==',f'{estado}').stream()
        zzx = [{'id': x.id} for x in yyx]
        contagem_desapego_pesq = len(bbx) + len(ddx) + len(ffx) + len(hhx) + len(jjx) + len(llx) + len(nnx) + len(
            ppx) + len(
            rrx) + len(ttx) + len(vvx) + len(xxy) + len(zzx)
        coaa = db.collection('destaque_home').where('estado','==',f'{estado}').stream()
        coee = [{'id': x.id} for x in coaa]
        contagem_destaque_lojas_pesq = len(coee)
        capp = db.collection('destaque_desapego').where('estado','==',f'{estado}').stream()
        cipp = [{'id': x.id} for x in capp]
        contagem_destaque_desapegos_pesq = len(cipp)
        numeros_pesq = numeros = [{'lojas': int(contagem_lojas_pesq), 'desapegos': int(contagem_desapego_pesq),
                                   'destaque_lojas': int(contagem_destaque_lojas_pesq),
                                   'destaque_desapegos': int(contagem_destaque_desapegos_pesq)}]
    else:
        numeros_pesq = [{'id': '0'}]
    return render(request, 'index.html', {'t': key, 'lista': numeros, 'lista2': numeros_pesq, 'ibge_uf': estados, 'ibge_mun': municipios})


def base(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'base.html', {'t': key})


def user_index(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_index.html', {'t': key})


def user_base(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_base.html', {'t': key})


def deslogar(request):
    logout(request)
    return HttpResponseRedirect("/")


# def criar_usuario(request):
#   if request.method == 'POST':
#      name = request.POST['name']
#     phone = request.POST['phone']
#    email = request.POST['email']
#   password = request.POST['password']
#  cep = request.POST['cep']
# if cep != "":
#    url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
#   headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
#  link = requests.get(url, headers=headers, verify=False)
# cde = link.json()
# else:
#   cde = {}
# user = auth.create_user(email=email, password=password)
# dados = db.collection('users').document(user.uid)
# dados.set({
# 'name': f'{name}',
# 'phone': f'{phone}',
# 'email': f'{email}',
# 'img': None,
# 'address': {
#   'city': f"{cde['cidade']['nome']}",
#    'district': f"{cde['bairro']}",
#     'lat': f"{cde['latitude']}",
#      'long': f"{cde['longitude']}",
#       'state': f"{cde['estado']['sigla']}",
#        'street': f"{cde['logradouro']}",
#         'zipCode': f"{cde['cep']}"
#      }
#   })
#    return redirect('criar_usuario_sucesso')
# return render(request, 'criar_usuario.html')


# def criar_usuario_sucesso(request):
#   return render(request, 'criar_usuario_sucesso.html')


def usuario_listagem(request, token):
    query = request.GET.get("query")

    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if query:
        usuarios = db.collection('users').where('name', '==', f"{query}").stream()
        doz = [{'id': x.id} for x in usuarios]
        ident = db.collection('users').where('name', '==', f"{query}").stream()
        docs = [x.to_dict() for x in ident]
        a = len(doz)
        [doz[x].update(keya) for x in range(a)]
    else:
        usuarios = db.collection('users').stream()
        doz = [{'id': x.id} for x in usuarios]
        ident = db.collection('users').stream()
        docs = [x.to_dict() for x in ident]
        a = len(doz)
        [doz[x].update(keya) for x in range(a)]
    return render(request, 'usuario_listagem.html', {'lista': docs, 'lista_id': doz, 't': key})


def usuario_dados(request, token, id):
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    cep = request.GET.get("cep")
    if cep != "":
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
        link = requests.get(url, headers=headers, verify=False)
        cde = link.json()
    else:
        abc = {'id': 0}
        cde = abc.json()
    dados = db.collection(f'users').document(f'{id}')
    dad = dados.get()
    abc = dad.to_dict()
    ident = {'id': f'{id}'}
    abc.update(ident)
    abc.update(cde)
    abc.update(keya)
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
        return redirect('atualizar_usuario_sucesso', token=token)
    return render(request, 'usuario_dados.html', {'lista': abc, 't': key})


def atualizar_usuario_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'atualizar_usuario_sucesso.html', {'t': key})


def remover_usuario(request, token, id, e):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        user = User.objects.get(email=e)
        user.delete()
        db.collection(f'users').document(f'{id}').delete()
        auth.delete_user(uid=id)
        return redirect('remover_usuario_sucesso')
    return render(request, 'remover_usuario.html', {'t': key})


def remover_usuario_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'remover_usuario_sucesso.html', {'t': key})


'''def adicionar_imagem_perfil(request, token, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados = db.collection(f"users")
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
      return redirect('adicionar_imagem_perfil_sucesso', token=token)
    return render(request, 'adicionar_imagem_perfil.html', {'t': key})'''

'''def criar_loja(request, token, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
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
        if cep != "":
            url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
            headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
            link = requests.get(url, headers=headers, verify=False)
            cde = link.json()
        else:
            cde = {}
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
                    'img_cupons': firestore.ArrayUnion([x for x in n['img_cupons']]),
                    'img': firestore.ArrayUnion([x for x in n['img']]),
                    'lid': f"{da[0]['id']}",
                    'name': f"{da[0]['name']}",
                    'img_ofertas': firestore.ArrayUnion([x for x in n['img_ofertas']]),
                    'img_destacadas': firestore.ArrayUnion([x for x in n['img_destacados']]),
                    'price': n['price'],
                    'cidade': n['cidade'],
                    'estado': n['estado'],
                    'created': firestore.firestore.SERVER_TIMESTAMP,
                    'promocao': f"{promocao}",
                    'trabalheConosco': f"{trabalhe_conosco}",
                    'whatsapp': f"{whatsapp}"
                })
        return redirect('criar_loja_sucesso', token=token)
    return render(request, 'criar_loja.html', {'t': key})'''

'''def criar_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'criar_loja_sucesso.html', {'t': key})'''


def categoria_listagem(request, token):
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    for x in usa:
        if str(x['email']) != user.email:
            return redirect('user_index')
    categorias = db.collection('categorias').stream()
    doz = [{'id': x.id} for x in categorias]
    ident = db.collection('categorias').stream()
    docs = [x.to_dict() for x in ident]
    a = len(doz)
    [doz[x].update(keya) for x in range(a)]
    return render(request, 'categoria_listagem.html', {'lista': docs, 'lista_id': doz, 't': key})


def lojas_listagem(request, token, id):
    q_estado = request.GET.get('q_estado')
    q_cidade = request.GET.get('q_cidade')
    estados_link = requests.get('http://servicodados.ibge.gov.br/api/v1/localidades/estados')
    estados = estados_link.json()
    if q_estado:
        municipios_link = requests.get(
            f"http://servicodados.ibge.gov.br/api/v1/localidades/estados/{q_estado}/municipios")
        municipios = municipios_link.json()
    else:
        municipios = {'null': 0}
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if q_cidade:
        lojas = db.collection(f'categorias/{id}/lojas').where('cidade', '==', f'{q_cidade}').stream()
        docs = [{'id': x.id} for x in lojas]
        lojas2 = db.collection(f'categorias/{id}/lojas').where('cidade', '==', f'{q_cidade}').stream()
        docs2 = [y.to_dict() for y in lojas2]
        a = len(docs)
        dzz = [{'categoria': f'{id}', 'token': str(token)}]
        categoria = {'categoria': f'{id}'}
        [docs[x].update(docs2[x]) for x in range(a)]
        [docs[x].update(categoria) for x in range(a)]
        [docs[x].update(keya) for x in range(a)]
    else:
        lojas = db.collection(f'categorias/{id}/lojas').stream()
        docs = [{'id': x.id} for x in lojas]
        lojas2 = db.collection(f'categorias/{id}/lojas').stream()
        docs2 = [y.to_dict() for y in lojas2]
        a = len(docs)
        dzz = [{'categoria': f'{id}', 'token': str(token)}]
        categoria = {'categoria': f'{id}'}
        [docs[x].update(docs2[x]) for x in range(a)]
        [docs[x].update(categoria) for x in range(a)]
        [docs[x].update(keya) for x in range(a)]
    return render(request, 'lojas_listagem.html',
                  {'lista': docs, 'order': dzz, 't': key, 'ibge_uf': estados, 'ibge_mun': municipios})


def lojas_dados(request, token, id, nome, cod):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    cep = request.GET.get("cep")
    if cep != "":
        url = f"http://cep.la/{cep}"
        headers = {'Accept': 'application/json'}
        link = requests.api.request('GET', url, headers=headers)
        cde = link.json()
    else:
        url = f"http://cep.la/0000001"
        headers = {'Accept': 'application/json'}
        link = requests.api.request('GET', url, headers=headers)
        cde = link.json()
    dados = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    abc = [x.to_dict() for x in dados]
    dados2 = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{nome}').stream()
    dec = [{'id': x.id} for x in dados2]
    a = len(dec)
    categoria = {'categoria': f'{id}'}
    keya = {'token': str(token)}
    [dec[x].update(abc[x]) for x in range(a)]
    [dec[x].update(categoria) for x in range(a)]
    [dec[x].update(cde) for x in range(a)]
    [dec[x].update(keya) for x in range(a)]
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
                'number': f'{whatsapp}',
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
            if cep != "":
                didi.set({
                    'cid': f"{da[0]['categoria']}",
                    'img_cupons': firestore.ArrayUnion([x for x in da[0]['img_cupons']]),
                    'img': firestore.ArrayUnion([x for x in da[0]['img']]),
                    'lid': f"{da[0]['id']}",
                    'name': f"{da[0]['name']}",
                    'img_ofertas': firestore.ArrayUnion([x for x in da[0]['img_ofertas']]),
                    'img_destacadas': firestore.ArrayUnion([x for x in da[0]['img_destacados']]),
                    'price': da[0]['price'],
                    'cidade': da[0]['cidade'],
                    'estado': da[0]['estado'],
                    'created': firestore.firestore.SERVER_TIMESTAMP,
                    'promocao': f"{promocao}",
                    'trabalheConosco': f"{trabalhe_conosco}",
                    'number': f"{whatsapp}"

                })
            else:
                didi.set({
                    'cid': f"{da[0]['categoria']}",
                    'img_cupons': firestore.ArrayUnion([""]),
                    'img': firestore.ArrayUnion([""]),
                    'lid': f"{da[0]['id']}",
                    'name': f"{da[0]['name']}",
                    'img_ofertas': firestore.ArrayUnion([""]),
                    'img_destacados': firestore.ArrayUnion([""]),
                    'price': da[0]['price'],
                    'cidade': da[0]['cidade'],
                    'estado': da[0]['estado'],
                    'created': firestore.firestore.SERVER_TIMESTAMP,
                    'promocao': f"{promocao}",
                    'trabalheConosco': f"{trabalhe_conosco}",
                    'number': f"{whatsapp}"

                })
            dados10 = db.collection(f"categorias/{id}/lojas").where('name', '==', f"{name}").stream()
            dados11 = [{'id': x.id} for x in dados10]
            dados12 = db.collection(f"categorias/{id}/lojas").where('name', '==', f"{name}").stream()
            dados13 = [x.to_dict() for x in dados12]
            a = len(dados11)
            categoria = {'categoria': f'{id}'}
            [dados11[x].update(dados13[x]) for x in range(a)]
            [dados11[x].update(categoria) for x in range(a)]
            [dados11[x].update(cde) for x in range(a)]

            dados14 = db.collection(f"categorias/{id}/lojas").where('name', '==', f"{name}").stream()
            dados15 = [{'id': x.id} for x in dados14]
            dados16 = db.collection(f"categorias/{id}/lojas").where('name', '==', f"{name}").stream()
            dados17 = [x.to_dict() for x in dados16]
            a = len(dados15)
            [dados15[x].update(dados17[x]) for x in range(a)]
            [dados15[x].update(categoria) for x in range(a)]
            [dados15[x].update(cde) for x in range(a)]
            final = db.collection(f"users/{dados11[0]['user']}/lojas").stream()
            final2 = [{'id': x.id} for x in final]
            final3 = db.collection(f"users/{dados15[0]['user']}/lojas").document(f"{final2[0]['id']}")
            final3.update({
                'status': 3
            })
            r12 = db.collection('msg_destaca_loja').where('name', '==', f"{da[0]['name']}").stream()
            r13 = [{'id': x.id} for x in r12]
            db.collection('msg_destaca_loja').document(f"{r13[0]['id']}").delete()
        elif des == False:
            desdes = db.collection(f'destaque_home').where('lid', '==', f'{cod}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'destaque_home').where('lid', '==', f'{cod}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            [da[x].update(dw[x]) for x in range(a)]
            db.collection('destaque_home').document(f"{da[0]['id']}").delete()

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
        return redirect('atualizar_loja_sucesso', token=token)
    return render(request, 'lojas_dados.html', {'lista': dec, 't': key})


def atualizar_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'atualizar_loja_sucesso.html', {'t': key})


'''def adicionar_imagens_loja(request, token, id, cod):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        tipo_imagem = request.POST['tipo_imagem']
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
        if tipo_imagem == 'normal':
            formform.update({
                'img': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'ofertas':
            formform.update({
                'img_ofertas': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'destacados':
            formform.update({
                'img_destacados': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'cupons':
            formform.update({
                'img_cupons': firestore.ArrayUnion([f'{url}'])
            })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('adicionar_imagens_loja_sucesso', token=token)
    return render(request, 'adicionar_imagens_loja.html', {'t': key})'''

'''def adicionar_imagens_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'adicionar_imagens_loja_sucesso.html', {'t': key})'''

'''def remover_imagens_loja(request, token, id, name, cod):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados = db.collection(f'categorias/{id}/lojas').where('name', '==', f'{name}').stream()
    docs = [x.to_dict() for x in dados]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        tipo_imagem = request.POST['tipo_imagem']
        formform = db.collection(f'categorias/{id}/lojas').document(f'{cod}')
        if tipo_imagem == 'normal':
            formform.update({
                'img': firestore.ArrayRemove([f'{imagem}'])
            })
        elif tipo_imagem == 'ofertas':
            formform.update({
                'img_ofertas': firestore.ArrayRemove([f'{imagem}'])
            })
        elif tipo_imagem == 'destacados':
            formform.update({
                'img_destacados': firestore.ArrayRemove([f'{imagem}'])
            })
        elif tipo_imagem == 'cupons':
            formform.update({
                'img_cupons': firestore.ArrayRemove([f'{imagem}'])
            })
        return redirect('remover_imagens_loja_sucesso', token=token)
    return render(request, 'remover_imagens_loja.html', {'lista': docs, 't': key})'''

'''def remover_imagens_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'remover_imagens_loja_sucesso.html', {'t': key})'''


def remover_loja(request, token, id, cod):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        db.collection(f'categorias/{id}/lojas').document(f'{cod}').delete()
        db.collection('destaque_home').where('lid', '==', f'{cod}').delete()
        return redirect('remover_loja_sucesso', token=token)
    return render(request, 'remover_loja.html', {'t': key})


def remover_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'remover_loja_sucesso.html', {'t': key})


'''def criar_desapego(request, token, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
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
        if cep != "":
            url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
            headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
            link = requests.get(url, headers=headers, verify=False)
            cde = link.json()
        else:
            cde = {}
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
                    'idCat': f"{n['categoria']}",
                    'img': firestore.ArrayUnion([""]),
                    'did': f"{n['id']}",
                    'name': f"{n['name']}",
                    'price': n['price'],
                    'cidade': n['cidade']['nome'],
                    'estado': n['estado']['sigla'],
                    'anunciante': f"{n['anunciante']}",
                    'number': f"{n['number']}",
                    'descricao': f"{n['descricao']}",
                    'idAdsUser': f"{n['idAdsUser']}",
                    'user': f"{n['user']}",
                    'viewsDestaque': 0,
                    'created': firestore.firestore.SERVER_TIMESTAMP,
                })
        return redirect('criar_loja_sucesso', token=token)
    return render(request, 'criar_desapego.html', {'t': key})'''

'''def criar_desapego_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'criar_desapego_sucesso.html', {'t': key})'''


def categoria_desapego_listagem(request, token):
    query = request.GET.get('query')
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if query:
        desapegos = db.collection('desapego').where('name', '==', f'{query}').stream()
        doz = [{'id': x.id} for x in desapegos]
        ident = db.collection('desapego').where('name', '==', f'{query}').stream()
        docs = [x.to_dict() for x in ident]
        a = len(doz)
        [doz[x].update(keya) for x in range(a)]
    else:
        desapegos = db.collection('desapego').stream()
        doz = [{'id': x.id} for x in desapegos]
        ident = db.collection('desapego').stream()
        docs = [x.to_dict() for x in ident]
        a = len(doz)
        [doz[x].update(keya) for x in range(a)]
    return render(request, 'categoria_desapego_listagem.html', {'lista': docs, 'lista_id': doz, 't': key})


def desapegos_listagem(request, token, id):
    q_estado = request.GET.get('q_estado')
    q_cidade = request.GET.get('q_cidade')
    estados_link = requests.get('http://servicodados.ibge.gov.br/api/v1/localidades/estados')
    estados = estados_link.json()
    if q_estado:
        municipios_link = requests.get(
            f"http://servicodados.ibge.gov.br/api/v1/localidades/estados/{q_estado}/municipios")
        municipios = municipios_link.json()
    else:
        municipios = {'null': 0}
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if q_cidade:
        desapegos = db.collection(f'desapego/{id}/desapegos').where('cidade', '==', f"{q_cidade}").stream()
        docs = [{'id': x.id} for x in desapegos]
        lojas2 = db.collection(f'desapego/{id}/desapegos').where('cidade', '==', f"{q_cidade}").stream()
        docs2 = [y.to_dict() for y in lojas2]
        a = len(docs)
        dzz = [{'categoria': f'{id}', 'token': str(token)}]
        categoria = {'categoria': f'{id}'}
        [docs[x].update(docs2[x]) for x in range(a)]
        [docs[x].update(categoria) for x in range(a)]
        [docs[x].update(keya) for x in range(a)]
    else:
        desapegos = db.collection(f'desapego/{id}/desapegos').stream()
        docs = [{'id': x.id} for x in desapegos]
        lojas2 = db.collection(f'desapego/{id}/desapegos').stream()
        docs2 = [y.to_dict() for y in lojas2]
        a = len(docs)
        dzz = [{'categoria': f'{id}', 'token': str(token)}]
        categoria = {'categoria': f'{id}'}
        [docs[x].update(docs2[x]) for x in range(a)]
        [docs[x].update(categoria) for x in range(a)]
        [docs[x].update(keya) for x in range(a)]
    return render(request, 'desapegos_listagem.html',
                  {'lista': docs, 'order': dzz, 't': key, 'ibge_uf': estados, 'ibge_mun': municipios})


def desapegos_dados(request, token, id, nome, cod):
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    cep = request.GET.get("cep")
    if cep != "":
        url = f"http://cep.la/{cep}"
        headers = {'Accept': 'application/json'}
        link = requests.api.request('GET', url, headers=headers)
        cde = link.json()
    else:
        url = f"http://cep.la/0000001"
        headers = {'Accept': 'application/json'}
        link = requests.api.request('GET', url, headers=headers)
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
    [dec[x].update(keya) for x in range(a)]
    if request.method == 'POST':
        name = request.POST['name']
        descricao = request.POST['descricao']
        price = request.POST['price']
        destaque = request.POST['destaque']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        anunciante = request.POST['anunciante']
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
                'bairro': f'{bairro}',
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
            didi.set({
                'idCat': f"{da[0]['categoria']}",
                'img': firestore.ArrayUnion([x for x in da[0]['img']]),
                'did': f"{da[0]['id']}",
                'name': f"{da[0]['name']}",
                'price': da[0]['price'],
                'bairro': da[0]['bairro'],
                'cidade': da[0]['cidade'],
                'estado': da[0]['estado'],
                'anunciante': f"{da[0]['anunciante']}",
                'number': f"{da[0]['number']}",
                'descricao': f"{da[0]['descricao']}",
                'idAdsUser': f"{da[0]['idAdsUser']}",
                'user': f"{da[0]['user']}",
                'viewsDestaque': 0,
                'created': firestore.firestore.SERVER_TIMESTAMP,
            })
            dados10 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados11 = [{'id': x.id} for x in dados10]
            dados12 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados13 = [x.to_dict() for x in dados12]
            a = len(dados11)
            categoria = {'categoria': f'{id}'}
            [dados11[x].update(dados13[x]) for x in range(a)]
            [dados11[x].update(categoria) for x in range(a)]
            [dados11[x].update(cde) for x in range(a)]

            dados14 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados15 = [{'id': x.id} for x in dados14]
            dados16 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados17 = [x.to_dict() for x in dados16]
            a = len(dados15)
            [dados15[x].update(dados17[x]) for x in range(a)]
            [dados15[x].update(categoria) for x in range(a)]
            [dados15[x].update(cde) for x in range(a)]
            final = db.collection(f"users/{dados11[0]['user']}/desapegos").stream()
            final2 = [{'id': x.id} for x in final]
            final3 = db.collection(f"users/{dados15[0]['user']}/desapegos").document(f"{final2[0]['id']}")
            final3.update({
                'status': 3
            })
            pop = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            ppp = [{'id': x.id} for x in pop]
            pap = db.collection('msg_destaca_desapego').where('idAds', '==', f"{ppp[0]['id']}").stream()
            pup = [{'id': x.id} for x in pap]
            db.collection(f"msg_destaca_desapego").document(f"{pup[0]['id']}").delete()
        elif des == False:
            desdes = db.collection(f'destaque_desapego').where('did', '==', f'{cod}').stream()
            da = [{'id': x.id} for x in desdes]
            dasdas = db.collection(f'destaque_desapego').where('did', '==', f'{cod}').stream()
            dw = [x.to_dict() for x in dasdas]
            a = len(da)
            [da[x].update(dw[x]) for x in range(a)]
            for n in da:
                db.collection('destaque_desapego').document(f"{n['id']}").delete()
            dados18 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados19 = [{'id': x.id} for x in dados18]
            dados20 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados21 = [x.to_dict() for x in dados20]
            a = len(dados19)
            categoria = {'categoria': f'{id}'}
            [dados19[x].update(dados21[x]) for x in range(a)]
            [dados19[x].update(categoria) for x in range(a)]
            [dados19[x].update(cde) for x in range(a)]
            dados22 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados23 = [{'id': x.id} for x in dados22]
            dados24 = db.collection(f"desapego/{id}/desapegos").where('name', '==', f"{name}").stream()
            dados25 = [x.to_dict() for x in dados24]
            a = len(dados23)
            [dados23[x].update(dados25[x]) for x in range(a)]
            [dados23[x].update(categoria) for x in range(a)]
            [dados23[x].update(cde) for x in range(a)]
            final4 = db.collection(f"users/{dados19[0]['user']}/desapegos").stream()
            final5 = [{'id': x.id} for x in final4]
            final6 = db.collection(f"users/{dados23[0]['user']}/desapegos").document(f"{final5[0]['id']}")
            final6.update({
                'destaque': False
            })
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
        return redirect('atualizar_desapego_sucesso', token=token)
    return render(request, 'desapegos_dados.html', {'lista': dec, 't': key})


def atualizar_desapego_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'atualizar_desapego_sucesso.html', {'t': key})


'''def adicionar_imagens_desapego(request, token, id, cod):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
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
        return redirect('adicionar_imagens_desapego_sucesso', token=token)
    return render(request, 'adicionar_imagens_desapego.html', {'t': key})'''

'''def adicionar_imagens_desapego_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'adicionar_imagens_desapego_sucesso.html', {'t': key})'''

'''def remover_imagens_desapego(request, token, id, name, cod):
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados = db.collection(f'desapego/{id}/desapegos').where('name', '==', f'{name}').stream()
    docs = [x.to_dict() for x in dados]
    a = len(docs)
    [docs[x].update(keya) for x in range(a)]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        formform = db.collection(f'desapego/{id}/desapegos').document(f'{cod}')
        formform.update({
            'img': firestore.ArrayRemove([f'{imagem}'])
        })

        return redirect('remover_imagens_desapego_sucesso', token=token)
    return render(request, 'remover_imagens_desapego.html', {'lista': docs, 't': key})'''

'''def remover_imagens_desapego_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    for x in usa:
        if str(x['email']) != user.email:
            return redirect('user_index')
    return render(request, 'remover_imagens_desapego_sucesso.html', {'t': key})'''


def remover_desapego(request, token, id, cod):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        db.collection(f'desapego/{id}/desapegos').document(f'{cod}').delete()
        return redirect('remover_desapego_sucesso', token=token)
    return render(request, 'remover_desapego.html', {'t': key})


def remover_desapego_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'remover_desapego_sucesso.html', {'t': key})


def notificacao(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        titulo = request.POST['titulo']
        mensagem = request.POST['mensagem']
        dados = db.collection('users').stream()
        dados2 = [{'id': x.id} for x in dados]
        for x in dados2:
            dados3 = db.collection(f"users/{x['id']}/tokens").stream()
            dados4 = [y.to_dict() for y in dados3]
            noti = messaging.Message(
                notification=messaging.Notification(titulo, mensagem),
                token=f"{dados4[0]['token']}"
            )
            messaging.send(noti)
            return redirect('notificacao_sucesso', token=token)
    return render(request, 'notificacao.html', {'t': key})


def notificacao_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'notificacao_sucesso.html', {'t': key})


def solicitacao_desapego_listagem(request, token):
    key = [str(token)]
    keya = {'token': token}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dsa = db.collection(f"msg_destaca_desapego").stream()
    dsae = [{'id': x.id} for x in dsa]
    dse = db.collection(f"msg_destaca_desapego").stream()
    dsee = [x.to_dict() for x in dse]
    a = len(dsae)
    [dsae[x].update(dsee[x]) for x in range(a)]
    [dsae[x].update(keya) for x in range(a)]
    return render(request, 'solicitacao_desapego_listagem.html', {'lista': dsae, 't': key})


def solicitacao_desapego_ver(request, token, name):
    key = [str(token)]
    keya = {'token': token}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    day = db.collection("msg_destaca_desapego").where('name', '==', f'{name}').stream()
    dey = [{'id': x.id} for x in day]
    diy = db.collection("msg_destaca_desapego").where('name', '==', f'{name}').stream()
    doy = [x.to_dict() for x in diy]
    a = len(dey)
    [dey[x].update(doy[x]) for x in range(a)]
    [dey[x].update(keya) for x in range(a)]
    return render(request, 'solicitacao_desapego_ver.html', {'lista': dey, 't': key})


def solicitacao_desapego_remover(request, token, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        db.collection("msg_destaca_desapego").document(f"{id}").delete()
        return redirect('solicitacao_desapego_remover_sucesso', token=token)
    return render(request, 'solicitacao_desapego_remover.html', {'t': key})


def solicitacao_desapego_remover_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'solicitacao_desapego_remover_sucesso.html', {'t': key})


def solicitacao_loja_listagem(request, token):
    key = [str(token)]
    keya = {'token': token}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dsa = db.collection(f"msg_destaca_loja").stream()
    dsae = [{'id': x.id} for x in dsa]
    dse = db.collection(f"msg_destaca_loja").stream()
    dsee = [x.to_dict() for x in dse]
    a = len(dsae)
    [dsae[x].update(dsee[x]) for x in range(a)]
    [dsae[x].update(keya) for x in range(a)]
    return render(request, 'solicitacao_loja_listagem.html', {'lista': dsae, 't': key})


def solicitacao_loja_ver(request, token, cat, name):
    key = [str(token)]
    keya = {'token': token}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    day = db.collection("msg_destaca_loja").where('name', '==', f'{name}').stream()
    dey = [{'id': x.id} for x in day]
    diy = db.collection("msg_destaca_loja").where('name', '==', f'{name}').stream()
    doy = [x.to_dict() for x in diy]
    duy = db.collection(f"categorias/{cat}/lojas").where('name', '==', f'{name}').stream()
    dry = [{'idLoja': x.id} for x in duy]
    dxy = db.collection(f"categorias/{cat}/lojas").where('name', '==', f'{name}').stream()
    dpy = [x.to_dict() for x in dxy]
    a = len(dey)
    b = len(dry)
    [dry[x].update(dpy[x]) for x in range(b)]
    [dey[x].update(doy[x]) for x in range(a)]
    [dey[x].update(keya) for x in range(a)]
    [dey[x].update(dry[x]) for x in range(a)]
    return render(request, 'solicitacao_loja_ver.html', {'lista': dey, 't': key})


def solicitacao_loja_remover(request, token, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    if request.method == 'POST':
        db.collection("msg_destaca_loja").document(f"{id}").delete()
        return redirect('solicitacao_loja_remover_sucesso', token=token)
    return render(request, 'solicitacao_loja_remover.html', {'t': key})


def solicitacao_loja_remover_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'solicitacao_loja_remover_sucesso.html', {'t': key})


def banners_imagem(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    dados7 = db.collection('banners_principal').stream()
    dados8 = [{'id': x.id} for x in dados7]
    dados9 = db.collection('banners_principal').stream()
    dados10 = [x.to_dict() for x in dados9]
    b = len(dados8)
    [dados8[x].update(dados10[x]) for x in range(b)]
    if usa == []:
        return redirect('login')

    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        dados = db.collection('banners_principal').stream()
        dados2 = [{'id': x.id} for x in dados]
        dados3 = db.collection('banners_principal').stream()
        dados4 = [x.to_dict() for x in dados3]
        a = len(dados2)
        [dados2[x].update(dados4[x]) for x in range(a)]
        arquivo = sto.blob(f"banners_principal/{dados2[0]['id']}/{img}")
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        dados5 = db.collection('banners_principal').stream()
        dados6 = [{'id': x.id} for x in dados5]
        formform = db.collection(f'banners_principal').document(f"{dados6[0]['id']}")
        formform.update({
            'img': firestore.ArrayUnion([f'{url}'])
        })

        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('banners_imagem_sucesso', token=token)
    return render(request, 'banners_imagem.html', {'t': key, 'lista': dados8})


def banners_imagem_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'banners_imagem_sucesso.html', {'t': key})


def banners_imagem_remover(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados = db.collection('banners_principal').stream()
    dados2 = [{'id': x.id} for x in dados]
    dados3 = db.collection('banners_principal').stream()
    dados4 = [x.to_dict() for x in dados3]
    a = len(dados2)
    [dados2[x].update(dados4[x]) for x in range(a)]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        formform = db.collection(f'banners_principal').document(f"{dados2[0]['id']}")
        formform.update({
            'img': firestore.ArrayRemove([f'{imagem}'])
        })
        return redirect('banners_imagem_remover_sucesso', token=token)
    return render(request, 'banners_imagem_remover.html', {'t': key, 'lista': dados2})


def banners_imagem_remover_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'banners_imagem_remover_sucesso.html', {'t': key})


def dicas_mix_imagens(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados7 = db.collection('dicas_mix_lojas').stream()
    dados8 = [{'id': x.id} for x in dados7]
    dados9 = db.collection('dicas_mix_lojas').stream()
    dados10 = [x.to_dict() for x in dados9]
    b = len(dados8)
    [dados8[x].update(dados10[x]) for x in range(b)]
    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        dados = db.collection('dicas_mix_lojas').stream()
        dados2 = [{'id': x.id} for x in dados]
        dados3 = db.collection('dicas_mix_lojas').stream()
        dados4 = [x.to_dict() for x in dados3]
        a = len(dados2)
        [dados2[x].update(dados4[x]) for x in range(a)]
        arquivo = sto.blob(f"dicas_mix_lojas/{dados2[0]['id']}/{img}")
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        formform = db.collection(f'dicas_mix_lojas').document()
        formform.set({
            'img': f"{url}"
        })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('dicas_mix_imagens_sucesso', token=token)
    return render(request, 'dicas_mix_imagens.html', {'t': key, 'lista': dados8})


def dicas_mix_imagens_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'dicas_mix_imagens_sucesso.html', {'t': key})


def dicas_mix_imagens_remover(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados = db.collection('dicas_mix_lojas').stream()
    dados2 = [{'id': x.id} for x in dados]
    dados3 = db.collection('dicas_mix_lojas').stream()
    dados4 = [x.to_dict() for x in dados3]
    a = len(dados2)
    [dados2[x].update(dados4[x]) for x in range(a)]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        db.collection(f'dicas_mix_lojas').document(f"{imagem}").delete()
        return redirect('dicas_mix_imagens_remover_sucesso', token=token)
    return render(request, 'dicas_mix_imagens_remover.html', {'t': key, 'lista': dados2})


def dicas_mix_imagens_remover_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'dicas_mix_imagens_remover_sucesso.html', {'t': key})


def dicas_mix_imagens_desapegos(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados7 = db.collection('dicas_mix_desapegos').stream()
    dados8 = [{'id': x.id} for x in dados7]
    dados9 = db.collection('dicas_mix_desapegos').stream()
    dados10 = [x.to_dict() for x in dados9]
    b = len(dados8)
    [dados8[x].update(dados10[x]) for x in range(b)]
    if request.method == 'POST':
        img = request.FILES['img']
        imagem_mix = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix.save()
        dados = db.collection('dicas_mix_desapegos').stream()
        dados2 = [{'id': x.id} for x in dados]
        dados3 = db.collection('dicas_mix_desapegos').stream()
        dados4 = [x.to_dict() for x in dados3]
        a = len(dados2)
        [dados2[x].update(dados4[x]) for x in range(a)]
        arquivo = sto.blob(f"dicas_mix_desapegos/{dados2[0]['id']}/{img}")
        arquivo.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        url = arquivo.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url = str(url)
        formform = db.collection(f'dicas_mix_desapegos').document()
        formform.set({
            'img': f"{url}"
        })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('dicas_mix_imagens_desapegos_sucesso', token=token)
    return render(request, 'dicas_mix_imagens_desapegos.html', {'t': key, 'lista': dados8})


def dicas_mix_imagens_desapegos_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'dicas_mix_imagens_desapegos_sucesso.html', {'t': key})


def dicas_mix_imagens_desapegos_remover(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    dados = db.collection('dicas_mix_desapegos').stream()
    dados2 = [{'id': x.id} for x in dados]
    dados3 = db.collection('dicas_mix_desapegos').stream()
    dados4 = [x.to_dict() for x in dados3]
    a = len(dados2)
    [dados2[x].update(dados4[x]) for x in range(a)]
    if request.method == 'POST':
        imagem = request.POST['imagem']
        db.collection(f'dicas_mix_desapegos').document(f"{imagem}").delete()
        return redirect('dicas_mix_imagens_desapegos_remover_sucesso', token=token)
    return render(request, 'dicas_mix_imagens_desapegos_remover.html', {'t': key, 'lista': dados2})


def dicas_mix_imagens_desapegos_remover_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    return render(request, 'dicas_mix_imagens_desapegos_remover_sucesso.html', {'t': key})


def politica_privacidade(request):
    return render(request, 'politica_privacidade.html')


def termos_uso(request):
    return render(request, 'termos_uso.html')


def solicitacao_exclusao_dados(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        abc = db.collection('solicitacao_exclusao_dados').document()
        abc.set({
            'email': f"{email}",
            'username': f"{username}"
        })
        return redirect('solicitacao_exclusao_dados_sucesso')
    return render(request, 'solicitacao_exclusao_dados.html')


def solicitacao_exclusao_dados_sucesso(request):
    return render(request, 'solicitacao_exclusao_dados_sucesso.html')


def solicitacao_exclusao_dados_listagem(request, token):
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(token)
    us = db.collection('admin').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('login')
    usuarios = db.collection('solicitacao_exclusao_dados').stream()
    docs = [{'id': x.id} for x in usuarios]
    ident = db.collection('solicitacao_exclusao_dados').stream()
    doz = [x.to_dict() for x in ident]
    a = len(docs)
    [docs[x].update(doz[x]) for x in range(a)]
    [docs[x].update(keya) for x in range(a)]
    return render(request, 'solicitacao_exclusao_dados_listagem.html', {'lista': docs, 't': key})


'''
# PARTE DE USUARIO
def user_criar_loja(request, token):
    key = [str(token)]
    user = auth.get_user(str(token))
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]

    if usa == []:
        return redirect('index', token=token)
    if request.method == 'POST':
        email = str(user.email)
        name = request.POST['name']
        categoria = request.POST['categoria']
        whatsapp = request.POST['whatsapp']
        trabalhe_conosco = request.POST['trabalhe_conosco']
        price = request.POST['price']
        cep = request.POST['cep']
        img = request.FILES['img']
        img_destacados = request.FILES['img_destacados']
        img_ofertas = request.FILES['img_ofertas']
        img_cupons = request.FILES['img_cupons']
        dex = False
        price = price.replace(',', '.')
        price = float(price)
        dados = db.collection(f'categorias/{categoria}/lojas').document()
        if cep != "":
            url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
            headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
            link = requests.get(url, headers=headers, verify=False)
            cde = link.json()
        else:
            cde = {}
        imagem_mix1 = IMAGEM_MIX.objects.create(imagem=img)
        imagem_mix2 = IMAGEM_MIX.objects.create(imagem=img_cupons)
        imagem_mix3 = IMAGEM_MIX.objects.create(imagem=img_ofertas)
        imagem_mix4 = IMAGEM_MIX.objects.create(imagem=img_destacados)
        imagem_mix1.save()
        imagem_mix2.save()
        imagem_mix3.save()
        imagem_mix4.save()
        arquivo1 = sto.blob(f'categorias/{categoria}/{token}/{img}')
        arquivo2 = sto.blob(f'categorias/{categoria}/{token}/{img_cupons}')
        arquivo3 = sto.blob(f'categorias/{categoria}/{token}/{img_ofertas}')
        arquivo4 = sto.blob(f'categorias/{categoria}/{token}/{img_destacados}')
        arquivo1.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img}")
        arquivo2.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img_cupons}")
        arquivo3.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img_ofertas}")
        arquivo4.upload_from_filename(f"/app/mix_brasil/settings/imagem/{img_destacados}")
        url1 = arquivo1.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url2 = arquivo2.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url3 = arquivo3.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        url4 = arquivo4.generate_signed_url(
            expiration=datetime.timedelta(weeks=200),
            method="GET",
        )
        dados.set({
            'name': f'{name}',
            'idCat': f'{categoria}',
            'whatsapp': f'{whatsapp}',
            'trabalhe_conosco': f'{trabalhe_conosco}',
            'price': price,
            'destaque': dex,
            'promocao': "",
            'img': firestore.ArrayUnion([f"{url1}"]),
            'img_destacados': firestore.ArrayUnion([f"{url4}"]),
            'img_ofertas': firestore.ArrayUnion([f"{url3}"]),
            'img_cupons': firestore.ArrayUnion([f"{url2}"]),
            'cidade': f"{cde['cidade']['nome']}",
            'estado': f"{cde['estado']['sigla']}",
            'uemail': f"{email}",
            'views': 0,
            'viewsWhats': 0,
            'user': f'{str(token)}',

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

        des = db.collection(f'users').where('email', '==', f'{email}').stream()
        pka = [{'id': x.id} for x in des]
        for y in pka:
            fad = db.collection(f"users/{y['id']}/loja").document()
            fad.set({
                'name': f'{name}',
                'idCat': f'{categoria}',
                'whatsapp': f'{whatsapp}',
                'trabalhe_conosco': f'{trabalhe_conosco}',
                'price': price,
                'destaque': dex,
                'promocao': "",
                'img': firestore.ArrayUnion([f"{url1}"]),
                'img_destacados': firestore.ArrayUnion([f"{url4}"]),
                'img_ofertas': firestore.ArrayUnion([f"{url3}"]),
                'img_cupons': firestore.ArrayUnion([f"{url2}"]),
                'cidade': f"{cde['cidade']['nome']}",
                'estado': f"{cde['estado']['sigla']}",
                'uemail': f"{email}",
                'idAds': f"{ff[0]['id']}",
                'views': 0,
                'viewsWhats': 0,
                'user': f'{str(token)}',
            })
        abx = db.collection(f"users/{token}/loja").where('uemail', '==', f'{email}').stream()
        abv = [{'id': x.id} for x in abx]
        pvc = db.collection(f"categorias/{categoria}/lojas").where('uemail', '==', f'{email}').stream()
        pvcz = [{'id': x.id} for x in pvc]
        apv = db.collection(f"categorias/{categoria}/lojas").document(f"{pvcz[0]['id']}")
        apv.update({
            'idAdsUser': f"{abv[0]['id']}"
        })
        return redirect('user_criar_loja_sucesso', token=token)
    return render(request, 'user_criar_loja.html', {'t': key})


def user_criar_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(str(token))
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_criar_loja_sucesso.html', {'t': key})


def user_loja_dados(request, token):
    key = [str(token)]
    keya = {'token': str(token)}
    user = auth.get_user(str(token))
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    cep = request.GET.get("cep")
    if cep != "":
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        headers = {'Authorization': 'Token token=866968b5a2faee988b72d9c44dc63d52'}
        link = requests.get(url, headers=headers, verify=False)
        cde = link.json()
    else:
        cde = {}
    email = user.email
    dados = db.collection('users').where('email', '==', f'{email}').stream()
    y = [{'id': x.id} for x in dados]
    dadoss = db.collection('users').where('email', '==', f'{email}').stream()
    yx = [{'id': x.id} for x in dadoss]
    con = db.collection(f"users/{y[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
    abc = [{'id': x.id} for x in con]
    cen = db.collection(f"users/{yx[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
    xyz = [x.to_dict() for x in cen]
    la = len(abc)
    [abc[x].update(xyz[x]) for x in range(la)]
    [abc[x].update(cde) for x in range(la)]
    [abc[x].update(keya) for x in range(la)]
    dados2 = db.collection('users').where('email', '==', f'{email}').stream()
    y2 = [{'id': x.id} for x in dados2]
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
        can = db.collection(f"users/{y2[0]['id']}/loja").document(f"{abc[0]['id']}")
        can.update({
            'name': f'{name}',
            'whatsapp': f'{whatsapp}',
            'trabalhe_conosco': f'{trabalheconosco}',
            'price': price,
            'promocao': f"{promocao}",
            'cidade': f"{cidade}",
            'estado': f"{estado}",
        })
        dadosx = db.collection('users').where('email', '==', f'{email}').stream()
        y7 = [{'id': x.id} for x in dadosx]
        dados3 = db.collection('users').where('email', '==', f'{email}').stream()
        y3 = [{'id': x.id} for x in dados3]
        con3 = db.collection(f"users/{y3[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
        abc3 = [{'id': x.id} for x in con3]
        cen3 = db.collection(f"users/{y7[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
        xyz3 = [x.to_dict() for x in cen3]
        op = len(abc3)
        [abc3[x].update(xyz3[x]) for x in range(op)]
        a = db.collection('users').where('email', '==', f'{email}').stream()
        b = [{'id': x.id} for x in a]
        g = db.collection('users').where('email', '==', f'{email}').stream()
        h = [{'id': x.id} for x in g]
        c = db.collection(f"users/{b[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
        d = [{'id': x.id} for x in c]
        e = db.collection(f"users/{h[0]['id']}/loja").where('uemail', '==', f'{email}').stream()
        f = [x.to_dict() for x in e]
        laxa = len(d)
        [d[x].update(f[x]) for x in range(laxa)]
        final = db.collection(f"categorias/{abc3[0]['idCat']}/lojas").document(f"{d[0]['idAds']}")
        final.update({
            'name': f'{name}',
            'whatsapp': f'{whatsapp}',
            'trabalhe_conosco': f'{trabalheconosco}',
            'price': price,
            'promocao': f"{promocao}",
            'cidade': f"{cidade}",
            'estado': f"{estado}",
        })
        return redirect('user_loja_dados_sucesso', token=token)
    return render(request, 'user_loja_dados.html', {'lista': abc, 't': key})


def user_loja_dados_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_loja_dados_sucesso.html', {'t': key})


def user_adicionar_imagem(request, token, cat, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    ac = db.collection(f"categorias/{cat}/lojas").where('uemail', '==', f'{user.email}').stream()
    ad = [{'id': x.id} for x in ac]
    if request.method == 'POST':
        tipo_imagem = request.POST['tipo_imagem']
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
        formform = db.collection(f'categorias/{cat}/lojas').document(ad[0]['id'])
        if tipo_imagem == 'normal':
            formform.update({
                'img': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'ofertas':
            formform.update({
                'img_ofertas': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'destacados':
            formform.update({
                'img_destacados': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'cupons':
            formform.update({
                'img_cupons': firestore.ArrayUnion([f'{url}'])
            })
        ffa = db.collection(f'users').where('email', '==', f'{user.email}').stream()
        yas = [{'id': x.id} for x in ffa]
        forfor = db.collection(f"users/{yas[0]['id']}/loja").where('uemail', '==', f'{user.email}').stream()
        fsa = [{'id': x.id} for x in forfor]
        ffae = db.collection(f'users').where('email', '==', f'{user.email}').stream()
        yase = [{'id': x.id} for x in ffae]
        final_final = db.collection(f"users/{yase[0]['id']}/loja").document(f"{fsa[0]['id']}")
        if tipo_imagem == 'normal':
            final_final.update({
                'img': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'ofertas':
            final_final.update({
                'img_ofertas': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'destacados':
            final_final.update({
                'img_destacados': firestore.ArrayUnion([f'{url}'])
            })
        elif tipo_imagem == 'cupons':
            final_final.update({
                'img_cupons': firestore.ArrayUnion([f'{url}'])
            })
        else:
            final_final.update({
                'img': firestore.ArrayUnion([f'{url}'])
            })
        IMAGEM_MIX.objects.all().delete()
        os.remove(f"/app/mix_brasil/settings/imagem/{img}")
        return redirect('user_adicionar_imagem_sucesso', token=token, cat=cat, id=id)
    return render(request, 'user_adicionar_imagem.html', {'t': key})


def user_adicionar_imagem_sucesso(request, token, cat, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    dados = [{'cat': cat, 'id': id, 'token': token}]
    return render(request, 'user_adicionar_imagem_sucesso.html', {'t': key, 'lista': dados})


def user_remover_imagens(request, token, cat, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    ac = db.collection(f"categorias/{cat}/lojas").where('uemail', '==', f'{user.email}').stream()
    ad = [{'id': x.id} for x in ac]
    ae = db.collection(f"categorias/{cat}/lojas").where('uemail', '==', f'{user.email}').stream()
    docs = [x.to_dict() for x in ae]
    lixo1 = request.GET.get('lixo1')
    lixo2 = request.GET.get('lixo1')
    lixo3 = request.GET.get('lixo1')
    lixo4 = request.GET.get('lixo1')
    imagem1 = request.GET.get('imagem1')
    imagem2 = request.GET.get('imagem2')
    imagem3 = request.GET.get('imagem3')
    imagem4 = request.GET.get('imagem4')
    formform = db.collection(f'categorias/{cat}/lojas').document(ad[0]['id'])
    if lixo1 == 'normal':
        formform.update({
            'img': firestore.ArrayRemove([f'{imagem1}'])
        })
    elif lixo2 == 'ofertas':
        formform.update({
            'img_ofertas': firestore.ArrayRemove([f'{imagem2}'])
        })
    elif lixo3 == 'destacados':
        formform.update({
            'img_destacados': firestore.ArrayRemove([f'{imagem3}'])
        })
    elif lixo4 == 'cupons':
        formform.update({
            'img_cupons': firestore.ArrayRemove([f'{imagem4}'])
        })
    ffa = db.collection(f'users').where('email', '==', f'{user.email}').stream()
    yas = [{'id': x.id} for x in ffa]
    forfor = db.collection(f"users/{yas[0]['id']}/loja").where('uemail', '==', f'{user.email}').stream()
    fsa = [{'id': x.id} for x in forfor]
    ffae = db.collection(f'users').where('email', '==', f'{user.email}').stream()
    yase = [{'id': x.id} for x in ffae]
    final_final = db.collection(f"users/{yase[0]['id']}/loja").document(f"{fsa[0]['id']}")
    if lixo1 == 'normal':
        final_final.update({
            'img': firestore.ArrayRemove([f'{imagem1}'])
        })
    elif lixo2 == 'ofertas':
        final_final.update({
            'img_ofertas': firestore.ArrayRemove([f'{imagem2}'])
        })
    elif lixo3 == 'destacados':
        final_final.update({
            'img_destacados': firestore.ArrayRemove([f'{imagem3}'])
        })
    elif lixo4 == 'cupons':
        final_final.update({
            'img_cupons': firestore.ArrayRemove([f'{imagem4}'])
        })
    return render(request, 'user_remover_imagens.html', {'lista': docs, 't': key})


def user_remover_imagens_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_loja_dados_sucesso.html', {'t': key})


def user_remover_loja(request, token, cat, id):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    if request.method == 'POST':
        papap = db.collection(f"categorias/{cat}/lojas").where('uemail', '==', f'{user.email}').stream()
        pas = [{'id': x.id} for x in papap]
        db.collection(f'categorias/{cat}/lojas').document(f"{pas[0]['id']}").delete()
        exa1 = db.collection(f'users').where('email', '==', f'{user.email}').stream()
        ex1 = [{'id': x.id} for x in exa1]
        exc = db.collection(f"users/{ex1[0]['id']}/loja").where('uemail', '==', f'{user.email}').stream()
        pa = [{'id': x.id} for x in exc]
        exa2 = db.collection(f'users').where('email', '==', f'{user.email}').stream()
        ex2 = [{'id': x.id} for x in exa2]
        db.collection(f"users/{ex2[0]['id']}/loja").document(f"{pa[0]['id']}").delete()
        return redirect('user_remover_loja_sucesso', token=token)
    return render(request, 'user_remover_loja.html', {'t': key})


def user_remover_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_remover_loja_sucesso.html', {'t': key})


def user_enviar_solicitacao_loja(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    if request.method == 'POST':
        mensagem = request.POST['mensagem']
        dados = db.collection(f"users/{token}/loja").where('uemail', '==', f'{user.email}').stream()
        d = [{'id': x.id} for x in dados]
        dados2 = db.collection(f"users/{token}/loja").where('uemail', '==', f'{user.email}').stream()
        da = [x.to_dict() for x in dados2]
        a = len(d)
        [d[x].update(da[x]) for x in range(a)]
        soli = db.collection('msg_destaca_loja').document()
        soli.set({
            'name': f"{d[0]['name']}",
            'whatsapp': f"{d[0]['whatsapp']}",
            'email': f"{d[0]['uemail']}",
            'mensagem': f"{mensagem}",
            'categoria': f"{d[0]['idCat']}",
            'user': f"{d[0]['user']}"
        })
        return redirect('user_enviar_solicitacao_loja_sucesso', token=token)
    return render(request, 'user_enviar_solicitacao_loja.html', {'t': key})


def user_enviar_solicitacao_loja_sucesso(request, token):
    key = [str(token)]
    user = auth.get_user(token)
    us = db.collection('users').where('email', '==', f'{user.email}').stream()
    usa = [x.to_dict() for x in us]
    if usa == []:
        return redirect('index', token=token)
    return render(request, 'user_enviar_solicitacao_loja_sucesso.html', {'t': key})
'''
