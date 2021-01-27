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

    path('index/', views.index, name='index'),

    path('categoria_listagem/', views.categoria_listagem, name='categoria_listagem'),
    path('lojas_listagem/<str:id>', views.lojas_listagem, name='lojas_listagem'),
    path('lojas_dados/<str:nome>/<str:id>/<str:cod>', views.lojas_dados, name='lojas_dados'),
    path('atualizar_loja_sucesso/', views.atualizar_loja_sucesso, name='atualizar_loja_sucesso'),
    path('criar_loja/<str:id>/', views.criar_loja, name='criar_loja'),
    path('criar_loja_sucesso/', views.criar_loja_sucesso, name='criar_loja_sucesso'),
    path('adicionar_imagens_loja/<str:id>/<str:cod>/', views.adicionar_imagens_loja, name='adicionar_imagens_loja'),
    path('adicionar_imagens_loja_sucesso/', views.adicionar_imagens_loja_sucesso,name='adicionar_imagens_loja_sucesso'),
    path('remover_imagens_loja/<str:id>/<str:name>/<str:cod>/', views.remover_imagens_loja,name='remover_imagens_loja'),
    path('remover_imagens_loja_sucesso/', views.remover_imagens_loja_sucesso, name='remover_imagens_loja_sucesso'),
    path('remover_loja/<str:id>/<str:cod>/', views.remover_loja, name='remover_loja'),
    path('remover_loja_sucesso/', views.remover_loja_sucesso, name='remover_loja_sucesso'),

    path('criar_desapego/<str:id>/', views.criar_desapego, name='criar_desapego'),
    path('criar_desapego_sucesso/', views.criar_desapego_sucesso, name='criar_desapego_sucesso'),
    path('categoria_desapego_listagem/', views.categoria_desapego_listagem, name='categoria_desapego_listagem'),
    path('desapegos_listagem/<str:id>/', views.desapegos_listagem, name='desapegos_listagem'),
    path('desapegos_dados/<str:id>/<str:nome>/<str:cod>/', views.desapegos_dados, name='desapegos_dados'),
    path('atualizar_desapego_sucesso/', views.atualizar_desapego_sucesso, name='atualizar_desapego_sucesso'),
    path('adicionar_imagens_desapego/<str:id>/<str:cod>/', views.adicionar_imagens_desapego,name='adicionar_imagens_desapego'),
    path('adicionar_imagens_desapego_sucesso/', views.adicionar_imagens_desapego_sucesso,name='adicionar_imagens_desapego_sucesso'),
    path('remover_imagens_desapego/<str:id>/<str:name>/<str:cod>/', views.remover_imagens_desapego,name='remover_imagens_desapego'),
    path('remover_imagens_desapego_sucesso/', views.remover_imagens_desapego_sucesso, name='remover_imagens_desapego_sucesso'),
    path('remover_desapego/<str:id>/<str:cod>/', views.remover_desapego, name='remover_desapego'),
    path('remover_desapego_sucesso/', views.remover_desapego_sucesso, name='remover_desapego_sucesso'),

    path('criar_usuario/', views.criar_usuario, name='criar_usuario'),
    path('criar_usuario_sucesso/', views.criar_usuario_sucesso, name='criar_usuario_sucesso'),
    path('usuario_dados/<str:id>/', views.usuario_dados, name='usuario_dados'),
    path('atualizar_usuario_sucesso/', views.atualizar_usuario_sucesso, name='atualizar_usuario_sucesso'),
    path('usuario_listagem/', views.usuario_listagem, name='usuario_listagem'),
    path('adicionar_imagem_perfil/<str:id>/', views.adicionar_imagem_perfil, name='adicionar_imagem_perfil'),
    path('remover_usuario/<str:id>/<str:email>/', views.remover_usuario, name='remover_usuario'),
    path('remover_usuario_sucesso/', views.remover_usuario_sucesso, name='remover_usuario_sucesso')
]
