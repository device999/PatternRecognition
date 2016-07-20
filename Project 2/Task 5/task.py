__author__ = 'Marina'

import numpy as np
from kdtreeTask.kd_tree import kDTree
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

set_of_rectangles = []

def traverseKDTree(tree):
    '''
    Traverses the kDTree to store the rectangle of each node in a list
    :param tree:
    '''
    if tree != None:
        traverseKDTree(tree.getLeftChild())
        set_of_rectangles.append(tree.rectangle)
        traverseKDTree(tree.getRightChild())

def plotkDTree(tree, data, filename=None):

    fig = plt.figure(facecolor='white')

    #setting axes parameters
    axs = fig.add_subplot(111)
    #axs.set_aspect('equal')

    x = data[:,0]
    y = data[:,1]

    axs.set_xlim(x.min() - 1, x.max() + 1)
    axs.set_ylim(y.min() - 1, y.max() + 1)

    # plot the tree data points
    axs.scatter(x, y, 20, c='r', edgecolor='None')

    traverseKDTree(tree)

    # plot each node's rectangle
    for i in range(len(set_of_rectangles)):
        r = set_of_rectangles[i]
        axs.add_patch(patches.Rectangle((r[0], r[1]), r[2] - r[0], r[3] - r[1], fill=False))

    # either show figure on screen or write it to disk
    if filename == None:
        plt.show()
    else:
        plt.savefig(filename, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1, dpi=800)
    plt.close()

if __name__ == "__main__":

    # read the train and test data
    dt = np.dtype([('w', np.float), ('h', np.float), ('g', np.str_, 1)])
    train_data = np.loadtxt('data2-train.dat', dtype=dt, comments='#', delimiter=None)
    train_data = np.array([[d[0], d[1]] for d in train_data])
    test_data = np.loadtxt('data2-test.dat', dtype=dt, comments='#', delimiter=None)
    test_data = np.array([[d[0], d[1]] for d in test_data])

    #train_data = train_data[:5]
    x = train_data[:,0]
    y = train_data[:,1]
    rectangle = [np.min(x), np.min(y), np.max(x), np.max(y)]

    # uncomment to compute a kDTree on the training data with the following input settings:
    #   select splitting dimensions in round robin fashion
    #   split at midpoint of the data
    newTree = kDTree(train_data, 0, 0, 0, 0, rectangle)

    #   select splitting dimensions in round robin fashion
    #   split at median of the data
    #newTree = kDTree(train_data, 0, 0, 1, 0, rectangle)

    #   select splitting dimension with higher variance
    #   split at midpoint of the data
    #newTree = kDTree(train_data, 0, 1, 0, 0, rectangle)

    #   select splitting dimension with higher variance
    #   split at median of the data
    #newTree = kDTree(train_data, 0, 1, 1, 0, rectangle)

    total_query_time = 0

    # compute 1-nearest neighbor for the test data
    print("computing 1-nearest neighbor for the test data...")
    for i in range(test_data.shape[0]):
        start = time.clock()
        nn = newTree.query_nearest_neighbor(newTree,test_data[i])
        total_query_time += time.clock() - start

    print("total query time", total_query_time)

    plotkDTree(newTree, train_data, "new.png")
    #newTree.printTree(newTree)