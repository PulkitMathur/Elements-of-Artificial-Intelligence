#!/usr/bin/python3
import numpy as np
from sys import stdout



HIDDEN_NODES = 180


def loadDataset(path):
    f = open(path, 'r')
    names = []
    labels = []
    data = []
    max_value = -1000
    for line in f:
        classes = [0.0]*4
        splits = line.split()
        vector = [float(x) for x in splits[2:]]
        names.append(splits[0])
        if max_value < max(vector):
            max_value = max(vector)
        data.append(vector)
        classes[int(int(splits[1])/90)] = 1
        labels.append(classes)
    return np.array(data) / max_value, np.array(labels), np.array(names)


def activation(x,deriv=False):
    if(deriv == True):
        '''
        #ReLU trial
        x[x <= 0] = 0
        x[x > 0] = 1
        return x
        '''
        #tanh activation function
        return 1.0 - np.tanh(x)**2

    return np.tanh(x) #np.maximum(x, 0)

def trainNeuralNetwork(trainFile,numIterations):
    print("Training the Neural Network")
    data, labels, names = loadDataset(trainFile) #Returns 3 numpy arrays
    model = {} #Size = 4
    '''
    print("len(data): ",len(data)) #36976 = total images in train data
    print("len(data[0]): ",len(data[0])) #192 = #pixel values for 1 image
    print("data",data) #data is a numpy array ( 1 list of list) -> each pixel value is normalized -> order same as of train file

    print("len(labels): ",len(labels))
    print("labels",labels) # label is a numpy array (1 list of list) -> a list of list for each image and val = 1 for that corresponding angle

    print("len(names): ",len(names))
    print("names",names) # a numpy array of list -> names of all train images
    '''
    #seed
    np.random.seed(1)

    weights0 = 2 * np.random.random((len(data[0]), HIDDEN_NODES)) - 1 #a numpy array (list of list)
    weights1 = 2 * np.random.random((HIDDEN_NODES, len(labels[0]))) - 1 #a numpy array (list of list)
    bias0 = 2 * np.random.random((1, HIDDEN_NODES)) - 1 #a numpy array (list of list)
    bias1 = 2 * np.random.random((1, len(labels[0]))) - 1 #a numpy array (list of list)

    iterations = len(data) #Iterate for all images in training set
    batch_size = 1
    rate = 0.01 #Initial Learning Rate
    #rate_decay = 0.01
    lowest_error = 1000
    best_syn0 = best_syn2 = best_bias0 = best_bias2 = -1

    for j in range(numIterations):
        errors = [] #Error at each layer for each iteration
        for index in range(iterations):
            i = index
            X = np.array(data[i * batch_size: min((i + 1) * batch_size, len(data)), :])
            Y = np.array(labels[i * batch_size: min((i + 1) * batch_size, len(data)), :])

            #Layers and Forward Propagation
            layer0 = X
            layer1 = (np.dot(layer0, weights0) + bias0)
            layer2 = (np.dot(activation(layer1), weights1) + bias1)

            #Backpropagation
            layer2_error = (Y - activation(layer2)) * activation(layer2, deriv=True)
            bias1 += rate ** 1 * layer2_error
            errors.append(np.mean(np.abs(Y - activation(layer2))))

            layer1_error = layer2_error.dot(weights1.T) * activation(layer1, deriv=True)
            bias0 += rate ** 1 * layer1_error

            weights1 += (rate) * activation(layer1).T.dot(layer2_error) #L1 -> L2
            weights0 += (rate) * layer0.T.dot(layer1_error) # L0 -> L1

        if np.mean(errors) < lowest_error:
            lowest_error = np.mean(errors)
            best_syn0 = weights0
            best_syn2 = weights1
            best_bias0 = bias0
            best_bias2 = bias1

        # Varying Learning Rate after every 10th iteration

        if j % 10 == 0:
            rate *= 0.5
        '''
        if j % 10 == 0:
            rate = rate * (rate / (rate + (rate * rate_decay)))
            print("Rate: ",rate
        '''

        print("\r" + "Iteration: %d Mean Error: %.5f" % (j + 1, np.mean(errors)))
        #sys.stdout.write("\r" + "Iteration: %d Mean Error: %.5f" % (j + 1, np.mean(errors)))
        #sys.stdout.flush()

    model['weights0'] = best_syn0
    model['weights1'] = best_syn2
    model['bias0'] = best_bias0
    model['bias1'] = best_bias2
    print()
    return model

def testNN(model,testFile):
    syn0 = model['weights0']
    syn2 = model['weights1']
    bias0 = model['bias0']
    bias2 = model['bias1']

    data, labels, names = loadDataset(testFile)
    output_file = open('output.txt', 'w')
    confusion_matrix = [[0] * len(labels[0]) for i in range(len(labels[0]))]
    count = 0
    correct = 0

    for i in range(len(data)):
        l0 = data[i]
        l1 = activation(np.dot(l0, syn0) + bias0)
        l3 = activation(np.dot(l1, syn2) + bias2)
        probs = l3[0]

        predicted = max([(probs[x], x) for x in range(len(probs))], key=lambda x: x[0])[1]
        actual = max([(labels[i][x], x) for x in range(len(labels[i]))], key=lambda x: x[0])[1]

        if predicted == actual:
            correct += 1

        confusion_matrix[actual][predicted] += 1

        output_file.write(names[i] + " " + str(predicted * 90) + "\n")
        count += 1
        #sys.stdout.write("\r" + "%d of %d Images Predicted Correctly %.2f accuracy" % (correct, count, correct / count * 100))
        #sys.stdout.flush()

    output_file.close()
    print("Total Number of test Images: ",count)
    print("Number of Images Predicted Correctly: ",correct)
    print("Accuracy: ",((correct/count)*100),end= " %")

    '''
    print()
    print("\n", "Here is the confusion matrix")
    matrix = pandas.DataFrame(confusion_matrix, [x * 90 for x in range(len(labels[0]))],[x * 90 for x in range(len(labels[0]))])
    print(matrix)
    '''

def calcTrainingAccuracy(model,trainFile):
    syn0 = model['weights0']
    syn2 = model['weights1']
    bias0 = model['bias0']
    bias2 = model['bias1']

    data, labels, names = loadDataset(trainFile)
    #output_file = open('output.txt', 'w')
    confusion_matrix = [[0] * len(labels[0]) for i in range(len(labels[0]))]
    count = 0
    correct = 0

    for i in range(len(data)):
        l0 = data[i]
        l1 = activation(np.dot(l0, syn0) + bias0)
        l3 = activation(np.dot(l1, syn2) + bias2)
        probs = l3[0]

        predicted = max([(probs[x], x) for x in range(len(probs))], key=lambda x: x[0])[1]
        actual = max([(labels[i][x], x) for x in range(len(labels[i]))], key=lambda x: x[0])[1]

        if predicted == actual:
            correct += 1

        confusion_matrix[actual][predicted] += 1

        #output_file.write(names[i] + " " + str(predicted * 90) + "\n")
        count += 1
        # sys.stdout.write("\r" + "%d of %d Images Predicted Correctly %.2f accuracy" % (correct, count, correct / count * 100))
        # sys.stdout.flush()

    print("Total Number of Train Images: ", count)
    print("Number of Training Images Predicted Correctly: ", correct)
    print("Training Accuracy: ", end="")
    print(((correct / count) * 100))

