import cv2 as openCv
import numpy as np
import logging
import imutils
import time
from utils.colors import COLOR_WHITE
from utils.keys import KEY_QUIT
from capturator import Capturator
from register import Register
from datetime import datetime
from services.parkings import getParkings,putParkings,postParkings
from detector.detectorHelper import DetectorHelper
from drawingUtils import DrawingUtils
from homography import Homography


class MotionDetector:
    
    DETECT_DELAY = 2.5 #(bici= 2) //(auto= 1) // retardos
    TOLERANCIA = 5 # // alarma
    UMBRAL_ORIGEN = 170 #(bici= 100) //(auto= 25) //sombras
    SPEED= 20
    FOTO_ESTADO_BICICLETERO = 5 #segundos

    def __init__(self, video, coordinates, start_frame, folder_photos, token, folder_photos_mobile):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.masks = []
        self.capturator = Capturator(folder_photos)
        self.registers = []
        self.token = token
        self.capturatorMobile = Capturator(folder_photos_mobile)
        self.drawingUtils = DrawingUtils()        

    def detect_motion(self,puntosHomography):
        capture = openCv.VideoCapture(self.video)
        openCv.namedWindow('frame', openCv.WINDOW_NORMAL) #nuevo ajuste imagen
        capture.set(openCv.CAP_PROP_POS_FRAMES, self.start_frame)
        coordinates_data = self.coordinates_data

        DetectorHelper.calculateMask(coordinates_data, self.contours, self.bounds, self.masks)

        statuses = [True] * len(coordinates_data)
        times = [None] * len(coordinates_data)
        firstFrame = None
        
        #nuevo
        comienzo = time.time()
        count_AUX=1
        
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
            self.drawingUtils.drawContoursInFrame(new_frame, statuses, self.coordinates_data)

            Homography.getVideoHomography(new_frame, puntosHomography)
            openCv.imshow(str(self.video), new_frame)

            #FOTO DEL ESTADO DEL BICICLETERO
            momento = time.time()
            if((int(momento) - int(comienzo)) == (count_AUX*MotionDetector.FOTO_ESTADO_BICICLETERO)):
                self.capturatorMobile.takePhotoStateBicycle(capture)
                count_AUX= count_AUX+1

            k = openCv.waitKey(MotionDetector.SPEED)
            if k == KEY_QUIT:
                break

        capture.release()
        openCv.destroyAllWindows()             

    def detectMoves(self, frame, firstFrame, frameGray):
        frameDelta = openCv.absdiff(firstFrame, frameGray)
        thresh = openCv.threshold(frameDelta, MotionDetector.UMBRAL_ORIGEN, 255, openCv.THRESH_BINARY)[1]
        thresh = openCv.dilate(thresh, None, iterations=2)
        contours = openCv.findContours(thresh.copy(), openCv.RETR_EXTERNAL, openCv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            if (openCv.contourArea(c) < 500):
                continue

            (x, y, w, h) = openCv.boundingRect(c)
            if(self.isDetectInAreaOK(x, y, w, h)):
                openCv.rectangle(frame, (x, y), (x + w, y + h), COLOR_WHITE, 2)

    def isDetectInAreaOK(self,x, y, w, h):
        #return (x > 100 and x < 2000 and y > 100 and y < 2000)#(x > 30 and x < 600 and y > 100 and y < 600)
        return True

    # ver nombre
    def calculateStatusByTime(self, capture, grayed, times, statuses):
        position_in_seconds = capture.get(openCv.CAP_PROP_POS_MSEC) / 1000.0
        self.registers = []
        for index, itemData in enumerate(self.coordinates_data):
            status = DetectorHelper.evaluate(grayed, index, itemData, self.bounds, self.masks)
            timesIsNone = times[index] is None

            if not timesIsNone and DetectorHelper.same_status(statuses, index, status):
                times[index] = None
                continue

            if not timesIsNone and DetectorHelper.status_changed(statuses, index, status):
                if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                    statuses[index] = status #true si está libre, false ocupado
                    times[index] = None
                    
                    estacionamiento = index+1
                    notificacionFoto = ''
                    dateText = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

                    if(statuses[index]):
                        notificacionFoto = "Egress_"+str(estacionamiento) + '_' + dateText
                    else:
                        notificacionFoto = 'Entrance_'+str(estacionamiento) + '_' + dateText

                    imageName=self.capturator.takePhoto(capture,notificacionFoto)
                    momento= time.time()
                    register= Register(statuses[index],estacionamiento,imageName,dateText,momento)
                    
                    self.registers.append(register)
                    
                continue

            if timesIsNone and DetectorHelper.status_changed(statuses, index, status):
                times[index] = position_in_seconds
    
        if (len(self.registers)>0):
            postParkings(self.registers, self.token)

class CaptureReadError(Exception):
    pass