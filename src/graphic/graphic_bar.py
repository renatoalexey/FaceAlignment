import numpy as np
import matplotlib.pyplot as plt
from enums.tecniques import Techs 
from enums.bright_type import Brights

def printGraphics(all_distances, image_types):
    plt.clf()

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'lightskyblue']
    values = []
    stds = []
    filters = []

    for tech in Brights:
        filters.append(tech.f_name)
        if all_distances[tech.name]:
            values.append(np.mean(all_distances[tech.name]))
            stds.append(np.std(all_distances[tech.name]))
        else:
            values.append(0)
            stds.append(0)
  
    plt.bar(filters, values, color=colors, yerr=stds, capsize=5)

    # Adicionando títulos e rótulos
    plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo Face Alignment após aplicação de filtro/técnica de pré-processamento')
    plt.xlabel('Filtros/técnicas')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")