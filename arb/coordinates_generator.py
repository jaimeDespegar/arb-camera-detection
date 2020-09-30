import cv2 as openCv
import numpy as np

from colors import COLOR_WHITE, COLOR_RED
from drawing_utils import draw_contours


class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = openCv.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []
        self.thickness = 1

        openCv.namedWindow(self.caption, openCv.WINDOW_GUI_EXPANDED)
        openCv.setMouseCallback(self.caption, self.drawRectangle)

    def buildSpaces(self):
        while True:
            openCv.imshow(self.caption, self.image)
            key = openCv.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        openCv.destroyWindow(self.caption)

    def drawRectangle(self, event, x, y, flags, params):

        if event == openCv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.__handle_done()

            elif self.click_count > 1:
                self.__handle_click_progress()

        openCv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        openCv.line(self.image, self.coordinates[-2], self.coordinates[-1], COLOR_RED , 1)

    def __handle_done(self):
        openCv.line(self.image, self.coordinates[2], self.coordinates[3], self.color, self.thickness)
        openCv.line(self.image, self.coordinates[3], self.coordinates[0], self.color, self.thickness)

        coordinates = np.array(self.coordinates)

        self.click_count = 0
        self.writeCoordinateInFileData()

        draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1
    

    def writeCoordinateInFileData(self):
        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")