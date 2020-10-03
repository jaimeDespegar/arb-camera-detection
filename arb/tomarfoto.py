import argparse
import cv2 as openCv


def parse_args():
    parser = argparse.ArgumentParser(description='Generates config from PrinterPhotos')

    parser.add_argument("--source",
                        dest="source",
                        required=False,
                        help="Source file to generate screenshot")

    return parser.parse_args()


args = parse_args()
source = 0 if args.source.lower() == 'webcam' else args.source

cap = openCv.VideoCapture(source)#(0)
leido, frame = cap.read()
if leido == True:
	openCv.imwrite("foto.jpg", frame)
	print("Foto tomada correctamente")
else:
	print("Error al acceder a la cámara")
#	Finalmente liberamos o soltamos la cámara
cap.release ()
