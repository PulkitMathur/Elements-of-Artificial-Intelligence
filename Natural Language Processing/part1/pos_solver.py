#!/usr/bin/python3
###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids:
# Pulkit Mathur(pulmath), Angad Dhillon (adhillon) and Jatin (jdbhutka)
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
'''
Contrbuters: Pulkit Mathur(pulmath), Angad Dhillon (adhillon) and Jatin (jdbhutka)
The output is as follows for bc.test:
    ==> So far scored 2000 sentences with 29442 words.
                          Words correct:     Sentences correct:
        0. Ground truth:      100.00%              100.00%
        1. Simplified:        93.95%               47.50%
        2. HMM VE:            93.71%               47.20%
        3. HMM MAP:           92.28%               40.90%

I. Simplified Algorithm:
    1. This model does not incorporate much evidence and each observed variable depends only on the current state.
    2. There is no dependency between the hidden states. To calculate the best tag sequence, at each time we calculate the emission probabilities for
       the word with all the possible tags. We pick the maximum emission probability and the tag corresponding to it is stored as the tag for that word.

II. Variable Elimination Algorithm:
    1. This algorithm involves calculating emission probability using initial probability and transition probability.
    2. The transition probability is calculated from the input text file. It is stored as a python dictionary (dic_transition).
        The format of transition probability is P("tag.tag") = value. For example P("adj.adp") = 0.14023
    3. The initial probability is also calculated from file and is stored in dic_word. The format of initial probabi;ity is P(word.tag) = value.
        For example P("apple.noun")=0.0025
III. Viterbi Algorithm:
    1. THe first step is to create a matrix with 12 rows (= number of tags) and columns equal to number of words in the input sentence.
    2. Initialize all values to 0 initially
    3. The first column represents the initial probability. The values are stored in dic_word python dictionary.
    4. Iterating through the rest of the matrix, taking one columns and filling row wise.
    5. The next value is the product of previous corresponding value, corresponding transition probability (stored in dic_transition)
       and the probability of the that word being a tag. All these values are the emission probabilities.
    6. The next step is to find the max value in each column of the matrix and corresponding indexes.
    7. All these indexes are used to map to corresponding tags.
    8. Finally we return the list of tags.
'''
####

import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#

import random
import math
dic_word_prob={}
dic_word = {}
dic_pos={}
dic_transition={}
dic_pos_to_word={}

class Solver:

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    #
    def train(self, data):
        t = ["noun", "num", "adj", "verb", "x", ".", "prt", "pron", "conj", "adv", "adp", "det"]
        num_words = 0

        for i in range(0, len(data)):

            num_words += len(data[i][0])
            for j in range(0, len(data[i][0])):

                iterator = ""
                iterator = iterator + data[i][0][j]
                iterator = iterator + "."
                iterator = iterator + data[i][1][j]

                if iterator not in dic_word.keys():
                    dic_word[iterator] = 1
                else:
                    dic_word[iterator] += 1

                if data[i][1][j] not in dic_pos.keys():
                    dic_pos[data[i][1][j]] = 1
                elif data[i][1][j] in dic_pos.keys():
                    dic_pos[data[i][1][j]] += 1

                if data[i][0][j] not in dic_word_prob.keys():
                    dic_word_prob[data[i][0][j]] = 1
                elif data[i][0][j] in dic_word_prob.keys():
                    dic_word_prob[data[i][0][j]] += 1




                    # dic_pos_to_word[iterator2]=(dic_word[iterator]*dic_word_prob[data[i][0][j]])/dic_pos[data[i][1][j]]
        for i in range(0, len(data)):
            for j in range(0, len(data[i][0])):
                iterator2 = ""
                iterator2 = iterator2 + data[i][1][j]
                iterator2 = iterator2 + "."
                iterator2 = iterator2 + data[i][0][j]

                iterator4 = ""
                iterator4 = iterator4 + data[i][0][j] + "." + data[i][1][j]
                if iterator2 not in dic_pos_to_word.keys():
                    dic_pos_to_word[iterator2] = dic_word[iterator4] / dic_pos[data[i][1][j]]

        for i in range(0, len(data)):
            for j in range(0, len(data[i][0]) - 1):
                iterator1 = ""
                iterator1 = iterator1 + data[i][1][j]
                iterator1 = iterator1 + "."
                iterator1 = iterator1 + data[i][1][j + 1]

                if iterator1 not in dic_transition.keys():
                    dic_transition[iterator1] = 1
                elif iterator1 in dic_transition.keys():
                    dic_transition[iterator1] += 1

        for i in range(0, 12):
            for j in range(0, 12):
                iterator3 = ""
                iterator3 = t[i] + "." + t[j]
                if iterator3 in dic_transition.keys():
                    dic_transition[iterator3] = dic_transition[iterator3] / dic_pos[t[i]]
                else:
                    dic_transition[iterator3] = 10 ** -7

        for i in dic_word.keys():
            dic_word[i] = dic_word[i] / num_words

        for i in dic_pos.keys():
            dic_pos[i] = dic_pos[i] / num_words

        for i in dic_word_prob.keys():
            dic_word_prob[i] = dic_word_prob[i] / num_words
    # Functions for each algorithm.
    #
    def simplified(self, sentence):
        t = ["noun", "num", "adj", "verb", "x", ".", "prt", "pron", "conj", "adv", "adp", "det"]
        return_list = ["noun"] * len(sentence)
        for i in range(0, len(sentence)):
            temp = 0
            temp1 = ""
            for j in range(0, 12):
                iterator = ""
                iterator = iterator + sentence[i] + "." + t[j]
                if iterator in dic_word.keys():
                    if dic_word[sentence[i] + "." + t[j]] > temp:
                        temp = dic_word[sentence[i] + "." + t[j]]
                        temp1 = t[j]
            if temp1 is "":
                return_list[i] = "noun"
            elif temp1 is not "":
                return_list[i] = temp1

        return return_list

    def hmm_ve(self, sentence):
        return_list2 = ["noun"] * len(sentence)
        taos = []
        for i in range(0, len(sentence)):
            taos.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        t = ["noun", "num", "adj", "verb", "x", ".", "prt", "pron", "conj", "adv", "adp", "det"]

        for i in range(0, 12):
            temp = 0
            iterator7 = ""
            iterator7 = iterator7 + t[i] + "." + sentence[0]
            for j in range(0, 12):
                iterator8 = ""
                iterator8 = iterator8 + t[j] + "." + t[i]
                temp += dic_pos[t[j]] * dic_transition[iterator8]
            if iterator7 in dic_pos_to_word.keys():
                taos[0][i] = temp * dic_pos_to_word[iterator7]
            else:
                taos[0][i] = temp * (10 ** -8)
        for i in range(1, len(sentence)):

            for j in range(0, 12):
                temp = 0
                for k in range(0, 12):
                    iterator5 = ""
                    iterator6 = ""
                    iterator5 = iterator5 + t[k] + "." + t[j]
                    iterator6 = iterator6 + t[j] + "." + sentence[i]
                    temp += dic_transition[iterator5] * taos[i - 1][k]

                if iterator6 in dic_pos_to_word.keys():
                    taos[i][j] = temp * dic_pos_to_word[iterator6]
                else:
                    taos[i][j] = temp * (10 ** -8)

        for i in range(0, len(taos)):
            temp22 = -1
            temp23 = 0
            for j in range(0, 12):
                if taos[i][j] > temp22:
                    temp22 = taos[i][j]
                    temp23 = j
            return_list2[i] = t[temp23]

        return return_list2

    def hmm_viterbi(self, sentence):
        ans = [[0 for i in range(len(sentence))] for j in range(12)]
        tags = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        firstWord = sentence[0]
        defaultProbability = 1/1000000000

        for i in range(12):
            temp = ''
            temp = firstWord + '.' + tags[i]
            if (temp in dic_word.keys()):
                ans[i][0] = dic_word[temp]
            else:
                ans[i][0] = 1 / 1000000000

        for col in range(1,len(ans[0])):
            for row in range(12):
                myWord = ''
                myWord = sentence[col] + '.' + tags[row]
                if (myWord in dic_word.keys()):
                    y = dic_word[myWord]
                else:
                    y = defaultProbability
                '''
                poss = []
                r = 0
                for k in range(-1*row,11-row):
                    poss.append(dic_transition[tags[r] + '.' + tags[row]]*y*ans[row+k][col-1])
                poss.sort()
                ans[row][col] = poss[len(poss) - 1]
                '''
                if row == 0:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r]+'.adj'] * y * ans[row+k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss)-1]
                elif row == 1:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r]+'.adv'] * y * ans[row+k][col - 1])
                        r = r+1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 2:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.adp'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 3:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.conj'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 4:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.det'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 5:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.noun'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 6:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.num'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 7:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.pron'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 8:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.prt'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 9:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.verb'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 10:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '.x'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]
                elif row == 11:
                    poss = []
                    r = 0
                    for k in range(-row,12-row):
                        poss.append(dic_transition[tags[r] + '..'] * y * ans[row + k][col - 1])
                        r = r + 1
                    poss.sort()
                    ans[row][col] = poss[len(poss) - 1]


        colMax = []
        colMaxIndexes = []
        for i in range(len(sentence)):
            max = -1
            maxIndex = -1
            for j in range(12):
                if(ans[j][i] >= max):
                    max = ans[j][i]
                    maxIndex = j
            colMax.append(max)
            colMaxIndexes.append(maxIndex)

        finalAns = []
        for i in colMaxIndexes:
            finalAns.append(tags[i])

        return finalAns

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence)
        else:
            print ("Unknown algo!")

