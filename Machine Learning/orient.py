#!/usr/bin/python3

#Adaboost uses different classifiers that we have trained on the training data and then executes adaboost algorithm on
# these classifiers to get weight of all the 
# classifiers and download it to models file. Then during testing these weights are uploaded and outputs from classifiers is weighted
# to get final output. The different classifeirs use classifiers such as comparing intensity of pixels on different corners and comparning 
# blue and green values of pixels on bottom and top of the picture etc.

'''
Network Architecture = 3 Layers(1 input layer of 192 neurons, 1 hidden layer of 180 neurons and 1 output layer of 4 neurons)
Iterations: 120

ANALYSIS:
            NUM_ITERATIONS     TRAINING ACCURACY    TEST ACCURACY(%)           MEAN TRAINING ERROR      NUM_HIDDEN_NODES
                60                75.603093            72.6405                     0.19186                    40
                120               75.554413            72.74655                    0.19128                    40
                200               75.5598225           72.74655                    0.19126                    40

                60                                     73.06468                     0.19254                   90
                80                                     72.64050                     0.19164                   90
                100                                    72.64059                     0.19143                   90
                120                                    72.74655                     0.19137                   90

                60                                     73.5949                      0.19416                   180
                120               76.528018            73.700954                    0.19187                   180**
                180                                    73.70095                     0.19183                   180
                360                                    73.70095                     0.19183                   180

                60                76.506382            70.83775                     0.19836                   200
                120                                                                 0.19587                   200
                180               76.587516            71.58006                     0.19582                   200

                60                                     71.8981                      0.19695                   270
                120                                    72.11028                     0.19370                   270
                180                                    72.004241                    0.19364                   270


                60                                     25.7688                      0.47324                   360
                120               26.5604              25.8748                      0.47413                   360




CONCLUSION:

1. For implementing the neural network I used the approach of going with an array based implementation. Both the weights of the
   network and biases can be efficiently stored and manipulated using numpy arrays. As far as other formulation goes, I have adhered to
   the standard algorithms for Stochastic gradient descent and  back-propagation

2. The main working of the program relies on the stochastic gradient descent technique. I use the whole dataset in a batch. 
   The neural network is trained on this batch 120 times.  Each item in the batch is
   forward propagated and then back propagated to find the error. The best set of weights are stored found during these iterations
   based on the average of the error accumulated in that iteration. The learning rate is initialized to 0.01 and gradually decays
   by a factor of 50% after every 10 iterations.  This helps to reduce the amount of adjustments done to weights and biases.
   The activation function used here is the tanh function.  We tried using the sigmoid activation function but dropped it due to a
   float value overflow.

3. A main design decision we made was using the tanh function instead of sigmoid activation. We also went with 4  output configuration for the
   neural network. Each output corresponds to one of the classes.  The node with the max output value during testing is considered the class label.  When training
   the neural network we also normalized the data  by dividing all the pixel values by 255 (the max value).  When training the network
   we also used biases for both the hidden layer and the output layer.

4. We tried several different configurations for the neural network viz. modifying the learning rate,  adding nodes to the hidden layer,
   using a single output node, normalizing or binning the data. We also tried a deeper network architecture with 2 hidden layers.
   The best performance we observed was for a neural network with a configuration of (192,180,4) representing the nodes in
   each layer. It came out to be 73.70%. We didn't try more iterations since we didn't want to overfit to the data.  We also normalized
   the data to 0-1 scale as inputs to the network.

Refernces:
[1] http://www.faqs.org/faqs/ai-faq/neural-nets/
[2] https://www.doc.ic.ac.uk/~nd/surprise_96/journal/vol4/cs11/report.html#Feed-forward networks
'''



'''
For K-Nearest Neighbours:
Distance Formula Used: Euclidean Distance

ANALYSIS: 
            K = 15 -> Accuracy = 70.09544%
            K = 25 -> Accuracy = 71.155%
            K = 35 -> Accuracy - 70.4135
            
BEST CLASSIFIER: Neural Network as it gave best accuracy on test set.

'''


import sys
import numpy as np
import random as rand

import math
def getDictadaboost(file):
    dic_train = {}
    with open(file) as f:
        for line in f:
            lineSplit = line.split(' ')
            key = lineSplit[0]+"|"+lineSplit[1]

            for i in range(2,len(lineSplit)):
                if(key in dic_train.keys()):
                    x = int(lineSplit[i])
                    dic_train[key].append(x)
                else:
                    dic_train[key]=[]
                    x = int(lineSplit[i])
                    dic_train[key].append(x)

    return dic_train

def testAdaBoost(test_file):

    outputs=[]
    z=[]
    file=open("model_file.txt",'r')
    input_string=file.readline()
    line=input_string.split("|")

    for i in range(0,len(line)-1):
        z.append(float(line[i]))

    test_dict=getDictadaboost(test_file)
    len_test_data = len(test_dict.keys())
    prediction=classifiers(test_dict)
    true_values = []
    for i in test_dict.keys():
        temp4 = i.split("|")
        true_values.append(temp4[1])

    for i in range(0,len_test_data):
        sum1=0
        for j in range(0,len(prediction)):
            if prediction[j][i]=="0":
                sum1+=1*z[j]
            elif prediction[j][i]=="90":
                sum1+=2*z[j]
            elif prediction[j][i]=="180":
                sum1+=3*z[j]
            elif prediction[j][i]=="270":
                sum1+=4*z[j]
        #print(sum1)



        if sum1<1.5:
            outputs.append("0")
        elif sum1>=1.5 and sum1<2.5:
            outputs.append("90")
        elif sum1>=2.5 and sum1<3.5:
            outputs.append("180")
        elif sum1>=3.5:
            outputs.append("270")
    count3=0
    keys_test_dict=[]
    for i in test_dict.keys():
        keys_test_dict.append(i)
    file=open("output.txt",'w')


    for i in range(0,len(keys_test_dict)):
        x=""
        temp5=keys_test_dict[i].split("|")
        x+=temp5[0]
        x+=" "+outputs[i]
        x+="\n"
        file.write(x)




    for i in range(0,len_test_data):
        if true_values[i]==outputs[i]:
            count3+=1
    print("Accuracy for Adaboost is ",100*(count3/len_test_data))

def getModel(modelFile):
    model = {}
    with open(modelFile, 'r') as f:
        for line in f:
            lineSplit = line.split(' ')
            key = lineSplit[0]
            num = lineSplit[1:len(lineSplit)-1]
            x = []
            y = []

            for i in num:
                y.append(float(i))

            x.append(y) #now x is a list of list

            e = np.array(x) #e is an np array

            if(key in model.keys()):
                model[key] = np.append(model[key],e,axis=0)
            else:
                model[key] = e
    return model


def getCorrectValues(myFile):
    correctAngle = {}
    with open(myFile) as f:
        for line in f:
            lineSplit = line.split(' ')
            #print(lineSplit)
            key = lineSplit[0]
            if (key in correctAngle.keys()):
                x = lineSplit[1]
                correctAngle[key] =x
            else:
                x = lineSplit[1]
                correctAngle[key] =x
    return correctAngle




def test(testFile,modelFile,classifier):
    if(classifier == 'nearest'):
        print("Testing k-Nearest Neighbour Classifier")
        correctAngle = getCorrectValues(testFile) #Returns a dictionary of test image_names -> correct_angles
        import nearest as near
        K = 25
        predictedAngle = near.testNearest(testFile,modelFile,K,correctAngle)
        print("Accuracy for k-Nearest Neighbour is: ", end=" ")
        print(near.getAccuracy(predictedAngle, correctAngle), end="%")
        print()
    elif(classifier == 'adaboost'):
        testAdaBoost(testFile)
    elif(classifier == 'nnet'):
        print("Testing Neural Network Classifier")
        import neuralnet as nn
        model = getModel(modelFile)
        nn.testNN(model,testFile)
    elif(classifier == 'best'):
        import best as b
        model = getModel(modelFile)
        b.testBest(model,testFile)

def classifiers(dic_train):
    def classifier1(dic_train):

        # print("training for Ada Boost classifier")

        count = 0
        count1 = 0
        predict = []
        for i in dic_train.keys():

            sum0 = 0
            sum2 = 0
            sum3 = 0
            sum4 = 0
            ans = ""

            z = i.split("|")
            angle = z[1]

            count += 1
            for j in range(1, 72, 3):
                sum0 += dic_train[i][j]
            for j in range(2, 72, 3):
                sum0 += dic_train[i][j]

            for j in range(121, 192, 3):
                sum2 += dic_train[i][j]
            for j in range(122, 192, 3):
                sum2 += dic_train[i][j]
            for j in range(0, 175, 24):
                sum3 += dic_train[i][j + 1]
                sum3 += dic_train[i][j + 2]
                sum3 += dic_train[i][j + 4]
                sum3 += dic_train[i][j + 5]
                sum3 += dic_train[i][j + 7]
                sum3 += dic_train[i][j + 8]
            for j in range(15, 192, 24):
                sum4 += dic_train[i][j + 1]
                sum4 += dic_train[i][j + 2]
                sum4 += dic_train[i][j + 4]
                sum4 += dic_train[i][j + 5]
                sum4 += dic_train[i][j + 7]
                sum4 += dic_train[i][j + 8]

            if sum0 > 4500:
                ans = "0"
            elif sum2 > 4500:
                ans = "180"
            elif sum3 > 4500 and sum4 < 4000:
                ans = "270"
            elif sum4 > 4500 and sum3 < 4000:
                ans = "90"
            else:
                ans = "0"
            predict.append(ans)

            if ans == angle:
                count1 += 1

            if ans == angle:
                count1 += 1

        # print("Accuracy for classifier 1 is ,",100*(count1/count))

        # print("Accuracy for classifier 1 is ,", 100 * (count1 / count))

        return predict

    # Accuracy for classifier 2 is , 41.05906533967979
    def classifier2(dic_train):

        count = 0
        sum0 = 0
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        sum6 = 0
        sum7 = 0
        count1 = 0
        predict = []
        for i in dic_train.keys():
            ans = ""
            count += 1

            z = i.split("|")
            angle = z[1]
            temp = ((dic_train[i][12] ** 2) + (dic_train[i][13] ** 2) + (dic_train[i][14] ** 2)) - (
                (dic_train[i][180] ** 2) + (dic_train[i][181] ** 2) + (dic_train[i][182] ** 2))
            temp2 = ((dic_train[i][93] ** 2) + (dic_train[i][94] ** 2) + (dic_train[i][95] ** 2)) - (
                (dic_train[i][72] ** 2) + (dic_train[i][73] ** 2) + (dic_train[i][74] ** 2))

            if temp > 3000 and temp2 < 3000:
                ans = "0"
            elif temp > -1000 and temp2 > 3000:
                ans = "90"
            elif temp < -3000 and temp2 > -1000:
                ans = "180"
            elif temp < 3000 and temp2 < -3000:
                ans = "270"
            else:
                ans = "0"
            predict.append(ans)
            if ans == angle:
                count1 += 1
        return predict
        # print("Accuracy for classifier 2 is ,", 100 * count1 / count)

    # Accuracy for classifier 3 is , 62.821830376460404

    def classifier3(dic_train):

        count = 0
        sum0 = 0
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        sum6 = 0
        sum7 = 0
        count1 = 0
        predict = []
        for i in dic_train.keys():
            ans = ""
            count += 1

            z = i.split("|")
            angle = z[1]
            temp = ((dic_train[i][0] ** 2) + (dic_train[i][1] ** 2) + (dic_train[i][2] ** 2)) - (
                (dic_train[i][189] ** 2) + (dic_train[i][190] ** 2) + (dic_train[i][191] ** 2))
            temp1 = ((dic_train[i][168] ** 2) + (dic_train[i][169] ** 2) + (dic_train[i][170] ** 2)) - (
                (dic_train[i][21] ** 2) + (dic_train[i][22] ** 2) + (dic_train[i][23] ** 2))

            if temp > 0 and temp1 < 0:
                ans = "0"
            elif temp < 0 and temp1 < 0:
                ans = "90"
            elif temp < 0 and temp1 > 0:
                ans = "180"
            elif temp > 0 and temp1 > 0:
                ans = "270"
            else:
                ans = "0"
            predict.append(ans)

            if ans == angle:
                count1 += 1
                # print("Accuracy for classifier 3 is ,",100*count1/count)

            if ans == angle:
                count1 += 1
        # print("Accuracy for classifier 3 is ,", 100 * count1 / count)

        return predict

    # Accuracy for classifier 4 is , 44.020445694504545
    def classifier4(dic_train):

        predict = []

        count = 0
        sum0 = 0
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        sum5 = 0
        sum6 = 0
        sum7 = 0
        sum8 = 0
        sum9 = 0
        sum10 = 0
        sum11 = 0
        sum12 = 0
        sum13 = 0
        sum14 = 0
        sum15 = 0
        count1 = 0
        for i in dic_train.keys():
            temp = 0
            temp2 = 0
            temp3 = 0
            temp4 = 0
            ans = ""
            count += 1

            z = i.split("|")
            angle = z[1]
            for j in range(0, 94, 3):
                temp += dic_train[i][j] ** 2
                temp += dic_train[i][j + 1] ** 2
                temp += dic_train[i][j + 2] ** 2

            for j in range(96, 192, 3):
                temp2 += dic_train[i][j] ** 2
                temp2 += dic_train[i][j + 1] ** 2
                temp2 += dic_train[i][j + 2] ** 2

            for j in range(0, 8):
                for k in range(0, 14):
                    temp3 += dic_train[i][24 * j + k] ** 2

            for j in range(0, 8):
                for k in range(14, 24):
                    temp4 += dic_train[i][24 * j + k] ** 2

            if temp - temp2 > 1000:
                ans = "0"
            elif temp4 - temp3 > 0:
                ans = "90"
            elif temp2 - temp > 1000:
                ans = "180"
            elif temp3 - temp4 > 0:
                ans = "270"
            else:
                ans = "0"
            predict.append(ans)
            if ans == angle:
                count1 += 1
        # print("Accuracy for classifier 4 is ,", 100 * count1 / count)
        return predict

    def classifier5(dic_train):
        # print(dic_train)
        sums = [[0 for j in range(64)] for i in range(4)]
        # print(len(sums[3]))
        for key in dic_train:
            sumRGB = [dic_train[key][i] + dic_train[key][64 + i] + dic_train[key][128 + i] for i in range(0, 64)]
            key = key.split('|')
            val = int(int(key[1]) / 90)
            # print("val " + str(val))
            sums[val] = [sums[val][i] + sumRGB[i] for i in range(64)]
        avgs = [[sums[i][j] / 10000 for j in range(64)] for i in range(4)]
        diff = [[0 for j in range(64)] for i in range(4)]
        diff[0] = [avgs[0][i] for i in range(64)]
        diff[1] = [avgs[1][i] - avgs[0][i] for i in range(64)]
        diff[2] = [avgs[2][i] - avgs[0][i] for i in range(64)]
        diff[3] = [avgs[3][i] - avgs[0][i] for i in range(64)]

        predict = []
        accu_cnt = 0
        for newkey in dic_train:
            part_res = [[0 for j in range(64)] for i in range(4)]
            newsumRGB = [dic_train[newkey][i] + dic_train[newkey][64 + i] + dic_train[newkey][128 + i] for i in
                         range(0, 64)]
            for i in range(4):
                for j in range(64):
                    if i == 0:
                        if diff[i][j] - 20 <= newsumRGB[j] <= diff[i][j] + 20:
                            part_res[i][j] = 1
                    else:
                        if diff[i][j] - 20 <= newsumRGB[j] - diff[0][j] <= diff[i][j] + 20:
                            part_res[i][j] = 1
            cnt = [part_res[i].count(1) for i in range(4)]
            angle = cnt.index(max(cnt))
            accu_cnt += 1 if newkey.split('|')[1] == str(angle * 90) else 0
            predict.append(str(angle * 90))

        # print("Accuracy for classifier 5 is ,", 100 * accu_cnt / len(dic_train))
        return predict

    def classifier7(dic_train):
        predict = []

        count = 0
        sum0 = 0
        sum1 = 0

        count1 = 0

        for i in dic_train.keys():
            blueup = 0
            bluedown = 0
            blueleft = 0
            blueright = 0
            for j in range(3, 24, 3):
                blueup += dic_train[i][j]
            for j in range(170, 192, 3):
                bluedown += dic_train[i][j]
            for j in range(3, 171, 24):
                blueleft += 1
            for j in range(21, 192, 24):
                blueright += 1
            if blueup > bluedown and blueup > blueleft and blueup > blueright:
                ans = "0"
            elif bluedown > blueup and bluedown > blueleft and bluedown > blueright:
                ans = "180"
            elif blueright > bluedown and blueright > blueleft and blueright > blueup:
                ans = "90"
            else:
                ans = "270"

            predict.append(ans)
        return predict

    prediction = []
    prediction.append(classifier3(dic_train))
    prediction.append(classifier4(dic_train))
    # prediction.append(classifier2(dic_train))
    prediction.append(classifier1(dic_train))
    prediction.append(classifier5(dic_train))
    prediction.append(classifier7(dic_train))
    return prediction


def trainAdaBoost(trainFile):

    print("Training for Ada Boost classifier")
    dic_train = getDictadaboost(trainFile)
    prediction=classifiers(dic_train)
    len_train_data=len(dic_train.keys())
    weights1=[]
    for i in range(0,len_train_data):
        weights1.append(1/len_train_data)

    true_values=[]
    for i in dic_train.keys():
        temp4=i.split("|")
        true_values.append(temp4[1])

    z=[]
    for i in range(0,len(prediction)):
        z.append(0)

    count9=[]
    for k in range(0,len(prediction)):
        error=0
        sum=0
        sum_weights=0
        count8=0
        for i in range(0,len_train_data):
            sum_weights+=weights1[i]
            if prediction[k][i]!=true_values[i]:
                error+=weights1[i]
            elif prediction[k][i]==true_values[i]:
                count8+=1
        error=error/sum_weights
        count9.append(count8)


        z[k] = math.log((1 - error) / error, 10) + math.log10(3)
        for i in range(0,len_train_data):
            if prediction[k][i]!=true_values[i]:
                weights1[i]=weights1[i]*(10**z[k])

        for i in range(0,len(weights1)):
            sum+=weights1[i]
        for i in range(0,len(weights1)):
            weights1[i]=weights1[i]/sum


    sumz=0
    for i in range(0,len(z)):
        z[i]=z[i]*count9[i]
    for i in range(0,len(z)):
        sumz+=z[i]


    for i in range(0,len(z)):
        z[i]=z[i]/sumz

    file=open("model_file.txt",'w')
    for i in range(0,len(z)):
        file.write(str(z[i]))
        file.write("|")




def writeModelToFile(modelFile,model):
    f = open(modelFile, 'w')
    for key in model.keys():
        #print("Key: ",key)
        val = model[key] # val is a list of list
        #print("len(val): ", len(val))
        #print(val)
        for list in val:
            f.write(key)
            f.write(" ")
            for e in list:
                f.write(str(e))
                f.write(" ")
            f.write("\n")



def train(trainFile,classifier,modelFile):
    if(classifier == 'nearest'):
        import nearest as near
        near.trainNearest(trainFile,modelFile)
    elif(classifier == 'adaboost'):
        trainAdaBoost(trainFile)
    elif(classifier == 'nnet'):
        import neuralnet as nn
        numIterations = 120
        model = nn.trainNeuralNetwork(trainFile,numIterations)
        writeModelToFile(modelFile,model)
        print("Training Completed")
        nn.calcTrainingAccuracy(model,trainFile)
    elif(classifier == 'best'):
        import best as b
        model = b.trainBest(trainFile)
        writeModelToFile(modelFile, model)
        print("Training Completed")





#Main Function
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Too few arguments")
        print("The program expects arguments in a different fashion")
        sys.exit()
    else:
        doWhat = sys.argv[1]
        myFile = sys.argv[2]
        modelFile = sys.argv[3]
        classifier = sys.argv[4]
        if(doWhat == 'train'):
            train(myFile,classifier,modelFile)
        elif(doWhat == 'test'):
            test(myFile,modelFile,classifier)
    sys.exit()
