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
    LAPLACIAN = 3 #(bici= 3) //(auto= 1.4) // sombras / superficies
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
        self.mask = []
        self.capturator = Capturator(folder_photos)
        self.registers = []
        self.token = token
        self.capturatorMobile = Capturator(folder_photos_mobile)

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
            self.drawContoursInFrame(new_frame, statuses)

            self.getVideoHomography(new_frame,puntosHomography)
            openCv.imshow(str(self.video), new_frame)

            #FOTO DEL ESTADO DEL BICICLETERO
            momento= time.time()
            if((int(momento) - int(comienzo)) == (count_AUX*MotionDetector.FOTO_ESTADO_BICICLETERO)):
                self.capturatorMobile.takePhotoStateBicycle(capture)
                count_AUX= count_AUX+1

            k = openCv.waitKey(MotionDetector.SPEED)
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

        #openCv.imshow('thresh',thresh)
        for c in contours:
            if (openCv.contourArea(c) < 500):#900
                continue

            (x, y, w, h) = openCv.boundingRect(c)
            if(self.isDetectInAreaOK(x, y, w, h)):
                openCv.rectangle(frame, (x, y), (x + w, y + h), COLOR_WHITE, 2)

    def isDetectInAreaOK(self,x, y, w, h):
        #return (x > 100 and x < 2000 and y > 100 and y < 2000)#(x > 30 and x < 600 and y > 100 and y < 600)
        return True

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
                    
                    estacionamiento= index+1
                    notificacionFoto= ''
                    dateText = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

                    if(statuses[index]):
                        notificacionFoto= "Egress_"+str(estacionamiento) + '_' + dateText
                    else:
                        notificacionFoto= 'Entrance_'+str(estacionamiento) + '_' + dateText

                    imageName=self.capturator.takePhoto(capture,notificacionFoto)
                    momento= time.time()
                    register= Register(statuses[index],estacionamiento,imageName,dateText,momento)
                    
                    self.registers.append(register)
                    

                continue

            if timesIsNone and self.status_changed(statuses, index, status):
                times[index] = position_in_seconds
    
        if (len(self.registers)>0):
            postParkings(self.registers, self.token)


           

    def drawContoursInFrame(self, frame, statuses):
        for index, p in enumerate(self.coordinates_data):
            coordinates = self._coordinates(p)
            color = COLOR_GREEN if statuses[index] else COLOR_BLUE
            draw_contours(frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)
   

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
