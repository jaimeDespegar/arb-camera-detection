from capturator import Capturator
from utils.keys import KEY_PHOTO, KEY_QUIT
import cv2 as openCv
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Generates config from PrinterPhotos')

    parser.add_argument("--source",
                        dest="source",
                        required=False,
                        help="Source file to generate screenshot")

    return parser.parse_args()

def resolveSource(args):
    return 0 if args.source.lower() == 'webcam' else args.source

def main():

    source = resolveSource(parse_args())
    capture = openCv.VideoCapture(source)
    capture.set(openCv.CAP_PROP_POS_FRAMES, 500)

    capturator = Capturator()

    while(capture.isOpened()):
        readed, frame = capture.read()

        openCv.imshow('frame', frame)
        key = openCv.waitKey(20)

        if key == KEY_PHOTO:    
            capturator.takePhoto(capture)
        if key == KEY_QUIT:
            break

    capture.release()
    openCv.destroyAllWindows()


main()