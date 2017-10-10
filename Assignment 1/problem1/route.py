#!/usr/bin/python
# List of References
#1 . https://math.stackexchange.com/questions/29157/how-do-i-convert-the-distance-between-two-lat-long-points-into-feet-meters

##############Explanation##################
#Question:1
# Both uniform and A-Star search seems to work best when the cost (distance,time and segments) has to be minimised. For example,
# if I want to minimise the travelled distance or the total elapsed time then uniform search gives the optimum value.

#There is however a significant trade-off involved here as i am optimising one cost function at a time, so If i ask uniform search to
#optimise distance then it will slightly increase the time and number of segments but will report the optimal distance route. The same
#is also true for the case when time is optimised, the other costs are slightly compromised.

#This optimum is however achieved at the cost of memory and computations, as the program is now evaluating
#each successor state objectively (in terms of distance, time and segments) rather then just looking for the goal state. The cost
#is even more in case of A-star as an evaluation function now has to be computed for each state.

# Question:2
# For 10 independent runs of the program, the DFS search always seems to report the results faster(on an average against
# BFS, uniform and A-Star). The results are not optimal but are obtained relatively quickly as compared to
# other search algorithms. This may be because, if the start and end cities are on the same branch then DFS
# will reach the goal state quickly as compared to the other algorithms. In other cases DFS may perform worse.

#Also, A-Star algorithm performed second fastest as compared to the BFS and Uniform search.

#A basic comparison rubric is a follows (these are normalised results for 10 runs on my MAC book pro) where DFS is faster:
#        BFS            uniform         A-Star
#DFS     3x faster      4x faster       3x faster ---> DFS is faster

#           BFS             uniform
#A-Star     2x             1.5x ~ 2x ---> A-Star is faster

#The above results are only valid when program don't revisit the states, if the same state are revisited again then DFS
#performance degrades rapidly.

#Question:3
#The DFS requires the least memory as compared to the other algorithms. This is so because, it's memory footprint
#will not cross O(bd) (b = branching factor, d = depth at which the goal is located). This is relatively better than
#other algorithms where the fringe size can reach O(b^d)--even better than O(b/2) for bi-directional search.

#A basic comparison rubric is a follows (these are normalised results for 5 runs on my MAC book pro) where DFS used less memory:
#        BFS                    uniform                A-Star
#DFS     1.5x less memory       2x less memory         3x-4x less memory ---> DFS is faster

#Question:4:
#Heuristic function: The following is the heuristic that i used:
#h(s) = Haversine distance between the current and the goal state
#evaluation distance f(s) = g(s) + h(s),
# g(s) = path length to reach the state from the start state,
# h(s) = heuristic cost to reach the goal state from the current state.
# For missing data, I used the heuristic cost of the parent minus the path length between the parent and the children as the
#heuristic estimate.

#This estimate works good but is not always accurate (especially when the two cities are far apart) because
#of the nature of the haversine fomrula. So, I adjusted for the overestimate by taking the root to the 3rd power.
#This adjustment seems to dramatically adjust the total cost to reach the goal state and prevent the cost from being overestimated.

#This heuristic estimate can become absolute if the missing GPS data can be completed. So, one way to do that is to get the GPS
# data for junctions (because it is missing for most junctions) and then use the coordinates to calculate the heuristic estimate.
#################END#################


from collections import defaultdict
from time import sleep
import sys
import math

#Function to perform BFS search. Popping will happen in FIFO manner
def implement_bfs():
    segment_count = 0;

    while len(fringe) != 0:

        popped_city = fringe.pop(0)
        where = path_for_other_search.index(popped_city)

        if popped_city not in visited:
            cities = succ(popped_city)

            for city in cities:

                elements = city.split("@")
                place = elements[0].strip()
                temp_cost = elements[1].strip()
                dcost = float(temp_cost) + float(dist_list[where])
                temp_cost = elements[2].strip()
                tcost = float(temp_cost) + float(time_list[where])
                highway = elements[3].strip()

                if chk_goal(place, end):
                    path_for_other_search.append(place)
                    track_list.append(where)
                    dist_list.append(dcost)
                    time_list.append(tcost)
                    via.append(highway)
                    segment_list.append(segment_count + 1)
                    del fringe[:]
                    break

                else:
                    fringe.append(place)
                    path_for_other_search.append(place)
                    track_list.append(where)
                    dist_list.append(dcost)
                    time_list.append(tcost)
                    via.append(highway)
                    segment_list.append(segment_count + 1)
        visited.add(popped_city)



#Function to perform DFS search. Popping will happen in LIFO manner
def implement_dfs():

    segment_count = 0

    while len(fringe) != 0:

        #Popping in LIFO fashion
        popped_city = fringe.pop()
        where = path_for_other_search.index(popped_city)

        cities = succ_dfs(popped_city)
        visited.add(popped_city)

        for city in cities:
            elements = city.split("@")
            place = elements[0].strip()
            temp_cost = elements[1].strip()
            dcost = float(temp_cost) + float(dist_list[where])
            temp_cost = elements[2].strip()
            tcost = float(temp_cost) + float(time_list[where])
            highway = elements[3].strip()

            if chk_goal(place, end):
                path_for_other_search.append(place)
                track_list.append(where)
                dist_list.append(dcost)
                time_list.append(tcost)
                via.append(highway)
                segment_list.append(segment_count + 1)
                del fringe[:]
                break

            else:
                fringe.append(place)
                path_for_other_search.append(place)
                track_list.append(where)
                dist_list.append(dcost)
                time_list.append(tcost)
                via.append(highway)
                segment_list.append(segment_count + 1)


#Function to implement uniform cost search. The order of checking the goal is preponed to adding to the fringe.
def implement_uniform():

    scost = 0
    fringe_uniform = list()
    fringe_uniform.append([start,0])

    while len(fringe_uniform) != 0:

        temp = find_high_priority(fringe_uniform)
        where = path_for_uniform_search.index(temp)

        if chk_goal(temp[0], end):
            if routing_option == "distance":
                path_for_uniform_search.append([place, dcost])
            elif routing_option == "time":
                path_for_uniform_search.append([place, tcost])
            else:
                path_for_uniform_search.append([place, scost])
            track_list.append(where)
            dist_list.append(dcost)
            time_list.append(tcost)
            via.append(highway)
            segment_list.append(scost)
            del fringe_uniform[:]
            break

        # Checking or the visited cities here, if visited then don't revisit again.
        if temp[0] not in visited:
            cities = succ_uniform(temp, data_dict_uniform, visited)
            scost = int(segment_list[where])
            scost = scost +1

            for city in cities:

                elements = city.split("@")
                place = elements[0].strip()
                temp_cost = elements[1].strip()
                dcost = float(temp_cost) + float(dist_list[where])
                temp_cost = elements[2].strip()
                tcost = float(temp_cost) + float(time_list[where])
                highway = elements[3].strip()

                if routing_option == "distance":
                    fringe_uniform.append([place, dcost])
                    path_for_uniform_search.append([place, dcost])
                elif routing_option == "time":
                    fringe_uniform.append([place, tcost])
                    path_for_uniform_search.append([place, tcost])
                else:
                    fringe_uniform.append([place, scost])
                    path_for_uniform_search.append([place, scost])

                track_list.append(where)
                dist_list.append(dcost)
                time_list.append(tcost)
                via.append(highway)
                segment_list.append(scost)
        visited.add(temp[0])


#Function to implement A-Star
def implement_astar():

    scost = 0
    fringe_uniform = list()
    fringe_uniform.append([start,0])

    while len(fringe_uniform) != 0:

        temp = find_high_priority(fringe_uniform)
        where = path_for_astar.index(temp)

        #Check for goal
        if chk_goal(temp[0], end):
            if routing_option == "distance":
                path_for_astar.append([place, hcost])
            else:
                path_for_astar.append([place, thcost])
            track_list.append(where)
            dist_list.append(tdcost)
            time_list.append(thcost)
            via.append(highway)
            segment_list.append(scost)
            del fringe_uniform[:]
            break

        # Checking or the visited cities here, if visited then don't revisit again.
        if temp[0] not in visited:
            cities = succ_uniform(temp, data_dict_uniform, visited)
            scost = int(segment_list[where])
            scost = scost + 1

            for city in cities:

                elements = city.split("@")
                place = elements[0].strip()
                temp_cost = elements[1].strip()
                tdcost = float(temp_cost) + float(dist_list[where])
                temp_cost = elements[2].strip()
                thcost = float(temp_cost) + float(time_list[where])
                highway = elements[3].strip()

                if place in gps_dict_uniform:

                    heu_dist = calculate_dist_using_gps(float(extract_gps_ccords(place)[0]),float(extract_gps_ccords(place)[1]),float(extract_gps_ccords(end)[0]),
                                                        float(extract_gps_ccords(end)[1]))

                    hcost = heu_dist + tdcost

                    if routing_option == "distance":
                        fringe_uniform.append([place, hcost])
                        path_for_astar.append([place, hcost])
                    elif routing_option == "time":
                        fringe_uniform.append([place, thcost])
                        path_for_astar.append([place, thcost])
                    else:
                        fringe_uniform.append([place, scost])
                        path_for_astar.append([place, scost])

                    track_list.append(where)
                    dist_list.append(tdcost)
                    time_list.append(thcost)
                    via.append(highway)
                    segment_list.append(scost)
                    heu_list.append(hcost)

                elif place not in gps_dict_uniform:

                    hcost = float(heu_list[where]) - float(elements[1].strip())

                    if routing_option == "distance":
                        fringe_uniform.append([place, hcost])
                        path_for_astar.append([place, hcost])
                    elif routing_option == "time":
                        fringe_uniform.append([place, thcost])
                        path_for_astar.append([place, thcost])
                    else:
                        fringe_uniform.append([place, scost])
                        path_for_astar.append([place, scost])

                    track_list.append(where)
                    dist_list.append(tdcost)
                    time_list.append(thcost)
                    via.append(highway)
                    segment_list.append(scost)
                    heu_list.append(hcost)

        visited.add(temp[0])


#Function to implement longtour cost
def implement_long_astar():

    segment_count = 0
    fringe_uniform = list()
    fringe_uniform.append([start,0])

    while len(fringe_uniform) != 0:

        temp = find_low_priority(fringe_uniform)
        where = path_for_astar.index(temp)

        if chk_goal(temp[0], end):
            path_for_astar.append([place, hcost])
            track_list.append(where)
            dist_list.append(dcost)
            heu_list.append(hcost)
            time_list.append(tcost)
            via.append(highway)
            segment_list.append(segment_count)
            del fringe_uniform[:]
            break

        #Checking or the visited cities here, if visited then don't revisit again.
        if temp[0] not in visited:
            cities = succ_uniform(temp, data_dict_uniform, visited)

            for city in cities:

                elements = city.split("@")
                place = elements[0].strip()
                temp_cost = elements[1].strip()
                dcost = float(temp_cost) + float(dist_list[where])
                temp_cost = elements[2].strip()
                tcost = float(temp_cost) + float(time_list[where])
                highway = elements[3].strip()

                if place in gps_dict_uniform:

                    heu_dist = calculate_dist_using_gps(float(extract_gps_ccords(place)[0]),float(extract_gps_ccords(place)[1]),float(extract_gps_ccords(end)[0]),
                                                        float(extract_gps_ccords(end)[1]))

                    hcost = heu_dist + dcost
                    fringe_uniform.append([place, hcost])
                    path_for_astar.append([place, hcost])
                    track_list.append(where)
                    dist_list.append(dcost)
                    time_list.append(tcost)
                    via.append(highway)
                    segment_list.append(segment_count)
                    heu_list.append(hcost)

                elif place not in gps_dict_uniform:

                    hcost = float(heu_list[where]) - float(elements[1].strip())

                    fringe_uniform.append([place, hcost])
                    path_for_astar.append([place, hcost])
                    track_list.append(where)
                    dist_list.append(dcost)
                    time_list.append(tcost)
                    via.append(highway)
                    segment_list.append(segment_count)
                    heu_list.append(hcost)

        visited.add(temp[0])


#Generate the succssor states (or connected cities from the current city)
def succ(city):
    children = data_dict_uniform[city]
    return children


#Generate the succssor states for dfs, check for visited states and omit them here.
def succ_dfs(city):
    children = data_dict_uniform[city]
    for child in children:
        if child.split("@")[0] in visited:
            children.remove(child)
    return children


#Generate the successor for uniform cost search, simple modification to handle additional distance constraints
def succ_uniform(city, data_dict_uniform, visited):
    children = data_dict_uniform[city[0]]
    for child in children:
        if child.split("@")[0] in visited:
            children.remove(child)
    return children


#Check the goal state. Simply check if the current city is goal or not.
def chk_goal(city,end):
        if city == end:
            return True

#Find the high priority state (the one with the lowest distance)
def find_high_priority(fringe_unifrom):
     wch = min(fringe_unifrom, key=lambda x:x[1])
     fringe_unifrom.remove(wch)
     return wch

#Find the high priority state (the one with the highest distance for long tour)
def find_low_priority(fringe_unifrom):
    wch = max(fringe_unifrom, key=lambda x: x[1])
    fringe_unifrom.remove(wch)
    return wch

#Extract the GPS coordinates for a given city.
def extract_gps_ccords(city):
    gps = [gps_dict_uniform[city][0],gps_dict_uniform[city][1]]
    return gps


#Function to find haversine distance see references--(1), this function is balanced for handling the overestimates when the cities are far apart.
def calculate_dist_using_gps(latitude1, longitude1, latitude2, longitude2):

    lat1_radia = math.radians(latitude1)
    lat2_radia = math.radians(latitude2)

    diff_lat = math.radians(abs(latitude2 - latitude1))
    diff_lon = math.radians(abs(longitude2 - longitude1))
    ang = (math.pow((math.sin(diff_lat / 2.0)), 2)) + math.cos(lat1_radia) * math.cos(lat2_radia) * (
        math.pow((math.sin(diff_lon / 2.0)), 2))
    arc = 2.0 * (math.atan2(*(math.sqrt(ang), math.sqrt(1 - ang))))
    distance = 3958.756 * arc

    #Using the conversion factor for Km to miles
    if routing_option == "longtour":
        distance = 3958.756 * arc
    else:
        distance = ((distance)**(1./3.))

    return distance


#Make a dictionary of the city and their GPS data
def make_gps_dict_uniform(input_file):
    file = open(input_file, "r")
    gps_dict = defaultdict(list)

    for line in file:

            elements = line.split(" ")
            city = elements[0].strip()
            lat = elements[1].strip()
            long = elements[2].strip()

            gps_dict[city].append(str(lat))
            gps_dict[city].append(str(long))

    file.close()
    return gps_dict


#Make a dictionary of the cities and their associated data
def make_node_dict_uniform(input_file):
    file = open(input_file, "r")
    data_dict = defaultdict(list)

    for line in file:

        if line.split(" ")[3].strip() != "0" and line.split(" ")[3].strip() != "":

            elements = line.split(" ")
            fcity = elements[0].strip()
            scity = elements[1].strip()
            dist = elements[2].strip()
            speed = elements[3].strip()
            highway = elements[4].strip()
            time = round(float(dist)/float(speed),2)

            data_dict[fcity].append(scity + "@" + str(dist) + "@" + str(time)+ "@" + str(highway))
            data_dict[scity].append(fcity + "@" + str(dist) + "@" + str(time)+ "@" + str(highway))

    file.close()
    return data_dict


#Setting up the input files. The program assumes that the input file are present in the same directory as the python program.
dist_file = "road-segments.txt"
gps_file = "city-gps.txt"

# end = 'Bloomington,_Indiana'
# start = 'San_Jose,_California'
# #start = 'New_York,_New_York'
# #start = 'Detroit,_Michigan'
# #start = "Indianapolis,_Indiana"
# #end = 'Chicago,_Illinois'
# method = "astar"
# routing_option = "segments"

start = sys.argv[1]
end = sys.argv[2]
method = sys.argv[3]
if method == "uniform" or method == "astar":
    routing_option = sys.argv[4]
else:
    routing_option = "nh"

path_for_uniform_search = list()
path_for_astar = list()
path_for_other_search = []
track_list = []
fringe = []
visited = set()
city_list = list()
dist_list = []
heu_list = []
segment_list = []
time_list = []
via = []

where = 0
ind = 0;
output_string = ""


data_dict_uniform = make_node_dict_uniform(dist_file)
gps_dict_uniform = make_gps_dict_uniform(gps_file)

#Check if start node is the destination itself (end), then return just the start node
if start == end:
    print("Destination reached"+str(start))

else:

    fringe.append(start)
    track_list.append(0)
    dist_list.append(0)
    time_list.append(0)
    heu_list.append(0)
    segment_list.append(0)
    via.append("")

    if method == "uniform":
        path_for_uniform_search.append([start, 0])
        implement_uniform()
    elif method == "astar":
        path_for_astar.append([start, 0])
        if routing_option == "longtour":
            implement_long_astar()
        else:
            implement_astar()
    elif method == "bfs":
        path_for_other_search.append(start)
        implement_bfs()
    elif method == "dfs":
        path_for_other_search.append(start)
        implement_dfs()


if method == "astar":
    ind = len(path_for_astar) - 1

    while ind!=0:
        city_list.append([path_for_astar[ind][0],dist_list[ind],time_list[ind],segment_list[ind],via[ind]])
        ind = track_list[ind]

        if ind == 0:
            city_list.append([path_for_astar[0][0],dist_list[ind],time_list[ind],segment_list[ind],via[0]])

elif method == "uniform":
    ind = len(path_for_uniform_search) - 1

    while ind!=0:
        city_list.append([path_for_uniform_search[ind][0],dist_list[ind],time_list[ind],segment_list[ind],via[ind]])
        ind = track_list[ind]

        if ind == 0:
            city_list.append([path_for_uniform_search[0][0],dist_list[ind],time_list[ind],segment_list[ind],via[0]])

elif method == "dfs" or method == "bfs":
    ind = len(path_for_other_search) - 1

    while ind != 0:
        city_list.append([path_for_other_search[ind], dist_list[ind], time_list[ind], segment_list[ind], via[ind]])
        ind = track_list[ind]

        if ind == 0:
            city_list.append([path_for_other_search[0], dist_list[ind], time_list[ind], segment_list[ind], via[0]])



if method == "astar" or method == "uniform":
    for elem in reversed(city_list):
        if elem[0] == start:
            print("Start from " + start + "\n")
            output_string = output_string + " " + str(elem[0])
        elif elem[0] == end:
            if routing_option == "distance":
                print("Hey, you reached, " + end + " " + " Covered " + routing_option + " is: " + str(elem[1]))
            elif routing_option == "time":
                print("Hey, you reached, " + end + " " + routing_option + "elapsed is: " + str(elem[2]))
            elif routing_option == "segments":
                print("sHey, you reached, " + end + " " + " Covered " + routing_option + " are: " + str(elem[3]))
            output_string = output_string + " " + str(elem[0])
            print(str(elem[1]) + " " + str(round(elem[2], 2)) + output_string)
            break
        else:
            print("Follow the : " + str(elem[4]) + " highway to " + str(elem[0]) + " " + "covered distance is: "
                  + str(elem[1]) + " miles, elapsed time is: " + str(round(elem[2], 2)) + " hours")
            output_string = output_string + " " + str(elem[0])


elif method == "bfs" or method == "dfs":

    for elem in reversed(city_list):

        if elem[0] == start:
            print("Start from " + start + "\n")
            output_string = output_string + " " + elem[0]

        elif elem[0] == end:
            print("Hey, you reached, "+ end)
            output_string = output_string + " " + elem[0]
            print(str(elem[1])+" "+str(round(elem[2],2))+output_string)
            break

        else:
            print("Follow the : "+ str(elem[4]) + " highway to " +str(elem[0]) + " " + "covered distance is: "+str(elem[1]) +
                  " miles, elapsed time is: "+
                  str(round(elem[2],2)) +" hours")
            output_string = output_string + " " + elem[0]



