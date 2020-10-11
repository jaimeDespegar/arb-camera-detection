import cv2 as openCv
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

    def __init__(self, video, coordinates, start_frame, folder_photos):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []
        self.capturator = Capturator(folder_photos)

    def detect_motion(self):
        capture = openCv.VideoCapture(self.video)
        openCv.namedWindow('frame', openCv.WINDOW_NORMAL) #nuevo ajuste imagen
        capture.set(openCv.CAP_PROP_POS_FRAMES, self.start_frame)
        coordinates_data = self.coordinates_data

        self.calculateMask(coordinates_data)

        statuses = [True] * len(coordinates_data)
        times = [None] * len(coordinates_data)
        firstFrame = None
        
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

            openCv.imshow(str(self.video), new_frame)

            k = openCv.waitKey(50) #10
            if k == KEY_QUIT:
                break

        capture.release()
        openCv.destroyAllWindows()

    def detectMoves(self, frame, firstFrame, frameGray):
        frameDelta = openCv.absdiff(firstFrame, frameGray)
        thresh = openCv.threshold(frameDelta, 25, 255, openCv.THRESH_BINARY)[1]
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

        for index, itemData in enumerate(self.coordinates_data):
            status = self.apply(grayed, index, itemData)
            timesIsNone = times[index] is None

            if not timesIsNone and self.same_status(statuses, index, status):
                times[index] = None
                continue

            if not timesIsNone and self.status_changed(statuses, index, status):
                if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                    statuses[index] = status
                    times[index] = None
                    print("movimiento detectado!")
                    self.capturator.takePhoto(capture)
                continue

            if timesIsNone and self.status_changed(statuses, index, status):
                times[index] = position_in_seconds
        
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
