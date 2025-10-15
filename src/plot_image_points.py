import os
import math
import cv2
import matplotlib.pyplot as plt
import utils
from PIL import Image

ground_truth_file_path = 'F:\\Bases\\cfp-dataset\\Data\\Fiducials\\015\\profile\\02.txt'
img_path = utils.get_image_path(ground_truth_file_path)

def tests_face_alignment():
    fa_points = utils.get_face_alignment_points(img_path)
    if fa_points:
        prints_graphic(fa_points, utils.get_fa_correspondent_points())
   

def prints_graphic(library_points, correspondent_points):

    img = cv2.imread(img_path)

    width, height = img.shape[:2]
    #img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    ground_truth_points = utils.get_ground_truth_points(ground_truth_file_path)
    
    side = utils.verifies_img_side(img, ground_truth_points)
    print(f"Side: {side}")

    if ground_truth_points:        
        plt.imshow(img)
        for i, ground_truth_point in enumerate(ground_truth_points, start=1):
            if correspondent_points.get(i) is not None:
                library_point = library_points[0][correspondent_points.get(i)]
                x, y = ground_truth_point
                plt.scatter(x, y, color="red", s=10)
                plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0,5), ha='center', color="red", fontsize=8)
                
                a, b = library_point
                plt.scatter(a, b, color="blue", s=10)
                plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0,5), ha='center', color="blue", fontsize=8)
        plt.imshow(img)
        plt.axis("off")
        #plt.savefig('demon.png')
        plt.show()

def print_points(fiducial_points, plt, color='red'):
    for i, fiducial_point in enumerate(fiducial_points, start=1):
        x, y = fiducial_point
        x = float(x)
        y = float(y)
        #x = round(x * x_factor, 2)
        #y = round(y * y_factor, 2)
        plt.scatter(x, y, color=color, s=10)
        plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0,5), ha='center', color="red", fontsize=8)
    return plt 

tests_face_alignment()

