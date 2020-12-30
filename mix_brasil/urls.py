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

    path('categoria_listagem/', views.categoria_listagem, name='categoria_listagem'),

    path('lojas_listagem/<str:id>', views.lojas_listagem, name='lojas_listagem'),

    path('lojas_dados/<str:name>/<str:lojas_listagem.id>', views.lojas_dados, name='lojas_dados')

]
