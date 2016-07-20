__author__ = 'Marina'
import numpy as np

class kDTree():

    def __init__(self, X, split_dim, split_dim_style, split_point_style, depth, rectangle):
        '''
        Creates a node of a kD-tree
        :param X: the data passed to the node
        :param split_dim: the splitting dimension passed to the node
            0 for x axis
            1 for y axis
        :param split_dim_style: determine splitting dimension style
            0 for round robin
            1 for higher variance dimension
        :param split_point_style: determite splitting point style
            0 for splitting at midpoint
            1 for splitting at median
        :param depth: the depth of the current node in the tree
        :param rectangle: the rectangle for the current node
        '''
        self.left = None
        self.right = None
        self.split_point = None
        self.X = X
        self.split_dim = split_dim
        self.depth = depth
        self.rectangle = rectangle
        self.split_dim_style = split_dim_style
        self.split_point_style = split_point_style

        # if the node is a leaf, exit
        if (self.X.size <= 2):
            self.split_point = self.X[0]
            return

        # adjust the node's splitting dimension according to the chosen splitting dimension style
        if (self.split_dim_style):
            # split along the dimension with higher variance
            self.split_dim = 0 if (np.var(self.X[:,0]) > np.var(self.X[:,1])) else 1
            new_dim = self.split_dim
        else:
            # split in round robin fashion
            self.split_dim = split_dim
            new_dim = 1 - self.split_dim

        self.data = self.X[:,self.split_dim]
        self.data = np.sort(self.data)

        # choose splitting point according to the chosen splitting point style
        if (self.split_point_style):
            # split according to median of data
            if ((self.data.size % 2) == 0):
                self.split_point = self.data[self.data.size/2 - 1]
            else:
                self.split_point = self.data[self.data.size/2]
        else:
            # split according to midpoint of data
            n = np.argmax(self.data > np.mean(self.data))
            self.split_point = self.data[n-1]

        # store the splitting point in a separate variable and remove it from the node's data
        point = self.X[self.X[:,self.split_dim] == self.split_point]
        self.X = self.X[self.X[:,self.split_dim] != self.split_point]

        # split the data in two parts according to the splitting point
        left_data = self.X[self.X[:,self.split_dim] <= self.split_point]
        right_data = self.X[self.X[:,self.split_dim] > self.split_point]

        # compute the new rectangles for the child nodes using the current node's rectangle
        # and changing it according the new spliting point
        rect_left = self.rectangle.copy()
        rect_right = self.rectangle.copy()

        if (self.split_dim):
            # the split is according to y axis (horizontal line)
            rect_left[3] = self.split_point
            rect_right[1] = self.split_point
        else:
            # the split is according to x axis (vertical line)
            rect_left[2] = self.split_point
            rect_right[0] = self.split_point

        self.split_point = point[0]

        # if the splitted data parts are not empty, add the appropriate node in the kD-tree
        if (left_data.size > 0):
            self.left = kDTree(left_data, new_dim, self.split_dim_style, self.split_point_style, depth+1, rect_left)
        if (right_data.size > 0):
            self.right = kDTree(right_data, new_dim, self.split_dim_style, self.split_point_style, depth+1, rect_right)

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def getNodeValue(self):
        return self.split_point

    def getNodeDepth(self):
        return self.depth

    def getNodeRectangle(self):
        return self.rectangle

    def getNode(self):
        return self

    def getSplitDimension(self):
        return self.split_dim

    def printTree(self, tree):
        '''
        Traverses a kD-tree and prints its nodes along with its parameters
        :param tree:
        :return:
        '''
        if tree != None:
            self.printTree(tree.getLeftChild())
            print("nodevalue, left child, right child, depth splitting dimension", tree.getNodeValue(), tree.getLeftChild(), tree.getRightChild(), tree.getNodeDepth(), tree.getSplitDimension())
            self.printTree(tree.getRightChild())

    nearest_neighbor = None

    def query_nearest_neighbor(self, kdtree, query_point):
        '''
        Calls the find_nearest_neighbor function recursively to find the nearest neigbor
        of a query point; initiates the function with the root of the input kD-tree;
        returns the nearest neighbor of the query point
        :param kdtree:
        :param query_point:
        :return: nearest_neighbor
        '''
        self.nearest_neighbor = kdtree.getNodeValue()
        self.find_nearest_neighbor(kdtree, query_point, self.nearest_neighbor)
        return self.nearest_neighbor

    def find_nearest_neighbor(self, kdtree, query, nearest_neighbor):
        '''
        Recursively moves down a kD-tree comparing the query point to node values;
        choses the closes point among the traversed node values
        :param kdtree:
        :param query:
        :param nearest_neighbor:
        '''
        root = kdtree.getNodeValue()

        if (np.linalg.norm(query-root) <= np.linalg.norm(query-nearest_neighbor)):
            self.nearest_neighbor = root
        else:
            self.nearest_neighbor = nearest_neighbor

        #print("closest_point, query, root, r, split_dim",nearest_neighbor, query, root, kdtree.getSplitDimension(),np.linalg.norm(query-root), np.linalg.norm(query-self.nearest_neighbor) )

        if (kdtree.getSplitDimension()):
            if (query[1] <= root[1]):
                if (kdtree.left is not None):
                    self.find_nearest_neighbor(kdtree.getLeftChild(), query, self.nearest_neighbor)
            else:
                if (kdtree.right is not None):
                    self.find_nearest_neighbor(kdtree.getRightChild(), query, self.nearest_neighbor)
        else:
            if (query[0] <= root[0]):
                if (kdtree.left is not None):
                    self.find_nearest_neighbor(kdtree.getLeftChild(), query, self.nearest_neighbor)
            else:
                if (kdtree.right is not None):
                    self.find_nearest_neighbor(kdtree.getRightChild(), query, self.nearest_neighbor)