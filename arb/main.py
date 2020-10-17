import argparse
import yaml
from coordinatesGenerator import CoordinatesGenerator
from motionDetector import MotionDetector
from utils.fileReader import FileReader
from utils.colors import *
import logging
from homography import Homography #nuevo
from homography_video import Homography_video #nuevo
import cv2 as openCv #nuevo


def main():
    logging.basicConfig(level=logging.INFO)
    puntosHomography = []

    config = FileReader(parse_args().config_file)
    
    image_file = config.getProp('image_file')
    video_file = config.getProp('video_file')
    data_file = config.getProp('data_file')
    start_frame = int(config.getProp('start_frame'))
    folder_photos = config.getProp('folder_photos')

    print("¿Quiere configurar los estacionemiento? Escriba S/N!")
    decision2 = input()
    if (decision2.lower() == 's'):
        print(f"Usted decidió {decision2}")
        drawCoordinates(image_file,data_file)

    print("¿Quiere configurar con homografia el estacionemiento? Escriba S/N!")
    decision1 = input()
    if (decision1.lower() == 's'):
        puntosHomography = get_image_homography(image_file)
        #get_video_homography(puntos) #nuevo

    with open(data_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video_file, points, int(start_frame), folder_photos)
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
    #image = openCv.imread(imageHomography).copy()
    puntos = [] #nuevo
    imagen= openCv.imread(image_file)#('../files/images/biciReal2.jpg') #nuevo
    homography= Homography(puntos,imagen) #nuevo
    imagenH=homography.getHomography() #nuevo
    return homography.getPuntos()

def get_video_homography(puntos):
    #puntos = [] #nuevo
    cap = openCv.VideoCapture('../files/videos/biciReal2.mp4') #nuevo
    ret, frame = cap.read() #nuevo
    homography_video= Homography_video(puntos,frame) #nuevo
    homography_video.getHomography_video() #nuevo

def drawCoordinates(image_file, data_file):
    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.buildSpaces()

if __name__ == '__main__':
    main()