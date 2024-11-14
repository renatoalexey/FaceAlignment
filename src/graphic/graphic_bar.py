import numpy as np
import matplotlib.pyplot as plt

def printGraphics(all_distances, image_types):
    colors = ['red', 'green', 'blue', 'orange']
    values = []
    stds = []
    # Barras para cada grupo
    for type in image_types:
        if all_distances[type]:
            values.append(np.mean(all_distances[type]))
            stds.append(np.std(all_distances[type]))
        else:
            values.append(0)
            stds.append(0)
  
    plt.bar(image_types, values, color=colors, yerr=stds, capsize=5)

    # Adicionando títulos e rótulos
    plt.title('Gráfico de Barras com Desvio Padrão')
    plt.xlabel('Categorias')
    plt.ylabel('Distâncias')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")