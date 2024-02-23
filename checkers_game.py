import numpy as np
import csv

def update_board(player1,player2, Print = True):
    board = np.empty((brd_size, brd_size)) * 0
    board = board.astype('int8')

    for idx in range(len(player1)):
        x, y = player1[idx]
        board[x, y] = 1
    for idx in range(len(player2)):
        x, y = player2[idx]
        board[x, y] = 2
    if Print==True:
        print(np.flip(board))

    return board
def read_file(filename):
    filename = open(filename)
    csvreader = csv.reader(filename)
    steps = []
    for row in csvreader:
        steps.append(row)
    steps = np.array(steps)
    return steps
def map_steps(player_num , CurrentPlayer):

    # right_moves=np.zeros((len(CurrentPlayer),5),dtype='int8')
    # left_moves=np.zeros((len(CurrentPlayer),5),dtype='int8')
    # for k in range(len(CurrentPlayer)):
    #     right_moves[k,:],left_moves[k,:]=map_steps(ply_idx+1, CurrentPlayer[k])
    # player_moves=np.append(right_moves,left_moves,axis=0)
    right_moves = np.zeros((len(CurrentPlayer), 5), dtype='int8')
    left_moves = np.zeros((len(CurrentPlayer), 5), dtype='int8')
    for k in range(len(CurrentPlayer)):
        loc = CurrentPlayer[k]
        vacant1 = 99
        vacant2 = 99
        sign = int(not(player_num-1))*1 + int(not(2-player_num))*-1
        loc1 = loc + np.array([sign * 1, -1])
        loc2 = loc + np.array([sign * 1, 1])

        if (player_num == 1) and (loc[0]==7):
            pass
        elif (player_num == 2) and (loc[0]==0):
            pass
        else:
            if loc[1]<7: # X component isn't on left edge
                vacant2 = int(board[loc2[0],loc2[1]] == 0)
                if board[loc2[0],loc2[1]] > 0:
                    pass
            if loc[1]>0: # X component isn't on right edge
                vacant1 = int(board[loc1[0], loc1[1]] == 0)
                if board[loc1[0],loc1[1]] > 0:
                    pass

        right_moves[k, 0] = vacant1
        right_moves[k, 1:3] = loc
        right_moves[k, 3:5] = loc1

        left_moves[k, 0] = vacant2
        left_moves[k, 1:3] = loc
        left_moves[k, 3:5] = loc2

    player_moves = np.append(right_moves, left_moves, axis=0)

    return player_moves
def map_capture(player,optional_steps):

    risked_bricks = []
    sign = int(not(player-1))*1 + int(not(2-player))*-1

    flag_capture = 0
    L=int(len(optional_steps))
    steps_capture = np.zeros((L,5))
    epsilon = 1e-2

    for k in range(L):
        capture = 99
        vacant = optional_steps[k,0]
        y0 = optional_steps[k,1]
        x0 = optional_steps[k,2]
        y1 = optional_steps[k,3]
        x1 = optional_steps[k,4]


        direction = np.sign(k+epsilon-(L/2))

        x2 = int(x1 + direction)
        y2 = y1 + sign
        ValidInBoard = int(0 <= x2 < 8 and 0 <= y2 < 8)  # verify that X2,Y2 are within table limits

        if vacant==99 or vacant==1:
            capture = int(not((99-vacant)))*99
        else:
            IsSamePlayer = int(board[y0, x0] == board[y1, x1])
            # check 2 prerequisites to enable capturing:
            # 1. is it opponent brick that were skipping during capture?
            # 2. is the new capture coordinates are within board bounds or outside?
            if (IsSamePlayer==0) and (ValidInBoard==1):
                # determine if potential capture slot is free and assign it to capture variable
                Vacant4Capture= int(board[y2, x2]==0)
                capture = Vacant4Capture

        steps_capture[k,0] = capture
        steps_capture[k,1] = y0
        steps_capture[k,2] = x0
        steps_capture[k,3] = y2
        steps_capture[k,4] = x2

        if flag_capture==0:
            flag_capture=int(capture==1)
        if capture==1:
            risked_bricks.append([y0, x0])

    return steps_capture, flag_capture, risked_bricks

def CheckLegalMove(player_poten_steps,next_step):
    x0 = next_step[0]
    y0 = next_step[1]
    x1 = next_step[2]
    y1 = next_step[3]
    Valid_Step = np.logical_not(player_poten_steps[:, 0] == 1)
    Valid_Step = np.reshape(Valid_Step, (Valid_Step.shape[0], 1))
    step_diff = player_poten_steps[:, 1:] - np.array([y0, x0, y1, x1])
    Valid_Step = np.dot(np.abs(step_diff), np.ones((4, 1))) + Valid_Step
    idx, type = np.where(Valid_Step == 0)

    return len(idx)

file = 'illegal_move.txt'

steps = read_file(file)
total_steps = len(steps)
move_count = 0
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
player2 = [[5, 0], [5, 2], [5, 4], [5, 6], [6, 1], [6, 3], [6, 5], [6, 7], [7, 0], [7, 2], [7, 4], [7, 6]]

turns = [1]*len(steps)
turns[1::2] = [2 for x in turns[1::2]]
while(move_count<total_steps):
    board = update_board(player1, player2, Print=True)
    ply_idx=turns[move_count]
    last_move = int(not(move_count+1-total_steps))
    if ply_idx == 2:
        CurrentPlayer = player2
        Opponent = player1
    else:
        CurrentPlayer = player1
        Opponent = player2

    player_moves = map_steps(ply_idx, CurrentPlayer)
    next_step = np.array(steps[move_count], dtype='int8')
    x0=next_step[0]
    y0=next_step[1]
    x1=next_step[2]
    y1=next_step[3]


    potential_captures, capture_exists,risked_bricks=map_capture(ply_idx, player_moves)
    CaptureAccomplished= CheckLegalMove(potential_captures, next_step)
    LegalMove= CheckLegalMove(player_moves, next_step)

    if (capture_exists==0) and LegalMove==1:
        idx = CurrentPlayer.index([y0, x0])
        CurrentPlayer[idx] = [y1, x1]
        print('player ' + str(board[y0, x0]) + ' moves from: [' + str(x0) + ',' + str(y0) + '] to [' + str(
            x1) + ',' + str(y1) + ']')

        # check if any of optional captures were done

    elif (capture_exists==0) and LegalMove==0:
        ilegal_msg= 'line ' + str(move_count+1) + ' illegal move: ' + str(x0) +',' + str(y0) +  ',' + str(x1) +',' + str(y1)
        print('ilegel move from: [' + str(x0) + ',' + str(y0) + '] to [' + str(x1) + ',' + str(y1) + ']')
        print('game stopped due to ilegal move')
        move_count=total_steps

    elif (capture_exists==1) and CaptureAccomplished==1:
        while(CaptureAccomplished):
            y_cap= int(np.mean((y0,y1)))
            x_cap= int(np.mean((x0,x1)))
            Opponent.remove([y_cap,x_cap])
            print('opponent brick was captured from [' + str(x_cap) + ',' + str(y_cap) + ']' )
            idx = CurrentPlayer.index([y0, x0])
            CurrentPlayer[idx] = [y1, x1]
            print('player ' + str(board[y0, x0]) + ' moves from: [' + str(x0) + ',' + str(y0) + '] to [' + str(
                x1) + ',' + str(y1) + ']')
            CaptureAccomplished = CaptureAccomplished*int(not(last_move))
            if last_move==0:
                next_step = np.array(steps[move_count+1], dtype='int8')

                brick_moves = map_steps(ply_idx, [[y1, x1]])
                brick_captures, brick_cap_exists, risked_bricks = map_capture(ply_idx, brick_moves)
                CaptureAccomplished = CheckLegalMove(brick_captures, next_step)
                if CaptureAccomplished:
                    turns_new = [turns[move_count+1] ]*(len(steps)-move_count-1)
                    turns_new[0::2] = [ ply_idx for x in turns_new[0::2] ]
                    turns[move_count+1:]=turns_new
                    move_count = move_count + 1
                    print('turn #' + str(move_count) + ' multi-capture move!' )
                    board = update_board(player1, player2, Print=True)


                x0 = next_step[0]
                y0 = next_step[1]
                x1 = next_step[2]
                y1 = next_step[3]

    #build compare

    move_count+=1
    board_flipped = np.flip(board)
    print('turn #' +str(move_count) + ' completed')

player1_bricks = len(player1)
player2_bricks = len(player2)
win_idx=np.sign(player1_bricks-player2_bricks)+1
win_L=['second','tie','first']
if(np.min([player1_bricks,player2_bricks])==0):
    print(win_L[win_idx])
elif LegalMove==0:
    print(ilegal_msg)
else:
    print('incomplete game')
