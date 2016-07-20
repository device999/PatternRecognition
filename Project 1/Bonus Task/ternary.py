import numpy as np
import matplotlib.pyplot as plt

def generateCircleEuclid(center_x, center_y, radius, transform):
    '''
    Generates coordinates of a circle in Euclidean space with given center and radius.
    Depending on parameter transform, it either transforms the coordinates to compositions or not.
    Then it plots the circle.
    :param center_x:
    :param center_y:
    :param radius:
    :param transform:
    :return:
    '''

    uppercircle_x = np.arange(center_x - radius, center_x + radius, 0.0005) # to accelerate the processing, increase the last parameter
    uppercircle_y = np.sqrt(np.abs(radius*radius - (uppercircle_x-center_x)*(uppercircle_x-center_x))) + center_y
    lowercircle_y = -np.sqrt(np.abs(radius*radius - (uppercircle_x-center_x)*(uppercircle_x-center_x))) + center_y

    coordinates_x = np.append(uppercircle_x, uppercircle_x[::-1])
    coordinates_y = np.append(uppercircle_y, lowercircle_y)

    coordinates_x = np.array([1])
    coordinates_y = np.array([1])

    if (transform):
        coordinates_x, coordinates_y = transformToCompositions(coordinates_x, coordinates_y)

    col = [cm(float(i)/(coordinates_x.size)) for i in range(coordinates_x.size)]
    axs.scatter(coordinates_x, coordinates_y, 2, c=col, edgecolors='none')

def transformToCompositions(euclead_x, euclead_y):
    '''
    Transforms the Eucledean space coordinates into compositions and
    further into coordinates suitable for representation on ternary plot
    :param euclead_x:
    :param euclead_y:
    :return:
    '''

    contrastMatrix = np.matrix([[1/np.sqrt(6), 1/np.sqrt(6), -np.sqrt(np.true_divide(2,3))], [1/np.sqrt(2), -1/np.sqrt(2), 0]])

    vector_x = np.array([])
    vector_y = np.array([])


    for i in range(euclead_x.size):
        # each pair of Eucledean coordinates is multiplied by the contrast matrix
        pair = np.array([euclead_x[i], euclead_y[i]])
        composition = np.asarray(np.dot(pair,contrastMatrix))[0]
        sum = 0

        # the inverse closure operator is applied to the result
        for i in range(composition.size):
            composition[i] = np.exp(composition[i])
            sum += composition[i]

        # the coordinates are normalized and compositions are obtained
        for i in range(composition.size):
            composition[i] = composition[i]/sum

        # calculating the compositions' coordinates for a ternary plot
        # y = sqrt(3) * (x - coord[1])
        y = composition[0] * height
        x = y / np.sqrt(3) + composition[1]
        vector_x = np.append(vector_x, x)
        vector_y = np.append(vector_y, y)

    return vector_x, vector_y

if __name__ == "__main__":

    fig = plt.figure()
    axs = fig.add_subplot(111, axisbg = 'white', )
    axs.set_aspect('equal')
    axs.set_xlim(-0.1, 1.1)
    axs.set_ylim(-0.1, 1)

    cm = plt.get_cmap("Spectral")

    # declaring the constants
    height = np.sqrt(3)/2
    offset = 0.05

    # drawing the center, the sides of the triangle and the axis labels
    axs.plot(0.5, height/3, linestyle='None', color='blue', markersize=3, marker="o")

    axs.plot([0, 0.5],[0, height], color='k', linewidth=1.5)
    axs.plot([0, 1],[0, 0], color='k', linewidth=1.5)
    axs.plot([0.5, 1],[height, 0], color='k', linewidth=1.5)

    axs.text(0 - offset, 0 - offset, r'$e_3$', style='italic', color='k', fontsize='16')
    axs.text(1 + offset/4, 0 - offset, r'$e_2$', style='italic', color='k', fontsize='16')
    axs.text(0.5 - offset/2, height + offset/2, r'$e_1$', style='italic', color='k', fontsize='16')

    # plot circles with center in (0,0) and various radii
    generateCircleEuclid(0,0,1,True)
    generateCircleEuclid(0,0,2,True)
    generateCircleEuclid(0,0,3,True)

    # uncomment to plot circles with center (1,1) of various radii in gradient color code
    """
    generateCircleEuclid(1, 1, 0.3, True)
    generateCircleEuclid(1, 1, 1, True)
    generateCircleEuclid(1, 1, 2, True)
    generateCircleEuclid(1, 1, 3, True)
    generateCircleEuclid(1, 1, 5, True)
    """

    # plots a circle in gradient color code as a legend
    generateCircleEuclid(0.1, 0.8, 0.1, False)

    axs.xaxis.set_visible(False)
    axs.yaxis.set_visible(False)

    filename = None#'circles1.png'
    # either show figure on screen or write it to disk
    if filename == None:
        plt.show()
    else:
        plt.savefig(filename, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1, dpi=800)
    plt.close()