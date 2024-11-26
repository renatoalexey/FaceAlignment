import numpy as np
import matplotlib.pyplot as plt
import heapq
from enums.tecniques import Techs

def printGraphics(all_distances):
    plt.clf()

    colors = ['red', 'green', 'blue', 'orange', 'limegreen', 'goldenrod', 'lightskyblue']
    values = []
    stds = []
    filters = []
    blabla = []
    for tech in all_distances:
        filters.append(tech.f_name)
        if all_distances[tech]:
            if tech == Techs.NORMAL:
                blabla = all_distances[tech]
            valid_distances = list(filter(lambda num: num != -1, all_distances[tech]))
            values.append(np.mean(valid_distances))
            stds.append(np.std(valid_distances))
            #print(f"Filtro: {tech.f_name} Média: {np.mean(valid_distances)}")
            #print(f"The five smallest values are: {heapq.nsmallest(5, valid_distances)}")
           # print(f"Size: {len(all_distances[tech])}")

    plt.bar(filters, values, color=colors, yerr=stds, capsize=5)
    # Adicionando títulos e rótulos
    plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    plt.xlabel('Filtros/técnicas')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")

    plt.clf()
    chaves = all_distances.keys()
    data_size = len(all_distances[list(chaves)[0]])
    new_values = []
    #print(f"blabla: {len(blabla)}") 
    #print(blabla)
    #print(np.mean(blabla))
    for i in range(data_size):
        min = 1000000
        for chave in chaves:
            #try: 
            if all_distances[chave][i] != -1 and all_distances[chave][i] < min:
                    min = all_distances[chave][i]
            #except Exception as e:  # Handle any other exception
             #   print(f"An error occurred: {e}, i: {i}, chave: {chave}, all_dist: {all_distances[chave]}")
        if min != 1000000:
            new_values.append(min)

    #print(new_values)
    plt.bar(["Normal", "best"], [np.mean(blabla), np.mean(new_values)], color=colors, capsize=5)
    # Adicionando títulos e rótulos
    plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    plt.xlabel('Filtros/técnicas')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig("best.png")