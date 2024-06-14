from PIL import Image
import pytesseract
import cv2
import argparse
import os
from datetime import datetime
import json

class recognizer(object):
    def read_config(self):
        with open('config.json') as conf
            self.config = json.loads(conf.read())

def arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
    ap.add_argument("-l", "--location", type=str, help="posicion where the target is. example:  x1,y1,x2,y2")
    return vars(ap.parse_args())

def image_processing(args):
    image = cv2.imread(args['image'])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    elif args["preprocess"] == "blur":
        gray = cv2.medianBlur(gray, 3)
    
    return gray

def image_cutting(tmp_filename, coordinates):
    path = os.getcwd()
    image = Image.open(f'{path}/tmp/{tmp_filename}.png')
    image = image.crop(coordinates)
    image.save(f'{path}/tmp/{tmp_filename}.png')    

def saving_tmp(image, tmp_filename):
    path = os.getcwd()
    if os.path.exists(f'{path}/tmp') == False:
        os.mkdir(f'{path}/tmp')

    cv2.imwrite(f'{path}/tmp/{tmp_filename}.png', image)

def ocr(tmp_filename):
    path = os.getcwd()
    image = Image.open(f'{path}/tmp/{tmp_filename}.png')
    return pytesseract.image_to_string(image)

if __name__ == '__main__':
    args = arguments()
    time = datetime.now()
    saving_tmp(image=image_processing(args=args), tmp_filename=time)
    if args["location"]:
        args["location"] = tuple(map(int, args["location"].split(',')))
        image_cutting(tmp_filename=time, coordinates=tuple(args["location"]))
    print(ocr(tmp_filename=time))

