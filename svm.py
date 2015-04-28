import os
import sys
import fnmatch
import getopt
import cv2
import numpy as np
import numpy
import datetime
from sklearn import svm
from heapq import *
from gasp import *


number_of_bins = 64
positive = 'dataset/positive'
negative = 'dataset/negative'
ds = 'dataset'


# Get all 'png' images from 'negative' and 'positive' folder
def getImages():
    imageFiles = []
    for i in range(2):
        if i == 0:
            path = positive
        elif i == 1:
            path = negative
        for j in sorted(os.listdir(path)):
            if fnmatch.fnmatch(j, '*.png'):
                imageFiles.append(j)
        i += 1
    return imageFiles


# Returns histogram result
def getHistogram(imageFiles):
    image = cv2.imread(imageFiles)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([gray],[0],None,[number_of_bins],[0,number_of_bins])
    transp = histogram.transpose()
    return transp.astype(np.float64)


# Gets all pictures' histograms
def getHistograms():
    images = getImages()
    histogramMap = {}
    for i in images:
        im = positive +'/'+ i
        histogramMap[im] = getHistogram(im)
    for i in images:
        im = negative +'/'+ i
        histogramMap[im] = getHistogram(im)
    return histogramMap.values()


# Sets the values positive 1 negative 0 for svm values
def getValues():
    values = []
    for i in range(2):
        if i == 0:
            path = positive
            j = 0
        elif i == 1:
            path = negative
            j = 1
        for i in sorted(os.listdir(path)):
            values.append((j,))
    return values


# Splits the matrix in desired format
def split(mtx,num):
    matrix = np.array(mtx)
    matrix_splitted = np.array(np.split(matrix, num))
    return np.fliplr(matrix_splitted)
    
    
# SVM learn and classify
def train():
    now = datetime.datetime.now()
    array = []
    trainData = map(lambda x: x[0], getHistograms())
    value = getValues()

    classify = svm.SVC(kernel='linear')
    classify.fit(trainData, value)


    for j in range(768):
        predict = getHistogram(ds +'/'+ str(j)+'.png')
        result = classify.predict(predict)

        if result == [1]:
            i = 0
        else:
            i = 1
        array.append(i)
    array = split(array,32).T
    #array = np.flipud(array)
    array = np.fliplr(array)

    print " "
    print "Prediction Time : " + str(datetime.datetime.now() - now)
    print " "
    print "##################################################"
    print "                     Area                        "
    print "##################################################"
    print " "
    print array

    #array[0,0] = 3
    return array
    
    

# A* Algorithm 
def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def path():
    
    array = train()
    start = (23,0)
    goal  = (0,31)
    
    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    closeSet = set()
    cameFrom = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in cameFrom:
                data.append(current)
                current = cameFrom[current]
            ## Draws path
            for i in range(0,len(data)):
                x = int(data[i:][0][0])
                y = int(data[i:][0][1])
                array[x,y] = 4
                #print x
                #print y
            print " "
            print "##################################################"
            print "                Area  with PATH                   "
            print "##################################################"
            print " "
            print array
	    print data
            return data

        closeSet.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in closeSet and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                cameFrom[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                path = heappush(oheap, (fscore[neighbor], neighbor))

    return False
    
# End of A* algorithm 
