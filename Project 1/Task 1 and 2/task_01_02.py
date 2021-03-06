import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def plotData2D(X, filename=None):
    # create a figure and its axes
    fig = plt.figure()
    axs = fig.add_subplot(111)

    # see what happens, if you uncomment the next line
    # axs.set_aspect('equal')
    # plot the data 
    axs.plot(X[0,:], X[1,:], 'ro', label='data')

    # set x and y limits of the plotting area
    xmin = X[0,:].min()
    xmax = X[0,:].max()
    axs.set_xlim(xmin-10, xmax+10)
    axs.set_ylim(-2, X[1,:].max()+10)

    # set properties of the legend of the plot
    leg = axs.legend(loc='upper left', shadow=True, fancybox=True, numpoints=1)
    leg.get_frame().set_alpha(0.5)

    # either show figure on screen or write it to disk
    if filename == None:
        plt.show()
    else:
        plt.savefig(filename, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1)
    plt.close()
    




if __name__ == "__main__":

    #######################################################################
    # Task 1.1: acquainting yourself with python for pattern recognition
    #######################################################################
    # read data as 2D array of data type 'object'
    data = np.loadtxt('whData.dat',dtype=np.object,comments='#',delimiter=None)

    # read height and weight data into 2D array (i.e. into a matrix)
    X = data[:,0:2].astype(np.float)

    # remove the outliers
    X = X[X[:,0] >= 0]

    # read gender data into 1D array (i.e. into a vector)
    y = data[:,2]

    # let's transpose the data matrix 
    X = X.T
    
    # now, plot weight vs. height using the function defined above
    plotData2D(X, 'plotWH.png')

    # next, let's plot height vs. weight 
    # first, copy information rows of X into 1D arrays
    w = np.copy(X[0,:])
    h = np.copy(X[1,:])
    
    # second, create new data matrix Z by stacking h and w
    Z = np.vstack((h,w))

    # third, plot this new representation of the data
    plotData2D(Z, 'plotHW.png')

    #######################################################################
    # Task 1.2: fitting a Normal distribution to 1D data
    #######################################################################

    # define type of data to be read and read data from file
    dt = np.dtype([('w', np.float), ('h', np.float), ('g', np.str_, 1)])
    data = np.loadtxt('whData.dat', dtype=dt, comments='#', delimiter=None)

    # read height, weight and gender information into 1D arrays
    ws = np.array([d[0] for d in data])
    hs = np.array([d[1] for d in data])
    gs = np.array([d[2] for d in data])

    # compute the mean and standard deviation using built-in numpy functions
    mean = np.mean(hs)
    std = np.std(hs)

    # draw the points on x axis
    x = np.linspace(hs.min()-10, hs.max()+10, 100)

    # for each point in x, plot the Normal distribution using built-in mlab function
    plt.plot(x, mlab.normpdf(x, mean, std))
    
    # plot the 1D heigh data
    plt.scatter(hs, np.zeros(hs.size))

    plt.grid(True)
    plt.show()
    print 'mean = ', mean
    print 'std = ', np.power(std, 2)