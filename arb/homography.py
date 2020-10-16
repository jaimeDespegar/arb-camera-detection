import cv2
import numpy as np
import matplotlib.pyplot as plt

class Homography:
	def __init__(self, puntos, imagen):
		self.puntos = puntos
		self.imagen = imagen

	def clics(self,event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN:
			cv2.circle(self.imagen,(x,y),5,(0,255,0),2)
			self.puntos.append([x,y])

	def uniendo4puntos(self,puntos):
		cv2.line(self.imagen,tuple(self.puntos[0]),tuple(self.puntos[1]),(255,0,0),1)
		cv2.line(self.imagen,tuple(self.puntos[0]),tuple(self.puntos[2]),(255,0,0),1)
		cv2.line(self.imagen,tuple(self.puntos[2]),tuple(self.puntos[3]),(255,0,0),1)
		cv2.line(self.imagen,tuple(self.puntos[1]),tuple(self.puntos[3]),(255,0,0),1)

	def escalarImagen(self,img):
		#Indicamos la escala a la que se reducirá.... 1/scale
		scale = 1
		#Escalamos la imagen
		img_rs = cv2.resize(img, None, fx=1./scale, fy=1./scale, interpolation=cv2.INTER_LANCZOS4)
		print ("Tamaño de imagen: \nimg: ",img.shape," img_rs: ", img_rs.shape)
		b,g,r = cv2.split(img_rs)
		img_rs = cv2.merge([r,g,b])
		plt.imshow(img_rs),plt.title('Original escalada')
		return img_rs

	def getHomography(self):
		#self.puntos = []
		#self.imagen= cv2.imread('../files/images/biciReal.jpg')
		aux = self.imagen.copy()
		cv2.namedWindow('Imagen')
		cv2.setMouseCallback('Imagen',self.clics)
		self.imagen= self.escalarImagen(self.imagen)
		#Homografía
		rows = self.imagen.shape[0]; # filas y 
		cols = self.imagen.shape[1]; # columnas x

		while True:

			if len(self.puntos) == 4:
				self.uniendo4puntos(self.puntos)
				pts1 = np.float32([self.puntos])
				pts2 = np.float32([[0,0], [cols,0], [0,rows], [cols,rows]])

				M = cv2.getPerspectiveTransform(pts1,pts2)
				dst = cv2.warpPerspective(self.imagen, M, (cols,rows))

				#nocv2.imshow('dst', dst)

				#Guardo la homografia
				imageName = "../files/images/homography.jpg"
				cv2.imwrite(imageName, dst)
			cv2.imshow('Imagen',self.imagen)
	
			k = cv2.waitKey(1) & 0xFF
			if k == ord('n'):
				self.imagen = aux.copy()
				self.puntos = []
		
			elif k == 27:
				break

		

		cv2.destroyAllWindows()
		return dst

	def getPuntos(self):
		return self.puntos