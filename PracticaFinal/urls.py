"""PracticaFinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from appFinal import views
from django.contrib.auth.views import logout, login

urlpatterns = [
    url(r'^$', views.barra),
    url(r'^update$', views.update),
    url(r'^aparcamientos$', views.aparcamientos),
    url(r'^aparcamientos/(\d+)$', views.info),
    url(r'^about$', views.about),
    url(r'^seleccionar$', views.seleccionar),
    url(r'^deseleccionar$', views.deseleccionar),
    url(r'^cambiarTitulo$', views.cambioTitulo),
    url(r'^cambiarEstilo$', views.cambioEstilo),
    url(r'^addComentario$', views.addComentario),
    url(r'^login$', views.mylogin),
    url(r'^logout$', views.mylogout),
    url(r'^css/style\.css$', views.css),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'static/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(.+)/xml$', views.xml),
    url(r'^(.+)', views.usuario),
]
