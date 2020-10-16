from django.http import HttpResponse
import datetime
from django.template import Template, Context

def saludo(request): #primera vista
	
	doc_externo=open("/home/javier/Escritorio/PPS/TP/arb-camera-detection/Proyecto1/Proyecto1/plantillas/miPlantilla.html")
	plt=Template(doc_externo.read())
	doc_externo.close()
	ctx= Context()
	#renderizo
	documento=plt.render(ctx)
	return HttpResponse(documento)

def despedida(request):

	return HttpResponse("Hasta luego!")

def dameFecha(request):
	fecha_actual= datetime.datetime.now()

	documento= """<html>
	<body>
	<h2>
	Fecha y hora actuales %s
	</h2>
	</body>
	</html>""" % fecha_actual

	return HttpResponse(documento)

def calculaEdad(request,edadActual, anio):

	#edadActual=18
	periodo=anio - 2020
	edadFutura= edadActual+periodo

	documento="<html><body><h2>En el año %s tendrás %s años" %(anio, edadFutura)

	return HttpResponse(documento)

def mostrarEstadias(request):#,posicion,hora,alarmaActiva
	posicion="1"
	hora="18:30"
	alarmaActiva="True"
	s= "Se ocupó la posicion "+ posicion+" en el horario "+hora+" y la alarma está "+alarmaActiva
	print(s)
	#documento="<html><body><h2>Se ocucpó la posicion %s en el horario %s y la alarma está: %s" %(posicion,hora,alarmaActiva)
	documento= """<html>
	<body>
	<h2>
	%s
	</h2>
	</body>
	</html>""" % s

	return HttpResponse(documento)