"""mix_brasil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.logar, name='logar'),
    path('login_erro/', views.login_erro, name='login_erro'),
    path('deslogar', views.deslogar, name='deslogar'),

    path('index/<str:token>/', views.index, name='index'),
    path('categoria_listagem/<str:token>/', views.categoria_listagem, name='categoria_listagem'),
    path('lojas_listagem/<str:token>/<str:id>', views.lojas_listagem, name='lojas_listagem'),
    path('lojas_dados/<str:token>/<str:nome>/<str:id>/<str:cod>', views.lojas_dados, name='lojas_dados'),
    path('atualizar_loja_sucesso/<str:token>/', views.atualizar_loja_sucesso, name='atualizar_loja_sucesso'),
    #path('criar_loja/<str:token>/<str:id>/', views.criar_loja, name='criar_loja'),
    #path('criar_loja_sucesso/<str:token>/', views.criar_loja_sucesso, name='criar_loja_sucesso'),
    #path('adicionar_imagens_loja/<str:token>/<str:id>/<str:cod>/', views.adicionar_imagens_loja, name='adicionar_imagens_loja'),
    #path('adicionar_imagens_loja_sucesso/<str:token>/', views.adicionar_imagens_loja_sucesso,name='adicionar_imagens_loja_sucesso'),
    #path('remover_imagens_loja/<str:token>/<str:id>/<str:name>/<str:cod>/', views.remover_imagens_loja,name='remover_imagens_loja'),
    #path('remover_imagens_loja_sucesso/<str:token>/', views.remover_imagens_loja_sucesso, name='remover_imagens_loja_sucesso'),
    path('remover_loja/<str:token>/<str:id>/<str:cod>/', views.remover_loja, name='remover_loja'),
    path('remover_loja_sucesso/<str:token>/', views.remover_loja_sucesso, name='remover_loja_sucesso'),
    path('notificacao/<str:token>/', views.notificacao, name='notificacao'),
    path('notificacao_sucesso/<str:token>/', views.notificacao_sucesso, name='notificacao_sucesso'),
    path('solicitacao_loja_listagem/<str:token>/', views.solicitacao_loja_listagem, name='solicitacao_loja_listagem'),
    path('solicitacao_loja_ver/<str:token>/<str:cat>/<str:name>/', views.solicitacao_loja_ver, name='solicitacao_loja_ver'),
    path('solicitacao_loja_remover/<str:token>/<str:id>/', views.solicitacao_loja_remover, name='solicitacao_loja_remover'),
    path('solicitacao_loja_remover_sucesso/<str:token>/', views.solicitacao_loja_remover_sucesso, name='solicitacao_loja_remover_sucesso'),
    path('solicitacao_desapego_listagem/<str:token>/', views.solicitacao_desapego_listagem, name='solicitacao_desapego_listagem'),
    path('solicitacao_desapego_ver/<str:token>/<str:name>/', views.solicitacao_desapego_ver, name='solicitacao_desapego_ver'),
    path('solicitacao_desapego_remover/<str:token>/<str:id>/', views.solicitacao_desapego_remover, name='solicitacao_desapego_remover'),
    path('solicitacao_desapego_remover_sucesso/<str:token>/', views.solicitacao_desapego_remover_sucesso, name='solicitacao_desapego_remover_sucesso'),

    #path('criar_desapego/<str:token>/<str:id>/', views.criar_desapego, name='criar_desapego'),
    #path('criar_desapego_sucesso/<str:token>/', views.criar_desapego_sucesso, name='criar_desapego_sucesso'),
    path('categoria_desapego_listagem/<str:token>/', views.categoria_desapego_listagem, name='categoria_desapego_listagem'),
    path('desapegos_listagem/<str:token>/<str:id>/', views.desapegos_listagem, name='desapegos_listagem'),
    path('desapegos_dados/<str:token>/<str:id>/<str:nome>/<str:cod>/', views.desapegos_dados, name='desapegos_dados'),
    path('atualizar_desapego_sucesso/<str:token>/', views.atualizar_desapego_sucesso, name='atualizar_desapego_sucesso'),
    #path('adicionar_imagens_desapego/<str:token>/<str:id>/<str:cod>/', views.adicionar_imagens_desapego,name='adicionar_imagens_desapego'),
    #path('adicionar_imagens_desapego_sucesso/<str:token>/', views.adicionar_imagens_desapego_sucesso,name='adicionar_imagens_desapego_sucesso'),
    #path('remover_imagens_desapego/<str:token>/<str:id>/<str:name>/<str:cod>/', views.remover_imagens_desapego,name='remover_imagens_desapego'),
    #path('remover_imagens_desapego_sucesso/<str:token>/', views.remover_imagens_desapego_sucesso, name='remover_imagens_desapego_sucesso'),
    path('remover_desapego/<str:token>/<str:id>/<str:cod>/', views.remover_desapego, name='remover_desapego'),
    path('remover_desapego_sucesso/<str:token>/', views.remover_desapego_sucesso, name='remover_desapego_sucesso'),
    path('banners_imagem/<str:token>/', views.banners_imagem, name='banners_imagem'),
    path('banners_imagem_sucesso/<str:token>/', views.banners_imagem_sucesso, name='banners_imagem_sucesso'),
    path('banners_imagem_remover/<str:token>/', views.banners_imagem_remover, name='banners_imagem_remover'),
    path('banners_imagem_remover_sucesso/<str:token>/', views.banners_imagem_remover_sucesso, name='banners_imagem_remover_sucesso'),
    path('dicas_mix_imagens/<str:token>/', views.dicas_mix_imagens, name='dicas_mix_imagens'),
    path('dicas_mix_imagens_sucesso/<str:token>/', views.dicas_mix_imagens_sucesso, name='dicas_mix_imagens_sucesso'),
    path('dicas_mix_imagens_remover/<str:token>/', views.dicas_mix_imagens_remover, name='dicas_mix_imagens_remover'),
    path('dicas_mix_imagens_remover_sucesso/<str:token>/', views.dicas_mix_imagens_remover_sucesso, name='dicas_mix_imagens_remover_sucesso'),

    #path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    #path('criar_usuario_sucesso/', views.criar_usuario_sucesso, name='criar_usuario_sucesso'),
    path('usuario_dados/<str:token>/<str:id>/', views.usuario_dados, name='usuario_dados'),
    path('atualizar_usuario_sucesso/<str:token>/', views.atualizar_usuario_sucesso, name='atualizar_usuario_sucesso'),
    path('usuario_listagem/<str:token>/', views.usuario_listagem, name='usuario_listagem'),
    #path('adicionar_imagem_perfil/<str:token>/<str:id>/', views.adicionar_imagem_perfil, name='adicionar_imagem_perfil'),
    path('remover_usuario/<str:token>/<str:id>/<str:e>/', views.remover_usuario, name='remover_usuario'),
    path('remover_usuario_sucesso/<str:token>/', views.remover_usuario_sucesso, name='remover_usuario_sucesso'),


    #path('user_index/<str:token>/', views.user_index, name='user_index'),
    #path('user_criar_loja/<str:token>/', views.user_criar_loja, name='user_criar_loja'),
    #path('user_criar_loja_sucesso/<str:token>/', views.user_criar_loja_sucesso, name='user_criar_loja_sucesso'),
    #path('user_loja_dados/<str:token>/', views.user_loja_dados, name='user_loja_dados'),
    #path('user_loja_dados_sucesso/<str:token>/', views.user_loja_dados_sucesso, name='user_loja_dados_sucesso'),
    #path('user_adicionar_imagem/<str:token>/<str:cat>/<str:id>/', views.user_adicionar_imagem, name='user_adicionar_imagem'),
    #path('user_adicionar_imagem_sucesso/<str:token>/<str:cat>/<str:id>/', views.user_adicionar_imagem_sucesso, name='user_adicionar_imagem_sucesso'),
    #path('user_remover_loja/<str:token>/<str:cat>/<str:id>/', views.user_remover_loja, name='user_remover_loja'),
    #path('user_remover_loja_sucesso/<str:token>/', views.user_remover_loja_sucesso, name='user_remover_loja_sucesso'),
    #path('user_remover_imagens/<str:token>/<str:cat>/<str:id>/', views.user_remover_imagens, name='user_remover_imagens'),
    #path('user_remover_imagens_sucesso/<str:token>/', views.user_remover_imagens_sucesso, name='user_remover_imagens_sucesso'),
    #path('user_enviar_solicitacao_loja/<str:token>/', views.user_enviar_solicitacao_loja, name='user_enviar_solicitacao_loja'),
    #path('user_enviar_solicitacao_loja_sucesso/<str:token>/', views.user_enviar_solicitacao_loja_sucesso, name='user_enviar_solicitacao_loja_sucesso'),

]
