#############################
# Seila Oliva Muñoz         #
#############################
# Ingeniería en Tecnologías #
# de la Telecomunicación    #
#############################

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
#Descarta los aparcamientos sin comentarios y ordena el resto por número de comentarios
    aparc_coment = Aparcamiento.objects.exclude(numComents=0)
    list_coment = aparc_coment.order_by('-numComents')

#Obtiene todos los tipos de aparcamiento o sólo los accesibles
    if request.method == "GET" or (request.method == "POST" and request.POST.get('boton') == '2'):
        value = 1
        texto = "Solo accesibles"
        list_aparcamientos = list_coment

    elif request.method == "POST" and request.POST.get('boton') == '1':
        value = 2
        texto = "Todos"
        list_aparcamientos = list_coment.filter(accesible=1)

#Coge sólo los 5 aparcamientos más comentados
    if len(list_aparcamientos) > 5:
        list_aparcamientos = list_aparcamientos[0:5]

    numAparc = Aparcamiento.objects.count()

#Obtiene los usuarios para indicar las páginas personales de cada uno
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

#Comprueba si el usuario está autenticado, y en ese caso, obtiene los aparcamientos que ha seleccionado
#para poner botón de seleccionar/deseleccionar
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
#Comprueba si el usuario introducido es válido y lo loguea.
#Comprueba si el usuario está ya en la base de datos, y si no está se introduce
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
    list_dist = list(set(Aparcamiento.objects.values_list('distrito',flat=True)))   #Obtiene lista de distritos

    tit = "Todos los aparcamientos"
    list_aparcamientos_selec = list_aparcamientos

#Llega un POST con el id del distrito buscado. Selecciona los aparcamientos de dicho distrito.
    if request.method == "POST":
        id = int(request.POST['DIST'])
        if id != 0:
            list_aparcamientos_selec = Aparcamiento.objects.filter(distrito=list_dist[id-1])
            if list_dist[id-1] == "":
                tit = "Aparcamientos sin distrito especificado"
            else:
                tit = "Aparcamientos en el distrito " + list_dist[id-1]

#Comprueba si el usuario está autenticado, y en ese caso, obtiene los aparcamientos que ha seleccionado
#para poner botón de seleccionar/deseleccionar
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
#Obtiene el aparcamiento que corresponde al id y sus comentarios, se lo pasa a la plantilla
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
#En la Query String viene la página donde se ha hecho la selección para redirigir de nuevo a esa página
    pag = request.GET.get('pag')
#Añade una selección a la base de datos
    if request.method == "POST":
        aparc = Aparcamiento.objects.get(nombre=request.POST['selec'])
        usuario = Usuario.objects.get(nombre=request.user.username)
        fecha = datetime.now()
        selec = Seleccionado(usuario=usuario, fecha=fecha, aparcamiento=aparc)
        selec.save()
    return HttpResponseRedirect(pag)


@csrf_exempt
def deseleccionar(request):
#En la Query String viene la página donde se ha hecho la selección para redirigir de nuevo a esa página

    pag = request.GET.get('pag')
#Elimina una selección de la base de datos
    if request.method == "POST":
        aparc = Aparcamiento.objects.get(nombre=request.POST['selec'])
        usuario = Usuario.objects.get(nombre=request.user.username)
        selec = Seleccionado.objects.get(aparcamiento=aparc, usuario=usuario)
        selec.delete()
    return HttpResponseRedirect(pag)


def usuario(request, user):
#En la Query String viene un id para identificar qué aparcamientos tiene que mostrar
    id = request.GET.get('id')
    if id == None:
        id = 0
    else:
        id = int(id)

#Comprueba si el usuario de la url es correcto, y selecciona 5 comentarios seleccionados por ese usuario
#Con el id de antes, mira qué comentarios tiene que mostrar
    usernames = list(User.objects.values_list('username',flat=True))
    if user in usernames:
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

            contexto = Context({'titulo': nompag,
                                'selec': aparc_user,
                                'user': request.user,
                                'userpag': user,
                                'id': id})
#Si un usuario no aparece aún en la base de datos es porque aún no ha hecho login,
#y por tanto no ha podido selecccionar aparcamientos (sólo aparecerá el nombre de la página)
        except Usuario.DoesNotExist:
            nompag = "Página de " + user
            contexto = Context({'titulo': nompag,
                                'user': request.user,
                                'userpag': user,
                                'id': id})

        plantilla = get_template("usuario.html")
        return HttpResponse(plantilla.render(contexto))

    else:
        return HttpResponse('Not Found 404', status=404)


def about(request):
    plantilla = get_template("about.html")
    contexto = Context({'titulo': "Información",
                        'user': request.user,
                        'curr3': 'id="current"',})
    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def cambioTitulo(request):
#En la Query String viene el nombre de usuario para después volver a redirigir a su página
#y para saber en qué usuario cambiar el título
    username = request.GET.get('user')
#Guarda el título el la base de datos con el usuaio correspondiente
    if request.method == "POST":
        titulo = request.POST['titPag']
        user = Usuario.objects.get(nombre=username)
        user.tituloPag = titulo
        user.save()
    return HttpResponseRedirect('/' + username)


@csrf_exempt
def cambioEstilo(request):
#En la Query String viene el nombre de usuario para después volver a redirigir a su página
#y para saber en qué usuario cambiar el título
    username = request.GET.get('user')
#Guarda el estilo el la base de datos con el usuaio correspondiente
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
#En la Query String viene el id del aparcamiento para después volver a redirigir a su página
#y para saber en qué aparcamiento añadir el comentario
    aparcid = request.GET.get('ap')
#Guarda el comentario con el aparcamiento correspondiente
    if request.method == "POST":
        aparc = Aparcamiento.objects.get(id=aparcid)
        aparc.numComents = aparc.numComents + 1
        aparc.save()
        comen = request.POST['comen']
        comentario = Comentarios(aparcamiento=aparc, texto=comen)
        comentario.save()
    return HttpResponseRedirect('/aparcamientos/' + aparcid)


@csrf_exempt
def usercanal(request, user, tipo):
#Obtiene los aparcamientos seleccionados por el usuario para generar el canal con ellos
    if request.method == "POST":
        usuario = Usuario.objects.get(nombre=user)
        selec = Seleccionado.objects.filter(usuario=usuario)
        list_selec = []
        for sel in selec:
            list_selec.append(sel.aparcamiento)

        contexto = Context({'user': user,
                            'desc': 'usuario',
                            'list': list_selec})
#En función del tipo de canal que pida, selecciona una plantilla u otra
        if tipo == "xml":
            plantilla = get_template("planxml.xml")
            return HttpResponse(plantilla.render(contexto), content_type="text/xml")
        elif tipo == "json":
            plantilla = get_template("planjson.json")
            return HttpResponse(plantilla.render(contexto), content_type="text/json")

@csrf_exempt
def barracanal(request, tipo):
#Selecciona los 5 aparcamientos con más comentarios
    aparc_coment = Aparcamiento.objects.exclude(numComents=0)
    list_coment = aparc_coment.order_by('-numComents')
    if len(list_coment) > 5:
        list_coment = list_coment[0:5]

    contexto = Context({'desc': 'barra',
                        'list': list_coment})

#En función del tipo de canal que pida, selecciona una plantilla u otra
    if tipo == "xml":
        plantilla = get_template("planxml.xml")
        return HttpResponse(plantilla.render(contexto), content_type="text/xml")
    elif tipo == "json":
        plantilla = get_template("planjson.json")
        return HttpResponse(plantilla.render(contexto), content_type="text/json")


def css(request):
    plantilla = get_template("style.css")
#Si el usuario está logueado, incluye en el CSS el color y el tamaño de la letra elegido por el usuario
    if request.user.is_authenticated():
        usuario = Usuario.objects.get(nombre=request.user.username)
        color = usuario.color
        letra = str(usuario.letra)
        letra2 = str(usuario.letra - 4)
        if color != "" and letra != '0':
            contexto = Context({'color': color,
                                'letra': letra,
                                'letra2': letra2})
        elif color != "" and letra == '0':
            contexto = Context({'color': color})
        elif color == "" and letra != '0':
            contexto = Context({'letra': letra,
                                'letra2': letra2})
        else:
            contexto = Context({})

        return HttpResponse(plantilla.render(contexto), content_type="text/css")
    else:
        return HttpResponse(plantilla.render(), content_type="text/css")


@csrf_exempt
def sumpunt(request):
#En la Query String viene el id del aparcamiento en el que sumar la puntuación y
#donde redirigir después
    aparcid = request.GET.get('ap')
    aparc = Aparcamiento.objects.get(id=aparcid)
    if request.method == 'POST':
        aparc.puntuacion += 1
        aparc.save()
        return HttpResponseRedirect('/aparcamientos/' + aparcid)
