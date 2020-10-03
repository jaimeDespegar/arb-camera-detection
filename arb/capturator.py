
import cv2 as openCv

class Capturator:
    

    
    def takePhoto(self, capture):
        
        #args = self.parse_args()
        #source = 0 if args.source.lower() == 'webcam' else args.source
        #capture = openCv.VideoCapture(source)

        leido, frame = capture.read()

        if leido == True:
            openCv.imwrite("foto.jpg", frame)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder a la cámara")
        #capture.release () #Finalmente liberamos la cámara