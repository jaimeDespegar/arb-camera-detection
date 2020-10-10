import cv2 as openCv
from datetime import datetime

class Capturator:
    
    def __init__(self, folderImages):
        self.folderImages = folderImages
        
    def takePhoto(self, capture):
        dateText = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        leido, frame = capture.read()
        
        if leido == True:
            imageName = self.folderImages + "image_"+ dateText + ".jpg"
            openCv.imwrite(imageName, frame)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder al contenido")