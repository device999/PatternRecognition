import numpy as np
import matplotlib.pyplot as plt

def generateUnitCircle(p):
    '''
    Generates a unit circle of norm p
    '''
    exponent = np.true_divide(1,p)

    x = np.arange(-1.0, +1.0, 0.001) # to accelerate the processing, increase the last parameter

    uppercircle_y = np.power(1 - np.abs(np.power(np.abs(x), p)), exponent)
    lowercircle_y = -np.power(1 - np.abs(np.power(np.abs(x), p)), exponent)

    coordinates_x = np.append(x, x[::-1])
    coordinates_y = np.append(uppercircle_y, lowercircle_y[::-1])

    return coordinates_x, coordinates_y

def plotData2D(x, y, p, filename=None):

    fig = plt.figure(facecolor='white')

    #setting axes parameters
    axs = fig.add_subplot(111)
    axs.set_aspect('equal')
    axs.axhline(0, color='black', lw=1)
    axs.axvline(0, color='black', lw=1)
    axs.set_xlim(x.min(), x.max())
    axs.set_ylim(y.min(), y.max())

    # plotting the generated coordinates
    axs.plot(x, y, c='b')
    plt.xlabel("p = " + np.str(p), fontsize="16")

    # either show figure on screen or write it to disk
    if filename == None:
        plt.show()
    else:
        plt.savefig(filename, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1, dpi=800)
    plt.close()


if __name__ == "__main__":

    # generating a unit circle of norm p as a parameter
    pnorm = 0.5
    coord_x, coord_y = generateUnitCircle(pnorm)

    plotData2D(coord_x, coord_y, pnorm, np.str(pnorm) + "norm.png")