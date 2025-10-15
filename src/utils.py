import math
from PIL import Image
import os
import face_alignment
import boto3
import cv2

rekognition = boto3.client("rekognition", region_name="us-east-1")
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)

def compare_points(ground_truth_pts, library_pts, correspondet_points, vertical_distance=1, horizontal_distance=1):
    all_distances = []

    for i, groud_truth_point in enumerate(ground_truth_pts, start=1):
        if correspondet_points.get(i) is not None:
            try:
                fa_point = library_pts[correspondet_points.get(i)]
                distance = calc_euclidean_distance(groud_truth_point[0], groud_truth_point[1],
                        fa_point[0], fa_point[0], vertical_distance, horizontal_distance)    
                all_distances.append(distance)
            except IndexError:
                print(f"Valor do i: {i} ### valor do correspondente: {correspondet_points.get(i)}")
    return all_distances

def calc_euclidean_distance(x1, y1, x2, y2, vertical_distance=1, horizontal_distance=1):
    return round(math.sqrt( ( (x2 - x1) / horizontal_distance ) **2 + ( (y2 - y1) / vertical_distance ) **2), 2)

def writes_euclidean_distances(image_path, face_detected, all_distances, file_path):
    
    with open(file_path, 'a') as file:
        image = Image.open(image_path)
        width, height = image.size
        color = image.mode

        #print(image_path)
        img_index = image_path.index("Images")
        msg = (
            f"name: {image_path[img_index + 7:len(image_path)]}, resolution: {width}x{height}, color: {color}, face detected: {face_detected}, "
            f"distances: {all_distances}, mean: { 0 if len(all_distances) == 0 else sum(all_distances) / len(all_distances)}\n"
        )

        file.write(msg)

def get_image_path(fiducials_file_path):
    return fiducials_file_path.replace("Fiducials", "Images").replace("txt", "jpg")
    #images_index = image_path.index("Images")
    
    #return image_path[images_index + len("Images"):len(image_path)]

def get_ground_truth_points(fiducials_folder):
    ground_truth_pts = []
    
    if os.path.exists(fiducials_folder):
        with open(fiducials_folder, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x, y = line.split(',')
                x = float(x)
                y = float(y)
                ground_truth_pts.append((x, y))

    return ground_truth_pts

def get_face_alignment_points(image_path):
    return fa.get_landmarks(image_path)

def get_fa_correspondent_points(img, ground_truth_points):
    if verifies_img_side(img, ground_truth_points) == True:
        return {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10, 10: 18, 11: 20, 12: 23, 13: 37, 15: 38, 17: 40, 18: 48, 19: 28, 20: 29, 21: 30, 22: 31, 25: 32, 28: 53, 26: 49, 29: 13} 
    return {2: 16, 3: 15, 4: 14, 5: 13, 6: 12, 7: 11, 8: 10, 9: 7, 10: 27, 11: 26, 12: 23, 12: 23, 14: 46, 15: 45, 16: 48, 18: 47, 20: 29, 21: 30, 22: 31, 23: 33, 24: 36, 26: 65, 27: 52, 29: 58, 30: 60}

def verifies_img_side(img, ground_truth_points):
    
    width, height = img.shape[:2]
    x = ground_truth_points[21][0]
    return x > width/2


def get_amazon_points(image_path):
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()

    # --- Chama o Rekognition ---
    response = rekognition.detect_faces(
        Image={'Bytes': img_bytes},
        Attributes=['ALL']
    )

    img = cv2.imread(image_path)
    h, w, _ = img.shape

    amazon_pts = []
    #print(f"Qte de faces: {response["FaceDetails"]}")
    # --- Para cada rosto detectado ---
    for face in response["FaceDetails"]:
        for landmark in face["Landmarks"]:
            x = float(landmark["X"] * w)
            y = float(landmark["Y"] * h)
            amazon_pts.append((x, y))

    return amazon_pts