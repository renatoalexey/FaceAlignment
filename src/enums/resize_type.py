
from enum import Enum
import cv2

class Sizes(Enum):
    
    def getSize450(gray_image):
        return cv2.resize(gray_image, (450, 450), interpolation=cv2.INTER_AREA)
    def getSize90(gray_image):
        return cv2.resize(gray_image, (900, 900), interpolation=cv2.INTER_AREA)
    def getSize700(gray_image):
        return cv2.resize(gray_image, (700, 700), interpolation=cv2.INTER_AREA)
    def getSize300(gray_image):
        return cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA)
    def getSize150(gray_image):
        return cv2.resize(gray_image, (150, 150), interpolation=cv2.INTER_AREA)

    SIZE_450 = ("Tam 450", getSize450)
    SIZE_900 = ("900x900", getSize90)
    SIZE_700 = ("700x700", getSize700)
    SIZE_300 = ("300x300", getSize300)
    SIZE_150 = ("150x150", getSize150)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech