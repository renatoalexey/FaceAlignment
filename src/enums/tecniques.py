from enum import Enum
import cv2

class Techs(Enum):
  
    def getNormal(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
    def getBorder(gray_image):
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)  # Borda na direção X
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)  # Borda na direção Y

        # Combina as bordas detectadas nas direções X e Y
        sobel_combined = cv2.addWeighted(cv2.convertScaleAbs(sobel_x), 0.5, cv2.convertScaleAbs(sobel_y), 0.5, 0)

        height, width = gray_image.shape
        copy = gray_image
        for i in range(height):
            for j in range(width):
                if sobel_combined[i][j] > 110:
                    copy[i][j] = 0
        return copy

    NORMAL = ("Normal", getNormal)
    GRAY = ("Cinza", getGray)
    BRIGHT_PLUS = ("Brilho +", getBrightPlus)
    BRIGHT_MINUS= ("Brilho -", getBrightMinus)
    MEAN = ("Média", getMean)
    MEDIAN = ("Mediana", getMedian)
    HIST = ("Realce", getHist)
    TESTE = ("Borda", getBorder)

    def __init__(self, f_name, getTech):
        self.f_name = f_name
        self.getTech = getTech