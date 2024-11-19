import numpy as np
from skimage import io
from scipy.io import loadmat
from pathlib import Path
from graphic import graphic_bar
import face_alignment
import cv2
import math
import matplotlib.pyplot as plt
import seaborn as sns
import os
from enums.tecniques import Techs
from enums.bright_type import Brights
from PIL import Image, ImageEnhance

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)
image_types = ['normal', 'gray', 'b_plus', 'b_minus', 'mean', 'median', 'n']
def calcEuclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

def initialize_distances():
    all_distances = {}
    all_points_distances = {}
    for type in Brights:
        all_distances[type.name] = []
        all_points_distances[type.name] = []
    return all_distances, all_points_distances
        
def readData():
    folder_image_path = Path('images')
    folder_landmarks_path = 'landmarks/'


    all_distances = {}
    all_points_distances = {}
    for tech in Techs:
        all_distances[tech.name] = []
        all_points_distances[tech.name] = []

    all_distances, all_points_distances = initialize_distances()
    cont = 0
    for file_image_path in folder_image_path.iterdir():
        #if cont == 50:
         #   break
        if(cont == 100 or cont == 500 or cont == 1000):
            print(f"Imagem n {cont}")
        cont +=1
        if file_image_path.is_file():
            file_name = os.path.splitext(os.path.basename(file_image_path))[0]
            file_landmarks_path = f'{folder_landmarks_path}{file_name}_pts.mat'

            all_distances, all_points_distances = calcPointsDiffs(file_image_path, file_landmarks_path, 
                                            all_distances, all_points_distances)

    #printGraph(all_points_distances)
    #print(all_points_distances)
    graphic_bar.printGraphics(all_distances, image_types)

def createImages(image):
    images = [image]
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    images.append(gray_image) 
    images.append(cv2.convertScaleAbs(gray_image, alpha=1, beta=50))
    images.append(cv2.convertScaleAbs(gray_image, alpha=1, beta=-50))
    images.append(cv2.blur(gray_image, (10, 10)))
    images.append(cv2.medianBlur(gray_image, 5))
    images.append(cv2.equalizeHist(gray_image))

    #normalized_image = gray_image.astype(np.float32) / 255.0
    #resized_image = cv2.resize(gray_image, (450, 450))
    #images.append(resized_image)

    return images

def calcPointsDiffs(file_image_path, file_landmarks_path, all_distances, all_points_distances):
    data = loadmat(file_landmarks_path)
    data_points = data['pts_2d']

    original_image = io.imread(file_image_path)
    
    img = cv2.imread(file_image_path)
    images = createImages(img)
    #gray_image = None
    gray_image = Techs.GRAY.getTech(img)
    #print_landmarks(img, data_points)

    format_img = None
    #return getAllTechs(file_image_path, all_distances, all_points_distances, data_points, img)
    return getBrightness(file_image_path, all_distances, all_points_distances, data_points, img, gray_image)

def getAllTechs(file_image_path, all_distances, all_points_distances, data_points, img):
    for tech in Techs:
        if tech.name == Techs.NORMAL.name:
            format_img = img
        elif tech.name == Techs.GRAY.name:
            gray_image = tech.getTech(img)
            format_img = gray_image
        else:
            format_img = tech.getTech(gray_image)

        prediction_points = fa.get_landmarks(format_img)
        #print_landmarks(image, prediction_points[0])

        if prediction_points is not None:
            euclidean_distances, euclidean_mean = getEuclideanMetrics(file_image_path, data_points, prediction_points)
            if euclidean_distances is not None:
                all_points_distances[tech.name].append(euclidean_distances)
                all_distances[tech.name].append(euclidean_mean)
            
    return all_distances, all_points_distances

def getBrightness(file_image_path, all_distances, all_points_distances, data_points, img, gray_image):
    
    for bright in Brights:
        if bright.name == Brights.NORMAL.name:
            format_img = img
        else:
            format_img = bright.getTech(gray_image)
        prediction_points = fa.get_landmarks(format_img)

        if prediction_points is not None:
            euclidean_distances, euclidean_mean = getEuclideanMetrics(file_image_path, data_points, prediction_points)
            if euclidean_distances is not None:
                all_points_distances[bright.name].append(euclidean_distances)
                all_distances[bright.name].append(euclidean_mean)
            
    return all_distances, all_points_distances

def getEuclideanMetrics(file_image_path, data_points, prediction_points):
    try: 
        for i in range(0, len(prediction_points)):
            euclidean_distances = getDistances(data_points, prediction_points, i) 
            euclidean_mean = np.mean(euclidean_distances)

            if euclidean_mean <= 50:
                return euclidean_distances, euclidean_mean

            if euclidean_mean > 50 and i == len(prediction_points):
                print(f"{file_image_path} - {euclidean_mean}")
    except Exception as e:  # Handle any other exception
        print(f"An error occurred: {e}, Prediction points: {prediction_points}")
    return None, None

def print_landmarks(img, points):
    
    for i, point in enumerate(points):
        x = round(point[0])
        y = round(point[1])
        cv2.circle(img, (x, y), 2, (255, 0, 0), -1)

    cv2.imshow("", img)
    cv2.waitKey(0)

def getDistances(data_points, prediction_points, l):
    euclidean_distances = []
    for i, pred_point in enumerate(prediction_points[l]):
        euclidean_distances.append( calcEuclideanDistance(pred_point[0], 
                    pred_point[1], data_points[i][0], data_points[i][1]))
            
    return euclidean_distances

def sum_points_diffs(all_points_distances, euclidean_distances, type):
    if not all_points_distances[type]:
        all_points_distances[type] = euclidean_distances
    else:
        temp = []
        for a, b in zip(all_points_distances[type], euclidean_distances):
            temp.append(a + b)
        all_points_distances[type] = temp
    return all_points_distances

def printGraph(all_distances):

    #distances_mean = list(map(lambda input: np.mean(input) , sizes))

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=all_distances['GRAY'])

    # Adicionando rótulos e título
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title('Pontos')

    plt.savefig('box.png')

def sample ():
    all_distances = {}
    points_d = {}
    for tech in Techs:
        all_distances[tech.name] = []
        points_d[tech.name] = []

    file_name = "IBUG_image_003_1_6.jpg"
    points = "landmarks/IBUG_image_003_1_6_pts.mat"
    all_distances, all_points = calcPointsDiffs(file_name, points, all_distances, points_d)
    print(all_distances)
    print(all_points)
    #printGraph(all_distances)
    graphic_bar.printGraphics(all_distances, image_types)

#sample()
readData()