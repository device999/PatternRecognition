import math
import time
import numpy as np
import matplotlib.pyplot as plt
colors = ["red", "green", "blue"]

class Point:
    '''
    An point in n dimensional space
    '''
    def __init__(self, coords):
        '''
        coords - A list of values, one per dimension
        '''

        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)
    def __getitem__(self, n):
        return self.coords[n]

class Cluster:
    '''
    A set of points and their centroid
    '''

    def __init__(self, points):
        '''
        points - A list of point objects
        '''

        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        # The points that belong to this cluster
        self.points = points

        # The dimensionality of the points in this cluster
        self.n = points[0].n

        # Assert that all points are of the same dimensionality
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")

        # Set up the initial centroid (this is usually based off one point)
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)

    def pop(self, point):
        self.points.remove(point)
        self.centroid = self.calculateCentroid()

    def add(self, point):
        self.points.append(point)
        self.centroid = self.calculateCentroid()


    def calc_sse(self):
        def get_dist(point):
            ret = reduce(lambda x,y: x + pow((self.centroid.coords[y]-point.coords[y]), 2),range(point.n),0)
            return math.sqrt(ret)

        sse = sum(map(get_dist, self.points))
        return sse


    def calculateCentroid(self):
        '''
        Finds a virtual center point for a group of n-dimensional points
        '''
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [round (math.fsum(dList)/numPoints,5) for dList in unzipped]

        return Point(centroid_coords)

def get_sse_sum(clusters):
    """
    returns cluster with min sse
    """
    sse = [clust.calc_sse() for clust in clusters]
    return sum(sse)


def plotit(plt, k, clusters):
    colors = ["red", "green", "blue", "yellow"]
    for i in range(k): 
        cluster = clusters[i]
        x= [a.coords[0] for a in cluster.points]
        y= [a.coords[1] for a in cluster.points]
        plt.scatter(x, y,color = colors[i])

        
def kmeans(points, k, verbose, cutoff=50):
    loop_cnt = 0
    clusters =[]
    for i in range(k):
        dots = points[int(math.ceil(len(points) *i/k)): int(round(len(points) *(i+1)/k))]
        clusters.append(Cluster(dots))
    if verbose:
        for i in range(k):
            cluster = clusters[i]
            x= [a.coords[0] for a in cluster.points]
            y= [a.coords[1] for a in cluster.points]
            plt.scatter(x, y,color = colors[i])
        plt.show()
    while True:
        loop_cnt +=1
        centroids_old = [c.centroid for c in clusters]
        for n in range(k):
            for point in clusters[n].points:
                if len(clusters[n].points) > 1:
                    min_sum = get_sse_sum(clusters)
                    target_cluster = n
                    clusters[n].pop(point)
                    rng = range(k)
                    rng.remove(n)
                    for s in rng:
                        clusters[s].add(point)
                        sse = get_sse_sum(clusters)
                        if sse < min_sum :
                            min_sum = sse
                            target_cluster = s
                        clusters[s].pop(point)
                    clusters[target_cluster].add(point)
        centroids = [c.centroid for c in clusters]
        if verbose:
            plotit(plt, k, clusters)
            plt.show()                
            print centroids_old
            print centroids
        if str(centroids) == str(centroids_old) or loop_cnt >= cutoff:
            print "Converged after %s iterations" % loop_cnt
            break
            
                
    
    return clusters


def calc_average_time(points, k, num_iterations):
    time_iter = []
    for i in range(num_iterations):
        start = time.time()
        clusters = kmeans(points, k, False)
        end = time.time() - start
        time_iter.append(end)
        print(end)

    val = np.mean(time_iter)
    print 'Average time for Hartigan algorithm:'
    print val

def main():
    # The K in k-means.
    num_clusters = 3

    # When do we say the optimization has 'converged' and stop updating clusters
    

    data = np.loadtxt('data-clustering-1.csv',delimiter=',')
    points = [Point(x) for x in data.transpose()]
    # Cluster those data!
    clusters = kmeans(points, num_clusters, True)
    

    # Print our clusters    
    for i,c in enumerate(clusters):
        for p in c.points:
            print " Cluster: ", i, "\t Point :", p

    
    import matplotlib.pyplot as plt
    plotit(plt, num_clusters, clusters)
    plt.title('Hartigans algorithm')
    plt.ylabel("y")
    plt.xlabel("x")

    plt.show()

    calc_average_time(points, num_clusters, 10)
    import matplotlib.pyplot as plt
    for step in range(1,5):
        clusters = kmeans(points, num_clusters, False)
        plt.subplot(2,2,step)
        plotit(plt, num_clusters, clusters)
    plt.show()



if __name__ == "__main__":
    main()