import re
import numpy as np
import matplotlib.pyplot as plt

def print_graph(means):
    plt.figure(figsize=(12, 7))
    plt.boxplot(means)
    plt.xlabel('Pontos fiduciais')
    plt.ylabel('Diferença em pixels')
    plt.show()

def get_distances(line):
    match = re.search(r"distances:\s*\[(.*?)\]", line)
    if match:
        values = match.group(1).split(",")   # separa por vírgula
        distances = [float(v.strip()) for v in values]  # converte pra float
        return distances
        #print(distances)

def run():
    cfp_resolutions_path = "output/cfp_resolutions.txt" 
    distance_means = []
    with open(cfp_resolutions_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            distances = get_distances(line)
            distance_means.append(np.mean(distances))
        print_graph(distance_means)
run()