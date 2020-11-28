import numpy as np
import cv2 as openCv


class DetectorHelper:
    
    LAPLACIAN = 3 #(bici= 3) //(auto= 1.4) // sombras / superficies
    
    @staticmethod
    def _coordinates(data):
        return np.array(data["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]
    
    @staticmethod
    def evaluate(grayed, index, p, bounds, mask):
        coordinates = DetectorHelper._coordinates(p)
        rect = bounds[index]
        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = openCv.Laplacian(roi_gray, openCv.CV_64F)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        return np.mean(np.abs(laplacian * mask[index])) < DetectorHelper.LAPLACIAN
    
    @staticmethod
    def calculateMask(coordinates_data, contours, bounds, masks):
        for p in coordinates_data:
            coordinates = DetectorHelper._coordinates(p)
            rect = openCv.boundingRect(coordinates)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]

            contours.append(coordinates)
            bounds.append(rect)

            mask = openCv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=openCv.LINE_8)

            mask = mask == 255
            masks.append(mask)