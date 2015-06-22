#"Stopwatch: The Game"

import simplegui

# define global variables

timer_value = 0
timer_is_running = False
tries = 0
wins = 0


# helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    #tenths of seconds
    d = t % 10
    #seconds
    t = (t - d) / 10
    bc = t % 60
    #minutes
    a = (t - bc) / 60
    if bc >= 10:
        bc = str(bc)
    else:
        bc = '0' + str(bc)
    return str(a) + ':' + bc + '.' + str(d)
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    global timer_is_running
    if not timer_is_running:
        timer_is_running = True
        timer.start()
        
        
def stop():
    global timer_is_running, wins, tries
    if timer_is_running:
        timer.stop()
        timer_is_running = False
        tries += 1
        if timer_value % 10 == 0:
            wins += 1
        

def reset():
    global timer_value, wins, tries, timer_is_running
    timer.stop()
    timer_is_running = False
    timer_value = 0
    wins = 0
    tries = 0
    
    


# define event handler for timer with 0.1 sec interval

def timer_handler():
    global timer_value
    timer_value += 1
    # we don't want time be more than 10 minutes
    timer_value %= 6000
    #print format(timer_value)

# define draw handler

def draw(canvas):
    canvas.draw_text(format(timer_value), (20, 75),
                     50, "White", "monospace")
    score = str(wins) + '/' + str(tries)
    #use width of score to place it in right corner
    scr_width = frame.get_canvas_textwidth(score, 
                                           30, "sans-serif")
    canvas.draw_text(score, (195 - scr_width, 25), 
                     30, "Green", "sans-serif")
    
# create frame

frame = simplegui.create_frame("Stopwatch: The Game", 
                               200, 120)
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)


# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)
#timer.start()

# start frame

frame.start()


###################################################
# Test code for the format function
# Note that function should always return a string with 
# six characters


#print format(0)
#print format(7)
#print format(17)
#print format(60)
#print format(63)
#print format(214)
#print format(599)
#print format(600)
#print format(602)
#print format(667)
#print format(1325)
#print format(4567)
#print format(5999)

###################################################
# Output from test

#0:00.0
#0:00.7
#0:01.7
#0:06.0
#0:06.3
#0:21.4
#0:59.9
#1:00.0
#1:00.2
#1:06.7
#2:12.5
#7:36.7
#9:59.9

