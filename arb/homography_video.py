import cv2
import numpy as np

class Homography_video:
	def __init__(self, puntos, frame):
		self.puntos = puntos
		self.frame = frame
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
		self.puntos = []
		#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		cap = cv2.VideoCapture('../files/videos/biciReal2.mp4')
		cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
		cv2.setMouseCallback('frame',self.clics)

		while True:
			ret, self.frame = cap.read()
			if ret == False: break
			self.dibujando_puntos(self.puntos)

			if len(self.puntos) == 4:
				self.uniendo4puntos(self.puntos)
				pts1 = np.float32([self.puntos])
				pts2 = np.float32([[0,0], [500,0], [0,300], [500,300]])

				M = cv2.getPerspectiveTransform(pts1,pts2)
				dst = cv2.warpPerspective(self.frame, M, (500,300))

				cv2.imshow('dst', dst)
			cv2.imshow('frame',self.frame)
	
			k = cv2.waitKey(1) & 0xFF
			if k == ord('n'): # Limpiar el contenido de la frame
				self.puntos = []
		
			elif k == 27:
				break
		cap.release()
		cv2.destroyAllWindows()