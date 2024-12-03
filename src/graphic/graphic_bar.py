import numpy as np
import matplotlib.pyplot as plt
import heapq
from enums.tecniques import Techs
import seaborn as sns

def printGraphics(graph_name, all_distances, all_points_distances):
    plt.clf()

    colors = ['lightskyblue']
    values = []
    stds = []
    mins = []
    maxs = []
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
            mins.append(np.min(valid_distances))
            maxs.append(np.max(valid_distances))
            #print(f"Filtro: {tech.f_name} Média: {np.mean(valid_distances)}")
            #print(f"The five smallest values are: {heapq.nsmallest(5, valid_distances)}")
            #print(f"Size: {len(all_distances[tech])}")

    errors = [ [mean - min_val, max_val - mean] for mean, min_val, max_val in zip(values, mins, maxs)]
    errors = np.array(errors).T  # Transpor para uso em `yerr`
    plt.figure(figsize=(8, 7))
    plt.bar(filters, values, color=colors, capsize=5, yerr=stds)

    for i, value in enumerate(values):
        plt.text(i - 0.2, value + 0.1, str(round(value, 2)), ha='center', va='bottom')

    plt.ylim(0, 9)
    # Adicionando títulos e rótulos
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de redimensionamentos')
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de brilhos')
    plt.xlabel('Técnicas/Filtros')
    plt.ylabel('Diferença média em pixels')

    # Mostrar o gráfico
    plt.savefig(f"{graph_name}_comparassion.png")

    plt.clf()
    chaves = all_distances.keys()
    data_size = len(all_distances[list(chaves)[0]])
    new_values = []
    
    best_sum = {}

    for i in range(data_size):
        min = 1000000
        chaveMin = None
        for chave in chaves:
            if all_distances[chave][i] != -1 and all_distances[chave][i] < min:
                    min = all_distances[chave][i]
                    chaveMin = chave
        if min != 1000000:
            new_values.append(min)
            if chaveMin in best_sum:
                best_sum[chaveMin] += 1
            else:
                best_sum[chaveMin] = 1

    means = [np.mean(normal_values), np.mean(new_values)]
    stds = [np.std(normal_values), np.std(new_values)]
    
    #errors = [ [mean - min_val, max_val - mean] for mean, min_val, max_val in zip(all_values, [np.min(normal_values), np.min(new_values)], np.max(normal_values), np.max(new_values))]
    #errors = np.array(errors).T  # Transpor para uso em `yerr`
    
    plt.bar(["Normal", "Melhor"], means, color=colors, capsize=5, yerr=stds)
    # Adicionando títulos e rótulos
    #plt.title('Média da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignment após aplicação de filtro/técnica de pré-processamento')
    for i, value in enumerate([np.mean(normal_values), np.mean(new_values)]):
        plt.text(i, value + 0.1, str(round(value, 2)), ha='center', va='bottom')
    plt.xlabel('Técnicas/filtros')
    plt.ylabel('Diferença média em pixels')
    plt.ylim(0, 7)

    # Mostrar o gráfico
    plt.savefig(f"{graph_name}_best.png")

    best_tech = getBestTech(best_sum)
    printBoxPlot(graph_name, best_tech, all_points_distances[best_tech])
    
def getBestTech(best_sum):
    best_tech = None
    sum_temp = -1
    for sum in best_sum:
        with open('output/sums.txt', 'a') as file:
            file.write(f'tech: {sum} sum: {best_sum[sum]} \n')
        if best_sum[sum] > sum_temp:
            sum_temp = best_sum[sum]
            best_tech = sum
    return best_tech

def printBoxPlot(graph_name, best_tech, best_distances):

    valid_distances = np.array(list(filter(lambda num: num != -1, best_distances)))
    size = len(valid_distances[0])
    new_data = [valid_distances[:, i].tolist() for i in range(size)]
    split_index = len(new_data) // 2
 #   print(valid_distances)

    plt.figure(figsize=(10, 6))
    plt.boxplot(new_data[:split_index], whis=3)
    plt.xlabel('Pontos fiduciais')
    plt.ylabel('Diferença em pixels')
    #plt.title(f'Box plot da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignmentdiferença após aplicar {best_tech.f_name} por ponto fiducial')

    plt.savefig(f'{graph_name}_box1.png')

    plt.figure(figsize=(10, 6))
    plt.boxplot(new_data[split_index:], positions=[35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68], whis=3)
    plt.xlabel('Pontos fiduciais')
    plt.ylabel('Diferença em pixels')
    #plt.title(f'Box plot da diferença entre os pontos fiduciais rotulados e os extraídos pelo \n Face Alignmentdiferença após aplicar {best_tech.f_name} por ponto fiducial')

    plt.savefig(f'{graph_name}_box2.png')