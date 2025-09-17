import os


def run():
    cfp_path = "/home/renatoalexey/Documents/Bases/cfp-dataset/Data/Images"

    for nome in os.listdir(cfp_path):
        caminho_completo = os.path.join(cfp_path, nome)
        if os.path.isdir(caminho_completo) and nome.isdigit():
            print(f"Pasta encontrada: {caminho_completo}")


run()