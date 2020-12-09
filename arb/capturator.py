import cv2 as openCv
from datetime import datetime
from utils.imageParser import ImageParser


class Capturator:
    
    def __init__(self, folderImages):
        self.folderImages = folderImages
        self.folderWeb = 'assets/images/'
        self.folderMobile = 'assets/images/'
        
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
        imageInBase64 = ImageParser.parseToBase64(frame)
        response = {
            "path": self.folderWeb + description + ".jpg",
            "imageBase64": imageInBase64          
        }
        return response

    def takePhotoStateBicycle(self, capture):
        leido, frame = capture.read()
        imageName=""
        if leido == True:
            imageName = self.folderImages +"estadoBicicletero.jpg"
            openCv.imwrite(imageName, frame)
            print("Foto estadoBicicletero tomada correctamente")
        else:
            print("Error al acceder al contenido")
        #return imageName TODO ver este harcodeo , mobile ?
        return self.folderMobile + "estadoBicicletero.jpg"