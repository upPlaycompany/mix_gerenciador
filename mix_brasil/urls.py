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
    path('/deslogar', views.deslogar, name='deslogar'),

    path('index/', views.index, name='index'),

    path('academia_suplementos_lojas/', views.academia_suplementos_lojas, name='academia_suplementos_lojas'),

    path('agencia_viagens_lojas/', views.agencia_viagens_lojas, name='agencia_viagens_lojas'),

    path('automoveis_lojas/', views.automoveis_lojas, name='automoveis_lojas'),

    path('brinquedos_lojas/', views.brinquedos_lojas, name='brinquedos_lojas'),

    path('cama_mesa_banho_lojas/', views.cama_mesa_banho_lojas, name='cama_mesa_banho_lojas')

]
