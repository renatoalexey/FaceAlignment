import numpy as np
import matplotlib.pyplot as plt
from enums.tecniques import Techs 

def printGraphics(all_distances, image_types):
    plt.clf()

    colors = ['red', 'green', 'blue', 'orange']
    values = []
    stds = []
    filters = []

    for tech in Techs:
        filters.append(tech.f_name)
        if all_distances[tech.name]:
            values.append(np.mean(all_distances[tech.name]))
            stds.append(np.std(all_distances[tech.name]))
        else:
            values.append(0)
            stds.append(0)
  
    plt.bar(filters, values, color=colors, yerr=stds, capsize=5)

    # Adicionando títulos e rótulos
    plt.title('Erro médio por filtro')
    plt.xlabel('Filtros')
    plt.ylabel('Erro médio')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")