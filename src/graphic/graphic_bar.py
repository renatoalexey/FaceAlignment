import numpy as np
import matplotlib.pyplot as plt

def printGraphics(all_distances, image_types):
    colors = ['red', 'green', 'blue', 'orange']
    values = []
    stds = []
    # Barras para cada grupo
    for type in image_types:
        values.append(np.mean(all_distances[type]))
        stds.append(np.std(all_distances[type]))
  
    plt.bar(image_types, values, color=colors, yerr=stds, capsize=5)

    # Adicionando títulos e rótulos
    plt.title('Gráfico de Barras com Desvio Padrão')
    plt.xlabel('Categorias')
    plt.ylabel('Distâncias')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")