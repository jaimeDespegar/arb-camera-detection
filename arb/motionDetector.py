import cv2 as open_cv
import numpy as np
import logging
import imutils
from drawingUtils import draw_contours
from utils.colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE
from utils.keys import KEY_QUIT
from capturator import Capturator

class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, video, coordinates, start_frame):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []
        self.capturator = Capturator()

    def detect_motion(self):
        capture = open_cv.VideoCapture(self.video)
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)
        coordinates_data = self.coordinates_data

        self.calculateMask(coordinates_data)

        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)
        
        firstFrame = None
        
        while capture.isOpened():
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame = frame.copy()

            if firstFrame is None:
                firstFrame = grayed
                continue

            self.detectMoves(new_frame, firstFrame, grayed)
            self.calculateStatusByTime(capture, grayed, times, statuses)
            self.drawContoursInFrame(new_frame, statuses)

            open_cv.imshow(str(self.video), new_frame)

            k = open_cv.waitKey(10)
            if k == KEY_QUIT:
                break

        capture.release()
        open_cv.destroyAllWindows()

    def detectMoves(self, frame, firstFrame, frameGray):
        frameDelta = open_cv.absdiff(firstFrame, frameGray)
        thresh = open_cv.threshold(frameDelta, 25, 255, open_cv.THRESH_BINARY)[1]
        thresh = open_cv.dilate(thresh, None, iterations=2)
        cnts = open_cv.findContours(thresh.copy(), open_cv.RETR_EXTERNAL, open_cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts: # loop over the contours
            if (open_cv.contourArea(c) < 400) or (open_cv.contourArea(c) > 700): #ignorar lo que es menor al min-area
                continue

            (x, y, w, h) = open_cv.boundingRect(c)
            open_cv.rectangle(frame, (x, y), (x + w, y + h), COLOR_WHITE, 2)
            #if(self.isDetectInAreaOK(x, y, w, h)):
            #    open_cv.rectangle(frame, (x, y), (x + w, y + h), COLOR_WHITE, 2)

    def isDetectInAreaOK(self,x, y, w, h):
        if(x>30 and x <600 and y>100 and y<600):
            return True
        else:
            return False

    # ver nombre
    def calculateMask(self, coordinates_data):
        for p in coordinates_data:
            coordinates = self._coordinates(p)
            rect = open_cv.boundingRect(coordinates)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask = mask == 255
            self.mask.append(mask)        

    # ver nombre
    def calculateStatusByTime(self, capture, grayed, times, statuses):
        position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0

        for index, c in enumerate(self.coordinates_data):
            status = self.__apply(grayed, index, c)
            timesIsNone = times[index] is None

            if not timesIsNone and self.same_status(statuses, index, status):
                times[index] = None
                continue

            if not timesIsNone and self.status_changed(statuses, index, status):

                if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                    statuses[index] = status
                    times[index] = None
                    print('position in seconds ' + str(position_in_seconds))
                    print('times index ' + str(times[index]))
                    print(status)
                    print('movimiento en espacio')
                    #self.capturator.takePhoto(capture)
                continue

            if timesIsNone and self.status_changed(statuses, index, status):
                times[index] = position_in_seconds
        
    def drawContoursInFrame(self, frame, statuses):
        for index, p in enumerate(self.coordinates_data):
            coordinates = self._coordinates(p)
            color = COLOR_GREEN if statuses[index] else COLOR_BLUE
            draw_contours(frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)        

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        rect = self.bounds[index]
        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
