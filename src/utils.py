import math
from PIL import Image
import os

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