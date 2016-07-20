import numpy as np
import matplotlib.pyplot as plt

#Creates the 'W' Matrix from the lectures
#Each row is created by taking one data point and raising it to various powers as per the column
#i.e., 0th Column - (x_i)^0, 1st Column - (x_i)^1, 2nd Column - (x_i)^2 and so on..
def xMatrix(l,d):
    xMatrix=np.zeros((len(l),d))
    for i in range(len(l)):
        for j in range(d):
            xMatrix[i][j]=l[i]**j
    return xMatrix

#Calculates the solution to the MAP weights equation - argmax_w(p(w|D))
def MAP(x,y,d,sigma0square):
    X=xMatrix(x,d)
    return np.matmul(np.linalg.inv(np.matmul(np.transpose(X),X)+(np.var(y)/sigma0square)*np.identity(d)),np.matmul(np.transpose(X),y))


if __name__=="__main__":
	data=np.genfromtxt("/whData.dat")

	dataOut=data[data[:,0]>0]	#Data Without Outliers
	dataWOut=data			#Data With Outliers	
	
	#Separates the data from file into height and weight data columns
	height=dataOut[:,1]#x
	weight=dataOut[:,0]#y
	
	weights=MAP(height,weight,6,33)

	pol=np.poly1d(np.flipud(weights))#Creates a polynomial given the weights. #FLIPUD flips the order of weights in poly1d function
	plt.scatter(height,weight)
	plt.plot(np.arange(140,205,0.1),pol(np.arange(140,205,0.1)))
	plt.legend(('d=5 Fit','Data Without Outliers'), loc=3)
	#plt.axis([np.amin(height)-10, np.amax(height)+20, np.amin(weight)-10, np.amax(weight)+20])
	plt.axis([150,200,-50,200])
	plt.show()




