import os
import face_alignment
import math
from PIL import Image

correspondet_points = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 10, 10: 18, 11: 20, 12: 23, 13: 37, 15: 38, 17: 40, 18: 48, 19: 28, 20: 29, 21: 30, 22: 31, 25: 32, 28: 53, 26: 49, 29: 13} 

def writesPointsNotFound(image_path, face_detected):
    with open("output/cfp_resolutions.txt", 'a') as file:
        image = Image.open(image_path)
        width, height = image.size
        color = image.mode

        file.write(f"Image: {image_path} resolution: {width}x{height} color: {color} face detected: {face_detected} \n")



#ground_truth_points_path = "/home/renatoalexey/Documents/Bases/cfp-dataset/Data/Fiducials"
ground_truth_points_path = "F:\\Bases\\cfp-dataset\\Data\\Fiducials"
    
def get_arquives_folder(base_path, name, file_name):
    file_name = file_name.split('.')[0]
    return f"{os.path.join(base_path, name)}\\profile\\{file_name}.txt"

def run():
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)
    #cfp_path = "/home/renatoalexey/Documents/Bases/cfp-dataset/Data/Images/009"
    cfp_path = "F:\\Bases\\cfp-dataset\\Data\\Images"

    i = 0
    for nome in os.listdir(cfp_path):
        #if i > 5: break
        folder_path = os.path.join(cfp_path, nome)
        if os.path.isdir(folder_path) and nome.isdigit():
            path_images_folder = f"{folder_path}\\profile"
            print(f"Pasta encontrada: {folder_path}")
            for image_name in os.listdir(path_images_folder):
                image_path = os.path.join(path_images_folder, image_name)
                #print(f"Imagem encontrada: {image_name}")
                try:
                    prediction_points = fa.get_landmarks(image_path)
                    face_detected = False
                    if prediction_points is not None:
                        #print("Imagem processada")
                        face_detected = True
                        gt_points = get_ground_truth_points(get_arquives_folder(ground_truth_points_path, nome, image_name))
                        #print(f"Chegou aqui 1: ${len(gt_points)}")
                        compare_points(gt_points, prediction_points)
                        
                    else: 
                        print("Deu ruim")
                        
                    writesPointsNotFound(image_path, face_detected)
                    
                except Exception as e:
                    print("Erro:", e)

                #i += 1

def get_ground_truth_points(fiducials_folder):
    ground_truth_pts = []
    
    if os.path.exists(fiducials_folder):
        with open(fiducials_folder, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines, start=1):
                x, y = line.split(',')
                x = float(x)
                y = float(y)
                
                ground_truth_pts.append((x, y))

    return ground_truth_pts
    
def compare_points(ground_truth_pts, fa_pts):
    for i, groud_truth_point in enumerate(ground_truth_pts, start=1):
        if correspondet_points.get(i) is not None:
            fa_point = fa_pts[0][correspondet_points.get(i)]
            print(f"Chegou aqui: ${fa_point}")
            distance = calcEuclideanDistance(groud_truth_point[0], groud_truth_point[1],
                                  fa_point[0], fa_point[0])    
            
            with open("output/distances.txt", 'a') as file:
                file.write(f"Distance: {distance}\n")


def calcEuclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)

if os.path.exists('output/cfp_resolutions.txt'):
    os.remove('output/cfp_resolutions.txt')  
run()