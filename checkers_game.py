import numpy as np
import csv


def read_file(filename):
    filename = open(filename)
    csvreader = csv.reader(filename)
    steps = []
    for row in csvreader:
        steps.append(row)
    steps = np.array(steps)
    return steps

def valid_steps(player , loc):
    loc1=np.array([-1,-1])
    loc2=np.array([-1,-1])
    sign = int(not(player-1))*1 + int(not(2-player))*-1
    if (player == 1) and (loc[1]==7):
        print('player 1 cannot proceed from line 7')
    elif (player == 2) and (loc[1]==0):
        print('player 2 cannot proceed from line 0')

    else:
        if loc[0]<7:
            loc2 = loc + np.array([1, sign*1])
            loc2_vacant = (board[loc2[1],loc2[0]] == 0)

            if board[loc2[1],loc2[0]] > 0:
                print('player ' + str(player) + ' cannot move left to ' + str(loc2) + ' since there is already a brick of player' + str(board[loc2[0],loc2[1]]))
        if loc[0]>0:
            loc1 = loc + np.array([-1, sign*1])
            loc1_vacant = (board[loc1[1], loc1[0]] == 0)
            if board[loc1[1],loc1[0]] > 0:
                print('player ' + str(player) + ' cannot move right to ' + str(loc1) + ' since there is already a brick of player' + str(board[loc1[0],loc1[1]]))


    print('optional player ' + str(player) + ' moves:  from ' + str(loc) + ' to ' + str(loc1) + ' or ' + str(loc2))

    return loc1,loc2



file = 'black.txt'

# with open('file', 'r') as f:
#     reader = csv.reader(f)
#     data = list(reader)
# data_array = np.array(data, dtype='unit8')

steps = read_file(file)
total_steps = len(steps)
step_count = 0
brd_size = 8
board = np.empty((brd_size,brd_size))*0
board = board.astype('int8')

# for k in range(brd_size):
#     for j in range(brd_size):
#         odd=np.mod(k + j, 2)
#         if k<3&odd:
#             board_empty[k,j]=1
#             print('j is ' + str(j), ' and k is ' + str(k) + ' np.mod(j+k,2)=' + str(np.mod(k+j,2)) )
#         # if k>4&odd:
#         #     print('j is ' + str(j), ' and k is ' + str(k) + ' np.mod(j+k,2)=' + str(np.mod(k+j,2)) )
#         #     board_empty[j,k]=2

player1 = [ [0,1], [0,3], [0,5], [0,7], [1,0], [1,2], [1,4], [1,6], [2,1], [2,3], [2,5], [2,7]]
player2 = [ [5,0], [5,2], [5,4], [5,6], [6,1], [6,3], [6,5], [6,7], [7,0], [7,2], [7,4], [7,6]]

for idx in range(len(player1)):
    x,y = player1[idx]
    board[x,y] = 1
    x,y = player2[idx]
    board[x,y] = 2

board
np.flip(board)

while(step_count<total_steps):
    next_step = np.array(steps[step_count], dtype='int8')
    x0=next_step[0]
    y0=next_step[1]
    x1=next_step[2]
    y1=next_step[3]
    step_count+=1
    board_flipped = np.flip(board)
    step_print = 'player ' + str(board[y0,x0]) + ' moves from: [' +str(x0) +',' + str(y0) + '] to [' +str(x1) +',' + str(y1) + ']'
    print('turn #' +str(step_count))
    print(step_print)