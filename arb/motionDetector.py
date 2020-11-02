import cv2 as openCv
import numpy as np
import logging
import imutils
from drawingUtils import draw_contours
from utils.colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE, COLOR_RED
from utils.keys import KEY_QUIT
from capturator import Capturator
from register import Register
from datetime import datetime
import time
from services.parkings import getParkings,putParkings,postParkings



class MotionDetector:
    LAPLACIAN = 1.4 #3 //1.4 SOMBRAS / superficies
    DETECT_DELAY = 1 #2 //1
    TOLERANCIA = 5 # ALARMA
    UMBRAL_ORIGEN = 25 #100 // 25 SOMBRAS
    


    def __init__(self, video, coordinates, start_frame, folder_photos, token):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []
        self.capturator = Capturator(folder_photos)
        self.registers = []
        self.token = token

    def detect_motion(self,puntosHomography):
        capture = openCv.VideoCapture(self.video)
        openCv.namedWindow('frame', openCv.WINDOW_NORMAL) #nuevo ajuste imagen
        capture.set(openCv.CAP_PROP_POS_FRAMES, self.start_frame)
        coordinates_data = self.coordinates_data

        self.calculateMask(coordinates_data)

        statuses = [True] * len(coordinates_data)
        times = [None] * len(coordinates_data)
        firstFrame = None
        
        #nuevo
        comienzo = time.time() 
        print('COMIENZO:', comienzo)
        
        while capture.isOpened():
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = openCv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = openCv.cvtColor(blurred, openCv.COLOR_BGR2GRAY)
            new_frame = frame.copy()

            if firstFrame is None:
                firstFrame = grayed
                continue

            self.detectMoves(new_frame, firstFrame, grayed)
            self.calculateStatusByTime(capture, grayed, times, statuses)
            self.drawContoursInFrame(new_frame, statuses)
            # NOTIFICAR SI HAY UN EXCESO DE HORA => NOTIFICAR
            self.activateAlarm(MotionDetector.TOLERANCIA)

            self.getVideoHomography(new_frame,puntosHomography)
            openCv.imshow(str(self.video), new_frame)

            k = openCv.waitKey(10) #10
            if k == KEY_QUIT:
                break

        capture.release()
        openCv.destroyAllWindows()

    def getVideoHomography(self,frame,puntosHomography):
        imagen= openCv.imread('../files/images/homography.jpg') #nuevo
        width = imagen.shape[1]; # columnas x
        height = imagen.shape[0]; # filas y

        pts1 = np.float32([puntosHomography])
        pts2 = np.float32([[0,0], [width,0], [0,height], [width,height]])

        M = openCv.getPerspectiveTransform(pts1,pts2)
        dst = openCv.warpPerspective(frame, M, (width,height))

        openCv.imshow('dst', dst)
             


    def detectMoves(self, frame, firstFrame, frameGray):
        frameDelta = openCv.absdiff(firstFrame, frameGray)
        thresh = openCv.threshold(frameDelta, MotionDetector.UMBRAL_ORIGEN, 255, openCv.THRESH_BINARY)[1]
        thresh = openCv.dilate(thresh, None, iterations=2)
        contours = openCv.findContours(thresh.copy(), openCv.RETR_EXTERNAL, openCv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            if (openCv.contourArea(c) < 900):
                continue

            (x, y, w, h) = openCv.boundingRect(c)
            if(self.isDetectInAreaOK(x, y, w, h)):
                openCv.rectangle(frame, (x, y), (x + w, y + h), COLOR_WHITE, 2)

    def isDetectInAreaOK(self,x, y, w, h):
        return (x > 30 and x < 600 and y > 100 and y < 600)

    # ver nombre
    def calculateMask(self, coordinates_data):
        for p in coordinates_data:
            coordinates = self._coordinates(p)
            rect = openCv.boundingRect(coordinates)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = openCv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=openCv.LINE_8)

            mask = mask == 255
            self.mask.append(mask)        

    # ver nombre
    def calculateStatusByTime(self, capture, grayed, times, statuses):
        position_in_seconds = capture.get(openCv.CAP_PROP_POS_MSEC) / 1000.0
        self.registers = []
        for index, itemData in enumerate(self.coordinates_data):
            status = self.apply(grayed, index, itemData)
            timesIsNone = times[index] is None

            if not timesIsNone and self.same_status(statuses, index, status):
                times[index] = None
                continue

            if not timesIsNone and self.status_changed(statuses, index, status):
                if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                    statuses[index] = status #true si está libre, false ocupado
                    times[index] = None
                    #print("movimiento detectado!")
                    estacionamiento= index+1
                    notificacionFoto= ""
                    dateText = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

                    if(statuses[index]):
                        #print("Egreso del estacionamiento: ",estacionamiento)
                        notificacionFoto= "Egreso_del_estacionamiento:"+str(estacionamiento)+"__"+dateText
                        #Activar Timer, si pasa X tiempo tirar otro print!
                    else:
                        #print("Ingreso del estacionamiento: ",estacionamiento)
                        notificacionFoto= "Ingreso_del_estacionamiento:"+str(estacionamiento)+"__"+dateText

                    imageName=self.capturator.takePhoto(capture,notificacionFoto)
                    momento= time.time()
                    register= Register(statuses[index],estacionamiento,imageName,dateText,momento)
                    self.registers.append(register)
                    
                continue

            if timesIsNone and self.status_changed(statuses, index, status):
                times[index] = position_in_seconds
    
        if (len(self.registers)>0):
            postParkings(self.registers, self.token)

    def activateAlarm(self,tolerancia):
        for x in range(0,len(self.registers)):
            estadia= self.registers[x]
            ahora = time.time()
            diferencia= int(ahora - estadia.getMomento())
            if(diferencia==tolerancia and estadia.isEgreso1() and (not estadia.is_AlarmActive())):
                estadia.set_ON_Alarm()
                print("ALARMA!", estadia.getPosition())

           

    def drawContoursInFrame(self, frame, statuses):
        for index, p in enumerate(self.coordinates_data):
            coordinates = self._coordinates(p)
            color = COLOR_GREEN if statuses[index] else COLOR_BLUE
            draw_contours(frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)
            #if(color == COLOR_BLUE):#es el color rojo!
                #print("Ingreso :", str(p["id"] + 1))     

    def apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        rect = self.bounds[index]
        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = openCv.Laplacian(roi_gray, openCv.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        return np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN

    @staticmethod
    def _coordinates(data):
        return np.array(data["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
