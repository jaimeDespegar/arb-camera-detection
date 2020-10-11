from capturator import Capturator
from utils.keys import KEY_PHOTO, KEY_QUIT
import cv2 as openCv
import argparse
import sys


def main():
    capturator = Capturator('../files/images/')
    source = resolveSource(parse_args())
    capture = openCv.VideoCapture(source)
    openCv.namedWindow('frame', openCv.WINDOW_NORMAL)
    capture.set(openCv.CAP_PROP_POS_FRAMES, 200)#500

    while(capture.isOpened()):
        readed, frame = capture.read()
        openCv.imshow('frame', frame)#nuevo, ajusta el tamaño ventana
        key = openCv.waitKey(20)#20

        if key == KEY_PHOTO:
            capturator.takePhoto(capture)
        if key == KEY_QUIT:
            break

    capture.release()
    openCv.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description='Generates config from PrinterPhotos')

    parser.add_argument("--source",
                        dest="source",
                        required=False,
                        help="Source file to generate screenshot")

    return parser.parse_args()

def resolveSource(args):
    return 0 if args.source.lower() == 'webcam' else args.source

main()