import cv2 as openCv
from detector.detectorHelper import DetectorHelper
from utils.colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE, COLOR_RED


class DrawingUtils:
    
    def draw_contours(self, image,
                    coordinates,
                    label,
                    font_color,
                    border_color=COLOR_RED,
                    line_thickness=1,
                    font=openCv.FONT_HERSHEY_SIMPLEX,
                    font_scale=0.5):

        openCv.drawContours(image,
                            [coordinates],
                            contourIdx=-1,
                            color=border_color,
                            thickness=2,
                            lineType=openCv.LINE_8)

        moments = openCv.moments(coordinates)

        center = (int(moments["m10"] / moments["m00"]) - 3,
                int(moments["m01"] / moments["m00"]) + 3)

        openCv.putText(image,
                        label,
                        center,
                        font,
                        font_scale,
                        font_color,
                        line_thickness,
                        openCv.LINE_AA)


    def drawContoursInFrame(self, frame, statuses, coordinates_data):
        for index, p in enumerate(coordinates_data):
            coordinates = DetectorHelper._coordinates(p)
            color = COLOR_GREEN if statuses[index] else COLOR_BLUE
            self.draw_contours(frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)
