import cv2 as openCv
from datetime import datetime

class Capturator:
    
    def __init__(self, folderImages):
        self.folderImages = folderImages
        self.folderWeb = 'assets/images/'
        
    def takePhoto(self, capture, description):
        leido, frame = capture.read()
        imageName=""
        if leido == True:
            imageName = self.folderImages + description + ".jpg"
            openCv.imwrite(imageName, frame)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder al contenido")
        #return imageName TODO ver este harcodeo , mobile ?
        return self.folderWeb + description + ".jpg"