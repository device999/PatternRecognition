import numpy as np
import math
import matplotlib.pyplot as plt


def newton(k,a,dataList):
    #We Input parameters 'k' and 'a' (alpha) into the function.
    N=len(dataList)

	#Calculated all the matrix elements of the Newtonian Method.
    B1=N/k-N*math.log(a)+np.sum(np.log(dataList))-np.sum(((dataList/a)**k)*np.log(dataList/a))
    B2=(k/a)*(np.sum((dataList/a)**k)-N)
    M11=-N/(k**2)-np.sum(((dataList/a)**k)*(np.log(dataList/a))**2)
    M22=(k/((a)**2))*(N-(k+1)*np.sum((dataList/a)**k))
    M12=M21=(1/a)*np.sum((dataList/a)**k)+(k/a)*np.sum(((dataList/a)**k)*np.log(dataList/a))-N/a
    return np.array(np.matmul(np.linalg.inv(np.matrix([[M11,M12],[M21,M22]])),np.array([-B1,-B2]))+np.array([k,a]))[0]


def iters(k,a,n,dataList):
    #This 'k' and 'a' are the initial parameters that we start with.
	#'n' is the number of iterations specified

	#Normally, a termination condition would also be specified, but since we have observed that 'k' and 'a' terminate to a fixed value,
	#when started from 'k'=1 and 'a'=1 in 20 iterations, no termination condition was written

	#Termination condition would be of the form while newPara!=oldPara (If they don't terminate exactly, we can specify a tolerance value)
    oldPara=np.array([k,a])
    for i in range(n):
        newPara=newton(oldPara[0],oldPara[1],dataList)
        oldPara=newPara
    return newPara


if __name__=="__main__":
	#numpy array was chosen as the calculations of the matrix elements becomes very simple
	histData=np.genfromtxt('myspace.csv', delimiter=",")[:,1]
	
	#Delete leading zeros.
	while histData[0]==0:
	    histData=np.delete(histData,0)
	
	#Generate x-Values for the histogram
	xValues=np.arange(1,len(histData)+1)

	#Data generation for Newton's Method.
	data=[];
	for i in range(len(histData)):
		data=np.append(data,[xValues[i]]*int(histData[i]))

	parameters=iters(1,1,20,data);
	k=parameters[0];
	a=parameters[1];

	plt.plot(xValues,histData)
	plt.axis([xValues[0],xValues[len(xValues)-1],0,max(histData)+10])

	#Scaling factor for the Weibull fit was derived by setting: scale_factor*integral[Weibull] = Area Under the Curve for Histogram
	plt.plot(sum(histData)*(k/a)*((xValues/a)**(k-1))*np.exp(-1*((xValues/a)**k)),'r')
	plt.legend(('Google Data','Scaled Weibull Fit'))
	plt.show()
 



