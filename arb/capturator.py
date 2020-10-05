import cv2 as openCv
from datetime import datetime

class Capturator:
    
    def __init__(self):
        self.id = 0    
        self.folderImages = "../files/images/"
        
    def takePhoto(self, capture):
        now = datetime.now()
        print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
        print("date and time =", dt_string)	
        leido, frame = capture.read()
        
        if leido == True:
            imgName = self.folderImages + "screen_"+ dt_string + ".jpg"
            print("imagen name " + imgName)
            openCv.imwrite(imgName, frame)
            #str(self.id)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder al contenido")

        self.id = self.id + 1