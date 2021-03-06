import math

def getDistance(pointA, pointB):
    X = math.pow(pointA[0] - pointB[0], 2)
    Y = math.pow(pointA[1] - pointB[1], 2)
    Z = math.pow(pointA[2] - pointB[2], 2)
    return math.sqrt(X + Y + Z)

def average(pointA, pointB):
    X = (pointA[0] + pointB[0])/2.0
    Y = (pointA[1] + pointB[1])/2.0
    Z = (pointA[2] + pointB[2])/2.0
    return (X, Y, Z)

def convertToInt(clusters):
    results = []
    for point in clusters:
        results.append((int(point[0]), int(point[1]), int(point[2])))
    return results

def removeClosestColor(clusters, point):
    closestPoint = None
    distance = float("inf")
    index = 0
    count = 0
    for cluster in clusters:
        if getDistance(point, cluster) < distance:
            distance = getDistance(point, cluster)
            closestPoint = cluster
            index = count
        count += 1
    clusters.remove(closestPoint)
    return (clusters, index)

def cluster(arr, num_clusters):
    clusters = []
    score = [0 for i in range(num_clusters)]
    for point in arr:
        if len(clusters) < num_clusters:
            clusters.append(point)
        else:
            closestPoint = -1
            distance = float("inf")
            for i in range(len(clusters)):
                testDistance = getDistance(clusters[i], point)
                if testDistance < distance:
                    distance = testDistance
                    closestPoint = i
            clusters[closestPoint] = average(clusters[closestPoint], point)
            score[closestPoint] += 1

    clusters = convertToInt(clusters)
    return (clusters, score)
