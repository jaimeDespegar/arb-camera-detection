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
    
    #get_image_homography() #nuevo
    #get_video_homography() #nuevo

    config = FileReader(parse_args().config_file)
    
    image_file = config.getProp('image_file')
    video_file = config.getProp('video_file')
    data_file = config.getProp('data_file')
    start_frame = int(config.getProp('start_frame'))
    folder_photos = config.getProp('folder_photos')

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.buildSpaces()

    with open(data_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video_file, points, int(start_frame), folder_photos)
        detector.detect_motion()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--config",
                        dest="config_file",
                        required=True,
                        help="Config file to start app")

    return parser.parse_args()

def get_image_homography():
    puntos = [] #nuevo
    imagen= openCv.imread('../files/images/biciReal.jpg') #nuevo
    homography= Homography(puntos,imagen) #nuevo
    homography.getHomography() #nuevo

def get_video_homography():
    puntos = [] #nuevo
    cap = openCv.VideoCapture('../files/videos/bicicleteroReal.mp4') #nuevo
    ret, frame = cap.read() #nuevo
    homography_video= Homography_video(puntos,frame) #nuevo
    homography_video.getHomography_video() #nuevo


if __name__ == '__main__':
    main()