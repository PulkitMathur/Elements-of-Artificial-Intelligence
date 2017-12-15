#!/usr/bin/python3
import math


def getAccuracy(predictedAngles,correctAngles):
    count = 0
    total = len(correctAngles)
    for k in correctAngles.keys():
        if(int(correctAngles[k]) == predictedAngles[k]):
            count = count + 1

    return (count/total)*100


def getDict(file):
    dic_train = {}
    with open(file) as f:
        for line in f:
            lineSplit = line.split(' ')
            key = lineSplit[0]
            if(key in dic_train.keys()):
                x = lineSplit[2:]
                dic_train[key].append(x)
            else:
                dic_train[key] = []
                x = lineSplit[2:]
                dic_train[key].append(x)
    return dic_train

def trainNearest(trainFile,modelFile):
    print("Training k-Nearest Classifier")
    with open(modelFile, 'w') as file_1, open(trainFile, 'r') as file_2:
        for line in file_2:
            file_1.write(line)
    print("Training Complete")



def getNearestNeighbour(trainDic,testList):
    ans = []
    #print("testList",testList)
    for key in trainDic.keys():
        list1 = trainDic[key]
        list1 = list(map(int, list1))
        list2 = testList
        list2 = list(map(int, list2))
        s = 0
        for i in range(len(list1)):
            s = s + (list1[i]-list2[i])*(list1[i]-list2[i])
        s = math.sqrt(s)
        ans.append(s)
    return ans




def testNearest(testFile,modelFile, K, correctAngle):
    dic_train = getDict(modelFile)
    dic_test = getDict(testFile)

    dic0 = {}
    dic90 = {}
    dic180 = {}
    dic270 = {}

    for key in dic_train.keys():
        lol = dic_train[key]
        dic0[key] = lol[0]
        dic90[key] = lol[1]
        dic180[key] = lol[2]
        dic270[key] = lol[3]

    #testSize = len(dic_test)
    predictedAngle = {}
    #count = 0
    #correct = 0
    f = open('output.txt', 'w')
    for key in dic_test.keys():
        x0 = []
        x90 = []
        x180 = []
        x270 = []
        print("Predicted Angle for ", end="")
        print(key, end=" : ")
        f.write(key)
        f.write(" ")
        x0 = getNearestNeighbour(dic0, dic_test[key][0])
        x90 = getNearestNeighbour(dic90, dic_test[key][0])
        x180 = getNearestNeighbour(dic180, dic_test[key][0])
        x270 = getNearestNeighbour(dic270, dic_test[key][0])
        y = []
        for i in x0:
            y.append(i)
        for i in x90:
            y.append(i)
        for i in x180:
            y.append(i)
        for i in x270:
            y.append(i)
        y.sort()
        zero = 0
        ninety = 0
        oneEighty = 0
        twoSeventy = 0
        for i in range(K):
            if (y[i] in x0):
                zero = zero + 1
            elif (y[i] in x90):
                ninety = ninety + 1
            elif (y[i] in x180):
                oneEighty = oneEighty + 1
            elif (y[i] in x270):
                twoSeventy = twoSeventy + 1
        z = []
        z.append(zero)
        z.append(ninety)
        z.append(oneEighty)
        z.append(twoSeventy)
        m = max(z)
        maxIndex = -1
        for i in range(len(z)):
            if (z[i] == m):
                maxIndex = i
                break
        if (maxIndex == 0):
            predictedAngle[key] = 0
        elif (maxIndex == 1):
            predictedAngle[key] = 90
        elif (maxIndex == 2):
            predictedAngle[key] = 180
        elif (maxIndex == 3):
            predictedAngle[key] = 270
        print(predictedAngle[key])
        f.write(str(predictedAngle[key]))
        f.write("\n")
    return predictedAngle
