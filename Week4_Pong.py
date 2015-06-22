# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD_VEL = 3
LEFT = False
RIGHT = True
FPS = 60.0
HARDER = 1.1
ball_pos = [WIDTH / 2.0, HEIGHT / 2.0]
ball_vel = [0.0, 0.0]
paddle1_pos = HEIGHT / 2.0
paddle2_pos = HEIGHT / 2.0
paddle1_vel = 0.0
paddle2_vel = 0.0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(120, 240) / FPS , - random.randrange(60, 180) / FPS]
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2.0
    paddle2_pos = HEIGHT / 2.0
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    score1 = 0
    score2 = 0
    spawn_ball(random.choice([LEFT, RIGHT]))
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        ball_pos[1] = BALL_RADIUS
    elif ball_pos[1] > (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        ball_pos[1] = (HEIGHT - 1) - BALL_RADIUS
                
            
    # draw ball
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    paddle2_pos += paddle2_vel
    if paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
        
    
    
    # draw paddles
    
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                         [0, paddle1_pos + HALF_PAD_HEIGHT]], 1, "White", "White")
    canvas.draw_polygon([[WIDTH - 1, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH - 1 - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH - 1 - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                         [WIDTH - 1, paddle2_pos + HALF_PAD_HEIGHT]], 1, "White", "White")
    
    # determine whether paddle and ball collide    
    if ball_pos[0] < BALL_RADIUS + PAD_WIDTH:
        if abs(ball_pos[1] - paddle1_pos) <= HALF_PAD_HEIGHT:
            ball_pos[0] = BALL_RADIUS + PAD_WIDTH
            ball_vel[0] *= -HARDER
            ball_vel[1] *= HARDER
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] > ((WIDTH -  PAD_WIDTH) - 1) - BALL_RADIUS:
        if abs(ball_pos[1] - paddle2_pos) <= HALF_PAD_HEIGHT:
            ball_pos[0] = ((WIDTH -  PAD_WIDTH) - 1) - BALL_RADIUS
            ball_vel[0] *= -HARDER
            ball_vel[1] *= HARDER
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    scorew = 0.5 * frame.get_canvas_textwidth(str(score1), 40, "monospace")
    canvas.draw_text(str(score1), [WIDTH / 2 - 70 - scorew, 50], 40, "White", "monospace")
    scorew = 0.5 * frame.get_canvas_textwidth(str(score2), 40, "monospace")
    canvas.draw_text(str(score2), [WIDTH / 2 + 70 - scorew, 50], 40, "White", "monospace")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == 'W':
        paddle1_vel -= PAD_VEL
    elif chr(key) == 'S':
        paddle1_vel += PAD_VEL
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += PAD_VEL
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == 'W':
        paddle1_vel += PAD_VEL
    elif chr(key) == 'S':
        paddle1_vel -= PAD_VEL
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel += PAD_VEL
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel -= PAD_VEL


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)


# start frame
new_game()
frame.start()
