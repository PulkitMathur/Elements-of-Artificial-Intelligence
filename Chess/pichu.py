#The heuristic function used in the code is the same taught in class where a value is assigned to each piece
# At each level we check the difference of number of same kind of pieces multiplied with their weight value
#and try to reach at a level that has max difference between the two teams. the weight taken is
# K=200, Q=9, R=5, B=3,N=3,P=1

import sys
import time
import copy

arguments = sys.argv
import copy
start = False


moveP1 = []
moveP2 = []
def moveParakeet(board,type,row,col):
   moveP1[:] = []
   moveP2[:] = []
   if(type == 'P'):
      #capital Parakeet
      if(row == 7):
         b2 = copy.deepcopy(board)
         b2[row][col] = 'Q'
         moveP1.append(b2)
         return moveP1
         #print("b2")
         #printInitialBoard(b2)
      if((row+1) <8):
         if(board[row+1][col] == '.'):
            b3 = copy.deepcopy(board)
            b3[row][col] = '.'
            b3[row+1][col] = 'P'
            moveP1.append(b3)
         if(col + 1 < 8):
            if(board[row+1][col+1] != '.'):
               x = board[row+1][col+1]
               if(x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k' or x == 'p'):
                  b4 = copy.deepcopy(board)
                  b4[row][col] = '.'
                  b4[row+1][col+1] = 'P'
                  moveP1.append(b4)
         if(col - 1 >= 0):
            if(board[row+1][col-1] != '.'):
               x = board[row + 1][col - 1]
               if (x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k' or x == 'p'):
                  b5 = copy.deepcopy(board)
                  b5[row][col] = '.'
                  b5[row + 1][col - 1] = 'P'
                  moveP1.append(b5)
      #print("For capital P")
      #print()
      #print()
      #for t in moveP1:
         #printInitialBoard(t)
      #print()
      #print()
      return moveP1


   elif(type == 'p'):
      if(row == 0):
         b6 = copy.deepcopy(board)
         b6[row][col] = 'q'
         moveP2.append(b6)
         #print("b6")
         #printInitialBoard(b6)
         return moveP2
      if((row - 1) >= 0):
         if (board[row - 1][col] == '.'):
            b7 = copy.deepcopy(board)
            b7[row][col] = '.'
            b7[row - 1][col] = 'p'
            moveP2.append(b7)
         if (col - 1 >= 0):
            if (board[row - 1][col - 1] != '.'):
               y = board[row - 1][col - 1]
               if(y == 'P' or y == 'R' or y == 'N' or y == 'B' or y == 'Q' or y == 'K'):
                  b8 = copy.deepcopy(board)
                  b8[row][col] = '.'
                  b8[row - 1][col - 1] = 'p'
                  moveP2.append(b8)
         if (col + 1 < 8):
            if (board[row - 1][col + 1] != '.'):
               y = board[row - 1][col + 1]
               if (y == 'P' or y == 'R' or y == 'N' or y == 'B' or y == 'Q' or y == 'K'):
                  b9 = copy.deepcopy(board)
                  b9[row][col] = '.'
                  b9[row - 1][col + 1] = 'p'
                  moveP2.append(b9)

      #print("For small p")
      #print()
      #print()
      #for t in moveP2:
         #printInitialBoard(t)
      #print()
      #print()
      return moveP2



moveR1 = []
moveR2 = []
def moveRobin(board,type,row,col):
   x = row
   y = col
   t1 = copy.deepcopy(board)
   if type == 'r':
      moveR1 = []

      for t in range(col + 1, 8):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][t] == '.'):
            t1[row][col] = '.'
            t1[row][t] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][t] == 'P' or t1[row][t] == 'R' or t1[row][t] == 'N' or t1[row][t] == 'B' or t1[row][
            t] == 'Q' or t1[row][t] == 'K'):
            t1[row][col] = '.'
            t1[row][t] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for t in range(col - 1, -1, -1):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][t] == '.'):
            t1[row][col] = '.'
            t1[row][t] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][t] == 'P' or t1[row][t] == 'R' or t1[row][t] == 'N' or t1[row][t] == 'B' or t1[row][
            t] == 'Q' or t1[row][t] == 'K'):
            t1[row][col] = '.'
            t1[row][t] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for m in range(row - 1, -1, -1):
         if (t1[m][col] == '.'):
            t1[row][col] = '.'
            t1[m][col] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[m][col] == 'P' or t1[m][col] == 'R' or t1[m][col] == 'N' or t1[m][col] == 'B' or t1[m][
            col] == 'Q' or t1[m][col] == 'K'):
            t1[row][col] = '.'
            t1[m][col] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for m in range(row + 1, 8):
         if (t1[m][col] == '.'):
            t1[row][col] = '.'
            t1[m][col] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[m][col] == 'P' or t1[m][col] == 'R' or t1[m][col] == 'N' or t1[m][col] == 'B' or t1[m][
            col] == 'Q' or t1[m][col] == 'K'):
            t1[row][col] = '.'
            t1[m][col] = type
            moveR1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break
      # for s in moveR1:
      #  print("\n\n")
      #  printInitialBoard(s)
      #  print("\n\n")
      return moveR1

   if type == 'R':
      moveR2 = []

      for u in range(col + 1, 8):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][u] == '.'):
            t1[row][col] = '.'
            t1[row][u] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][u] == 'p' or t1[row][u] == 'r' or t1[row][u] == 'n' or t1[row][u] == 'b' or t1[row][
            u] == 'Q' or t1[row][u] == 'K'):
            t1[row][col] = '.'
            t1[row][u] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for u in range(col - 1, -1, -1):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][u] == '.'):
            t1[row][col] = '.'
            t1[row][u] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][u] == 'p' or t1[row][u] == 'r' or t1[row][u] == 'n' or t1[row][u] == 'b' or t1[row][

            u] == 'Q' or t1[row][u] == 'K'):
            t1[row][col] = '.'
            t1[row][u] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for v in range(row - 1, -1, -1):
         if (t1[v][col] == '.'):
            t1[row][col] = '.'
            t1[v][col] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[v][col] == 'p' or t1[v][col] == 'r' or t1[v][col] == 'n' or t1[v][col] == 'b' or t1[v][
            col] == 'q' or t1[v][col] == 'k'):
            t1[row][col] = '.'
            t1[v][col] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for v in range(row + 1, 8):
         if (t1[v][col] == '.'):
            t1[row][col] = '.'
            t1[v][col] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[v][col] == 'p' or t1[v][col] == 'r' or t1[v][col] == 'n' or t1[v][col] == 'b' or t1[v][
            col] == 'q' or t1[v][col] == 'k'):
            t1[row][col] = '.'
            t1[v][col] = type
            moveR2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break
      # for s in moveR2:
      #  print("\n\n")
      #  printInitialBoard(s)
      #  print("\n\n")
      return moveR2

moves1 = []
moves2 = []
def moveBlueJay(board,type,row,col):
   x = row
   y = col
   if type == 'b':
      moves1 = []
      t1 = copy.deepcopy(board)
      while (x >= 1 and y >= 1):
         x -= 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x >= 1 and y < 7):
         x -= 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y >= 1):
         x += 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y < 7):
         x += 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves1.append(t1)
            break
         else:
            break
      # for s in moves1:
      #  print("\n\n")
      #  printInitialBoard(s)
      #  print("\n\n")
      return moves1

   elif type == 'B':
      moves2 = []
      t1 = copy.deepcopy(board)
      while (x >= 1 and y >= 1):
         x -= 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x >= 1 and y < 7):
         x -= 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y >= 1):
         x += 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y < 7):
         x += 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            moves2.append(t1)
            break
         else:
            break
      # for n in moves2:
      #  print("\n\n")
      #  printInitialBoard(n)
      #  print("\n\n")
      return moves2


moveq1 = []
moveq2 = []
def moveQueztal(board,type,row,col):
   x = row
   y = col
   if type == 'q':
      movesq1 = []
      t1 = copy.deepcopy(board)
      while (x >= 1 and y >= 1):
         x -= 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x >= 1 and y < 7):
         x -= 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y >= 1):
         x += 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y < 7):
         x += 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'P' or t1[x][y] == 'R' or t1[x][y] == 'N' or t1[x][y] == 'B' or t1[x][y] == 'Q' or t1[x][
            y] == 'K'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break
      for t in range(col + 1, 8):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][t] == '.'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][t] == 'P' or t1[row][t] == 'R' or t1[row][t] == 'N' or t1[row][t] == 'B' or t1[row][
            t] == 'Q' or t1[row][t] == 'K'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for t in range(col - 1, -1, -1):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][t] == '.'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][t] == 'P' or t1[row][t] == 'R' or t1[row][t] == 'N' or t1[row][t] == 'B' or t1[row][
            t] == 'Q' or t1[row][t] == 'K'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for m in range(row - 1, -1, -1):
         if (t1[m][col] == '.'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[m][col] == 'P' or t1[m][col] == 'R' or t1[m][col] == 'N' or t1[m][col] == 'B' or t1[m][
            col] == 'Q' or t1[m][col] == 'K'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for m in range(row + 1, 8):
         if (t1[m][col] == '.'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[m][col] == 'P' or t1[m][col] == 'R' or t1[m][col] == 'N' or t1[m][col] == 'B' or t1[m][
            col] == 'Q' or t1[m][col] == 'K'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq1.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

         # for s in movesq1:
         # print("\n\n")
         # printInitialBoard(s)
         # print("\n\n")
      return movesq1

   if type == 'Q':
      movesq2 = []
      t1 = copy.deepcopy(board)
      while (x >= 1 and y >= 1):
         x -= 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x >= 1 and y < 7):
         x -= 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y >= 1):
         x += 1
         y -= 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      x = row
      y = col
      t1 = copy.deepcopy(board)
      while (x < 7 and y < 7):
         x += 1
         y += 1
         if t1[x][y] == '.':
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[x][y] == 'p' or t1[x][y] == 'r' or t1[x][y] == 'n' or t1[x][y] == 'b' or t1[x][y] == 'q' or t1[x][
            y] == 'k'):
            t1[row][col] = '.'
            t1[x][y] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break
      for t in range(col + 1, 8):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][t] == '.'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][t] == 'p' or t1[row][t] == 'r' or t1[row][t] == 'n' or t1[row][t] == 'b' or t1[row][
            t] == 'q' or t1[row][t] == 'k'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for t in range(col - 1, -1, -1):
         # if (x >= 0 and x < 8 and y >= 0 and y < 8):
         if (t1[row][t] == '.'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)

         elif (t1[row][t] == 'p' or t1[row][t] == 'r' or t1[row][t] == 'n' or t1[row][t] == 'b' or t1[row][
            t] == 'q' or t1[row][t] == 'k'):
            t1[row][col] = '.'
            t1[row][t] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for m in range(row - 1, -1, -1):
         if (t1[m][col] == '.'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[m][col] == 'p' or t1[m][col] == 'r' or t1[m][col] == 'n' or t1[m][col] == 'b' or t1[m][
            col] == 'q' or t1[m][col] == 'k'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      for m in range(row + 1, 8):
         if (t1[m][col] == '.'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
         elif (t1[m][col] == 'p' or t1[m][col] == 'r' or t1[m][col] == 'n' or t1[m][col] == 'b' or t1[m][
            col] == 'q' or t1[m][col] == 'k'):
            t1[row][col] = '.'
            t1[m][col] = type
            movesq2.append(t1)
            t1 = copy.deepcopy(board)
            break
         else:
            break

      # for s in movesq2:
      #  print("\n\n")
      #  printInitialBoard(s)
      #  print("\n\n")
      return movesq2
def moveKingfisher(board,type,row,col):
   moves = []
   if((col+1) < 8):
      if(board[row][col+1] == '.'):
         t1 = copy.deepcopy(board)
         t1[row][col] = '.'
         t1[row][col+1] = type
         moves.append(t1)
      if(type == 'K'):
         if (board[row][col + 1] == 'p' or board[row][col + 1] == 'r' or board[row][col + 1] == 'n'
             or board[row][col + 1] == 'b' or board[row][col + 1] == 'q' or board[row][col + 1] == 'k'):
            t2 = copy.deepcopy(board)
            t2[row][col] = '.'
            t2[row][col + 1] = 'K'
            moves.append(t2)
      elif (type == 'k'):
         if (board[row][col + 1] == 'P' or board[row][col + 1] == 'R' or board[row][col + 1] == 'N'
             or board[row][col + 1] == 'B' or board[row][col + 1] == 'Q' or board[row][col + 1] == 'K'):
            t3 = copy.deepcopy(board)
            t3[row][col] = '.'
            t3[row][col + 1] = 'k'
            moves.append(t3)
   if((col - 1) > 0):
      if (board[row][col - 1] == '.'):
         t4 = copy.deepcopy(board)
         t4[row][col] = '.'
         t4[row][col - 1] = type
         moves.append(t4)
      if (type == 'K'):
         if (board[row][col - 1] == 'p' or board[row][col - 1] == 'r' or board[row][col - 1] == 'n'
             or board[row][col - 1] == 'b' or board[row][col - 1] == 'q' or board[row][col - 1] == 'k'):
            t5 = copy.deepcopy(board)
            t5[row][col] = '.'
            t5[row][col - 1] = 'K'
            moves.append(t5)
      elif (type == 'k'):
         if (board[row][col - 1] == 'P' or board[row][col - 1] == 'R' or board[row][col - 1] == 'N'
             or board[row][col - 1] == 'B' or board[row][col - 1] == 'Q' or board[row][col - 1] == 'K'):
            t6 = copy.deepcopy(board)
            t6[row][col] = '.'
            t6[row][col - 1] = 'k'
            moves.append(t6)

   if((row - 1) > 0):
      if (board[row - 1][col] == '.'):
         t7 = copy.deepcopy(board)
         t7[row][col] = '.'
         t7[row-1][col] = type
         moves.append(t7)
      if (type == 'K'):
         if (board[row - 1][col] == 'p' or board[row - 1][col] == 'r' or board[row - 1][col] == 'n'
             or board[row - 1][col] == 'b' or board[row - 1][col] == 'q' or board[row - 1][col] == 'k'):
            t8 = copy.deepcopy(board)
            t8[row][col] = '.'
            t8[row-1][col] = 'K'
            moves.append(t8)
      elif (type == 'k'):
         if (board[row - 1][col] == 'P' or board[row - 1][col] == 'R' or board[row - 1][col] == 'N'
             or board[row - 1][col] == 'B' or board[row - 1][col] == 'Q' or board[row - 1][col] == 'K'):
            t9 = copy.deepcopy(board)
            t9[row][col] = '.'
            t9[row-1][col] = 'k'
            moves.append(t9)


   if((row+1) < 8):
      if (board[row + 1][col] == '.'):
         t10 = copy.deepcopy(board)
         t10[row][col] = '.'
         t10[row + 1][col] = type
         moves.append(t10)
      if (type == 'K'):
         if (board[row + 1][col] == 'p' or board[row + 1][col] == 'r' or board[row + 1][col] == 'n'
             or board[row + 1][col] == 'b' or board[row + 1][col] == 'q' or board[row + 1][col] == 'k'):
            t11 = copy.deepcopy(board)
            t11[row][col] = '.'
            t11[row + 1][col] = 'K'
            moves.append(t11)
      elif (type == 'k'):
         if (board[row + 1][col] == 'P' or board[row + 1][col] == 'R' or board[row + 1][col] == 'N'
             or board[row + 1][col] == 'B' or board[row + 1][col] == 'Q' or board[row + 1][col] == 'K'):
            t12 = copy.deepcopy(board)
            t12[row][col] = '.'
            t12[row+1][col] = 'k'
            moves.append(t12)

   return moves


movesN1 = []
movesN2 = []
def moveNightwalk(board,type,row,col):
   movesN1[:] = []
   movesN2[:] = []
   if( (row - 2) >= 0 and (col + 1) < 8):
      if(board[row-2][col+1] == '.'):
         t1 = copy.deepcopy(board)
         t1[row][col] = '.'
         t1[row-2][col+1] = type
         if(type == 'N'):
            movesN1.append(t1)
         else:
            movesN2.append(t1)
      elif(type == 'N'):
         x = board[row-2][col+1]
         if(x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t2 = copy.deepcopy(board)
            t2[row][col] = '.'
            t2[row - 2][col + 1] = type
            movesN1.append(t2)
      elif(type == 'n'):
         x = board[row - 2][col + 1]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t3 = copy.deepcopy(board)
            t3[row][col] = '.'
            t3[row - 2][col + 1] = type
            movesN2.append(t3)

   if ((row - 2) >= 0 and (col - 1) > 0):
      if (board[row - 2][col - 1] == '.'):
         t4 = copy.deepcopy(board)
         t4[row][col] = '.'
         t4[row - 2][col - 1] = type
         if (type == 'N'):
            movesN1.append(t4)
         else:
            movesN2.append(t4)
      elif (type == 'N'):
         x = board[row - 2][col - 1]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t5 = copy.deepcopy(board)
            t5[row][col] = '.'
            t5[row - 2][col - 1] = type
            movesN1.append(t5)
      elif (type == 'n'):
         x = board[row - 2][col - 1]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t6 = copy.deepcopy(board)
            t6[row][col] = '.'
            t6[row - 2][col - 1] = type
            movesN2.append(t6)

   if ((row - 1) >= 0 and (col + 2) < 8):
      if (board[row - 1][col + 2] == '.'):
         t7  = copy.deepcopy(board)
         t7[row][col] = '.'
         t7[row - 2][col + 2] = type
         if (type == 'N'):
            movesN1.append(t7)
         else:
            movesN2.append(t7)
      elif (type == 'N'):
         x = board[row - 1][col + 2]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t8 = copy.deepcopy(board)
            t8[row][col] = '.'
            t8[row - 1][col + 2] = type
            movesN1.append(t8)
      elif (type == 'n'):
         x = board[row - 1][col + 2]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t9 = copy.deepcopy(board)
            t9[row][col] = '.'
            t9[row - 1][col + 2] = type
            movesN2.append(t9)

   if ((row - 1) >= 0 and (col - 2) > 0):
      if (board[row - 1][col - 2] == '.'):
         t10  = copy.deepcopy(board)
         t10[row][col] = '.'
         t10[row - 1][col - 2] = type
         if(type == 'N'):
            movesN1.append(t10)
         else:
            movesN2.append(t10)
      elif (type == 'N'):
         x = board[row - 1][col - 2]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t11 = copy.deepcopy(board)
            t11[row][col] = '.'
            t11[row - 1][col - 2] = type
            movesN1.append(t11)
      elif (type == 'n'):
         x = board[row - 1][col - 2]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t12 = copy.deepcopy(board)
            t12[row][col] = '.'
            t12[row - 1][col - 2] = type
            movesN2.append(t12)

   if ((row + 2) < 8 and (col + 1) < 8):
      if (board[row + 2][col + 1] == '.'):
         t13  = copy.deepcopy(board)
         t13[row][col] = '.'
         t13[row + 2][col + 1] = type
         if(type == 'N'):
            movesN1.append(t13)
         else:
            movesN2.append(t13)
      elif (type == 'N'):
         x = board[row + 2][col + 1]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t14 = copy.deepcopy(board)
            t14[row][col] = '.'
            t14[row + 2][col + 1] = type
            movesN1.append(t14)
      elif (type == 'n'):
         x = board[row + 2][col + 1]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t15 = copy.deepcopy(board)
            t15[row][col] = '.'
            t15[row + 2][col + 1] = type
            movesN2.append(t15)

   if ((row + 2) < 8 and (col - 1) >= 0):
      if (board[row + 2][col - 1] == '.'):
         t16  = copy.deepcopy(board)
         t16[row][col] = '.'
         t16[row + 2][col - 1] = type
         if(type == 'N'):
            movesN1.append(t16)
         else:
            movesN2.append(t16)
      elif (type == 'N'):
         x = board[row + 2][col - 1]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t17 = copy.deepcopy(board)
            t17[row][col] = '.'
            t17[row + 2][col - 1] = type
            movesN1.append(t17)
      elif (type == 'n'):
         x = board[row + 2][col - 1]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t18 = copy.deepcopy(board)
            t18[row][col] = '.'
            t18[row + 2][col - 1] = type
            movesN2.append(t18)

   if ((row + 1) < 8 and (col + 2) < 8):
      if (board[row + 1][col + 2] == '.'):
         t19  = copy.deepcopy(board)
         t19[row][col] = '.'
         t19[row + 1][col + 2] = type
         if(type == 'N'):
            movesN1.append(t19)
         else:
            movesN2.append(t19)
      elif (type == 'N'):
         x = board[row + 1][col + 2]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t20 = copy.deepcopy(board)
            t20[row][col] = '.'
            t20[row + 1][col + 2] = type
            movesN1.append(t20)
      elif (type == 'n'):
         x = board[row + 1][col + 2]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t21 = copy.deepcopy(board)
            t21[row][col] = '.'
            t21[row + 1][col + 2] = type
            movesN2.append(t21)

   if ((row + 1) < 8 and (col - 2) >= 0):
      if (board[row + 1][col - 2] == '.'):
         t22  = copy.deepcopy(board)
         t22[row][col] = '.'
         t22[row + 1][col - 2] = type
         if(type == 'N'):
            movesN1.append(t22)
         else:
            movesN2.append(t22)
      elif (type == 'N'):
         x = board[row + 1][col - 2]
         if (x == 'p' or x == 'r' or x == 'n' or x == 'b' or x == 'q' or x == 'k'):
            t23 = copy.deepcopy(board)
            t23[row][col] = '.'
            t23[row + 1][col - 2] = type
            movesN1.append(t23)
      elif (type == 'n'):
         x = board[row + 1][col - 2]
         if (x == 'P' or x == 'R' or x == 'N' or x == 'B' or x == 'Q' or x == 'K'):
            t24 = copy.deepcopy(board)
            t24[row][col] = '.'
            t24[row + 1][col - 2] = type
            movesN2.append(t24)

   if(type == 'N'):
      #print("N1")
      #print()
      #for k in movesN1:
         #printInitialBoard(k)
         #print()
         #print()
      return  movesN1
   #print("N2")
   #print()
   #for k in movesN1:
      #printInitialBoard(k)
      #print()
      #print()
   return movesN2

def getSuccessors(board,startPlayer):
   #print("Board:")
   #print(board)
   succ = []
   if(startPlayer == 'w'):
      for i in range(8):
         for j in range(8):
            if (board[i][j] == 'P'):
               a = moveParakeet(board, board[i][j], i, j)
               if a is not None:
                  for k in a:
                     succ.append(k)
            elif (board[i][j] == 'R'):
               b = moveRobin(board, board[i][j], i, j)
               if b is not None:
                  for k in b:
                     succ.append(k)
            elif (board[i][j] == 'B'):
               c = moveBlueJay(board, board[i][j], i, j)
               if c is not None:
                  for k in c:
                     succ.append(k)
            elif (board[i][j] == 'Q'):
               d = moveQueztal(board, board[i][j], i, j)
               if d is not None:
                  for k in d:
                     succ.append(k)
            elif (board[i][j] == 'K'):
               e = moveKingfisher(board, board[i][j], i, j)
               if e is not None:
                  for k in e:
                     succ.append(k)
            elif (board[i][j] == 'N'):
               f = moveNightwalk(board, board[i][j], i, j)
               if f is not None:
                  for k in f:
                     succ.append(k)
   elif (startPlayer == 'b'):
      for i in range(8):
         for j in range(8):
            if (board[i][j] == 'p'):
               a = moveParakeet(board, board[i][j], i, j)
               if a is not None:
                  for k in a:
                     succ.append(k)
            elif (board[i][j] == 'r'):
               b = moveRobin(board, board[i][j], i, j)
               if b is not None:
                  for k in b:
                     succ.append(k)
            elif (board[i][j] == 'b'):
               c = moveBlueJay(board, board[i][j], i, j)
               if c is not None:
                  for k in c:
                     succ.append(k)
            elif (board[i][j] == 'q'):
               d = moveQueztal(board, board[i][j], i, j)
               if d is not None:
                  for k in d:
                     succ.append(k)
            elif (board[i][j] == 'k'):
               e = moveKingfisher(board, board[i][j], i, j)
               if e is not None:
                  for k in e:
                     succ.append(k)
            elif (board[i][j] == 'n'):
               f = moveNightwalk(board, board[i][j], i, j)
               if f is not None:
                  for k in f:
                     succ.append(k)
   return succ


def printInitialBoard(board):
   for i in range(8):
      for j in range(8):
         print(board[i][j],end="  ")
      print()


#returns a list of list
def getBoard(status):
   board = [[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8,[0]*8]

   a = status[0:8]
   b = status[8:16]
   c = status[16:24]
   d = status[24:32]
   e = status[32:40]
   f = status[40:48]
   g = status[48:56]
   h = status[56:64]

   t=0
   for i in a:
      board[0][t]=i
      t+=1

   t = 0
   for i in b:
      board[1][t] = i
      t += 1

   t = 0
   for i in c:
      board[2][t] = i
      t += 1

   t = 0
   for i in d:
      board[3][t] = i
      t += 1


   t = 0
   for i in e:
      board[4][t] = i
      t += 1


   t = 0
   for i in f:
      board[5][t] = i
      t += 1

   t = 0
   for i in g:
      board[6][t] = i
      t += 1

   t = 0
   for i in h:
      board[7][t] = i
      t += 1
   return board
countpieces={}
heuristic_dic={}
def heuristic(turn_capital,succ):
   for arr in succ:
      countpieces_p =0
      countpieces_P = 0
      countpieces_r = 0
      countpieces_R = 0
      countpieces_b = 0
      countpieces_B = 0
      countpieces_n = 0
      countpieces_N = 0
      countpieces_k = 0
      countpieces_K = 0
      countpieces_q = 0
      countpieces_Q = 0
      heuristic_value=0
      for i in range(0,8):
         for j in range(0,8):

            if arr[i][j]=='p':
               countpieces_p+=1
            elif arr[i][j]=='P':
               countpieces_P+=1
            elif arr[i][j]=='r':
               countpieces_r+=1
            elif arr[i][j]=='R':
               countpieces_R+=1
            elif arr[i][j]=='b':
               countpieces_b+=1
            elif arr[i][j]=='B':
               countpieces_B+=1
            elif arr[i][j] == 'n':
               countpieces_n += 1
            elif arr[i][j] == 'N':
               countpieces_N += 1
            elif arr[i][j] == 'k':
               countpieces_k += 1
            elif arr[i][j] == 'K':
               countpieces_K += 1
            elif arr[i][j] == 'q':
               countpieces_q += 1
            elif arr[i][j] == 'Q':
               countpieces_Q += 1
      heuristic_value = 200 * (countpieces_K - countpieces_k) + 9 * (countpieces_Q - countpieces_q) + 5 * (countpieces_R - countpieces_r) + 3 * (countpieces_B - countpieces_b) + 3 * (countpieces_N - countpieces_n) + 1 * (countpieces_P - countpieces_p)
      if turn_capital==True:
         arr.append(heuristic_value)
      else:
         arr.append(-1*heuristic_value)

   return succ



def playPichku(startPlayer,board,time):
   objList = []
   if(startPlayer == 'w'):
      obj0 = Node(board,heuristic(True,board),0,[],None)
      temp = getSuccessors(board,'w')
      for s in temp:
         obj = Node(s,heuristic(True,s),1,[],obj0)
         obj0.mySucc.append(obj)
      objList.append(obj0)

   elif(startPlayer == 'b'):
      h = 1






class Node(object):
   def __init__(self, board,heu,level,mySucc,parent):
      self.board = board
      self.heu = heu
      self.level = level
      self.mySucc = mySucc
      self.parent = parent



if __name__ == '__main__':
   player = arguments[1]
   inputBoardString = arguments[2]
   time = arguments[3]
   #print("Player 1: ")
   #print(player1)
   #print("Player 2: ")
   #print(player2)
   if(inputBoardString ==
	      "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"):
	   start = True
   board = getBoard(inputBoardString)
   #print("Initial Board")
   #printInitialBoard(board)
   print("Thinking! Please wait...")
   print("New board:")
   playPichku(player,board,time)