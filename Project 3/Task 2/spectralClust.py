__author__ = 'Marina'

import numpy as np
import csv
import matplotlib.pyplot as plt
import math
from scipy.sparse import csgraph

def plotData(data1, data2, filename):

    fig = plt.figure(facecolor='white')

    #setting axes parameters
    axs = fig.add_subplot(111)
    #axs.set_aspect('equal')

    x1 = np.asarray(data1[0])
    y1 = np.asarray(data1[1])
    x2 = np.asarray(data2[0])
    y2 = np.asarray(data2[1])

    # plot the tree data points
    axs.scatter(x1, y1, 30, c='r', edgecolor='None')
    axs.scatter(x2, y2, 30, c='b', edgecolor='None')

    # either show figure on screen or write it to disk
    if filename == None:
        plt.show()
    else:
        plt.savefig(filename, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1, dpi=800)

    plt.close()

if __name__ == "__main__":

    data = []
    csvfile = open('data-clustering-2.csv', 'r', newline='')
    reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    for row in reader:
        new = [float(x) for x in row if x != '']
        data.append(new)

    #plotData(data, data, None)

    data = np.transpose(np.asarray(data))
    beta = 1

    S = np.zeros((data.shape[0], data.shape[0]))
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            S[i][j] = np.exp(-beta*np.linalg.norm(data[i]-data[j])**2)

    # The Laplacian matrix can be also computed using this built-in function
    # L = csgraph.laplacian(S, normed=False)

    D = np.zeros(S.shape)

    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            if i == j:
                D[i][j] = np.sum(S[:,j])

    L = D - S

    a, b = np.linalg.eig(L)

    dict = {}
    for i in range(a.shape[0]):
        dict[a[i]] = b[i]

    t = sorted(dict.items())
    fiedler = t[1]

    c1 = []
    c2 = []

    for i in range(fiedler[1].shape[0]):
        if fiedler[1][i] > 0:
            c1.append(data[i])
        else:
            c2.append(data[i])

    c1 = np.transpose(list(c1))
    c2 = np.transpose(list(c2))
    plotData(c1, c2, None)
