# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# initialize global variables for deck and hands
deck=[]
player_hand=[]
dealer_hand=[]


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards=[]	# create Hand object

    def __str__(self):
        # return a string representation of a hand
        result=""	
        for card in self.cards:
            result += str(card) + " "
        return result

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        count = 0
        aces = False
        for card in self.cards:
            count += VALUES[card.rank]
            if card.rank == "A":
                aces=True
        if aces and count < 12:
            count += 10
        return count
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        offset = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + offset,pos[1]])
            offset += 1.2 * CARD_SIZE[0]
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)                          

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop(-1)
                                  
    
    def __str__(self):
        # return a string representing the deck
        result = ""	
        for card in self.cards:
            result += str(card) + " "
        return result



#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, dealer_hand, player_hand
    
    if in_play:
        #print "Dealer win"
        outcome = "Dealer win last round. Hit or stand?"
        score -= 1
    else:
        outcome = "Hit or stand?"

    # your code goes here
    deck = Deck()
    deck.shuffle()
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    #print "New deal:"
    #print "Dealer hand", dealer_hand, dealer_hand.get_value()
    #print "Player hand", player_hand, player_hand.get_value()
    in_play = True

def hit():
    global in_play, score, outcome
    # if the hand is in play, hit the player
    if player_hand.get_value() <= 21 and in_play:
        outcome = "Hit or stand?"
        player_hand.add_card(deck.deal_card())
        #print"Hit:"
        #print "Player hand", player_hand, player_hand.get_value()
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome="You went busted and lose. New deal?"
            score -= 1
            #print "You have busted"
            in_play = False
    
       
def stand():
    global in_play, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            #print "Dealer hand", dealer_hand, dealer_hand.get_value()
        in_play=False
        if dealer_hand.get_value() > 21:
            outcome = "Dealer went busted. New deal?"
            score += 1
            #print "Dealer have busted"
        elif dealer_hand.get_value() < player_hand.get_value():
            outcome = "You win. New deal?"
            score += 1
            #print "Player win"
        else:
            outcome = "You lose. New deal?"
            score -= 1
            #print "Dealer win"

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    dealer_hand.draw(canvas, [20, 100])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, 
                          CARD_BACK_SIZE, 
                          [20+CARD_BACK_CENTER[0], 100+CARD_BACK_CENTER[1]], 
                          CARD_BACK_SIZE)
    player_hand.draw(canvas, [20, 400])
    canvas.draw_text("BLACKJACK", [30, 80], 50, "Blue", 'monospace')
    outcome_width = frame.get_canvas_textwidth(outcome, 35, 'sans-serif')
    canvas.draw_text(outcome, [300 - outcome_width / 2, 300], 35, "Yellow", 'sans-serif')
    canvas.draw_text("Score: "+str(score), [400, 80], 30, "Yellow", 'sans-serif')
    canvas.draw_text("Dealer's hand ", [60, 220], 15, "Black", 'sans-serif')
    canvas.draw_text("Player's hand ", [60, 520], 15, "Black", 'sans-serif')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric