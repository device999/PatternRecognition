import numpy as np
import matplotlib.pyplot as plt

def generateSinusoid(amplitude, cmap):
    x = np.arange(0, 1, 0.0001)
    y = amplitude * np.sin(2*np.pi*x)

    col = [cmap(float(i)/(x.size)) for i in range(x.size)]
    axs.scatter(x, y, 2, c=col, edgecolors='none')

    x1, x2 = transformToCompositions(x,y)
    axs2.scatter(x1, x2, 2, c=col, edgecolors='none')

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

    plt.figure(1)
    axs = plt.subplot(122)
    #axs.set_aspect('equal')
    axs.grid(True)

    axs2 = plt.subplot(121)
    axs2.set_aspect('equal')
    axs2.set_xlim(-0.15, 1.15)
    axs2.set_ylim(-0.1, 1)

    # declaring the constants
    height = np.sqrt(3)/2
    offset = 0.05

    axs2.plot(0.5, height/3, linestyle='None', color='blue', markersize=3, marker="o")

    axs2.plot([0, 0.5],[0, height], color='k', linewidth=1.5)
    axs2.plot([0, 1],[0, 0], color='k', linewidth=1.5)
    axs2.plot([0.5, 1],[height, 0], color='k', linewidth=1.5)

    axs2.text(0 - offset, 0 - offset, r'$e_1$', style='italic', color='k', fontsize='20')
    axs2.text(1 + offset/4, 0 - offset, r'$e_2$', style='italic', color='k', fontsize='20')
    axs2.text(0.5 - offset/2, height + offset/2, r'$e_3$', style='italic', color='k', fontsize='20')

    axs2.xaxis.set_visible(False)
    axs2.yaxis.set_visible(False)

    generateSinusoid(0.5, plt.get_cmap("gist_heat"))
    generateSinusoid(1, plt.get_cmap("winter"))
    generateSinusoid(2, plt.get_cmap("autumn"))

    plt.show()