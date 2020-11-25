import numpy as np

class DetectorHelper:
    
    @staticmethod
    def _coordinates(data):
        return np.array(data["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]