from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request
from appFinal.models import Usuario
from appFinal.models import Seleccionado
from appFinal.models import Aparcamiento
from appFinal.models import Direccion
from appFinal.models import DatosContacto
from appFinal.models import Comentarios
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers

# Create your views here.

class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.inNombre = False
        self.inDescr = False
        self.inAcc = False
        self.inUrl = False
        self.inClVia = False
        self.inNomVia = False
        self.inNum = False
        self.inLocalidad = False
        self.inProv = False
        self.inCP = False
        self.inLat = False
        self.inLong = False
        self.inBarrio = False
        self.inDistrito = False
        self.inTlf = False
        self.inMail = False
        self.theContent = ""
        self.dicc = {'nom':'','des':'','acc':'','url':'','clvia':'','nomvia':'',
                     'num':'0','loc':'','prov':'','cp':'0','lat':'0','long':'0',
                     'bar':'', 'dis':'','tlf':'','mail':''}
        self.list_dic = []

    def startElement(self, name, attrs):
        if name == 'contenido':
            self.inItem = True
        elif self.inItem:
            if name == 'atributo':
                if attrs['nombre'] == 'NOMBRE':
                    self.inContent = True
                    self.inNombre = True
                elif attrs['nombre'] == 'DESCRIPCION':
                    self.inContent = True
                    self.inDescr = True
                elif attrs['nombre'] == 'ACCESIBILIDAD':
                    self.inContent = True
                    self.inAcc = True
                elif attrs['nombre'] == 'CONTENT-URL':
                    self.inContent = True
                    self.inUrl = True
                elif attrs['nombre'] == 'CLASE-VIAL':
                    self.inContent = True
                    self.inClVia = True
                elif attrs['nombre'] == 'NOMBRE-VIA':
                    self.inContent = True
                    self.inNomVia = True
                elif attrs['nombre'] == 'NUM':
                    self.inContent = True
                    self.inNum = True
                elif attrs['nombre'] == 'LOCALIDAD':
                    self.inContent = True
                    self.inLocalidad = True
                elif attrs['nombre'] == 'PROVINCIA':
                    self.inContent = True
                    self.inProv = True
                elif attrs['nombre'] == 'CODIGO-POSTAL':
                    self.inContent = True
                    self.inCP = True
                elif attrs['nombre'] == 'BARRIO':
                    self.inContent = True
                    self.inBarrio = True
                elif attrs['nombre'] == 'DISTRITO':
                    self.inContent = True
                    self.inDistrito = True
                elif attrs['nombre'] == 'LATITUD':
                    self.inContent = True
                    self.inLat = True
                elif attrs['nombre'] == 'LONGITUD':
                    self.inContent = True
                    self.inLong = True
                elif attrs['nombre'] == 'TELEFONO':
                    self.inContent = True
                    self.inTlf = True
                elif attrs['nombre'] == 'EMAIL':
                    self.inContent = True
                    self.inMail = True

    def endElement(self, name):
        if name == 'contenido':
            direccion = Direccion(claseVia=self.dicc['clvia'], nombreVia=self.dicc['nomvia'],
                                  numero=self.dicc['num'], localidad=self.dicc['loc'],
                                  provincia=self.dicc['prov'], cp=int(self.dicc['cp']))
            direccion.save()
            datCon = DatosContacto(telefono=self.dicc['tlf'], email=self.dicc['mail'])
            datCon.save()
            aparc = Aparcamiento(nombre=self.dicc['nom'],direccion=direccion,
                                 latitud=float(self.dicc['lat']),longitud=float(self.dicc['long']),
                                 descripcion=self.dicc['des'],barrio=self.dicc['bar'],
                                 distrito=self.dicc['dis'],datosContacto=datCon,
                                 url=self.dicc['url'], accesible=int(self.dicc['acc']))
            aparc.save()
            self.dicc = {'nom':'','des':'','acc':'','url':'','clvia':'','nomvia':'',
                         'num':'0','loc':'','prov':'','cp':'0','lat':'0','long':'0',
                         'bar':'', 'dis':'','tlf':'','mail':''}
            self.inItem = False
        elif self.inItem and self.inContent:
            if name == 'atributo':
                if self.inNombre:
                    self.dicc['nom'] = self.theContent
                    self.inNombre = False
                elif self.inDescr:
                    self.dicc['des'] = self.theContent
                    self.inDescr = False
                elif self.inAcc:
                    self.dicc['acc'] = self.theContent
                    self.inAcc = False
                elif self.inUrl:
                    self.dicc['url'] = self.theContent
                    self.inUrl = False
                elif self.inClVia:
                    self.dicc['clvia'] = self.theContent
                    self.inClVia = False
                elif self.inNomVia:
                    self.dicc['nomvia'] = self.theContent
                    self.inNomVia = False
                elif self.inNum:
                    self.dicc['num'] = self.theContent
                    self.inNum = False
                elif self.inLocalidad:
                    self.dicc['loc'] = self.theContent
                    self.inLocalidad = False
                elif self.inProv:
                    self.dicc['prov'] = self.theContent
                    self.inProv = False
                elif self.inCP:
                    self.dicc['cp'] = self.theContent
                    self.inCP = False
                elif self.inBarrio:
                    self.dicc['bar'] = self.theContent
                    self.inBarrio = False
                elif self.inDistrito:
                    self.dicc['dis'] = self.theContent
                    self.inDistrito = False
                elif self.inLat:
                    self.dicc['lat'] = self.theContent
                    self.inLat = False
                elif self.inLong:
                    self.dicc['long'] = self.theContent
                    self.inLong = False
                elif self.inTlf:
                    self.dicc['tlf'] = self.theContent
                    self.inTlf = False
                elif self.inMail:
                    self.dicc['mail'] = self.theContent
                    self.inMail = False

                self.theContent = ""
                self.inContent = False



    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def update(request):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    xmlFile = urllib.request.urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
    theParser.parse(xmlFile)

    return HttpResponseRedirect('/')


@csrf_exempt
def barra(request):
    aparc_coment = Aparcamiento.objects.exclude(numComents=0)
    list_coment = aparc_coment.order_by('-numComents')


    if request.method == "GET" or (request.method == "POST" and request.POST.get('boton') == '2'):
        value = 1
        texto = "Solo accesibles"
        list_aparcamientos = list_coment

    elif request.method == "POST" and request.POST.get('boton') == '1':
        value = 2
        texto = "Todos"
        list_aparcamientos = list_coment.filter(accesible=1)

    if len(list_aparcamientos) > 5:
        list_aparcamientos = list_aparcamientos[0:5]

    numAparc = Aparcamiento.objects.count()

    usuarios = User.objects.all()
    pagper = ""
    for us in usuarios:
        try:
            user = Usuario.objects.get(nombre=us.username)
            if user.tituloPag != "":
                nompag = user.tituloPag
            else:
                nompag = "Página de " + us.username
        except Usuario.DoesNotExist:
            nompag = "Página de " + us.username
        pagper += us.username + ": <a href='/" + us.username + "'>" + nompag + "</a></p1><br/><br/>"

    list_selec = []
    if request.user.is_authenticated():
        us_selec = Usuario.objects.get(nombre=request.user)
        aparc_user = Seleccionado.objects.filter(usuario=us_selec)
        aparc_selec = list(set(aparc_user.values_list('aparcamiento',flat=True)))
        for ap in aparc_selec:
            list_selec.append(Aparcamiento.objects.get(id=ap))

    plantilla = get_template("barra.html")
    contexto = Context({'selec': list_selec,
                    'numAparc': numAparc,
                    'list': list_aparcamientos,
                    'value': value,
                    'texto': texto,
                    'user': request.user,
                    'pagpers': pagper,
                    'curr1': 'id="current"',
                    'titulo':'Aparcamientos más comentados'})
    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def mylogin(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    usuario = Usuario.objects.get(nombre=username)

                except Usuario.DoesNotExist:
                    usuario = Usuario(nombre=username)
                    usuario.save()
    return HttpResponseRedirect('/')

@csrf_exempt
def mylogout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect('/')


@csrf_exempt
def aparcamientos(request):
    list_aparcamientos = Aparcamiento.objects.all()
    list_dist = list(set(Aparcamiento.objects.values_list('distrito',flat=True)))

    tit = "Todos los aparcamientos"
    list_aparcamientos_selec = list_aparcamientos
    if request.method == "POST":
        id = int(request.POST['DIST'])
        if id != 0:
            list_aparcamientos_selec = Aparcamiento.objects.filter(distrito=list_dist[id-1])
            if list_dist[id-1] == "":
                tit = "Aparcamientos sin distrito especificado"
            else:
                tit = "Aparcamientos en el distrito " + list_dist[id-1]

    list_selec = []
    if request.user.is_authenticated():
        us_selec = Usuario.objects.get(nombre=request.user)
        aparc_user = Seleccionado.objects.filter(usuario=us_selec)
        aparc_selec = list(set(aparc_user.values_list('aparcamiento',flat=True)))
        for ap in aparc_selec:
            list_selec.append(Aparcamiento.objects.get(id=ap))

    plantilla = get_template("aparcamientos.html")
    contexto = Context({'selec': list_selec,
                    'dist': list_dist,
                    'list':list_aparcamientos_selec,
                    'titDis': tit,
                    'user': request.user,
                    'curr2': 'id="current"',
                    'titulo':'Listado de aparcamientos'})
    return HttpResponse(plantilla.render(contexto))

def info(request, id):
    aparc = Aparcamiento.objects.get(id=id)

    comentarios = Comentarios.objects.filter(aparcamiento=aparc)

    plantilla = get_template("info.html")
    contexto = Context({'numcomen': len(comentarios),
                    'comentarios': comentarios,
                    'titulo': aparc.nombre,
                    'aparc': aparc,
                    'user': request.user})
    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def seleccionar(request):
    if request.method == "POST":
        aparc = Aparcamiento.objects.get(nombre=request.POST['selec'])
        usuario = Usuario.objects.get(nombre=request.user.username)
        fecha = datetime.now()
        selec = Seleccionado(usuario=usuario, fecha=fecha, aparcamiento=aparc)
        selec.save()
    return HttpResponseRedirect('/')

@csrf_exempt
def deseleccionar(request):
    if request.method == "POST":
        aparc = Aparcamiento.objects.get(nombre=request.POST['selec'])
        usuario = Usuario.objects.get(nombre=request.user.username)
        selec = Seleccionado.objects.get(aparcamiento=aparc, usuario=usuario)
        selec.delete()
    return HttpResponseRedirect('/')

def usuario(request, user):
    id = request.GET.get('id')

    if id == None:
        id = 0
    else:
        id = int(id)

    usuarios = User.objects.all()
    usernames = list(User.objects.values_list('username',flat=True))
    list_selec = []
    if user in usernames:
        pagper = ""
        try:
            usuario = Usuario.objects.get(nombre=user)
            if usuario.tituloPag != "":
                nompag = usuario.tituloPag
            else:
                nompag = "Página de " + user

            aparc_user = Seleccionado.objects.filter(usuario=usuario)[id:id+5]
            id += 5
            if id >= Seleccionado.objects.filter(usuario=usuario).count():
                id = 0
            aparc_selec = list(set(aparc_user.values_list('aparcamiento',flat=True)))
            for ap in aparc_selec:
                list_selec.append(Aparcamiento.objects.get(id=ap))

        except Usuario.DoesNotExist:
            nompag = "Página de " + user
    else:
        nompag = "No existe el usuario"

    plantilla = get_template("usuario.html")
    contexto = Context({'titulo': nompag,
                    'selec': aparc_user,
                    'user': request.user,
                    'userpag': user,
                    'id': id})
    return HttpResponse(plantilla.render(contexto))


def about(request):
    cuerpo = "SHEILA OLIVA MUÑOZ<br/><br/>FUNCIONAMIENTO......"
    plantilla = get_template("about.html")
    contexto = Context({'titulo': "Información",
                        'curr3': 'id="current"',})
    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def cambioTitulo(request):
    username = request.GET.get('user')
    if request.method == "POST":
        titulo = request.POST['titPag']
        user = Usuario.objects.get(nombre=username)
        user.tituloPag = titulo
        user.save()
    return HttpResponseRedirect('/' + username)


@csrf_exempt
def cambioEstilo(request):
    username = request.GET.get('user')
    if request.method == "POST":
        tamano = request.POST['tamLet']
        color = request.POST['COLOR']
        user = Usuario.objects.get(nombre=username)
        if tamano != "":
            user.letra = int(tamano)
        if color != "0":
            user.color = color
        user.save()
    return HttpResponseRedirect('/' + username)

@csrf_exempt
def addComentario(request):
    aparcid = request.GET.get('ap')
    if request.method == "POST":
        aparc = Aparcamiento.objects.get(id=aparcid)
        aparc.numComents = aparc.numComents + 1
        aparc.save()
        comen = request.POST['comen']
        comentario = Comentarios(aparcamiento=aparc, texto=comen)
        comentario.save()
    return HttpResponseRedirect('/aparcamientos/' + aparcid)

@csrf_exempt
def xml(request, user):
    if request.method == "POST":
        usuario = Usuario.objects.get(nombre=user)
        selec = Seleccionado.objects.filter(usuario=usuario)

        contexto = Context({'user': user,
                            'selec': selec})
        plantilla = get_template("planxml.xml")
        return HttpResponse(plantilla.render(contexto), content_type="text/xml")


def css(request):
    plantilla = get_template("style.css")
    if request.user.is_authenticated():
        usuario = Usuario.objects.get(nombre=request.user.username)
        color = usuario.color
        letra = str(usuario.letra)
        letra2 = str(usuario.letra - 4)
        if color != "" and letra != 0:
            contexto = Context({'color': color,
                            'letra': letra,
                            'letra2': letra2})
        elif color != "" and letra == 0:
            contexto = Context({'color': color})
        elif color == "" and letra != 0:
            contexto = Context({'letra': letra,
                            'letra2': letra2})
        else:
            contexto = Context({})
        return HttpResponse(plantilla.render(contexto), content_type="text/css")
    else:
        return HttpResponse(plantilla.render(), content_type="text/css")
