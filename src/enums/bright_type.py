from enum import Enum
import cv2

class Brights(Enum):
    
    def getBright1(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=10)
    def getBright2(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=30)
    def getBright3(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=50)
    def getBright4(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=70)
    def getBright5(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=90)

    BRIGHT_1 = ("Brilho 10", getBright1)
    BRIGHT_2 = ("Brilho 30", getBright2)
    BRIGHT_3 = ("Brilho 50", getBright3)
    BRIGHT_4 = ("Brilho 70", getBright4)
    BRIGHT_5 = ("Brilho 90", getBright5)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech