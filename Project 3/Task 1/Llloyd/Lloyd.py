import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import time


def plotit(plt, k, data, y_pred):
    colors = ["red", "green", "blue", "yellow"]
    for i in range(k):
        cluster = data[:,y_pred ==i]
        x= np.copy(cluster[1])    
        y = np.copy(cluster[0]) 
        plt.scatter(x, y,color = colors[i])
        

data = np.loadtxt('data-clustering-1.csv',delimiter=',')

n_samples=len(data[0])

# create y vector for data
y = np.copy(data[0])
    
# create x vector for data
x = np.copy(data[1])

#plot 
plt.scatter(y, x)
plt.ylabel("y")
plt.xlabel("x")
plt.title('Distribution of points')
plt.show()

# select the number of clusters
k = 3
num_iterations = 10

time_iter = []

for i in range(num_iterations):
    start = time.time()
    y_pred = KMeans(n_clusters=k).fit_predict(data.transpose())
    end = time.time() - start
    time_iter.append(end)
    print(end)
         
plotit(plt,k,data, y_pred)
plt.title('Lloyd algorithm')
plt.ylabel("y")
plt.xlabel("x")
plt.show()

import matplotlib.pyplot as plt
for step in range(1,5):
    y_pred = KMeans(n_clusters=k).fit_predict(data.transpose())
    plt.subplot(2,2,step)
    plotit(plt, k, data, y_pred)
plt.show()

val = np.mean(time_iter)
print 'Average time for Lloyd algorithm:'
print val