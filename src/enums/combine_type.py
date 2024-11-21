from enum import Enum
from enums.tecniques import Techs
from enums.bright_type import Brights
import cv2

class MedianBright(Enum):
    
    def getMedianBright1(gray_image):
        return Brights.getBright1(Techs.getMedian(gray_image))

    M_BRIGHT_1 = ("Mediana Brilho 10", getMedianBright1)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech