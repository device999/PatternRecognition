import numpy as np
import matplotlib.pyplot as plt
 
def main():  
    # read data as 2D array of data type 'object'
    data = np.loadtxt('whData.dat',dtype=np.object,comments='#',delimiter=None)
    
    # read height and weight data into 2D array (i.e. into a matrix)
    data = data[:,0:2].astype(np.float)
    
    # remove the outliers
    data_train = data[data[:,0] > 0]
    
    # prediction data (outliers)
    data_pred = data[data[:,0] ==-1]
    
    # create height vector for prediction data
    predict_x = np.copy(data_pred[:,1])
    
    # create weight vector for train data
    y = np.copy(data_train[:,0])
    
    # create height vector for train data
    x = np.copy(data_train[:,1])
    
    d = [1, 5, 10] 
    
    #plot 
    plt.scatter(x, y)
    plt.ylabel("Weight")
    plt.xlabel("Height")
    plt.show()
    
    for i in d:
        #model, res, _,_ = np.linalg.lstsq(np.vander(x, i + 1), y)
        #predicator = np.poly1d(model) #polyfit
        #predicator = np.poly1d(np.polynomial.polynomial.polyfit(x,y,i)) #
        predicator = np.poly1d(np.polyfit(x,y,i)) #
                
        predict_y = predicator(predict_x)
        for n in range(len(predict_y)):
            print 'X = ', predict_x[n], '| Y = ',predict_y[n] 
        print "This is our polynomial function: \n", predicator
        #print predict_x, predict_y
        
        
        xs = np.linspace(x.min() - 1, x.max() + 1, 1000)
        ys = np.dot(np.vander(xs, i + 1), predicator) 
        plt.plot(xs, ys, '-')
        plt.plot(x, y, 'o')
        plt.plot(predict_x,predict_y,'*')
        plt.ylabel("Y: Weight")
        plt.xlabel("X: Height")
        plt.show()
        res = np.array([y[k] - predicator(x[k]) for k in range(len(x))])
        ssres = np.sum(res**2) 
        sstot =np.sum((y - np.mean(y))**2)
        r2 = 1-ssres/sstot
        print 'R-squared = ', r2
if __name__ == '__main__':
    main()
    