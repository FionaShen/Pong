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
LEFT = False
RIGHT = True
PAD_SPEED = 5

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # initialize ball position
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    # initialize random velocity based on direction
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
    else:
        ball_vel[0] = -random.randrange(2, 4)
    ball_vel[1] = -random.randrange(1, 3)

    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # reset
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    # initialize random start direction
    direction = random.choice([0, 1])
    if direction == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect off of top or bottom walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]        
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_new_pos = paddle1_pos + paddle1_vel
    paddle2_new_pos = paddle2_pos + paddle2_vel
    if paddle1_new_pos >= HALF_PAD_HEIGHT and paddle1_new_pos <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = paddle1_new_pos
    if paddle2_new_pos >= HALF_PAD_HEIGHT and paddle2_new_pos <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = paddle2_new_pos      	
        
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], 
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                         [0, paddle1_pos + HALF_PAD_HEIGHT]],
                        1, "White", "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                         [WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                         [WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                         [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]],
                        1, "White", "White")
    
    # determine whether paddle and ball collide 
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        # collide with left paddle, reflect
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * 1.1
        # collide with left gutter, update score, respawn ball
        else: 
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH :
        # collide with right paddle, reflect
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * 1.1
        # collide with right gutter, update score, respawn ball
        else:
            score1 += 1  
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), (225, 100), 50, "White")
    canvas.draw_text(str(score2), (350, 100), 50, "White")
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == 'w' or chr(key) == 'W':
        paddle1_vel = -PAD_SPEED
    elif chr(key) == 's' or chr(key) == 'S':
        paddle1_vel = PAD_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED    
               
            
def keyup(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == 'w' or chr(key) == 'W':
        paddle1_vel = 0
    elif chr(key) == 's' or chr(key) == 'S':
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0 

        
def restart():
    new_game()
    
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart)


# start frame
new_game()
frame.start()
