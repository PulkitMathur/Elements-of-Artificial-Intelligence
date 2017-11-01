 #First, we started with cleaning the data where we removed the punctuations and used the linux code shared by Professor.
#Next, we looked for text based classification information and referred [1]
#After running the first version, we saw a very low accuracy so we added basic stopwords
#Design decisions-
#We decided to store the values in the form of tables for frequency and probabilites.
#We used Laplace smoothening
#Our code is giving 2% accuracy which is very low.
#May be adding more stop words or changing the probability calculation methods we can improve the accuracy
#Thus top 5 words could not be generated
#CITATIONS:
#[1]https://monkeylearn.com/blog/practical-explanation-naive-bayes-classifier/
#[2]Logic discussion about with cgalani_sahk_skpanick


import string
import math
import sys

train_d =sys.argv[1]
test_d = sys.argv[2]
outp_d = sys.argv[3]


train_d=open(train_d,"r")


lines =train_d.read()
#print lines
train_d.close()
data_inp = lines.rstrip()
data1=data_inp.strip()
data = data1.splitlines()
#print "input",data
tweets_data=[]
tweets_data1=[]
i = 0
#convert next line tweets to one line if that tweet doesn't contain ",_"
for x in range(len(data)):
    try:
         data[x].index(",_")
         tweets_data.insert(i, data[x])

         i +=1

    except ValueError:
         tweets_data[i-1] = tweets_data[i-1] + " " + data[x]
#print tweets_data
#print "here9", tweets_data1
#print "here8", tweets_data
j=0
loc = []
twee = []
for x in tweets_data:
    try:
        j+=1
        loc.append(x[:x.index(" ")])
        twee.append(x[x.index(" "):])
        #print "here", loc
        #print "here1",twee
    except ValueError:
        print "Error"


no_dup_word = set() #used to get unique words from tweet
uni_loc = set(loc) #used to get unique locations
uni_location = list(uni_loc)
all_words = [] #stores all the tweets
loc_dict = dict()
#print "loc", uni_location
no_punc_tweet_list = []
punct = set(".\"\':;!?/#@$&)(\\,_=+-**0123456789")
stopwords=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his'\
    ,'himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who',
           'whom','this','that','these','those','am','is','are','was']
d = " amp "
for x in twee:
    out = ''.join(c for c in x if not c in punct)
    #print "cleaned",out
    output1=out.lower()
    if output1 in stopwords:
        continue
    output = output1.split() #final data all words in uppercase without punctuations
    #print "upp", output

    no_punc_tweet_list.append(output)
    for words in output:
        all_words.append(words)
        no_dup_word.add(words)

no_dup_word_list = list(no_dup_word)

counter=1
for i,j in loc_dict.iteritems():
    for x in tweets_data:
        if loc_dict[i] == x[:x.index(" ")]:
            loc_dict.update()
            counter+=1
    print "dict",loc_dict[i]

#print "here3",no_dup_word_list
#print "here4",all_words
#print "here!!!! ",no_punc_tweet_list

# for words in no_dup_word_list:
#     rem = set('x')
#     out1 = ''.join(c for c in words if not c in rem)
#     print out1


##########
#using a table like in DP we can calculate the word frequency for each tweet and location
#
#########
rows = len(no_dup_word_list)+2
cols = len(uni_location)+2
#print str(rows)+" rows and "+str(cols)+" cols :)"
freq_mat = []
freq_mat = [[0 for c in range(cols)]for r in range(rows)]
#print freq_mat

#store freq of each word for that loc
c=1
#use dictionary to find the location of location(cities)  in the table
loc_loc = dict()
for i in uni_location:
    freq_mat[0][0] = "Words in r and Loc in c"
    freq_mat[0][c] = i
    loc_loc[i] = c
    c+=1
#print freq_mat
#print loc_loc
r=1
#use dictionary to find the location of the word in the table
loc_word = dict()
for j in no_dup_word_list:
    freq_mat[r][0] = j
    loc_word[j] = r
    r+=1
#print freq_mat
#print loc_word

cou = 0
for frag in no_punc_tweet_list:
    #check if the word in fragment is present
    #print frag
    loc_ls = loc[cou]
    for word in frag:
        #print word
        #print "here999",loc_word[word], loc_loc[loc_ls]
        freq_mat[loc_word[word]][loc_loc[loc_ls]]+= 1

    cou+=1
#print freq_mat

#Now calculate rows sum and columns sum
n = len(freq_mat)
for r in range(1,n):
    rowSum = 0
    for c in range(1,len(freq_mat[0])):
         #print "r = ",r
         #print "c = ",c
         #print freq_mat[r][c]
         rowSum+= freq_mat[r][c]
         #print "rowSum",rowSum
    freq_mat[r][len(freq_mat[0])-1]=rowSum
    #print '\n'
#print freq_mat

for c in range(1,len(freq_mat[0])):
    colSum=0
    for r in range(1,n-1):
        #print freq_mat[r][c]
        colSum+= freq_mat[r][c]
    freq_mat[len(freq_mat)-1][c]= colSum
    #print freq_mat
    #print '\n'

#print freq_mat

#calculate probability
prob_tab = [[0 for c in range(cols)]for r in range(rows)]
#prob_tab1 = [[0 for c in range(cols)]for r in range(rows)]
#1. create rows and column names
coun=1
for o in uni_location:
    prob_tab[0][0] = "Words in r and Loc in c"
    prob_tab[0][coun] = o
    coun+=1
r=1
for u in no_dup_word_list:
    prob_tab[r][0] = u
    r+=1
#print prob_tab
#print "jug",len(uni_location)
#print "l", len(freq_mat)
#2. Calculate P(word=something|Location=Chicago)
for i in range(1,len(freq_mat)):
    for k in range(1,len(uni_location)+1):
        try:
            #print freq_mat[len(freq_mat)-1][k]
            prob_tab[i][k]=(freq_mat[i][k])+1/float(freq_mat[len(freq_mat)-1][k]+len(uni_location))
            #prob_tab1[i][k]=(freq_mat[i][len(uni_location)]/len(freq_mat))
            #print "here", freq_mat[len(freq_mat)-1][len(uni_location)]
        except:
            print "error at "+str(i)+" on "+str(k)
    #print '\n'
#print prob_tab

#prob_all_loc = dict()
#for i in range(len(prob_tab[0])+1):
    #for j in range():
#print "here",prob_tab[0]
#for i in range(1,len(prob_tab[0])):
        #for i in range(1,6):
            #try:
              #print max(prob_tab[k][i])
              #print "here"
            #except:
                #print "Error at some i, k"




######################
test_data=open(test_d,"r")

lines1 =test_data.read()
#print lines
train_d.close()
data_inp1 = lines1.rstrip()
data11=data_inp1.strip()
data10 = data11.splitlines()
#print "input",data10
tweets_data1=[]

i = 0
#convert next line tweets to one line if that tweet doesn't contain ",_"
for x in range(len(data10)):
    try:
         data10[x].index(",_")
         tweets_data1.insert(i, data10[x])

         i +=1

    except ValueError:
         tweets_data1[i-1] = tweets_data1[i-1] + " " + data10[x]
#print tweets_data1
#print "here9", tweets_data1
#print "here8", tweets_data
j=0
loc1 = []
twee11 = []
for x in tweets_data1:
    try:
        j+=1
        loc1.append(x[:x.index(" ")])
        twee11.append(x[x.index(" "):])
        #print "here", loc
        #print "here1",twee
    except ValueError:
        print "here is an Err"


no_dup_word1 = set() #used to get unique words from tweet
uni_loc1 = set(loc1) #used to get unique locations
uni_location1 = list(uni_loc1)
all_words1 = [] #stores all the tweets
#print "loc", uni_location
no_punc_tweet_list1 = []
punct1 = set(".\"\':;!?/#@*$&)(\\,_=+-0123456789")
stopwords=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his'\
    ,'himself','she','her','hers','herself','it','its','itself']

d = " amp "
for x in twee11:
    out_n = ''.join(c for c in x if not c in punct1)
    #print "cleaned",out
    output1_n=out_n.lower()
    if output1_n in stopwords:
        continue
    output_n = output1_n.split() #final data all words in uppercase without punctuations
    #print "upp", output_n
    #print output_n,x
    no_punc_tweet_list1.append(output_n)
    for words in output_n:
        all_words1.append(words)
        no_dup_word1.add(words)
no_dup_word_list1 = list(no_dup_word1)
#print "my test",no_dup_word_list1


rows1 = len(no_dup_word_list1)+2
cols1 = len(uni_location1)+2
words_list = []
loc_mat =[]
words_list = [[0 for i in range (0,2)] for c in range(rows1)]
loc_mat = [0 for r in range(cols1)]
#print freq_mat

#store freq of each word for that loc
c=1
#use dictionary to find the location of location(cities)  in the table
loc_loc_test = dict()
for i in uni_location:
    loc_mat[0] = "Words in r and Loc in c"
    loc_mat[c] = i
    loc_loc_test[i] = c
    c+=1
#print freq_mat_test
q=1
#use dictionary to find the location of the word in the table
loc_word1 = dict()
for j in no_dup_word_list1:
    words_list[q] = j
    loc_word1[j] = q
    q+=1
#print words_list


cou = 0
index = 0
file=open("check.txt","w+")
value_max = 0
#res = list()
res=''
for p in range(len(no_punc_tweet_list1)):
    final_dict = dict()
    for l in range(1,len(uni_location1)+1):
        #print "l" , l
        totProb=1
        fin_prod =1
        for h in range(1,len(no_punc_tweet_list1[p])):
            words1= no_punc_tweet_list1[p][h]
            #print words1
            try:
                index = loc_word1[words1]
                #print index
            except KeyError:
                index = -99
            if index != -99:
                totProb = prob_tab[index][l]
                #print "here",type(totProb)
                fin_prod *=totProb
            else:
                totProb = 0+1/float(freq_mat[len(freq_mat)-1][l]+len(uni_location1))
                fin_prod*=totProb
                #print fin_prod
        final_dict[freq_mat[0][l]]=fin_prod
    value_max= max(final_dict.values())
    res = [key for key,value in final_dict.iteritems() if value == value_max]
    file.write(str(res)+str(loc1[p])+','+str(no_punc_tweet_list1[p])+'\n')

  
