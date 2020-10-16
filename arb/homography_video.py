import cv2
import numpy as np
import matplotlib.pyplot as plt

class Homography_video:
	def __init__(self, puntos, frame):
		self.puntos = puntos
		self.frame = frame
		self.dst = frame

	def clics(self,event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.puntos.append([x,y])

	def dibujando_puntos(self,puntos):
		for x, y in self.puntos:
			cv2.circle(self.frame,(x,y),5,(0,255,0),2)

	def uniendo4puntos(self,puntos):
		cv2.line(self.frame,tuple(self.puntos[0]),tuple(self.puntos[1]),(255,0,0),1)
		cv2.line(self.frame,tuple(self.puntos[0]),tuple(self.puntos[2]),(255,0,0),1)
		cv2.line(self.frame,tuple(self.puntos[2]),tuple(self.puntos[3]),(255,0,0),1)
		cv2.line(self.frame,tuple(self.puntos[1]),tuple(self.puntos[3]),(255,0,0),1)

	def getHomography_video(self):
		save_name = "../files/videos/homography.mp4"
		imagen= cv2.imread('../files/images/homography.jpg') #nuevo
		fps = 10
		#imagen= self.escalarImagen(imagen)
		#height, width = img.shape[0:2]
		width = imagen.shape[1]; # columnas x
		height = imagen.shape[0]; # filas y

		output_size = (width, height)
		out = cv2.VideoWriter(save_name,cv2.VideoWriter_fourcc('M','J','P','G'), fps , output_size )

		##self.puntos = []
		#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		cap = cv2.VideoCapture('../files/videos/biciReal2.mp4')
		cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
		cv2.setMouseCallback('frame',self.clics)
		print(self.puntos)

		while True:
			ret, self.frame = cap.read()
			if ret == False: break
			self.dibujando_puntos(self.puntos)

			if len(self.puntos) == 4:
				self.uniendo4puntos(self.puntos)
				pts1 = np.float32([self.puntos])
				#pts2 = np.float32([[0,0], [500,0], [0,300], [500,300]])
				pts2 = np.float32([[0,0], [width,0], [0,height], [width,height]])

				M = cv2.getPerspectiveTransform(pts1,pts2)
				self.dst = cv2.warpPerspective(self.frame, M, (width,height))

				cv2.imshow('dst', self.dst)
				out.write(cv2.resize(self.dst, output_size ))
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			cv2.imshow('frame',self.frame)
	
			k = cv2.waitKey(1) & 0xFF
			if k == ord('n'): # Limpiar el contenido de la frame
				self.puntos = []
		
			elif k == 27:
				break
		cap.release()
		out.release()
		cv2.destroyAllWindows()
		return self.dst

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

#	def saveVideo():
#		save_name = "homography.mp4"
#		fps = 10
#		width = 600
#		height = 480
#		output_size = (width, height)
#		out = cv2.VideoWriter(save_name,cv2.VideoWriter_fourcc('M','J','P','G'), fps , output_size )
#
#		cap = cv2.VideoCapture(0) # 0 for webcam or you can put in videopath
#		while(True):
#    		_, frame = cap.read()
#    		cv2.imshow('Video Frame', frame)
#    		out.write(cv2.resize(frame, output_size ))
#    		if cv2.waitKey(1) & 0xFF == ord('q'):
#        		break
#		cap.release()
#		out.release()
#		cv2.destroyAllWindows()