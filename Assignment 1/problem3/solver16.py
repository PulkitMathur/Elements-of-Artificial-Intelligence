=#@author: Pulkit Mathur
#Date: October 1, 2017

#1) This program solves the 15 puzzle.
#Formulation of the search problem.

#Initial State: The initial state is the 4x4 board configuration given as input in the text file.


#Goal State: The goal state is the canonical configuration of the board with tiles 1-15 arranged sequentially
# and empty tile in the lower right corner. The value of heuristic function will be 0 at goal state.

#State Space: The state space will contain all board configurations with an even permutation inversion generated by the
# successor function. The states with odd permutation inversion are filtered out.

#Successor function: The successor function will slide tiles surrounding the empty tile one by one into the empty tile.
# Every state will have 12 successor #states because an empty tile can move 1 or 2 ot 3 units in up or down or left or right direction.


#Edge weights: The edge weight of a state n is the total cost f(n), where f(n)=g(n)+h(n), g(n) is the cost of reaching
# the state n from start state, h(n) is #the heuristic cost, the cost of reaching the goal state from the state n.

#Heuristic Function
#Manhattan distance: heuristicManhattan(state) method  in this code calculates the total manhattan distance of the tiles in
#a state. This heuristic is admissible because for a tile it adds the minimum cost of reaching the correct position of the tile.
# Therefore, it will be less than the actual cost. This heuristic assumes that a tile is isolated and free to move within
# the board, hence it will never overestimate the actual cost.


#Linear conflict: linearConflict(state) method  in this code calculates the linear conflict between tiles of a state.
#This heuristic is admissible because it adds two moves for each pair of conflicting tiles which are in their goal row, column
#but incorrectly placed such that they have to be moved by atleast two moves:


#2) The search begins with generating the successors of the initial state.
# Each new successor state is tested for goal state by comparing its heuristic value #to 0.
# The successor states are added to the fringe which is a dictionary with key =g(n)+h(n) i.e
#the total cost of the state; and value as the state #configuration stored as a list. The search is a modified DFS in which
#during the pop operation the successor state with lowest key is picked to  get an optimal solution.
#In case, more than one state has the same key value, the leftmost state is popped first.
#The search stops when we find a successor state with heuristic cost=0.

#3) This code gives optimal solution for all puzzles with initial permutation inversion<=40. For the tougher puzzles, speed is
#given preference to optimality.
#This is done by multiplying the initial cost g(n) by a constant to favor a greedy approach.
# The constant which worked best was 0.5.


import sys
import time
import copy

# Read input filename
arguments = sys.argv


# Goal State
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]



# Class for state with heuristic value
class BoardState(object):
	def __init__(self, board, steps_list,cost,heu_man,perm_inv):
		self.board = board
		self.steps_list = steps_list
		self.cost = cost
		self.perm_inv = permutationInversion(self.board)
		self.heu_man = heuristicManhattan(self.board) + linearConflict(self.board)

coordinates=[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3]]

import math
def heuristicManhattan(board):

	board2 = []
	for i in range(4):
		for j in range(4):
			board2.append(board[i][j])
	h = 0
	for i in range(0, 16):
		if board2[i] != 0:
			x = math.fabs(coordinates[i][0] - coordinates[board2[i] - 1][0])
			y = math.fabs(coordinates[i][1] - coordinates[board2[i] - 1][1])
			h += x + y
	return int(h)

def linearConflict(board):
	board2 = []

	for i in range(4):
		for j in range(4):
			board2.append(board[i][j])
	linear_conflict = 0

	for i in range(0, 16 - 1):
		element = board2[i]
		for j in range(i + 1, 16):
			b = board2[j]
			if b < element and b != 0:
				should_be = coordinates[element - 1]
				also_should_be = coordinates[b - 1]
				element_current = [i // 4, i % 4]
				board_j_current = [j // 4, j % 4]
				if (should_be == board_j_current and also_should_be == element_current):
					linear_conflict += 2
	return linear_conflict

def permutationInversion(board):
	if isinstance(board, BoardState):
		print("obj h bhai")
		return 0

	print("In permutationInversion")
	print("Board")
	print(board)
	board2 = []
	for i in range(4):
		for j in range(4):
			board2.append(board[i][j])

	print("Board 2")
	print(board2)
	p = 0
	zero = 0
	for i in range(0, 15):
		element = board2[i]
		if element == 0:
			zero = i // 4 + 1
		for j in range(i + 1, 16):
				b = board2[j]
				if b < element and b != 0:
					p += 1
	return p + zero





# Get row of blank tile
def getRowOfTile(tile, board):
	print("in get row of tile")
	for i in range(4):
		for j in range(4):
			if (board[i][j] == tile):
				return i
	return -1

# Get row of blank tile
def getColOfTile(tile, board):
	print("in get col of tile")
	for i in range(4):
		for j in range(4):
			if (board[i][j] == tile):
				return j
	return -1


#This method reads the input file and returns a list (initial board).
def initialState(fileName):
    board=[]
    a = []
    try:
        file=open(fileName,mode='r')
        for line in file.readlines():
            board.append(line.split())
        file.close()
    except IOError:
        print ("Cannot read from file:")
        return
    for i in range(4):
	    for j in range(4):
		    board[i][j] = (int)(board[i][j])
    return board


# Function to print the board
def printBoard(board):
	print("--------------------")
	for i in range(4):
		for j in range(4):
			print(board[i][j], "", end="")
		print()
	print("--------------------")
	return


# Get Successors for one move
def getSuccessorforOneMove(state,row,col):
    print("In getSuccessorforOneMove")
    boardState1 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState2 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState3 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState4 = copy.deepcopy(BoardState(state, [],0,0,0))

    # Move Down
    if(row +1 <= 3):
        x = boardState1.board[row + 1][col]
        boardState1.board[row + 1][col] = 0
        boardState1.board[row][col] = x
        boardState1.steps_list.append("D1" + str(col))
        boardState1.perm_inv = permutationInversion(boardState1.board)
        boardState1.heuristic_value = heuristicManhattan(boardState1.board) + linearConflict(boardState1.board)
        print("One move down")
        printBoard(boardState1.board)

    if(row -1 >= 0):
        x = boardState2.board[row -1][col]
        boardState2.board[row][col] = x
        boardState2.board[row-1][col] = 0
        boardState2.steps_list.append("U1" + str(col))
        boardState2.perm_inv = permutationInversion(boardState2.board)
        boardState2.heuristic_value = heuristicManhattan(boardState2.board) + linearConflict(boardState2.board)
        print("One Move up")
        printBoard(boardState2.board)

    if(col + 1 <= 3):
        x = boardState3.board[row][col + 1]
        boardState3.board[row][col + 1] = 0
        boardState3.board[row][col] = x
        boardState3.steps_list.append("R1" + str(row))
        boardState3.perm_inv = permutationInversion(boardState3.board)
        boardState3.heuristic_value = heuristicManhattan(boardState3.board) + linearConflict(boardState3.board)
        print("one move right")
        printBoard(boardState3.board)

    if(col - 1 >= 0):
        x = boardState4.board[row][col - 1]
        boardState4.board[row][col - 1] = 0
        boardState4.board[row][col] = x
        boardState4.steps_list.append("L1" + str(col))
        boardState4.perm_inv = permutationInversion(boardState4.board)
        boardState4.heuristic_value = heuristicManhattan(boardState4.board) + linearConflict(boardState4.board)
        print("one move left")
        printBoard(boardState4.board)

    ans = []
    ans.append(boardState1)
    ans.append(boardState2)
    ans.append(boardState3)
    ans.append(boardState4)
    return ans


# Get Successors for two moves
def getSuccessorforTwoMoves(state, row, col):
    print("In getSuccessorforTwoMoves")
    boardState1 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState2 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState3 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState4 = copy.deepcopy(BoardState(state, [],0,0,0))

    if (row + 2 <= 3):
        boardState1.board[row][col] = boardState1.board[row+1][col]
        boardState1.board[row+1][col] = boardState1.board[row+2][col]
        boardState1.board[row+2][col] = 0
        boardState1.steps_list.append("D2" + str(col))
        boardState1.perm_inv = permutationInversion(boardState1.board)
        boardState1.heuristic_value = heuristicManhattan(boardState1.board) + linearConflict(boardState1.board)
        print("Two move down")
        printBoard(boardState1.board)

    if (row - 2 >= 0):
        boardState2.board[row][col] = boardState2.board[row-1][col]
        boardState2.board[row - 1][col] = boardState2.board[row-2][col]
        boardState2.board[row - 2][col] = 0
        boardState2.steps_list.append("U2" + str(col))
        boardState2.perm_inv = permutationInversion(boardState2.board)
        boardState2.heuristic_value = heuristicManhattan(boardState2.board) + linearConflict(boardState2.board)
        print("Two move up")
        printBoard(boardState2.board)

    if (col + 2 <= 3):
        a = boardState3.board[row][col + 1]
        b = boardState3.board[row][col + 2]
        boardState3.board[row][col] = a
        boardState3.board[row][col + 1] = b
        boardState3.board[row][col + 2] = 0
        boardState3.steps_list.append("R2" + str(row))
        boardState3.perm_inv = permutationInversion(boardState3.board)
        boardState3.heuristic_value = heuristicManhattan(boardState3.board) + linearConflict(boardState3.board)
        print("Two move right")
        printBoard(boardState3.board)

    if (col - 2 >= 0):
        a = boardState4.board[row][col - 1]
        b = boardState4.board[row][col - 2]
        boardState4.board[row][col] = a
        boardState4.board[row][col - 1] = b
        boardState4.board[row][col - 2] = 0
        boardState4.steps_list.append("L2" + str(row))
        boardState4.perm_inv = permutationInversion(boardState4.board)
        boardState4.heuristic_value = heuristicManhattan(boardState4.board) + linearConflict(boardState4.board)
        print("Two move left")
        printBoard(boardState4.board)

    ans = []
    ans.append(boardState1)
    ans.append(boardState2)
    ans.append(boardState3)
    ans.append(boardState4)
    return ans


# Get Successors for three moves
def getSuccessorforThreeMoves(state, row, col):
    print("In getSuccessorforThreeMoves")
    boardState1 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState2 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState3 = copy.deepcopy(BoardState(state, [],0,0,0))
    boardState4 = copy.deepcopy(BoardState(state, [],0,0,0))

    if (row + 3 <= 3):
        a = boardState1.board[row+1][col]
        b = boardState1.board[row + 2][col]
        c = boardState1.board[row + 3][col]
        boardState1.board[row][col] = a
        boardState1.board[row+1][col] = b
        boardState1.board[row+2][col] = c
        boardState1.board[row+3][col] = 0
        boardState1.steps_list.append("D3" + str(col))
        boardState1.perm_inv = permutationInversion(boardState1.board)
        boardState1.heuristic_value = heuristicManhattan(boardState1.board) + linearConflict(boardState1.board)
        print("Three move down")
        printBoard(boardState1.board)

    if (row - 3 >= 0):
        a = boardState2.board[row - 3][col]
        b = boardState2.board[row - 2][col]
        c = boardState2.board[row - 1][col]
        boardState2.board[row][col] = c
        boardState2.board[row - 1][col] = b
        boardState2.board[row - 2][col] = a
        boardState2.board[row - 3][col] = 0
        boardState2.steps_list.append("U3" + str(col))
        boardState2.perm_inv = permutationInversion(boardState2.board)
        boardState2.heuristic_value = heuristicManhattan(boardState2.board) + linearConflict(boardState2.board)
        print("Three move up")
        printBoard(boardState2.board)

    if (col + 3 <= 3):
        a = boardState3.board[row][col+1]
        b = boardState3.board[row][col+2]
        c = boardState3.board[row][col+3]
        boardState3.board[row][col] = a
        boardState3.board[row][col+1] = b
        boardState3.board[row][col+2] = c
        boardState3.board[row][col+3] = 0
        boardState3.steps_list.append("R3" + str(row))
        boardState3.perm_inv = permutationInversion(boardState3.board)
        boardState3.heuristic_value = heuristicManhattan(boardState3.board) + linearConflict(boardState3.board)
        print("Three move right")
        printBoard(boardState3.board)

    if (col - 3 >= 0):
        a = boardState4.board[row][col - 3]
        b = boardState4.board[row][col - 2]
        c = boardState4.board[row][col - 1]
        boardState4.board[row][col] = c
        boardState4.board[row][col - 1] = b
        boardState4.board[row][col - 2] = a
        boardState4.board[row][col - 3] = 0
        boardState4.steps_list.append("L3" + str(row))
        boardState4.perm_inv = permutationInversion(boardState4.board)
        boardState4.heuristic_value = heuristicManhattan(boardState4.board) + linearConflict(boardState4.board)
        print("Three move left")
        printBoard(boardState4.board)

    ans = []
    ans.append(boardState1)
    ans.append(boardState2)
    ans.append(boardState3)
    ans.append(boardState4)
    return ans


# Successor function to generate next states
def successor_function(board, row, col):
	import collections

	print("In successor func")
	successor_states = []
	successor_states1 = []
	successor_states2 = []
	successor_states3 = []

	successor_states1 = getSuccessorforOneMove(board,row,col)
	successor_states2 = getSuccessorforTwoMoves(board, row, col)
	successor_states3 = getSuccessorforThreeMoves(board, row, col)

	ans = []
	for i in range(len(successor_states1)):
		ans.append(successor_states1[i])

	for i in range(len(successor_states2)):
		ans.append(successor_states2[i])

	for i in range(len(successor_states3)):
		ans.append(successor_states3[i])

	d = collections.defaultdict(list)

	for x in ans:
		d[x.heu_man].append(x)
	return d

    #return ans





# Solve function for 15 puzzle problem
def solveAstar(board):
	import collections
	fringe = collections.defaultdict(list)
	visited = []
	greedy = 1
	obj = BoardState(board,[],0,0,0)
	min_heu = obj.heu_man
	fringe[min_heu] = obj
	init_perm = obj.perm_inv

	if init_perm%2 == 1:
		print("Go back")
	if init_perm > 40:
		greedy = 0.5

	while(len(fringe)):
		minimum = min(key for key in fringe.keys())
		get_elem = fringe[minimum]
		elem = get_elem.board
		steps_list = get_elem.steps_list
		cost = get_elem.cost
		p = get_elem.perm_inv
		if elem not in visited and p%2 == 0:
			row = getRowOfTile(0,elem)
			col = getColOfTile(0,elem)
			print("row: " + str(row))
			print("col: " + str(col))
			temp = successor_function(elem,row,col)
			for k,v in temp.items():
				new_steps_list = copy.copy(steps_list)
				new_steps_list.append(k)
				c = cost + 1
				obj = BoardState(v,new_steps_list,c,0,0)
				hm = obj.heu_man
				if hm==0:
					print("Goal Reached")
					print(v)
					print(" ".join(steps_list for steps_list in new_steps_list))
					return 0
				p = obj.perm_inv
				k = c*greedy + hm
				if p%2 == 0:
					fringe[k].append(obj)
		visited.append(elem)
	return "Fail"










if __name__ == '__main__':
	initial_board = initialState(arguments[1])
	print("Initial Board")
	solveAstar(initial_board)
