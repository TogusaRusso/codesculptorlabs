# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# import modules
import simplegui
import random
import math

# define global variables
secret_number = 0
range = 100
guesses_remain = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, guesses_remain
    secret_number = random.randrange(range)
    # deterimnate number of guesses by formula
    guesses_remain = int(math.ceil(math.log(range + 1, 2)))
    print "New game. Range is from 0 to", range
    print "Number of remaining guesses is", guesses_remain
    print


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range
    range = 100
    new_game()
  
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range
    range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global guesses_remain
    guess = int(guess)
    print "Guess was", guess
    guesses_remain -= 1
    if guess == secret_number:
        print "Correct"
        print
        new_game()
    elif guesses_remain == 0:
        print "You ran out of guesses. The number was", secret_number
        print
        # start new game and exit function 
        new_game()
    elif guess < secret_number:
        print "Number of remaining guesses is", guesses_remain
        print "Higher"
        print
    else:
        print "Number of remaining guesses is", guesses_remain
        print "Lower"
        print
    
# create frame
frame = simplegui.create_frame("Guess the number", 0, 150)


# register event handlers for control elements and start frame
frame.add_input("Enter your guess", input_guess, 150)
frame.add_button("Range 0 -   100", range100, 150)
frame.add_button("Range 0 - 1000", range1000, 150)


# call new_game 
frame.start()
new_game()


# always remember to check your completed program against the grading rubric
