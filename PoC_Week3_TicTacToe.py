"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """ run a trial random game on current board """
    while board.check_win() == None:
        move = random.choice(board.get_empty_squares())
        board.move(move[0], move[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player): 
    """ updates scores using results of trial game """
    winner = board.check_win()
    if winner == provided.DRAW or winner == None:
        return
    loser = provided.switch_player(winner)
    for row in xrange(board.get_dim()):
        for col in xrange(board.get_dim()):
            if board.square(row, col) == winner:
                if player == winner:
                    scores[row][col] += SCORE_CURRENT
                else:
                    scores[row][col] += SCORE_OTHER
            elif board.square(row, col) == loser:
                if player == loser:
                    scores[row][col] -= SCORE_CURRENT
                else:
                    scores[row][col] -= SCORE_OTHER

def get_best_move(board, scores):
    """ chosses random empty square with best score """
    best_score = 0
    candidates = []
    for square in board.get_empty_squares():
        if (not candidates or 
            best_score < scores[square[0]][square[1]]):
            # list is empty or obsolete
            best_score = scores[square[0]][square[1]]
            candidates = [square]           
        elif best_score == scores[square[0]][square[1]]:
            candidates.append(square)
    return random.choice(candidates)

def mc_move(board, player, trials):
    """ made move after set of trials """
    scores = [[0.0 for _ in xrange(board.get_dim())] 
              for _ in xrange(board.get_dim())]
    for _ in xrange(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)
              
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

