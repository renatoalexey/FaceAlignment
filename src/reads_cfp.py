import os
import face_alignment
from PIL import Image

def writesPointsNotFound(image_path, face_detected):
    with open("output/cfp_resolutions.txt", 'a') as file:
        image = Image.open(image_path)
        width, height = image.size
        color = image.mode

        file.write(f"Image: {image_path} resolution: {width}x{height} color: {color} face detected: {face_detected} \n")

def run():
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)
    cfp_path = "/home/renatoalexey/Documents/Bases/cfp-dataset/Data/Images/009"
    #cfp_path = "F:\\Bases\\cfp-dataset\\Data\\Images"

    i = 0
    for nome in os.listdir(cfp_path):
        #if i > 5: break
        folder_path = os.path.join(cfp_path, nome)
        if os.path.isdir(folder_path) and nome.isdigit():
            path_images_folder = f"{folder_path}/profile"
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
                    else: 
                        print("Deu ruim")
                    writesPointsNotFound(image_path, face_detected)
                except Exception as e:
                    print("Erro:", e)

                #i += 1
run()