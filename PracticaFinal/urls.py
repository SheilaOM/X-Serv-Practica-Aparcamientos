#############################
# Seila Oliva Muñoz         #
#############################
# Ingeniería en Tecnologías #
# de la Telecomunicación    #
#############################

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
    url(r'^$', views.barra, name='Pagina principal'),
    url(r'^update$', views.update, name='Carga los datos de aparcamientos'),
    url(r'^aparcamientos$', views.aparcamientos, name='Página con todos los aparcamientos'),
    url(r'^aparcamientos/(\d+)$', views.info, name='Página con información de cada aparcamiento'),
    url(r'^about$', views.about, name='Información de la práctica'),
    url(r'^seleccionar$', views.seleccionar, name='Selecciona aparcamiento'),
    url(r'^deseleccionar$', views.deseleccionar, name='Deselecciona aparcamiento'),
    url(r'^cambiarTitulo$', views.cambioTitulo, name='Cambia titulo de la página personal'),
    url(r'^cambiarEstilo$', views.cambioEstilo, name='Cambia estilo de la página de un usuario'),
    url(r'^addComentario$', views.addComentario, name='Añade comentario a aparcamiento'),
    url(r'^login$', views.mylogin, name='Loguea a un usuario'),
    url(r'^logout$', views.mylogout, name='Desloguea a un usuario'),
    url(r'^css/style\.css$', views.css, name='Estilo CSS'),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'static/'}, name='Pide las imágenes'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^canal(.+)$', views.barracanal, name='Genera canal XML o JSON de la página principal'),
    url(r'^punt$', views.sumpunt, name='Suma puntuación al aparcamiento'),
    url(r'^(.+)/(.+)$', views.usercanal, name='Genera canal XML o JSON de la página de un usuario'),
    url(r'^(.+)', views.usuario, name='Página personal de un usuario'),
]
