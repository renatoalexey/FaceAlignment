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
from enums.combine_type import MedianBright
from enums.resize_type import Sizes
from PIL import Image, ImageEnhance

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)

def calcEuclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

all_distances = {}
all_points_distances = {} 

def initialize_distances(pipeline):
    
    for tech in pipeline:
        all_distances[tech] = []
        all_points_distances[tech] = []
        
def readData(pipeline):
    folder_image_path = Path('images')
    folder_landmarks_path = 'landmarks/'

    initialize_distances(pipeline)

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

            all_distances, all_points_distances = calcPointsDiffs(file_image_path, file_landmarks_path, pipeline)

    #printGraph(all_points_distances)
    #print(all_points_distances)
    graphic_bar.printGraphics(all_distances)

def calcPointsDiffs(file_image_path, file_landmarks_path, pipeline):
    data = loadmat(file_landmarks_path)
    data_points = data['pts_2d']

    img = cv2.imread(file_image_path)
    gray_image = Techs.GRAY.getTech(img)
    print_landmarks(img, data_points)

    return getTechsResults(file_image_path, data_points, img, gray_image, pipeline)

def getTechsResults(file_image_path, data_points, normal_image, gray_image, pipeline):

    for tech in pipeline:
        entry_image = gray_image
        if tech == Techs.NORMAL or tech == Techs.GRAY:
            entry_image = normal_image
        #else:
         #   entry_image = gray_image
        
        format_image = tech.getTech(entry_image)
        prediction_points = fa.get_landmarks(format_image)
        if prediction_points is not None:
            print_landmarks(format_image, prediction_points[0])
            euclidean_distances, euclidean_mean = getEuclideanMetrics(file_image_path, data_points, prediction_points)
            if euclidean_distances is not None:
                all_points_distances[tech].append(euclidean_distances)
                all_distances[tech].append(euclidean_mean)
            
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

def sample(pipeline):

    file_name = "IBUG_image_003_1_6.jpg"
    points = "landmarks/IBUG_image_003_1_6_pts.mat"

    initialize_distances(pipeline)
    all_distances, all_points = calcPointsDiffs(file_name, points, pipeline)
    print(all_distances)
    print(all_points)
    #printGraph(all_distances)
    graphic_bar.printGraphics(all_distances)

pipeline = [Techs.NORMAL, MedianBright.M_BRIGHT_1]
#pipeline = [Techs.NORMAL, Brights.BRIGHT_1, Brights.BRIGHT_2, Brights.BRIGHT_3, Brights.BRIGHT_4, Brights.BRIGHT_5]
#pipeline = [Techs.NORMAL, Techs.GRAY, Techs.BRIGHT_MINUS, Techs.BRIGHT_PLUS, Techs.MEAN, Techs.MEDIAN, Techs.HIST, Techs.BORDER]
#pipeline = [Techs.NORMAL, Sizes.SIZE_1, Sizes.SIZE_2, Sizes.SIZE_3, Sizes.SIZE_4, Sizes.SIZE_5] 
sample(pipeline)
#readData(pipeline)