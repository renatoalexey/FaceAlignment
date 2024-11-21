import numpy as np
import matplotlib.pyplot as plt
from enums.tecniques import Techs 
from enums.bright_type import Brights

def printGraphics(all_distances):
    plt.clf()

    colors = ['red', 'green', 'blue', 'orange', 'limegreen', 'goldenrod', 'lightskyblue']
    values = []
    stds = []
    filters = []

    for tech in all_distances:
        filters.append(tech.f_name)
        if all_distances[tech]:
            values.append(np.mean(all_distances[tech]))
            stds.append(np.std(all_distances[tech]))
            print(f"Filtro: {tech.f_name} Média: {np.mean(all_distances[tech])}")
        else:
            values.append(0)
            stds.append(0)
  
    plt.bar(filters, values, color=colors, yerr=stds, capsize=5)

    # Adicionando títulos e rótulos
    plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    plt.xlabel('Filtros/técnicas')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")