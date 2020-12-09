import cv2 as openCv
import base64

class ImageParser():
    
    @staticmethod
    def parseToBase64(imageFrame):
        retval, buffer = openCv.imencode('.jpg', imageFrame)
        jpg_as_text = base64.b64encode(buffer)
        data_base64 = jpg_as_text.decode() 
        return 'data:image/jpeg;base64,' + data_base64