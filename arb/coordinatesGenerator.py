import cv2 as openCv
import numpy as np
from utils.keys import KEY_PHOTO, KEY_QUIT
from utils.colors import COLOR_WHITE, COLOR_RED
from drawingUtils import DrawingUtils
from homography import Homography
from services.parkings import postBicycleParkings,postPlace

class CoordinatesGenerator:

    def __init__(self, imageHomography, output, color, token):
        self.output = output
        self.caption = imageHomography
        self.color = color
        self.image = openCv.imread(imageHomography).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []
        self.xMasChicos = []
        self.xMasGrandes = []
        self.thickness = 1
        self.drawingUtils = DrawingUtils()
        self.token= token
        openCv.namedWindow(self.caption, openCv.WINDOW_GUI_EXPANDED)
        openCv.setMouseCallback(self.caption, self.drawRectangle)

    def buildSpaces(self):
        while True:
            openCv.imshow(self.caption, self.image)
            key = openCv.waitKey(0)

            if key == KEY_QUIT:
                break
        openCv.destroyWindow(self.caption)

    def drawRectangle(self, event, x, y, flags, params):

        if event == openCv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.__handle_done()

            #elif self.click_count > 1:
            #    self.__handle_click_progress()

        openCv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        openCv.line(self.image, self.coordinates[-2], self.coordinates[-1], COLOR_RED , 1)

    def __handle_done(self):
        #openCv.line(self.image, self.coordinates[2], self.coordinates[3], self.color, self.thickness)
        #openCv.line(self.image, self.coordinates[3], self.coordinates[0], self.color, self.thickness)
        
        #self.orderRectangle(2)

        #coordinates = np.array(self.coordinates)
        coordinates = np.array(self.orderRectangle())

        self.click_count = 0
        self.writeCoordinateInFileData()

        self.drawingUtils.draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)

        postPlace(self.token, self.ids + 1)

        for i in range(0, 4):
            #self.coordinates.pop()
            self.coordinates= []

        self.ids += 1
    

    def writeCoordinateInFileData(self):
        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

    def createBicycleParking(self,token):
        postBicycleParkings(token)

    def orderRectangle(self):
        count0_xMasChicos= 0
        if(self.coordinates[0][0] <= self.coordinates[1][0]):
            count0_xMasChicos= count0_xMasChicos +1
        if(self.coordinates[0][0] <= self.coordinates[2][0]):
            count0_xMasChicos= count0_xMasChicos +1
        if(self.coordinates[0][0] <= self.coordinates[3][0]):
            count0_xMasChicos= count0_xMasChicos +1
        if(count0_xMasChicos>=2):
            self.xMasChicos.append(self.coordinates[0])
        else:
            self.xMasGrandes.append(self.coordinates[0])
        #############################################
        count1_xMasChicos= 0
        if(self.coordinates[1][0] <= self.coordinates[0][0]):
            count1_xMasChicos= count1_xMasChicos +1
        if(self.coordinates[1][0] <= self.coordinates[2][0]):
            count1_xMasChicos= count1_xMasChicos +1
        if(self.coordinates[1][0] <= self.coordinates[3][0]):
            count1_xMasChicos= count1_xMasChicos +1
        if(count1_xMasChicos>=2):
            self.xMasChicos.append(self.coordinates[1])
        else:
            self.xMasGrandes.append(self.coordinates[1])
        #############################################
        count2_xMasChicos= 0
        if(self.coordinates[2][0] <= self.coordinates[0][0]):
            count2_xMasChicos= count2_xMasChicos +1
        if(self.coordinates[2][0] <= self.coordinates[1][0]):
            count2_xMasChicos= count2_xMasChicos +1
        if(self.coordinates[2][0] <= self.coordinates[3][0]):
            count2_xMasChicos= count2_xMasChicos +1
        if(count2_xMasChicos>=2):
            self.xMasChicos.append(self.coordinates[2])
        else:
            self.xMasGrandes.append(self.coordinates[2])
        #############################################
        count3_xMasChicos= 0
        if(self.coordinates[3][0] <= self.coordinates[0][0]):
            count3_xMasChicos= count3_xMasChicos +1
        if(self.coordinates[3][0] <= self.coordinates[1][0]):
            count3_xMasChicos= count3_xMasChicos +1
        if(self.coordinates[3][0] <= self.coordinates[2][0]):
            count3_xMasChicos= count3_xMasChicos +1
        if(count3_xMasChicos>=2):
            self.xMasChicos.append(self.coordinates[3])
        else:
            self.xMasGrandes.append(self.coordinates[3])
        #############################################
        coordinatesAux= []
        
        #Busco P0
        if(self.xMasChicos[0][1] <= self.xMasChicos[1][1]):
            coordinatesAux.append(self.xMasChicos[0])
        else:
            coordinatesAux.append(self.xMasChicos[1])

        #Busco P1 y P2
        if(self.xMasGrandes[0][1] <= self.xMasGrandes[1][1]):
            coordinatesAux.append(self.xMasGrandes[0])
            coordinatesAux.append(self.xMasGrandes[1])
        else:
            coordinatesAux.append(self.xMasGrandes[1])
            coordinatesAux.append(self.xMasGrandes[0])

        #Busco P3
        if(self.xMasChicos[0][1] >= self.xMasChicos[1][1]):
            coordinatesAux.append(self.xMasChicos[0])
        else:
            coordinatesAux.append(self.xMasChicos[1])


        openCv.line(self.image, coordinatesAux[0], coordinatesAux[1], self.color, self.thickness)
        openCv.line(self.image, coordinatesAux[1], coordinatesAux[2], self.color, self.thickness)
        openCv.line(self.image, coordinatesAux[2], coordinatesAux[3], self.color, self.thickness)
        openCv.line(self.image, coordinatesAux[3], coordinatesAux[0], self.color, self.thickness)
        self.coordinates= []
        self.coordinates.append(coordinatesAux[0])
        self.coordinates.append(coordinatesAux[1])
        self.coordinates.append(coordinatesAux[2])
        self.coordinates.append(coordinatesAux[3])

        self.xMasChicos.pop()
        self.xMasChicos.pop()
        self.xMasGrandes.pop()
        self.xMasGrandes.pop()

        return self.coordinates