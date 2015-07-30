"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(180)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if player == provided.PLAYERX:
        other_player = provided.PLAYERO
    else:
        other_player = provided.PLAYERX
    minmax = (-2 * SCORES[player], (-1, -1))
    for move in board.get_empty_squares():
        c_board = board.clone()
        c_board.move(move[0], move[1], player)
        result = c_board.check_win()
        if result is None:
            result = mm_move(c_board, other_player)[0]
        else:
            result = SCORES[result]
        if (result - minmax[0]) * SCORES[player] > 0:
            minmax = (result, move)
    return minmax

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
