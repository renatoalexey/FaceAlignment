from enum import Enum
from enums.tecniques import Techs
from enums.bright_type import Brights
from enums.resize_type import Sizes
import cv2

class MedianBright(Enum):
    
    def getMedianBright(gray_image):
        return Brights.getBright1(Techs.getMedian(gray_image))
    def getSizeMedianBright(gray_image):
        return Brights.getBright1(Techs.getMedian(Sizes.getSize700(gray_image)))
    def getBorderBright(gray_image):
        return Brights.getBright1(Techs.getBorder(gray_image))
    def getSizeBorderBright(gray_image):
        return Brights.getBright1(Techs.getMedian(Sizes.getSize700(gray_image)))

    MEDIAN_BRIGHT = ("Mediana \nBrilho 10", getMedianBright)
    S_MEDIAN_BRIRHT = ("Resize Mediana \nBrilho 10", getSizeMedianBright)
    BORDER_BRIGHT = ("Borda Brilho 10", getBorderBright)
    S_BORDER_BRIGHT = ("R B Mediana \nBrilho 10", getSizeBorderBright)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech