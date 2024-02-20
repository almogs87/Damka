import numpy as np
import csv

def update_board(player1,player2):
    board = np.empty((brd_size, brd_size)) * 0
    board = board.astype('int8')

    for idx in range(len(player1)):
        x, y = player1[idx]
        board[x, y] = 1
        x, y = player2[idx]
        board[x, y] = 2
    np.flip(board)

    return board
def read_file(filename):
    filename = open(filename)
    csvreader = csv.reader(filename)
    steps = []
    for row in csvreader:
        steps.append(row)
    steps = np.array(steps)
    return steps
def map_steps(player , loc):
    vacant1 = 99
    vacant2 = 99
    sign = int(not(player-1))*1 + int(not(2-player))*-1
    loc1 = loc + np.array([sign * 1, -1])
    loc2 = loc + np.array([sign * 1, 1])

    if (player == 1) and (loc[0]==7):
        print('player 1 cannot proceed from line 7')

    elif (player == 2) and (loc[0]==0):
        print('player 2 cannot proceed from line 0')

    else:
        if loc[1]<7: # X component isn't on left edge
            vacant2 = int(board[loc2[0],loc2[1]] == 0)

            if board[loc2[0],loc2[1]] > 0:
                print('player ' + str(player) + ' cannot move left to ' + str(loc2) + ' since there is already a brick of player' + str(board[loc2[0],loc2[1]]))
        if loc[1]>0: # X component isn't on right edge
            vacant1 = int(board[loc1[0], loc1[1]] == 0)
            if board[loc1[0],loc1[1]] > 0:
                print('player ' + str(player) + ' cannot move right to ' + str(loc1) + ' since there is already a brick of player' + str(board[loc1[0],loc1[1]]))


    print('optional player ' + str(player) + ' moves:  from ' + str(loc) + ' to ' + str(loc1) + ' or ' + str(loc2))
    steps_return = np.zeros((1,10),dtype='int8')
    steps_return[0, 0] = vacant1
    steps_return[0, 1:3] = loc
    steps_return[0, 3:5] = loc1
    steps_return[0, 5] = vacant2
    steps_return[0, 6:8] = loc
    steps_return[0, 8:10] = loc2

    steps_right = np.zeros((1,5),dtype='int8')
    steps_right[0, 0] = vacant1
    steps_right[0, 1:3] = loc
    steps_right[0, 3:5] = loc1
    steps_left = np.zeros((1,5),dtype='int8')
    steps_left[0, 0] = vacant2
    steps_left[0, 1:3] = loc
    steps_left[0, 3:5] = loc2


    return steps_right,steps_left
def map_capture(player,optional_steps):

    sign = int(not(player-1))*1 + int(not(2-player))*-1

    flag_capture = 0
    L=int(len(optional_steps)/2)
    steps_capture = np.zeros((2*L,5))

    for k in range(L):
        capture = 99
        vacant = optional_steps[k+L,0]
        y0 = optional_steps[k+L,1]
        x0 = optional_steps[k+L,2]
        y1 = optional_steps[k+L,3]
        x1 = optional_steps[k+L,4]

        x2 = x1 + 1
        y2 = y1 + sign
        if vacant==99 or vacant==1:
            capture = int(not((99-vacant)))*99
        else:
            IsSamePlayer = int(board[y0, x0] == board[y1, x1])
            if IsSamePlayer<1:
                Valid_right = int(0<=x2<8 and 0<=y2<8) # verify that X2,Y2 are within table limits
                capture = Valid_right

        steps_capture[k+L,0] = capture
        steps_capture[k+L,1] = y0
        steps_capture[k+L,2] = x0
        steps_capture[k+L,3] = y2
        steps_capture[k+L,4] = x2

        if flag_capture==0:
            flag_capture=int(capture==1)

    for k in range(L):
        capture = 99
        vacant = optional_steps[k,0]
        y0 = optional_steps[k,1]
        x0 = optional_steps[k,2]
        y1 = optional_steps[k,3]
        x1 = optional_steps[k,4]

        x2 = x1 - 1
        y2 = y1 + sign
        if vacant==99 or vacant==1:
            capture = int(not((99-vacant)))*99
        else:
            IsSamePlayer = int(board[y0, x0] == board[y1, x1])
            if IsSamePlayer<1:
                Valid_right = int(0<=x2<8 and 0<=y2<8) # verify that X2,Y2 are within table limits
                capture = Valid_right

        steps_capture[k,0] = capture
        steps_capture[k,1] = y0
        steps_capture[k,2] = x0
        steps_capture[k,3] = y2
        steps_capture[k,4] = x2

        if flag_capture==0:
            flag_capture=int(capture==1)

    return steps_capture, flag_capture

file = 'black.txt'

# with open('file', 'r') as f:
#     reader = csv.reader(f)
#     data = list(reader)
# data_array = np.array(data, dtype='unit8')

steps = read_file(file)
total_steps = len(steps)
step_count = 0
brd_size = 8


# for k in range(brd_size):
#     for j in range(brd_size):
#         odd=np.mod(k + j, 2)
#         if k<3&odd:
#             board_empty[k,j]=1
#             print('j is ' + str(j), ' and k is ' + str(k) + ' np.mod(j+k,2)=' + str(np.mod(k+j,2)) )
#         # if k>4&odd:
#         #     print('j is ' + str(j), ' and k is ' + str(k) + ' np.mod(j+k,2)=' + str(np.mod(k+j,2)) )
#         #     board_empty[j,k]=2
player1 = [[0, 1], [0, 3], [0, 5], [0, 7], [1, 0], [1, 2], [1, 4], [1, 6], [2, 1], [2, 3], [2, 5], [2, 7]]
player2 = [[3, 2], [5, 2], [5, 4], [5, 6], [6, 1], [6, 3], [6, 5], [6, 7], [7, 0], [7, 2], [7, 4], [7, 6]]
board = update_board(player1,player2)

while(step_count<total_steps):

    # =np.zeros((len(player1),10),dtype='int8')
    player1_right=np.zeros((len(player1),5),dtype='int8')
    player1_left=np.zeros((len(player1),5),dtype='int8')

    for k in range(len(player1)):
        player1_right[k,:],player1_left[k,:]=map_steps(1, player1[k])
    player1_steps=np.append(player1_right,player1_left,axis=0)

    player2_right=np.zeros((len(player1),5),dtype='int8')
    player2_left=np.zeros((len(player1),5),dtype='int8')

    for k in range(len(player1)):
        player2_right[k, :], player2_left[k, :]=map_steps(2, player2[k])
    player2_steps = np.append(player2_right, player2_left, axis=0)

    potential_captures, capture_exists=map_capture(1, player1_steps)
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