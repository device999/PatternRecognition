__author__ = 'aw3s0_000'

import numpy as np
import time
from scipy.stats import itemfreq

'''
Determine k data points in data that are closest to the query point (query_point)
'''
def k_nearest_neighbors(data, query_point, k):
    #calculate distance vector and use argsort - to sort the indices.
    sorted_inds = np.argsort(np.sum((data - query_point)**2, axis=1))
    #return first k of sorted indices
    return sorted_inds[:k]

'''
Calculate majority voting
Returns class of element which has the more votes
Input - neighbor vector
'''
def classify(neighbors):
    freqresult = itemfreq(neighbors)
    sorted_freq = freqresult[freqresult[:, 1].argsort()[::-1]]
    return sorted_freq[0, 0]

def calc_accuracy(test_data, predictions):
    correct = 0
    num_patterns = test_data.shape[0];
    for data_index in xrange(num_patterns):
        if test_data[data_index, -1] == predictions[data_index]:
            correct += 1
    return (correct/float(num_patterns)) * 100.0

def calc_knn_for_k(data_train, data_test, k):
    #number of attributes without classification (last column)
    num_attributes = data_test.shape[1] - 1

    #remove last column containing class assign results
    data_train_without_class = data_train[:, :num_attributes]
    predictions = []

    for q_point_index in xrange(len(data_test)):
        #find neighbors
        neighbors = k_nearest_neighbors(data_train_without_class, data_test[q_point_index, :num_attributes], k)
        prediction = classify(data_train[neighbors, -1])
        predictions.append(prediction)

    accuracy = calc_accuracy(data_test, predictions)
    print('Accuracy for k: ' + repr(k) + ' is : ' + repr(accuracy) + ' %')

if __name__=="__main__":
    #data to evaluate accuracy
    data_test = np.loadtxt('data2-test.dat', ndmin=2)
    #data that knn uses to make predictions
    data_train = np.loadtxt('data2-train.dat', ndmin=2)

    if data_test.shape[1] != data_train.shape[1]:
        raise IOError("Number of attributes of train and test data should be the same")

    k_arr = [1, 3, 5]

    #start measuring time for k = 1
    start = time.time()
    calc_knn_for_k(data_train, data_test, k_arr[0])
    end = time.time()

    calc_knn_for_k(data_train, data_test, k_arr[1])
    calc_knn_for_k(data_train, data_test, k_arr[2])

    print('Time elapsed for k = 1 ' + repr(end - start))