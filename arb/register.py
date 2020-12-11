from datetime import datetime

class Register:
	def __init__(self, isEgreso, position, pathFoto, hourFoto, momento, imgBase64):
		self.isEgreso = isEgreso
		self.position = position
		self.pathFoto = pathFoto
		self.hourFoto = hourFoto
		self.momento = momento
		self.imgBase64 = imgBase64

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