import pygame as py
import os

py.font.init()
py.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("StarWars")

BULLET_FIRE_SOUND = py.mixer.Sound(os.path.join('assets', 'heat-vision.mp3'))
BULLET_HIT_SOUND = py.mixer.Sound(os.path.join('assets', 'impact.wav'))
WIN_SOUND = py.mixer.Sound(os.path.join('assets', 'WIN.wav'))
HEALTH_FONT = py.font.SysFont('comicsans', 40)
WINNER_FONT = py.font.SysFont('comicsans', 120)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3



YELLOW_HIT = py.USEREVENT + 1
RED_HIT = py.USEREVENT + 2

BORDER = py.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)

SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT = 50, 40

YELLOW_SPACESHIP_IMAGE = py.image.load(os.path.join('assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = py.transform.rotate(py.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = py.image.load(os.path.join('assets','spaceship_red.png'))
RED_SPACESHIP = py.transform.rotate(py.transform.scale(RED_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACE_SHIP_HEIGHT)), 270)

BACKGROUND_IMAGE = py.image.load(os.path.join('assets', 'space.png'))
BACKGROUND = py.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0,0))
    py.draw.rect(WIN, WHITE, BORDER)
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))    
        
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    draw_bullets(red_bullets, yellow_bullets)

    py.display.update()
    return 0


def move_spaceship_yellow(yellow, keys_pressed):

    if keys_pressed[py.K_a] and yellow.x - VEL > 0:#Left Yellow
        yellow.x -= VEL
    if keys_pressed[py.K_d] and yellow.x + VEL + yellow.width < BORDER.x:#Right Yellow
        yellow.x += VEL
    if keys_pressed[py.K_w] and yellow.y - VEL > 0:#UP Yellow
        yellow.y -= VEL
    if keys_pressed[py.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 5:#Down Yellow
        yellow.y += VEL
    return 0    


def move_spaceship_red(red, keys_pressed):
    if keys_pressed[py.K_LEFT] and red.x - VEL  > BORDER.x + BORDER.width + 10 :#Left Red
        red.x -= VEL
    if keys_pressed[py.K_RIGHT] and red.x + VEL + red.width < WIDTH :#Right Red
        red.x += VEL
    if keys_pressed[py.K_UP] and red.y > 0:#UP Red
        red.y -= VEL
    if keys_pressed[py.K_DOWN] and red.y + VEL + red.height < HEIGHT - 5 :#Down Red
        red.y += VEL
    return 0

def handel_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            py.event.post(py.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            py.event.post(py.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    return 0


def draw_bullets(red_bullets, yellow_bullets):
    for bullet in red_bullets:
        py.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        py.draw.rect(WIN, YELLOW, bullet)
    return 0

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - 50))
    py.display.update()
    py.time.delay(5000)
    return 0

def main():
    red = py.Rect(700,200,SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT)
    yellow = py.Rect(200,200,SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = py.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                
            if event.type == py.KEYDOWN:
                if event.key == py.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = py.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 + 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == py.K_RCTRL and len(red_bullets) < MAX_BULLETS: 
                    bullet = py.Rect(red.x, red.y + red.height//2 + 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT: 
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner = ''
        if red_health <= 0:
            winner = 'Yellow is Winner!'
        if yellow_health <= 0:
            winner = 'Red is Winner!'
        if winner != '':
            WIN_SOUND.play()
            draw_winner(winner)
            break
        keys_pressed = py.key.get_pressed()
        move_spaceship_yellow(yellow, keys_pressed)
        move_spaceship_red(red, keys_pressed)
        handel_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()


if __name__ == '__main__':
    main()