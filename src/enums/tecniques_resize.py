from enum import Enum
from enums.resize_type import Sizes
import cv2

class TechsResize(Enum):
  
    def getNormal(image):
        #return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return cv2.resize(image, (300, 300), interpolation=cv2.INTER_AREA)
    def getBrightPlus(gray_image):
        return cv2.convertScaleAbs(cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA), alpha=1, beta=50)
    def getBrightMinus(gray_image):
        return cv2.convertScaleAbs(cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA), alpha=1, beta=-50)
    def getMean(gray_image):
        return cv2.blur(cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA), (10, 10))
    def getMedian(gray_image):
        return cv2.medianBlur(cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA), 5)
    def getHist(gray_image):
        return cv2.equalizeHist(cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA))
    def getBorder(gray_image):
        resized_image = cv2.resize(gray_image, (300, 300), interpolation=cv2.INTER_AREA)
        sobel_x = cv2.Sobel(resized_image, cv2.CV_64F, 1, 0, ksize=3)  # Borda na direção X
        sobel_y = cv2.Sobel(resized_image, cv2.CV_64F, 0, 1, ksize=3)  # Borda na direção Y

        # Combina as bordas detectadas nas direções X e Y
        sobel_combined = cv2.addWeighted(cv2.convertScaleAbs(sobel_x), 0.5, cv2.convertScaleAbs(sobel_y), 0.5, 0)

        height, width = resized_image.shape
        copy = resized_image
        for i in range(height):
            for j in range(width):
                if sobel_combined[i][j] > 110:
                    copy[i][j] = 0
        return copy

    NORMAL = ("Original \n300x300", getNormal)
    BRIGHT_PLUS = ("Brilho +10 \n300x300", getBrightPlus)
    BRIGHT_MINUS= ("Brilho -10 \n300x300", getBrightMinus)
    MEAN = ("Média \n300x300", getMean)
    MEDIAN = ("Mediana \n300x300", getMedian)
    HIST = ("Equalização \nHistograma \n300x300", getHist)
    BORDER = ("Borda \n300x300", getBorder)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech