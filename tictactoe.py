"""
Tic Tac Toe Player
"""

import math
import copy
import json

X = "X"
O = "O"
EMPTY = None
state_map = dict()

def flatten(t):
    return [item for sublist in t for item in sublist]

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    number_of_x = 0
    number_of_o = 0
    for row in board:
        for cell in row:
            if cell == X:
                number_of_x+=1
            elif cell == O:
                number_of_o+=1
    if number_of_o>=number_of_x:
        return X
    else:
        return O 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range (len(board)):
        for j in range (len(board[0])):
            if board[i][j] == EMPTY:
                actions.add(tuple([i, j]))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action == None:
        return board
    board_copy = copy.deepcopy(board) 
    board_copy[action[0]][action[1]] = player(board_copy)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0]!= EMPTY and all(element == row[0] for element in row):
            return row[0]
    cols =[]
    for i in range (len(board[0])):
        column = []
        for j in range (len(board)):
            column.append(board[j][i])
        cols.append(column)
    for column in cols:
        if column[0]!= EMPTY and all(element == column[0] for element in column):
            return column[0]
    diagonal = []
    for i in range (len(board)):
        for j in range (len(board[0])):
            if i == j:
                diagonal.append(board[i][j])
    if diagonal[0]!= EMPTY and all(element == diagonal[0] for element in diagonal):
            return diagonal[0]       
    diagonal = []
    for i in range (len(board)):
        for j in range (len(board[0])):
            if i == 2-j:
                diagonal.append(board[i][j])
    if diagonal[0]!= EMPTY and all(element == diagonal[0] for element in diagonal):
            return diagonal[0]   
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == None:
        for row in board:
            for cell in row:
                if cell == EMPTY:
                    return False
    return True         


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def mini(board):
    if terminal(board):
        return utility(board)
    score = []
    for action in actions(board):
            result_ = result(board, action)
            score_of_result = maxi(result_)
            score.append(score_of_result)
            state_map[(tuple(flatten(board)), action)] = score_of_result
    min_score = min(score)
    return min_score



def maxi(board):
    if terminal(board):
        return utility(board)
    score = []
    for action in actions(board):
            result_ = result(board, action)
            score_of_result = mini(result_)
            score.append(score_of_result)
            state_map[(tuple(flatten(board)), action)] = score_of_result
    max_score = max(score)
    return max_score
def read_map():
    try:
        with open("turn_map.txt", 'r') as file: 
            counter = 0
            key1 = []
            key2 = []
            val = []  
            for line in file:
                if counter == 0:
                    key1 = list(line[:-1].split(" "))
                    for i in range (len(key1)):
                        if key1[i] == 'None':
                            key1[i] = None
                if counter == 1:
                    key2 = list(map(int, line[:-1].split(" ")))
                if counter == 2:
                    val = int(line[:-1])
                    state_map[(tuple(key1), tuple(key2))] = val
                    counter = 0
                    continue
                counter+=1
        state_map[(tuple(key1), tuple(key2))] = val
    except:
        return
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if len(state_map) == 0:
        read_map()
    if len(state_map) == 0:
        maxi(initial_state())
        # state_map[((1,2), (3,4))] = 5
        with open("turn_map.txt", 'w') as f: 
            for key, value in state_map.items(): 
                f.write('%s\n%s\n%s\n' % (" ".join(map(str, key[0])), " ".join(map(str, key[1])), str(value)))
    for action in actions(board):
        if not (tuple(flatten(board)), action) in state_map:
            continue
        if player(board) == X and state_map[(tuple(flatten(board)), action)] == 1:
            return action
        elif player(board) == O and state_map[(tuple(flatten(board)), action)] == -1:
            return action
    for action in actions(board):
        if not (tuple(flatten(board)), action) in state_map:
            continue
        if state_map[(tuple(flatten(board)), action)] == 0:
            return action        
    return action
