#!/usr/bin/python3
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2017)
#
'''
Contributers: Pulkit Mathur(pulmath), Angad Dhillon (adhillon) and Jatin (jdbhutka)
I. Simplified Algorithm
    1. Weighted sum is taken by comparing two letters pixel by pixel.
    2. If there is a match, higher weights are given and vice versa.
    3. At end average of weighted sum is taken and the corresponding letter is predicted by most matching pixels.
II. Variable Elimination Algorithm
    1. First transition probabilities are calculated using text file and stored in dic_trans
    2. Next step is to calculate "Tau" for all character.
    3. Variables are eliminated by checking sum of all characters.
III. Viterbi Algorithm
    1. The transition probabilities are calculated first.
    2. A matrix of rows equal to 72(= number of letters) and column equal to no of letters in test data is created.
    3. The first column of the matrix is filled with initial probabilities calculated by matching pixel to pixel.
    4. The next emission probabilities are calculated using transition probabilities and previous corresponding value.
    5. The last step is to do backtracking and find the corresponding letter where we get the maximum value.
    6. Return the string
'''

from PIL import Image, ImageDraw, ImageFont
import sys
import math


CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

dic_trans={}
dic_letters={}
dic_letters_initial={}
dic_trans2={}
dic_trans3={}
dic_trans4={}


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print (im.size)
    #print (int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]

train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

def file_input():
    s=""
    with open("test-strings.txt") as text_file:
        lines = [line.strip() for line in text_file]
    #print(lines)
    return lines



def simplified(test_letters,train_letters):
    s=""
    key_list=[]
    for key in train_letters.keys():
        key_list.append(key)


    ans=[""]*len(test_letters)
    for i in range(0,len(test_letters)):
        count_list=[]
        temp=0
        temp1=0
        for l in train_letters.keys():
             count=0
             count1=0
             count2=0
             for j in range(0,25):
                for k in range(0,14):
                    if train_letters[l][j][k]==test_letters[i][j][k]=="*":
                        count+=1
                    elif train_letters[l][j][k]==test_letters[i][j][k]==" ":
                        count2+=1
                    else:
                        count1+=1
             count_list.append((0.9*count+0.05*count1+0.4*count2)/350)

        for p in range(0,len(count_list)):
            if count_list[p]>temp:
                temp=count_list[p]
                temp1=p
        s=s+key_list[temp1]


    return s

print("Simple:",simplified(test_letters,train_letters) )


def prob_calculator(state,obs_ch_pix):
    prob=1
    prob1=0
    prob2=0
    num=0
    for i in range(0,25):
        for j in range(0,14):

            if obs_ch_pix[i][j]==train_letters[state][i][j]=="*":
                prob=prob+1
            elif obs_ch_pix[i][j]==train_letters[state][i][j]==" ":
                prob2=prob2+1
            elif obs_ch_pix[i][j]!=train_letters[state][i][j]:
                prob1=prob1+1
    num = (0.3 * prob2 + 0.6 * prob + 0.1 * prob1) / 350

    return num

def transition_prob():
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    lines=file_input()
    num=0
    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])):
            num+=1

            if lines[i][j] in dic_letters.keys():
                dic_letters[lines[i][j]]+=1
            else:
                dic_letters[lines[i][j]]=1

    for i in range(0,len(lines)):
        if lines[i]!="":
            if lines[i][0] in dic_letters_initial.keys():
                dic_letters_initial[lines[i][0]]+=1
            else :
                dic_letters_initial[lines[i][0]] = 1

    for i in dic_letters_initial.keys():
        dic_letters_initial[i]=dic_letters_initial[i]/len(lines)

    for i in range(0,len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[i] not in dic_letters_initial.keys():
            dic_letters_initial[TRAIN_LETTERS[i]]=10**-9

    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])-1):

            iterator=""
            iterator=iterator+lines[i][j]+"."+lines[i][j+1]
            if iterator in dic_trans.keys():
                dic_trans[iterator]+=1
            else:
                dic_trans[iterator]=1



    for i in range(0,len(TRAIN_LETTERS)):
        for j in range(0,len(TRAIN_LETTERS)):
            iterator3=""
            iterator3=iterator3+TRAIN_LETTERS[j]+"."+TRAIN_LETTERS[i]
            if iterator3 in dic_trans.keys() and TRAIN_LETTERS[j] in dic_letters.keys():
                dic_trans[iterator3]=dic_trans[iterator3]/dic_letters[TRAIN_LETTERS[j]]
            elif iterator3 not in dic_trans.keys():
                dic_trans[iterator3]=10**-12


    for i in dic_letters.keys():
        dic_letters[i]=dic_letters[i]/num


    for i in range(0,len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[i] not in dic_letters.keys():
            dic_letters[TRAIN_LETTERS[i]]=10**-7

def transition_prob3():
    dic_letters_new={}
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    lines=file_input()
    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])-1):
            iterator=lines[i][j]+lines[i][j+1]
            if iterator in dic_trans3.keys():
                dic_trans3[iterator]+=1
            else:
                dic_trans3[iterator]=1

    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])):
            if lines[i][j] in dic_letters_new.keys():
                dic_letters_new[lines[i][j]]+=1
            else:
                dic_letters_new[lines[i][j]]=1
    list1=[]
    list1=dic_letters_new.keys()
    list2=[]
    list2=dic_trans3.values()
    len1=sum(list2)
    for i in list1:
        for j in list1:
            if i+j in dic_trans3.keys() and i+j in dic_letters_new.keys():
                #dic_trans3[i+j]=dic_trans3[i+j]/dic_letters_new[i]
                dic_trans3[i + j] = dic_trans3[i + j] /(dic_letters_new[i]+dic_letters_initial[j])
                #dic_trans3[i + j] = dic_trans3[i + j] / 5184
            else:
                dic_trans3[i+j]=10**-7

    for i in TRAIN_LETTERS:
        for j in TRAIN_LETTERS:
            if i+j in dic_trans3.keys():
                dic_trans4[i+j]=dic_trans3[i+j]
            else:
                dic_trans4[i+j]=10**-5

    for i in TRAIN_LETTERS:
        for j in TRAIN_LETTERS:
            if i+j not in dic_trans3.keys():
                dic_trans3[i+j]=10**-9


transition_prob()
transition_prob3()

def variable_elimination(train_letters,test_letters):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    taos=[]
    taos2 = []
    for i in range(0,len(TRAIN_LETTERS)):
        temp = 0

        for j in range(0,len(TRAIN_LETTERS)):
            iterator4=""
            iterator4=iterator4+TRAIN_LETTERS[i]+"."+TRAIN_LETTERS[j]
            temp+=dic_letters_initial[TRAIN_LETTERS[j]]*dic_trans[iterator4]
            #temp += dic_letters_initial[TRAIN_LETTERS[j]]

        temp*=prob_calculator(TRAIN_LETTERS[i],test_letters[0])

        taos2.append(temp)

    taos.append(taos2)


    for i in range(1,len(test_letters)):
        taos2 = []
        for j in range(0,len(TRAIN_LETTERS)):#j is S1 and k is s2
            temp=0
            for k in range(0,len(TRAIN_LETTERS)):
                    iterator4=""
                    iterator4=iterator4+TRAIN_LETTERS[j]+TRAIN_LETTERS[k]
                    #temp+=dic_trans4[iterator4]*taos[i-1][k]
                    temp+=taos[i-1][k]
            temp*=prob_calculator(TRAIN_LETTERS[j], test_letters[i])
            taos2.append(temp)
        taos.append(taos2)

    final_string=""
    for i in range(0, len(taos)):
        temp22 = 0
        temp23 = 0
        for j in range(0, len(TRAIN_LETTERS)):
            if taos[i][j] > temp22:
                temp22 = taos[i][j]
                temp23 = j
        final_string=final_string+TRAIN_LETTERS[temp23]
    print("HMM VE:",final_string)

variable_elimination(train_letters,test_letters)


def viterbi(train_letters,test_letters):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    taos = []
    taos2=[]


    for j in range(0,len(TRAIN_LETTERS)):
        taos2.append(math.log(prob_calculator(TRAIN_LETTERS[j],test_letters[0]),2))
    taos.append(taos2)

    for i in range(1,len(test_letters)):
        taos2=[]

        temp2=[]
        temp4=[]

        for k in range(0,len(TRAIN_LETTERS)):
            temp=0
            temp1=0
            for j in range(0,len(TRAIN_LETTERS)):
                temp3=0
                iterator=TRAIN_LETTERS[k]+TRAIN_LETTERS[j]
                temp3=taos[i-1][j]+math.log(dic_trans4[iterator],2)
                if temp3>temp:
                    temp=temp3
                    temp1=j
            taos2.append(temp+math.log(prob_calculator(TRAIN_LETTERS[k],test_letters[i]),2))
            temp2.append(temp1)
        taos.append(taos2)
        temp4.append(temp2)


    ans=""
    for i in range(0,len(test_letters)):
        temp5 = 0
        temp=-9999999999999
        for j in range(0,len(TRAIN_LETTERS)):
            if taos[i][j]>temp:
                temp=taos[i][j]
                temp5=j
        ans=ans+TRAIN_LETTERS[temp5]


    print("HMM MAP:",ans)
viterbi(train_letters,test_letters)







