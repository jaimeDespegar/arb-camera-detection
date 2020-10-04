import cv2 as openCv


class Capturator:
    
    def __init__(self):
        self.id = 0    
    
    def takePhoto(self, capture):
        
        leido, frame = capture.read()
        
        if leido == True:
            openCv.imwrite("../files/images/screen_"+ str(self.id)+ ".jpg", frame)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder al contenido")

        self.id = self.id + 1