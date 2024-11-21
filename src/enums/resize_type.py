
from enum import Enum
import cv2

class Sizes(Enum):
    
    def getSize1(gray_image):
        return cv2.resize(gray_image, (450, 450), interpolation=cv2.INTER_AREA)
    def getSize2(gray_image):
        return cv2.resize(gray_image, (900, 900), interpolation=cv2.INTER_AREA)
    def getSize3(gray_image):
        return cv2.resize(gray_image, (700, 700), interpolation=cv2.INTER_AREA)
    def getSize4(gray_image):
        return cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA)
    def getSize5(gray_image):
        return cv2.resize(gray_image, (150, 150), interpolation=cv2.INTER_AREA)

    SIZE_1 = ("Size 10", getSize1)
    SIZE_2 = ("Size 30", getSize2)
    SIZE_3 = ("Size 50", getSize3)
    SIZE_4 = ("Size 70", getSize4)
    SIZE_5 = ("Size 90", getSize5)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech