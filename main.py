import random
from os import path
from Explosion import Explosion
import pygame
from Bullet import *
from Meteor import *
from Player import *
from begin_state import *

# TODO Refactor 將參數統一放到另外一個檔案
from Env import *


sound_dir = path.join(path.dirname(__file__), 'sound')
font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)







screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(path.join(img_dir,'background.png'))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_enemies = pygame.sprite.Group()
bullets_boss = pygame.sprite.Group()
supports=pygame.sprite.Group()

last_shot = pygame.time.get_ticks()

now = 0
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)
get_weapon=False

class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemies,all):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(3, 8)
        image = pygame.image.load(path.join(img_dir, "enemyBlack1.png"))
        self.image = pygame.transform.scale(image, (self.size * 8, self.size * 8))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = 0
        self.speedx = 0
        self.speedy = 5
        self.image_origin=self.image
        self.rot_angle=5
        self.angle=0
        self.group=enemies
        self.all_sprites=all
        self.last_shot=pygame.time.get_ticks()
        self.now=pygame.time.get_ticks()
    def update(self):
        global last_shot_enemy
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.y > HEIGHT):
            self.newEnemy()
            self.kill()
        self.now=pygame.time.get_ticks()
        if self.now-self.last_shot>SHOT_DELAY:
            self.shoot_enemy()
            self.last_shot=self.now

    def shoot_enemy(self):
        sound_pew.play()
        bullet = Bullet_enemy(self.rect.centerx,self.rect.centery)
        bullets_enemies.add(bullet)
        all_sprites.add(bullet)

    def newEnemy(self):
        #global all_sprites
        e = Enemy(self.group,self.all_sprites)
        self.group.add(e)
        self.all_sprites.add(e)
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "enemyBlue1.png"))
        self.image = pygame.transform.scale(image, (200, 120))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy=1
        self.last_shot=pygame.time.get_ticks()
        self.angle=0
        #self.now=pygame.time.get_ticks()
        old_center=self.rect.center
        self.image_origin=self.image
        self.rot_angle=180
        self.angle=self.angle+self.rot_angle
        self.image=pygame.transform.rotate(self.image_origin,self.angle)
        self.rect=self.image.get_rect()
        self.rect.center=old_center
        self.shield=100

    def update(self):
        self.rect.y += self.speedy
        self.now=pygame.time.get_ticks()
        if self.now-self.last_shot>SHOT_DELAY:
            self.shoot_boss()
            self.last_shot=self.now

    def shoot_boss(self):
        sound_pew.play()
        bullet = Bullet_boss2(self.rect.centerx,self.rect.centery)
        bullet2 = Bullet_boss(self.rect.centerx+60,self.rect.centery)
        bullet3 = Bullet_boss(self.rect.centerx-60,self.rect.centery)
        bullets_boss.add(bullet)
        bullets_boss.add(bullet2)
        bullets_boss.add(bullet3)
        all_sprites.add(bullet)
        all_sprites.add(bullet2)
        all_sprites.add(bullet3)
boss=Boss(WIDTH/2,0)
def newMeteor():
    global all_sprites
    m = Meteor(meteors,all_sprites)
    meteors.add(m)
    all_sprites.add(m)
for i in range(8):
    newMeteor()
def newEnemy():
    global all_sprites
    e = Enemy(enemies,all_sprites)
    enemies.add(e)
    all_sprites.add(e)
for i in range(8):
    newEnemy()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
running = True
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))
#live=pygame.image.load(path.join(img_dir,"playerShip1_orange.png"))
live=3
def draw_lives():
    global live
    img_live = pygame.transform.scale(player.image,(30,20))
    if player.shield<=0:
        live-=1
        if live!=0:
            player.shield=100
    for i in range(live):
        live_rect = img_live.get_rect()
        live_rect.x = 700+25*i
        live_rect.y = 10
        screen.blit(img_live,live_rect)
def draw_shield():
    shield_bar=pygame.rect.Rect(10,10,player.shield,10)
    outline=pygame.rect.Rect(10,10,100,10)
    pygame.draw.rect(screen,GREEN,shield_bar)
    pygame.draw.rect(screen,(255,255,255),outline,2)
def draw_shield_boss():
    shield_bar=pygame.rect.Rect(10,50,boss.shield,10)
    outline=pygame.rect.Rect(10,50,100,10)
    pygame.draw.rect(screen,YELLOW,shield_bar)
    pygame.draw.rect(screen,(255,255,255),outline,2)
def check_meteor_hit_player():
    global running, meteors
    hits = pygame.sprite.spritecollide(player, meteors, False,pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player"        )
            newMeteor()
            
            player.shield-=hit.size*5
            #print(player.shield)
            #if player.shield<=0:
            #    running = False
def check_enemy_hit_player():
    global running, enemies
    hits = pygame.sprite.spritecollide(player, enemies, False,pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player"        )
            newEnemy()
            
            player.shield-=hit.size*5
            #print(player.shield)
            #if player.shield<=0:
            #    running = False
weapon=False
weapon_time=0
def check_player_hit_supports():
    global running, supports,score,weapon,weapon_time,get_weapon
    hits = pygame.sprite.spritecollide(player,supports, False,pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            if hit.type==0:
                get_weapon=True
                weapon_time=pygame.time.get_ticks()
            elif hit.type==1:
                player.shield+=25
                if player.shield>100:
                    player.shield=100
            # print("check_meteor_hit_player")

class Support(pygame.sprite.Sprite):
    def __init__(self,x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type==0:
            self.image =pygame.image.load(path.join(img_dir,"star_gold.png"))
        else:
            self.image =pygame.image.load(path.join(img_dir,"shield_silver.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 8
        self.type=type
    
    def update(self):
        self.rect.centery = self.rect.centery + self.speedy
        if self.rect.centery>HEIGHT:
            self.kill()
def check_bullets_hit_meteor():
    global  score
    hits = pygame.sprite.groupcollide(meteors,bullets, True, True,pygame.sprite.collide_circle_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            score += (hit.size)*2
            
            # print("check_bullets_hit_meteor")
            newMeteor()
            explosion=Explosion(hit.rect.centerx,hit.rect.centery)
            all_sprites.add(explosion)
            type=random.randint(0,1)
            support=Support(hit.rect.centerx,hit.rect.centery,type)
            supports.add(support)
            all_sprites.add(supports)

def check_bullets_hit_enemy():
    global  score
    hits = pygame.sprite.groupcollide(enemies,bullets,True,True,pygame.sprite.collide_circle_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            score += (hit.size)*2
            
            # print("check_bullets_hit_meteor")
            newEnemy()
            explosion=Explosion(hit.rect.centerx,hit.rect.centery)
            all_sprites.add(explosion)
            type=random.randint(0,1)
            support=Support(hit.rect.centerx,hit.rect.centery,type)
            supports.add(support)
            all_sprites.add(supports)
def check_bullets_hit_player():
    global  score
    hits = pygame.sprite.spritecollide(player,bullets_enemies,False,pygame.sprite.collide_circle_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            player.shield-= 5
            
            # print("check_bullets_hit_meteor")
def check_bullets_boss_hit_player():
    global  score
    hits = pygame.sprite.spritecollide(player,bullets_boss,False,pygame.sprite.collide_circle_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            player.shield-= 10
            
            # print("check_bullets_hit_meteor")
def check_bullets_hit_boss():
    global  score
    hits = pygame.sprite.spritecollide(boss,bullets,False,pygame.sprite.collide_circle_ratio(1))
    if hits:
        for hit in hits:
            hit.kill()
            boss.shield-= 5
            
            # print("check_bullets_hit_meteor")
def draw_score():
    font = pygame.font.Font(font_name, 14)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 20)
    screen.blit(text_surface, text_rect)
    pass


def shoot():
    sound_pew.play()
    bullet = Bullet(player.rect.centerx, player.rect.centery)
    bullets.add(bullet)
    all_sprites.add(bullet)
def shoot2():
    sound_pew.play()
    bullet = Bullet(player.rect.centerx-10, player.rect.centery)
    bullets.add(bullet)
    all_sprites.add(bullet)
    bullet2 = Bullet(player.rect.centerx+10, player.rect.centery)
    bullets.add(bullet2)
    all_sprites.add(bullet2)

gamestate="begin"
def show_text(text,x,y,size):
    font=pygame.font.Font(font_name,size)
    text=font.render(text,True,YELLOW)
    screen.blit(text,(x,y))
def show_begin_screen():
    show_text("SHUMP!",250,150,100)
    show_text("Arrow keys move. Space to Fire",230,300,30)
    show_text("Press Space to begin.",320,400,20)
begin_state=Begin_state(screen)
show_boss=False
boss_alive=False
while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)
    # event trigger
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if gamestate=="begin":
        begin_state.show_begin_screen()
        begin_state.keyhandle()
        if begin_state.keyhandle()==True:
            score=0
            show_boss=False
        gamestate=begin_state.updatestate()
    elif gamestate=="start":
        keystate = pygame.key.get_pressed()
        now_z=pygame.time.get_ticks()
        if keystate[pygame.K_z]:
            if get_weapon==True:
                if weapon==True:
                    weapon=False
                    Bullet.speedy=10
                else:
                    weapon=True
                    Bullet.speedy=100
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            now=pygame.time.get_ticks()
            if now-last_shot>SHOT_DELAY:
                if weapon==False:
                    shoot()
                    last_shot=now
                else:
                    if pygame.time.get_ticks()-weapon_time<=10000:
                        shoot2()
                        last_shot=now
                    else:
                        weapon=False
                        get_weapon=False
                        Bullet.speedy=10
        if live<=0:
            player.shield=100
            live=3
            gamestate="begin"
            #boss.kill()
            begin_state.reset()
            

        if score>500 and show_boss==False:
            #boss=Boss(WIDTH/2,0)
            all_sprites.add(boss)
            #draw_shield_boss()
            show_boss=True
            boss_alive=True
        
        if boss.shield<=0:
            boss.kill()
            boss_alive=False
        if boss.rect.y>HEIGHT:
            boss.kill()
            boss_alive=False
        if score>400:
            bg=pygame.image.load(path.join(img_dir,'star_wars2.jpg'))
        elif score>200:
            bg=pygame.image.load(path.join(img_dir,'star_wars1.jpg'))
        # update the state of sprites
        check_meteor_hit_player()
        #
        check_bullets_hit_meteor()
        check_player_hit_supports()
        check_enemy_hit_player()
        check_bullets_hit_enemy()
        check_bullets_hit_player()
        check_bullets_boss_hit_player()


        all_sprites.update()

        # draw on screen

        # screen.fill(BLACK)
        screen.blit(bg,bg_rect)
        draw_score()
        draw_shield()
        draw_lives()
        if boss_alive==True:
            draw_shield_boss()
            check_bullets_hit_boss()
        
        all_sprites.draw(screen)
        # flip to display
    pygame.display.flip()

pygame.quit()
