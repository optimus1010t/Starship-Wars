import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("STARSHIP WARS")
colour = (14,19,24)
black =(0,0,0)

border = pygame.Rect((WIDTH//2)-5,0,10,HEIGHT)
FPS =  60
VEL = 5
ss_w,ss_h= 55,40


h_font = pygame.font.SysFont ('comicsans',25)
w_font = pygame.font.SysFont ('comicsans',60)
y_hit = pygame.USEREVENT + 1
r_hit = pygame.USEREVENT + 2

bg = pygame.transform.scale(pygame.image.load(os.path.join('Assets','back.jpg')),(WIDTH,HEIGHT))

b_vel = 8
n_b = 3

y_ss = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
y_ss = pygame.transform.rotate(pygame.transform.scale(y_ss,(ss_w,ss_h)),270)
r_ss = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
r_ss = pygame.transform.rotate(pygame.transform.scale(r_ss,(ss_w,ss_h)),90)

def draw_window(red,yellow,r_bullets, y_bullets,red_h,yellow_h):
    WIN.blit(bg,(0,0))
    pygame.draw.rect(WIN,black,border)
    red_h_text = h_font.render("Health:"+str(red_h),1,(255,255,255))
    WIN.blit(red_h_text,(WIDTH-red_h_text.get_width()-10,10))
    yellow_h_text = h_font.render("Health:"+str(yellow_h),1,(255,255,255))
    WIN.blit(yellow_h_text,(10,10))
    WIN.blit(y_ss,(yellow.x,yellow.y))
    WIN.blit(r_ss,(red.x,red.y))
    
    for bullet in r_bullets:
        pygame.draw.rect(WIN,(255,0,0),bullet)
    for bullet in y_bullets:
        pygame.draw.rect(WIN,(255,255,0),bullet)

    pygame.display.update()

def y_controls (keys_pressed,yellow):  
        if keys_pressed [pygame.K_a] and yellow.x+VEL >= 0: #LEFT
            yellow.x -= VEL
        if keys_pressed [pygame.K_d] and yellow.x+VEL -10 <= border.x-ss_w+5: #RIGHT
            yellow.x += VEL
        if keys_pressed [pygame.K_w] and yellow.y+VEL-10 >=0: #UP
            yellow.y -= VEL
        if keys_pressed [pygame.K_s] and yellow.y+VEL+10 < HEIGHT-ss_h: #DOWN
            yellow.y += VEL
def r_controls (keys_pressed,red):
        if keys_pressed [pygame.K_LEFT] and red.x+VEL >= border.x+20: #LEFT
            red.x -= VEL
        if keys_pressed [pygame.K_RIGHT] and red.x+VEL +ss_w -25 <= 900: #RIGHT
            red.x += VEL
        if keys_pressed [pygame.K_UP] and red.y+VEL-10 >=0: #UP
            red.y -= VEL
        if keys_pressed [pygame.K_DOWN] and red.y+VEL+10 < HEIGHT-ss_h: #DOWN
            red.y += VEL

def h_bullets (y_bullets,r_bullets,yellow,red):
    for bullet in y_bullets:
        bullet.x += b_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(r_hit))
            y_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            y_bullets.remove(bullet)
    
    for bullet in r_bullets:
        bullet.x -= b_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(y_hit))
            r_bullets.remove(bullet)
        elif bullet.x < 0:
            r_bullets.remove(bullet)    

def draw_winner(text):
    d_text = w_font.render(text,1,(255,255,255))
    WIN.blit(d_text,(WIDTH/2-d_text.get_width()//2,HEIGHT/2-d_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    red = pygame.Rect(700,200,ss_w,ss_h)
    yellow = pygame.Rect(100,200,ss_w,ss_h)
    r_bullets = []
    y_bullets = []
    red_h = 10
    yellow_h = 10
     
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and (len(y_bullets) < n_b):
                     bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                     y_bullets.append(bullet)
                    
                
                if event.key == pygame.K_RCTRL and (len(r_bullets) < n_b):   
                     bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                     r_bullets.append(bullet)
                     
            if event.type == r_hit:
                red_h -= 1
                
            if event.type == y_hit:
                yellow_h -= 1
                
        w_text=""    
        if red_h <= 0 :
            w_text = "YELLOW WINS!!"
        if yellow_h <= 0:
            w_text = "RED WINS!!"
        if w_text != "" :
            draw_winner(w_text) #SOMEBODY WON
            break 
                        
        print (r_bullets,y_bullets)    
        keys_pressed = pygame.key.get_pressed()
        y_controls (keys_pressed, yellow)
        r_controls (keys_pressed, red)
        
        h_bullets (y_bullets, r_bullets, yellow, red)
        
        draw_window(red,yellow,r_bullets,y_bullets,red_h,yellow_h)      
    main()

if __name__  == "__main__":
    main()
              