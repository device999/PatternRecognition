__author__ = 'Aleksandr Korovin'

import numpy as np
import scipy, scipy.spatial
import matplotlib.pyplot as plt
import time

def macqueen_kmeans(data, k):
    centres = []
    #vector for storing cluster sizes
    n_clusters = np.zeros(len(data))
    #initialize means randomly
    for cluster in range(0, k):
        centres.append(data[np.random.randint(0, len(data), size=1)].flatten().tolist())

    clusters = [[] for i in range(k)]

    i = 0
    for j in range(len(data)):
        if j < k:
            centres[i] = data[j]
            n_clusters[i] = 1
            i = i + 1
        else:
            distance, mu_index = scipy.spatial.cKDTree(centres).query(data[j])
            # winner = centres[mu_index]
            # centres[i] = winner + (1/(n_clusters[i])) * (data[j] - winner)
            # n_clusters[i] = n_clusters[i] + 1
            winner = centres[mu_index]
            centres[mu_index] = winner + (1/(n_clusters[mu_index])) * (data[j] - winner)
            n_clusters[mu_index] = n_clusters[mu_index] + 1

    for idx, point in enumerate(data):
        distance, mu_index = scipy.spatial.cKDTree(centres).query(point)
        try:
            clusters[mu_index].append(point)
        except KeyError:
            clusters[mu_index] = [point]

    return clusters

colors = ["red", "green", "blue"]

def plot_differences(points, k, plot_index_x, plot_index_y, plot_index):
    clusters = macqueen_kmeans(points, k)
    plt.subplot(plot_index_x, plot_index_y, plot_index)

    for i in range(k):
        cluster = clusters[i]
        x = [a[0] for a in cluster]
        y = [a[1] for a in cluster]
        # plt.subplot(plot_index_x, plot_index_y, plot_index)
        plt.scatter(x, y, color = colors[i])

    plt.title('MacQueen algorithm')
    plt.ylabel("y")
    plt.xlabel("x")

def calc_average_time(points, k, num_iterations):
    time_iter = []
    for i in range(num_iterations):
        start = time.time()
        clusters = macqueen_kmeans(points, k)
        end = time.time() - start
        time_iter.append(end)
        print(end)

    val = np.mean(time_iter)
    print 'Average time for MacQueen algorithm:'
    print val

def main():
    k = 3
    data = np.loadtxt('data-clustering-1.csv',delimiter=',')
    points = np.array(data.transpose())

    for i in range(4):
        plot_differences(points, k, 2, 2, i + 1)
    plt.show()
    #calc_average_time(points, k, 10)




if __name__ == "__main__":
    main()
