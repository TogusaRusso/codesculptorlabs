# implementation of card game - Memory

import simplegui
import random

deck = []
exposed = []
paired = [] #Little addition, I want show paired cards
turns = 0
state = 0
turned = []
#Ok, let's have some fun
mlp_sprites = simplegui.load_image("http://i57.tinypic.com/157hipv.jpg")
    
    
# helper function to initialize globals
def new_game():
    """Shuffling and hiding new deck, setting states"""
    global deck
    global exposed
    global state
    global turns
    global turned
    global paired
    #new deck shuffled
    deck = 2 * range(8)
    random.shuffle(deck)
    #hide all cards
    exposed = 16*[False]
    #set state
    state = 0
    #and turns
    turns = 0
    label.set_text("Turns = "+str(turns))
    turned = []
    paired = 16*[False]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    pass
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    """Drawing our cards"""
    xc = 50
    yc = 50
    n=0
    for card in deck:
        #Show numbers of cards only if they exposed
        if (exposed[n]):
            #canvas.draw_text(str(card),[xc-10,yc+10],40,"White")
            #canvas.draw_polygon([(xc - 23, yc - 47), (xc + 23, yc - 47),
            #                     (xc + 23, yc + 47), (xc - 23, yc + 47)],
            #                     2, "White")
            if (paired[n]): #Show new images if paired
                canvas.draw_image(mlp_sprites, (card*200+150, 50), (100, 100),
                                  (xc, yc), (100, 100))
            else:
                canvas.draw_image(mlp_sprites, (card*200+50, 50), (100, 100),
                                  (xc, yc), (100, 100))
        else:
            canvas.draw_polygon([(xc - 50, yc - 50), (xc + 50, yc - 50),
                                 (xc + 50, yc + 50), (xc - 50, yc + 50)],
                                 3, "White", "Green")
        xc += 100
        if(xc > 400):
            #Next row
            xc = 50
            yc += 100
        n += 1

def check_paired():
    """check if two cards paired and change their look"""
    global turned
    global paired
    global deck
    if(deck[turned[0]] == deck[turned[1]]):
        paired[turned[0]] = True
        paired[turned[1]] = True
        print "Paired!"
        
def mouseclick(pos):
    """Let's open this cards"""
    
    global exposed
    global state
    global turned
    global deck
    global turns
    
    card_n = 4 * (pos[1] // 100) + pos[0] // 100
    if(exposed[card_n]):
        return #Ignoring already exposed card
    
    
    #Let's count from 1
    print "Clicked card n:", card_n+1 
    exposed[card_n] = True
    if state == 0:
        #Opening first card
        state = 1
        #Remember card, wich we opening now
        turned = [card_n]
    elif state == 1:
        #Opening second card
        state = 2
        #Remember second card
        turned += [card_n]
        check_paired()
        turns += 1 #Count turn
        label.set_text("Turns = "+str(turns))
    else:
        #Two cards was open before this
        state = 1
        if(not (deck[turned[0]] == deck[turned[1]])):
            #If two cards don't match, hide them
            exposed[turned[0]] = False
            exposed[turned[1]] = False
        #Remember new card
        turned = [card_n]
    #print state, turned

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 400, 400)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# And my record is 13 turns!