from datetime import datetime

class Register:
	def __init__(self, isEgreso, position, pathFoto, hourFoto, momento):
		self.isEgreso = isEgreso
		self.position = position
		self.pathFoto = pathFoto
		self.hourFoto = hourFoto
		self.momento = momento

	def getPosition(self):
 		return self.position

	def getHour(self):
		return self.hourFoto

	def getPathFoto(self):
		return self.pathFoto

	def getMomento(self):
		return self.momento

	def isEgreso1(self):
		return self.isEgreso


# devolver un objeto que tenga la hora del egreso/ingreso "lugar, hora y foto(ruta)"

# hacer un objeto ingreso (hardcodeado) y comparar los horarios, hacer con un while true, 
# chequear si pasaron los x segundos y decidir si dar el mensaje de "alerta robo"
# OBS: buscar jobs en python 