import cv2 as openCv
import numpy as np
import matplotlib.pyplot as plt

class Homography:
    
	def __init__(self, puntos, imagen):
		self.puntos = puntos
		self.imagen = imagen

		self.xMasChicos = []
		self.xMasGrandes = []

	def clics(self,event,x,y,flags,param):
		if event == openCv.EVENT_LBUTTONDOWN:
			openCv.circle(self.imagen,(x,y),5,(0,255,0),2)
			self.puntos.append([x,y])

	def uniendo4puntos(self,puntos):
		openCv.line(self.imagen,tuple(self.puntos[0]),tuple(self.puntos[1]),(255,0,0),1)
		openCv.line(self.imagen,tuple(self.puntos[0]),tuple(self.puntos[2]),(255,0,0),1)
		openCv.line(self.imagen,tuple(self.puntos[2]),tuple(self.puntos[3]),(255,0,0),1)
		openCv.line(self.imagen,tuple(self.puntos[1]),tuple(self.puntos[3]),(255,0,0),1)

	def escalarImagen(self,img):
		#Indicamos la escala a la que se reducirá.... 1/scale
		scale = 1
		#Escalamos la imagen
		img_rs = openCv.resize(img, None, fx=1./scale, fy=1./scale, interpolation=openCv.INTER_LANCZOS4)
		#print ("Tamaño de imagen: \nimg: ",img.shape," img_rs: ", img_rs.shape)
		b,g,r = openCv.split(img_rs)
		img_rs = openCv.merge([r,g,b])
		plt.imshow(img_rs),plt.title('Original escalada')
		return img_rs

	def getHomography(self):
		#self.puntos = []
		#self.imagen= openCv.imread('../files/images/biciReal.jpg')
		aux = self.imagen.copy()
		openCv.namedWindow('Imagen')
		openCv.setMouseCallback('Imagen',self.clics)
		self.imagen= self.escalarImagen(self.imagen)
		#Homografía
		rows = self.imagen.shape[0]; # filas y 
		cols = self.imagen.shape[1]; # columnas x

		while True:

			if len(self.puntos) == 4:
				self.uniendo4puntos(self.orderRectangle())
				pts1 = np.float32([self.puntos])
				pts2 = np.float32([[0,0], [cols,0], [0,rows], [cols,rows]])

				M = openCv.getPerspectiveTransform(pts1,pts2)
				dst = openCv.warpPerspective(self.imagen, M, (cols,rows))

				#Guardo la homografia
				imageName = "../files/images/homography.jpg"
				openCv.imwrite(imageName, dst)
			openCv.imshow('Imagen', self.imagen)
	
			k = openCv.waitKey(1) & 0xFF
			if k == ord('n'):
				self.imagen = aux.copy()
				self.puntos = []
		
			elif k == 27:
				break

		openCv.destroyAllWindows()
		return dst

	def getPuntos(self):
		return self.puntos

	@staticmethod
	def getVideoHomography(frame, puntosHomography):
		imagen = openCv.imread('../files/images/homography.jpg') #nuevo
		width = imagen.shape[1]; # columnas x
		height = imagen.shape[0]; # filas y

		pts1 = np.float32([puntosHomography])
		pts2 = np.float32([[0,0], [width,0], [0,height], [width,height]])

		M = openCv.getPerspectiveTransform(pts1,pts2)
		dst = openCv.warpPerspective(frame, M, (width,height))

		openCv.imshow('dst', dst)

	def orderRectangle(self):
		count0_xMasChicos= 0
		if(self.puntos[0][0] <= self.puntos[1][0]):
			count0_xMasChicos= count0_xMasChicos +1
		if(self.puntos[0][0] <= self.puntos[2][0]):
			count0_xMasChicos= count0_xMasChicos +1
		if(self.puntos[0][0] <= self.puntos[3][0]):
			count0_xMasChicos= count0_xMasChicos +1
		if(count0_xMasChicos>=2):
			self.xMasChicos.append(self.puntos[0])
		else:
			self.xMasGrandes.append(self.puntos[0])
		#############################################
		count1_xMasChicos= 0
		if(self.puntos[1][0] <= self.puntos[0][0]):
			count1_xMasChicos= count1_xMasChicos +1
		if(self.puntos[1][0] <= self.puntos[2][0]):
			count1_xMasChicos= count1_xMasChicos +1
		if(self.puntos[1][0] <= self.puntos[3][0]):
			count1_xMasChicos= count1_xMasChicos +1
		if(count1_xMasChicos>=2):
			self.xMasChicos.append(self.puntos[1])
		else:
			self.xMasGrandes.append(self.puntos[1])
		#############################################
		count2_xMasChicos= 0
		if(self.puntos[2][0] <= self.puntos[0][0]):
			count2_xMasChicos= count2_xMasChicos +1
		if(self.puntos[2][0] <= self.puntos[1][0]):
			count2_xMasChicos= count2_xMasChicos +1
		if(self.puntos[2][0] <= self.puntos[3][0]):
			count2_xMasChicos= count2_xMasChicos +1
		if(count2_xMasChicos>=2):
			self.xMasChicos.append(self.puntos[2])
		else:
			self.xMasGrandes.append(self.puntos[2])
        #############################################
		count3_xMasChicos= 0
		if(self.puntos[3][0] <= self.puntos[0][0]):
			count3_xMasChicos= count3_xMasChicos +1
		if(self.puntos[3][0] <= self.puntos[1][0]):
			count3_xMasChicos= count3_xMasChicos +1
		if(self.puntos[3][0] <= self.puntos[2][0]):
			count3_xMasChicos= count3_xMasChicos +1
		if(count3_xMasChicos>=2):
			self.xMasChicos.append(self.puntos[3])
		else:
			self.xMasGrandes.append(self.puntos[3])
        #############################################
		coordinatesAux= []
        
		#Busco P0
		if(self.xMasChicos[0][1] <= self.xMasChicos[1][1]):
			coordinatesAux.append(self.xMasChicos[0])
		else:
			coordinatesAux.append(self.xMasChicos[1])

		#Busco P1 y P2
		if(self.xMasGrandes[0][1] <= self.xMasGrandes[1][1]):
			coordinatesAux.append(self.xMasGrandes[0])
			coordinatesAux.append(self.xMasGrandes[1])
		else:
			coordinatesAux.append(self.xMasGrandes[1])
			coordinatesAux.append(self.xMasGrandes[0])

		#Busco P3
		if(self.xMasChicos[0][1] >= self.xMasChicos[1][1]):
			coordinatesAux.append(self.xMasChicos[0])
		else:
			coordinatesAux.append(self.xMasChicos[1])

		self.puntos= []
		self.puntos.append(coordinatesAux[0])
		self.puntos.append(coordinatesAux[1])
		self.puntos.append(coordinatesAux[3])
		self.puntos.append(coordinatesAux[2])
		

		self.xMasChicos.pop()
		self.xMasChicos.pop()
		self.xMasGrandes.pop()
		self.xMasGrandes.pop()

		return self.puntos