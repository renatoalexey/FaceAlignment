import numpy as np
import matplotlib.pyplot as plt
import heapq
from enums.tecniques import Techs
import seaborn as sns

def printGraphics(all_distances, all_points_distances):
    plt.clf()

    colors = ['lightskyblue']
    values = []
    stds = []
    filters = []
    normal_values = []
    for tech in all_distances:
        filters.append(tech.f_name)
        if all_distances[tech]:
            if tech == Techs.NORMAL:
                normal_values = all_distances[tech]
            valid_distances = list(filter(lambda num: num != -1, all_distances[tech]))
            values.append(np.mean(valid_distances))
            stds.append(np.std(valid_distances))
            #print(f"Filtro: {tech.f_name} Média: {np.mean(valid_distances)}")
            #print(f"The five smallest values are: {heapq.nsmallest(5, valid_distances)}")
            #print(f"Size: {len(all_distances[tech])}")


    plt.figure(figsize=(8, 6))
    plt.bar(filters, values, color=colors, capsize=5)

    for i, value in enumerate(values):
        plt.text(i, value + 0.1, str(round(value, 2)), ha='center', va='bottom')

    plt.ylim(0, 6)
    # Adicionando títulos e rótulos
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de redimensionamentos')
    plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de brilhos')
    plt.xlabel('Filtros/técnicas')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig("comparassion.png")

    plt.clf()
    chaves = all_distances.keys()
    data_size = len(all_distances[list(chaves)[0]])
    new_values = []
    
    best_sum = {}

    for i in range(data_size):
        min = 1000000
        chaveMin = None
        for chave in chaves:
            #try: 
            if all_distances[chave][i] != -1 and all_distances[chave][i] < min:
                    min = all_distances[chave][i]
                    chaveMin = chave
            #except Exception as e:  # Handle any other exception
             #   print(f"An error occurred: {e}, i: {i}, chave: {chave}, all_dist: {all_distances[chave]}")
        if min != 1000000:
            new_values.append(min)
            if chaveMin in best_sum:
                best_sum[chaveMin] += 1
            else:
                best_sum[chaveMin] = 1

    print(best_sum)
    #print(new_values)
    plt.bar(["Normal", "best"], [np.mean(normal_values), np.mean(new_values)], color=colors, capsize=5)
    # Adicionando títulos e rótulos
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    plt.xlabel('Filtros/técnicas')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig("best.png")

    best_tech = getBestTech(best_sum)
    printBoxPlot(best_tech, all_points_distances[best_tech])

    
def getBestTech(best_sum):
    best_tech = None
    sum_temp = -1
    for sum in best_sum:
        if best_sum[sum] > sum_temp:
            sum_temp = best_sum[sum]
            best_tech = sum
    return best_tech

def printBoxPlot(best_tech, best_distances):

    valid_distances = list(filter(lambda num: num != -1, best_distances))

    plt.figure(figsize=(18, 6))
    sns.boxplot(data=valid_distances)

    # Adicionando rótulos e título
    plt.xlabel('Pontos fiduciais')
    plt.ylabel('Diferença em pixels')
    plt.title(f'Box plot da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignmentdiferença após aplicar {best_tech.f_name} por ponto fiducial')

    plt.savefig('box.png')