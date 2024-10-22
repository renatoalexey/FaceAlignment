from skimage import io
from scipy.io import loadmat
from pathlib import Path
from graphic import graphic_bar
import face_alignment
import cv2
import math
import matplotlib.pyplot as plt
import os
import numpy as np

image_types = ['normal', 'gray', 'mean', 'median']
def calcEuclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

def readData():
    folder_image_path = Path('images')
    folder_landmarks_path = 'landmarks/'


    all_distances = {}
    for type in image_types:
        all_distances[type] = []

    for file_image_path in folder_image_path.iterdir():
        if file_image_path.is_file():
            file_name = os.path.splitext(os.path.basename(file_image_path))[0]
            file_landmarks_path = f'{folder_landmarks_path}{file_name}_pts.mat'

            all_distances = calcPointsDiffs(file_image_path, file_landmarks_path, all_distances)

    #printGraph(all_distances)
    graphic_bar.printGraphics(all_distances, image_types)

def createImages(image):
    images = [image]
    print("Normal finished")
    images.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)) 
    print("Gray finished")
    images.append(cv2.blur(image, (10, 10)))
    print("Mean finished")
    images.append(cv2.medianBlur(image, 5))

    return images

def calcPointsDiffs(file_image_path, file_landmarks_path, all_distances):
    data = loadmat(file_landmarks_path)
    data_points = data['pts_2d']

    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)
    input = io.imread(file_image_path)
    images = createImages(input)

    for k, image in enumerate(images):
        prediction_points = fa.get_landmarks(image)

        if prediction_points is not None:
            euclidean_distances = []
            for i, pred_point in enumerate(prediction_points[0]):
                euclidean_distances.append( calcEuclideanDistance(pred_point[0], 
                    pred_point[1], data_points[i][0], data_points[i][1])) 
            
            all_distances[image_types[k]].append(np.mean(euclidean_distances))
    return all_distances

def printGraph(all_distances):

    x = [i * 5 for i in range(1, 35)] * 2
    y = [ 20 for i in range(1, 35) ] + [ 40 for i in range(1, 35) ]
    sizes = []

    for i in range(68):
        temp = []
        for row in all_distances:
            temp.append(row[i])
        sizes.append(temp)

    distances_mean = list(map(lambda input: np.mean(input) , sizes))

    print(len(x))
    print(len(y))
    print(len(distances_mean))

    print(f"Média: {np.dis}")
    # Criação do gráfico de bolhas
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=distances_mean, alpha=0.5, c='blue', edgecolors='w', linewidth=0.5)

    # Adicionando rótulos e título
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title('Gráfico de Bolhas')

    # Exibir o gráfico
    plt.grid(True)
    plt.show()

readData()