import argparse
import yaml
from coordinatesGenerator import CoordinatesGenerator
from motionDetector import MotionDetector
from utils.fileReader import FileReader
from utils.colors import *
import logging
from homography import Homography
import cv2 as openCv
from services.parkings import login, getAllBicycleParkings
from utils.questionInput import QuestionInput

def main():
    logging.basicConfig(level=logging.INFO)
    puntosHomography = []

    config = FileReader(parse_args().config_file)
    
    image_file = config.getProp('image_file')
    video_file = config.getProp('video_file')
    data_file = config.getProp('data_file')
    start_frame = int(config.getProp('start_frame'))
    folder_photos = config.getProp('folder_photos')
    folder_photos_mobile = config.getProp('folder_photos_mobile')
    
    response = login().json()
    question1 = "¿Quiere configurar los estacionemiento? Escriba S/N!"
    if (QuestionInput.realize(question1)):
        drawCoordinates(image_file, data_file, response['token'])
    else:
        print("Bicicleteros:")
        res=getAllBicycleParkings(response['token'])
        question1_2 = "Elija un número de bicicletero existente:"
        if (QuestionInput.realizeNumberBicycle(question1_2)==1):
            data_file = config.getProp('cache_data_file')


    question2 = "¿Quiere configurar con homografia el estacionemiento? Escriba S/N!"
    if (QuestionInput.realize(question2)):
        puntosHomography = get_image_homography(image_file)
        
    with open(data_file, "r") as data:
        points = yaml.load(data)
        #response = login().json()
        detector = MotionDetector(video_file, points, int(start_frame), folder_photos, response['token'], folder_photos_mobile)
        detector.detect_motion(puntosHomography)
    #get_video_homography(puntos) #Corregir

def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--config",
                        dest="config_file",
                        required=True,
                        help="Config file to start app")

    return parser.parse_args()

def get_image_homography(image_file):
    puntos = []
    imagen= openCv.imread(image_file)
    homography= Homography(puntos,imagen) 
    imagenH=homography.getHomography()
    return homography.getPuntos()


def drawCoordinates(image_file, data_file, token):
    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED, token)
            generator.createBicycleParking(token)
            generator.buildSpaces()

if __name__ == '__main__':
    main()
