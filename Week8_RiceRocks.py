# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
extra_life_given = 0
#if this variable > 0 we shoot torpedo, not puny missiles!
shoot_photon_torpedo = 0

# constants
MAXIMUM_OF_ROCKS = 12 # as in description
SAFE_DISTANCE_MULT = 2
DIFFICULTY_BASE = 1.03 # base of difficulty growth, must be > 1
DIFFICULTY_STEP = 1 # score to next step in difficulty
BASE_SPEED = .3 # base speed of rock
EXTRA_LIFE = 10
SHIP_ANGLE_VEL = .1
BONUS_TORPEDO = 10

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = list()
asteroid_image.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png"))
asteroid_image.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png"))
asteroid_image.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png"))

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image_alpha = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image_orange = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
# list of blue explosions
explosion_image_blue = list()
explosion_image_blue.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png"))
explosion_image_blue.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png"))


# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += SHIP_ANGLE_VEL
        
    def decrement_angle_vel(self):
        self.angle_vel -= SHIP_ANGLE_VEL
        
    def shoot(self):
        #global a_missile
        global shoot_photon_torpedo
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        #a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        if shoot_photon_torpedo > 0:
            shoot_photon_torpedo -= 1
            missile_vel = [self.vel[0] + 12 * forward[0], self.vel[1] + 12 * forward[1]]
            missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0,
                                     # i'm crazy guy, let's shoot PHOTON TORPEDO
                                     explosion_image_alpha, explosion_info,
                                     missile_sound))
        else:
            missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
            missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0,
                                     missile_image, missile_info, 
                                     missile_sound))
        
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def get_image(self):
        return self.image
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            offset = self.age * self.image_size[0]
            canvas.draw_image(self.image, 
                              [self.image_center[0] + offset, self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # updating age
        self.age +=1
        return self.age > self.lifespan
  
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def get_image(self):
        return self.image

    def collide(self, other_object):
        minimum_distance = self.get_radius() + other_object.get_radius()
        return minimum_distance > dist(self.get_position(),  other_object.get_position())

# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, extra_life_given
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        # (re)start game
        started = True
        lives = 3
        score = 0
        soundtrack.play()
        extra_life_given = 0

def explode(obj):
    global explosion_group
    #let's check it's asteroid
    if obj.get_image() in asteroid_image:
        explosion_group.add(Sprite(obj.get_position(), [0, 0], 0, 0, 
                                   #let's have random explosion for asteroid
                                   explosion_image_blue[random.randrange(len(explosion_image_blue))], 
                                   explosion_info, explosion_sound))
    #and if it's a ship, let's blew it orange!
    elif obj.get_image() == ship_image:
        explosion_group.add(Sprite(obj.get_position(), [0, 0], 0, 0, 
                                   explosion_image_orange, 
                                   explosion_info, explosion_sound))
        
        
def process_sprite_group(canvas, sprites):
    for sprite in set(sprites):
        #  remove this sprite?
        if sprite.update():
            sprites.discard(sprite)
        else:
            sprite.draw(canvas)


def is_group_collide(group, other_object):
    collide = False
    for obj in set(group):
        if obj.collide(other_object):
            collide = True
    return collide
        

def group_collide(group, other_object):
    collide = False
    for obj in set(group):
        if obj.collide(other_object):
            explode(obj)
            group.discard(obj)
            collide = True
    return collide

def group_group_collide(first_group, second_group):
    collisions=0
    for obj in set(first_group):
        if group_collide(second_group, obj):
            explode(obj)
            collisions += 1
            first_group.discard(obj)
    return collisions

#primitive physics engine for asteroids of equal mass
def process_collisions(group):
    processed = set()
    while len(group) > 0:
        obj1 = group.pop()
        for obj2 in group:
            if obj1.collide(obj2):
                obj1.vel, obj2.vel = obj2.vel, obj1.vel
                while obj1.collide(obj2):
                    obj1.update()
                    obj2.update()
        processed.add(obj1)
    group.update(processed)

def draw(canvas):
    global time, started, lives, score, extra_life_given, shoot_photon_torpedo
    global rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    
    if group_collide(rock_group, my_ship) and started:
        lives -= 1
        #no, it don't
        #score += 1 # yes, it's counts!
        explode(my_ship)
        shoot_photon_torpedo = 0 # no bonus for you!
        
    score += group_group_collide(rock_group, missile_group)
    
    # bonus life and super omega weapon!
    if score - extra_life_given >= EXTRA_LIFE:
        lives += 1
        extra_life_given = EXTRA_LIFE * (score // EXTRA_LIFE)
        shoot_photon_torpedo += BONUS_TORPEDO
    
    # endgame?
    if lives == 0:
        started = False
        rock_group = set()
        missile_group = set()
        soundtrack.rewind()
            
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    #add some physic to asteroids
    process_collisions(rock_group)
    
    # update ship
    my_ship.update()
    #a_rock.update()
    #a_missile.update()

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    # draw UI
    #and draw it last, over everything!
    if lives == 0:
        lives_text = "No lives left"
    else:
        lives_text = "Lives"
    canvas.draw_text(lives_text, [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    #canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    #let's do more interesting lives
    for i in xrange(lives):
        canvas.draw_image(ship_image, ship_info.get_center(), ship_info.get_size(),
                          [50 + i * 30, 80], [30, 30], -0.5 * math.pi)

        
# timer handler that spawns a rock    
def rock_spawner():
    #global a_rock
    #global rock_group
    if len(rock_group) < MAXIMUM_OF_ROCKS and started:
        # let's speed of asteroids grows
        max_speed = BASE_SPEED * (DIFFICULTY_BASE ** (score // DIFFICULTY_STEP))
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * 2 * max_speed - max_speed, random.random() * 2 * max_speed - max_speed]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image[random.randrange(len(asteroid_image))], asteroid_info)
        minimum_distance = a_rock.get_radius() + my_ship.get_radius()
        distance = dist(a_rock.get_position(), my_ship.get_position())
        # spawn rock only if distance big enough
        if SAFE_DISTANCE_MULT * minimum_distance < distance and not is_group_collide(rock_group, a_rock):
            rock_group.add(a_rock)
            
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and empty sets of rocks and missiles
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
rock_group = set() #Should call it  BEATLES
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set()
explosion_group = set()

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
