from django.contrib import admin

# Register your models here.
from appFinal.models import Usuario
admin.site.register(Usuario)

from appFinal.models import Direccion
admin.site.register(Direccion)

from appFinal.models import DatosContacto
admin.site.register(DatosContacto)

from appFinal.models import Aparcamiento
admin.site.register(Aparcamiento)

from appFinal.models import Seleccionado
admin.site.register(Seleccionado)

from appFinal.models import Comentarios
admin.site.register(Comentarios)
