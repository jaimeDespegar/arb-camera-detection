import argparse
import yaml
from coordinatesGenerator import CoordinatesGenerator
from motionDetector import MotionDetector
from utils.fileReader import FileReader
from utils.colors import *
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    
    config = FileReader(parse_args().config_file)
    
    image_file = config.getProp('image_file')
    video_file = config.getProp('video_file')
    data_file = config.getProp('data_file')
    start_frame = int(config.getProp('start_frame'))

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.buildSpaces()

    with open(data_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video_file, points, int(start_frame))
        detector.detect_motion()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--config",
                        dest="config_file",
                        required=True,
                        help="Config file to start app")

    return parser.parse_args()


if __name__ == '__main__':
    main()