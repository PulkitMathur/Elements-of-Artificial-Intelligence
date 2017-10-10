#!/usr/bin/python

##############Explanation############
# The program is implemented in a greedy search manner (also a brute force fashion is applied) to find the best solution locally.
#It then proceeds in an iterative manner and look for local optimum solutions until all the students are categorized into
#a group.

# Basically, each local optimum here is one state that has the lowest cost (penalties etc.).

#Initial State:
#To start the process, a random assignment of peoples to various groups is done.
#This is a combinatorial process in nature. First generate all possible groups of 1, 2 and 3 people in the given dataset.
#The groups are overlapping in this step as there is no hard assignment of people yet. So, one person can belong to multiple groups.

#Goal State:
# The goal state is achieved when there are no more people to assign to any more groups. This ensures that every
# person belongs to a group. The goal state is achieved while ensuring that the previous states were all locally best
#the solutions. This simply means that out of all possible groups, the one that has the lowest cost is locally the best.

#Set of states and Successor function
#At each iteration until the goal in not achieved, a successor function returns a random grouping of all remaining peoples. This
#grouping does not include people who were already assigned to group in the previous state. So, each time a successor is called,
#out of all possible groups of remaining peoples, the one with the lowest cost is selected. The grouping again involves all
#groups of 1,2 and 3 people so no combination is left.

#Cost function:
# The cost function here is the objective cost of each state. The total cost for the state including all the
# penalties for size, likes and dislikes. This cost is used for selecting the lowest scoring candidate from the priority queue.

#The program works based on the logic that if a lowest cost candidate is selected at each iteration then the final
#result will be a combination of all such local optimums. 


import itertools
from collections import defaultdict
import sys

#Function for reading the contraints file
def read_file():
    file = open(input_file, "r")
    data_dict = defaultdict(list)

    for line in file:
        if line != "\n":
            elements =  line.split(" ")
            name = elements[0].strip()
            size = elements[1].strip()
            like = elements[2].strip()
            dislike = elements[3].strip()

            data_dict[name].append(size)
            data_dict[name].append(like)
            data_dict[name].append(dislike)

    return data_dict

#Generate the successor states of the current state
def succ_gen_group(person_list):

    groups = []

    if len(person_list)>3:

        for comb in itertools.combinations(person_list,3):
            groups.append(comb)

    elif len(person_list) > 2:

        for comb in itertools.combinations(person_list, 2):
            groups.append(comb)

    elif len(person_list)==2 or len(person_list)==3 or len(person_list) == 1:
        groups.append(tuple(person_list))

    return groups


#Calculate the cost for the current state  and return the minimum of that. So, basically the penalties are calculated based on the
#constraints and addition of the penalties becomes the local cost for the state.
def cal_cost(groups, data_dict, like_penalty, dislike_penalty):

    group_dict = defaultdict()
    total_cost = 0

    for group in groups:

            for person in group:
                size_violation = 0
                like_violation = 0
                dislike_violation = 0
                # print "person is: " +str(person)
                size = data_dict[person][0]
                likes = data_dict[person][1]
                dislikes = data_dict[person][2]

                if size != "0":
                    if size != len(group):
                        size_violation = size_violation + 1

                if likes != "_" and "," in likes:
                    like_array = likes.split(",")

                    for every_person in like_array:
                        if every_person not in group:
                            like_violation = like_violation + 1

                elif likes != "_" and "," not in likes:
                    if likes not in group:
                        like_violation = like_violation + 1

                if dislikes != "_" and "," in dislikes:
                    dislike_array = dislikes.split(",")

                    for every_person in dislike_array:
                        if every_person in group:
                            dislike_violation = dislike_violation + 1

                elif dislikes != "_" and "," not in dislikes:
                    if dislikes in group:
                        dislike_violation = dislike_violation + 1

                total_cost = total_cost + size_violation + (like_violation * like_penalty) + (dislike_violation * dislike_penalty)
                # print "size violation is: " + str(size_violation)
                # print "like violation is:" + str(like_violation)
                # print "dislike violation is: " + str(dislike_violation)
                # print "total cost is:" +str(total_cost)

            group_dict[group] = total_cost

    try:
        return min(group_dict.items(), key=lambda x: x[1])
    except UnboundLocalError:
        print "group was: " + str(group)

#Check for the goal state.
def chk_goal(final_groups,person_list):
        sum = 0
        for i in final_groups:
            sum = sum + len(i[0])

        if sum  == len(person_list.keys())-1:
            return True

#Setup the input parameters here.
#input_file = "test22.txt"
input_file = sys.argv[1]
group_time = int(sys.argv[2])
dislike_penalty = int(sys.argv[3])
like_penalty = int(sys.argv[4])

person_dict = read_file()
status_bit=1
grouped_dict = []
set_of_ungrouped= []
final_groups = []



#Search initiated
while status_bit==1:

    if chk_goal(final_groups,person_dict):
        status_bit=0
        break

    for person in person_dict.keys():
         if person not in grouped_dict:
             set_of_ungrouped.append(person)

    #Generate the successors here.
    get_grouping = succ_gen_group(set_of_ungrouped)
    del set_of_ungrouped[:]
    #get the min cost successor
    min_cost_group = cal_cost(get_grouping,person_dict,like_penalty,dislike_penalty)
    del get_grouping[:]

    #Add the min cost successor to the final list
    for person in min_cost_group[0]:
        grouped_dict.append(person)

    final_groups.append(min_cost_group)


line =""
partial_cost = 0

#Parse the data for printing the output.
for group in final_groups:
    for person in group[0]:
        line = line +" "+ person
    print line
    partial_cost = partial_cost + group[1]
    line = ""
total_cost = partial_cost + (len(final_groups)*10)
print total_cost

