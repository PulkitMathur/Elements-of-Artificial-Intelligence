#HIDDEN_NODES_1 = 98
#HIDDEN_NODES_2 = 51

'''
def loadDataset(path):
    f = open(path, 'r')
    names = []
    labels = []
    data = []
    max_value = -1000
    for line in f:
        classes = [0.0]*4
        splits = line.split()
        #print("splits",splits)
        vector = [float(x) for x in splits[2:]]
        #print("vector",vector)
        names.append(splits[0])
        if max_value < max(vector):
            max_value = max(vector)
        data.append(vector)
        #print("int(splits[1])",int(splits[1]))
        classes[int(int(splits[1])/90)] = 1
        labels.append(classes)
    return np.array(data) / max_value, np.array(labels), np.array(names)



def activation(x,deriv=False):
    if(deriv==True):
        return 1.0 - np.tanh(x)**2

    return np.tanh(x)
'''

'''
data, labels, names = loadDataset(trainFile)  # Returns 3 numpy arrays
model = {}
# seed
np.random.seed(1)

syn0 = 2 * np.random.random((len(data[0]), HIDDEN_NODES_1)) - 1  # a numpy array (list of list) #input->hidden1
syn1 = 2 * np.random.random((HIDDEN_NODES_1, HIDDEN_NODES_2)) - 1  # a numpy array (list of list)
syn2 = 2 * np.random.random((HIDDEN_NODES_2, len(labels[0]))) - 1

bias0 = 2 * np.random.random((1, HIDDEN_NODES_1)) - 1  # a numpy array (list of list)
bias1 = 2 * np.random.random((1, HIDDEN_NODES_2)) - 1
bias2 = 2 * np.random.random((1, len(labels[0]))) - 1  # a numpy array (list of list)

iterations = len(data)  # Iterate for all images in training set
batch_size = 1
rate = 0.01  # Initial Learning Rate
lowest_error = 1000
best_syn0 = best_syn2 = best_bias0 = best_bias2 = best_syn1 = best_bias1 = -1
numIterations = 60
for j in range(numIterations):
    errors = []  # Error at each layer for each iteration
    for index in range(iterations):
        i = index
        X = np.array(data[i * batch_size: min((i + 1) * batch_size, len(data)), :])

        Y = np.array(labels[i * batch_size: min((i + 1) * batch_size, len(data)), :])

        # Layers
        layer0 = X
        layer1 = (np.dot(layer0, syn0) + bias0)
        layer2 = (np.dot(activation(layer1), syn1) + bias1)
        layer3 = (np.dot(activation(layer2), syn2) + bias2)

        # Backpropagation
        layer3_error = (Y - activation(layer3)) * activation(layer3, deriv=True)
        bias2 += rate ** 1 * layer3_error
        errors.append(np.mean(np.abs(Y - activation(layer3))))

        layer2_error = (Y - activation(layer2)) * activation(layer2, deriv=True)
        bias1 += rate ** 1 * layer2_error
        errors.append(np.mean(np.abs(Y - activation(layer2))))

        layer1_error = layer2_error.dot(syn2.T) * activation(layer1, deriv=True)
        bias0 += rate ** 1 * layer1_error

        syn2 += (rate) * activation(layer2).T.dot(layer3_error)
        syn1 += (rate) * activation(layer1).T.dot(layer2_error)
        syn0 += (rate) * layer0.T.dot(layer1_error)

    if np.mean(errors) < lowest_error:
        lowest_error = np.mean(errors)
        best_syn0 = syn0
        best_syn1 = syn1
        best_syn2 = syn2
        best_bias0 = bias0
        best_bias1 = bias1
        best_bias2 = bias2

    if j % 10 == 0:
        rate *= 0.5

    print("\r" + "Iteration: %d Mean Error: %.5f" % (j + 1, np.mean(errors)))

model['syn0'] = best_syn0
model['syn1'] = best_syn1
model['syn2'] = best_syn2
model['bias0'] = best_bias0
model['bias1'] = best_bias1
model['bias2'] = best_bias2
print()
return model
'''

def trainBest(trainFile):
    print("Training Best Classifier")
    import neuralnet as nn
    numIterations = 180
    return nn.trainNeuralNetwork(trainFile, numIterations)


def testBest(model,testFile):
    print("Testing Best Classifier")
    import neuralnet as nn
    nn.testNN(model, testFile)
