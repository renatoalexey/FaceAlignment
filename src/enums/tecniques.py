from enum import Enum
import cv2

class Techs(Enum):
  
    def getGray(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    def getBrightPlus(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=50)
    def getBrightMinus(gray_image):
        return cv2.convertScaleAbs(gray_image, alpha=1, beta=-50)
    def getMean(gray_image):
        return cv2.blur(gray_image, (10, 10))
    def getMedian(gray_image):
        return cv2.medianBlur(gray_image, 5)
    def getHist(gray_image):
        return cv2.equalizeHist(gray_image)

    GRAY = ("Cinza", getGray)
    BRIGHT_PLUS = ("Brilho +", getBrightPlus)
    BRIGHT_MINUS= ("Brilho -", getBrightMinus)
    MEAN = ("Média", getMean)
    MEDIAN = ("Mediana", getMedian)
    HIST = ("Realce", getHist)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech