import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import chi2

data = np.loadtxt('whData.dat',dtype=np.object,comments='#',delimiter=None)

# read height and weight data into 2D array (i.e. into a matrix)
data = data[:,0:2].astype(np.float)

# remove the outliers
data_train = data[data[:,0] >= 0]

# prediction data (outliers)
data_pred = data[data[:,0] ==-1]

# create height vector for prediction data
predict_x = np.copy(data_pred[:,1])

# create weight vector for train data
y = np.copy(data_train[:,0])
# create height vector for train data
x = np.copy(data_train[:,1])
#Rahimbeyli Sattar
#needed for calculation!
meanofweight = np.round(np.mean(y),2)
meanofheight = np.round(np.mean(x),2)
devweight = np.round(np.std(y),2)
devheight = np.round(np.std(x),2)
corrcoef = np.corrcoef(x,y)[0,1]
z = 0
predict_y =np.zeros([len(predict_x)])
while (z!=len(predict_x)):
    h0 = predict_x[z]
    predicted = meanofweight+corrcoef *(h0 - meanofheight) *devweight/devheight
    print predicted
    predict_y[z] = predicted
    z= z + 1
#done
#for graph

plt.plot(x, y, 'ro',predict_x,predict_y,'bs')
plt.axis([np.amin(x)-10, np.amax(x)+20, np.amin(y)-10, np.amax(y)+20])
plt.show()


