import os
import face_alignment

def run():
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)
    #cfp_path = "/home/renatoalexey/Documents/Bases/cfp-dataset/Data/Images"
    cfp_path = "F:\\Bases\\cfp-dataset\\Data\\Images"

    i = 0
    for nome in os.listdir(cfp_path):
        #if i > 5: break
        caminho_completo = os.path.join(cfp_path, nome)
        if os.path.isdir(caminho_completo) and nome.isdigit():
            path_images_folder = f"{caminho_completo}\\profile"
            print(f"Pasta encontrada: {caminho_completo}")
            for image in os.listdir(path_images_folder):
                image_path = os.path.join(path_images_folder, image)
                print(f"Imagem encontrada: {image}")
                try:
                    prediction_points = fa.get_landmarks(image_path)
                    if prediction_points is not None:
                        print("Imagem processada")
                    else: 
                        print("Deu ruim")
                except Exception as e:
                    print("Erro:", e)

                #i += 1
run()