from skimage import io
from scipy.io import loadmat
from pathlib import Path
import face_alignment
import cv2
import math
import matplotlib.pyplot as plt
import os
import numpy as np

def calcEuclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

def readData():
    folder_image_path = Path('../images')
    folder_landmarks_path = '../landmarks/'

    all_distances = []

    for file_image_path in folder_image_path.iterdir():
        if file_image_path.is_file():
            file_name = os.path.splitext(os.path.basename(file_image_path))[0]
            file_landmarks_path = f'{folder_landmarks_path}{file_name}_pts.mat'

            distances = calcPointsDiffs(file_image_path, file_landmarks_path)

            if distances is not None: 
                all_distances.append(distances)
            else:
                print(distances)

    printGraph(all_distances)

def calcPointsDiffs(file_image_path, file_landmarks_path):
    data = loadmat(file_landmarks_path)
    data_points = data['pts_2d']

    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)
    input = io.imread(file_image_path)
    prediction_points = fa.get_landmarks(input)

    if prediction_points is not None:
        #for i, pred in enumerate(preds):
        #print(len(pred))
        euclidean_distances = []
        for i, pred_point in enumerate(prediction_points[0]):
            euclidean_distances.append( calcEuclideanDistance(pred_point[0], 
                pred_point[1], data_points[i][0], data_points[i][1])) 
            #cv2.circle(input, (int(pred_point[0]), int(pred_point[1])), 2, (0, 255, 0), -1)

        #cv2.imshow('dasas', input)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return euclidean_distances
    else:
        return None

def printGraph(all_distances):

    x = [i * 5 for i in range(1, 35)] * 2
    y = [ 20 for i in range(1, 35) ] + [ 40 for i in range(1, 35) ]
    sizes = []

    for i in range(68):
        temp = []
        for row in all_distances:
            temp.append(row[i])
        sizes.append(temp)

    distances_mean = list(map(lambda input: np.mean(input) * 10, sizes))

    print(len(x))
    print(len(y))
    print(len(distances_mean))

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