# Count of pieces in given row
def count_on_row(board, row):
    return sum(board[row] )

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] )

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]


def is_goal(board):
    return count_pieces(board) == N and \
           all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
           all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )



def print_board(board):
    if(type == "nrook"):
        ch = 'R'
    elif (type == 'nqueen'):
        ch = 'Q'
    x =''
    for i in range(len(board)):
        for j in range(len(board[i])):
            if [i,j]!=[Row,Col]:
                if(board[i][j] == 1):
                    x = x + ch + ' '
                    #print(ch)
                else:
                    x = x + '_' + ' '
                    #print("_")
            else:
                x = x + 'X' + ' '
                #print('X')
        if(len(x)> 0):
            print(x)
        x = ''
    #return "\n".join([ " ".join([ ch if col else "_" for col in row ]) for row in board])



def last_queens(row_checker, col_checker, diagonal_list):
    flag=True
    for r in range(0,N):
        if r not in row_checker:
            flag=False
            for col in range(0,N):
                if col not in col_checker:
                    if [r,col] not in diagonal_list:
                        flag= True
            if not flag:#Return as soon as a row is found where no Queen can be placed.
                return False
    return flag

def successors_rooks(board, neg_row, neg_col):
    row_list=[]
    col_list=[]
    answer=[]
    #Store positions where there is already a rook.
    for r in range(0, N) :
        for c in range(0,N):
            if board[r][c]==1:
                row_list.append(r)
                col_list.append(c)
    total_pieces = count_pieces(board)+1

    if total_pieces <= N:
        #Generate states with no two rooks on same row or column.
        for r in range(0, N) :
            for c in range(0,N):
                if r not in row_list and c not in col_list:
                    if [r,c]!=[neg_row,neg_col]:
                        new_state = add_piece(board, r, c)
                        if(new_state !=board):
                            answer.append(new_state)
    return answer



from collections import deque
def solve_for_rooks(initial_board, neg_row, neg_col):
    my_list={}
    my_list[0] = deque([initial_board])
    my_list[1]=[]
    while (my_list[0]):
        data=my_list[0].pop()
        if is_goal(data):
            return(data)
        if data not in my_list[1] :
            for s in successors_rooks(data, neg_row, neg_col):
                my_list[0].append(s)
            my_list[1].append(data)
    return False




def get_possible_diagonals(row, col):
    diagonal_list=[]
    r=row
    c=col
    while(r>0 and c>0):
        r-=1
        c-=1
        diagonal_list.append([r,c])
    r=row
    c=col
    while(r<N-1 and c<N-1):
        r+=1
        c+=1
        diagonal_list.append([r,c])
    r=row
    c=col
    while(r<N-1 and c>0):
        r+=1
        c-=1
        diagonal_list.append([r,c])
    r=row
    c=col
    while(r>0 and c<N-1):
        r-=1
        c+=1
        diagonal_list.append([r,c])
    return diagonal_list


import copy
def successors_queen(board):
    my_row_list=[]
    my_col_list=[]
    my_diagonal_list=[]
    answer=[]
    #Store positions where there is already a queen.
    for row in range(0,N):
        for col in range(0, N) :
            if board[row][col]==1:
                my_row_list.append(row)
                my_col_list.append(col)
                my_diagonal_list.extend(get_possible_diagonals(row, col))

    total_pieces=count_pieces(board)+1
    if total_pieces <= N:
        #Generate states with no two queens on same row or column or diagonal.
        for r in range(0,N):
            for c in range(0, N) :
                if r not in my_row_list and c not in my_col_list and [r,c] not in my_diagonal_list:
                    flag=True
                    new_state=add_piece(board, r, c)
                    if(new_state !=board):
                        if total_pieces>=N//2 :
                            r1=copy.copy(my_row_list) #Syntax of copy taken from https://docs.python.org/2/library/copy.html
                            r1.append(r)
                            c1=copy.copy(my_col_list)
                            c1.append(c)
                            d1=copy.copy(my_diagonal_list)
                            d1.extend(get_possible_diagonals(r, c))
                            flag= last_queens(r1, c1, d1)
                    if (flag):
                        answer.append(new_state)
    return answer



def solve_for_queen(initial_board):
    my_dict={}
    my_dict[0]=deque([initial_board])
    my_dict[1]=[]
    while (my_dict[0]):
        item=my_dict[0].pop()
        if is_goal(item):
            return(item)
        if item not in my_dict[1]:
            for s in successors_queen(item):
                my_dict[0].append(s)
            my_dict[1].append(item)
    return False




import sys
from time import time

N = int(sys.argv[2])
type = sys.argv[1]
Row = int(sys.argv[3])
Col = int(sys.argv[4])
#print("Type",type)
#print("N: ",N)
#print("Row: ",Row)
#print("Col: ",Col)
Row = Row - 1
Col = Col - 1

initial_board = [[0]*N for i in range(N)]

def Rook():
    #print ("NRook Problem")
    #print ("Initial State:")
    #print()
    #print_board(initial_board)
    #print()
    #print("Final State:")
    #print()
    start = time()
    solution_rooks = solve_for_rooks(initial_board, Row, Col)
    stop = time()
    print(stop - start)
    if solution_rooks:
        print_board(solution_rooks)
    else:
        print("No solution found for rooks.")

def Queen():
    #print("NQueen Problem")
    #print ("Initial State:")
    #print()
    #print_board(initial_board)
    #print("Final State:")
    #print()
    solution_queen = solve_for_queen(initial_board)
    if solution_queen:
        print_board(solution_queen)
    else:
        print("No solution found for queens.")


if(type == 'nrook'):
    Rook();
elif(type == 'nqueen'):
    Queen();
else:
    print("Invalid Input")