#Initialising Pygame
import pygame
from sys import exit
from random import randint, choice


#Creating the Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)
    def player_input(self): #Keyboard inputs and character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 :
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_d]:  #Allowing Player to move to the right
            self.rect.x += 5
        if keys[pygame.K_a]:  #Allowing Player to move to the left
            self.rect.x -= 5
        if self.rect.x <= 0:  #Prevents Player from going out of the screen(Left side)
            self.rect.x = 0
        if self.rect.x >=800: #Returns the Player to the start if the character walks out of screen(right)
            self.rect.x = 0

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= ground:
            self.rect.bottom = ground
    def animation_stage(self): #Basic Player animation
        if self.rect.bottom < ground:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_stage()

#Creating Obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly': #For flies
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else: #For snails
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = ground

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self): #Animations(works for both)
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def collision_sprite(): #Checks if player collides with obstacles
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

#Displaying the score ->using time as score
def display_score():
    current_time = int((pygame.time.get_ticks() /1000)) - start_time
    score_surf = test_font.render('Score: '+str(current_time),False,(64,64,64))
    score_rect = score_surf.get_rect(center = (screen_x/2, 50))
    screen.blit(score_surf, score_rect)
    return current_time

#Pygame Settings
pygame.init()
screen_x = 800
screen_y = 400
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('The Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)

#Background Audio
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.5)
background_music.play(loops = -1)

#Starting game at menu
game_active = False
start_time = 0
score = 0

#Creating Player and Obstacle objects
player = pygame.sprite.GroupSingle()
player.sprite = Player()
obstacle_group = pygame.sprite.Group()

#Creating sky and ground
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
ground = 300


#Player Start Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (390, 200))

#END SCREEN TEXT
instructions_surf = test_font.render('PRESS SPACE TO START THE GAME!', False, (111,196,169))
instructions_rect = instructions_surf.get_rect(center =(screen_x/2,330))
game_name_surf = test_font.render('THE RUNNER', False, (111,196,169))
game_name_rect = game_name_surf.get_rect(center =(screen_x/2, 80))

#Timer for Obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


#Running -> Main Game
while True:
    #Exiting Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

    if game_active:
        #Graphics
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()


        #Player
        player.draw(screen)
        player.update()

        #obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        #Checking for collisions between player and obstacles
        game_active = collision_sprite()

    else:
        #Resetting player position and gravity
        player.sprite.rect.midbottom = (100, 300)
        player.sprite.gravity = 0

        #End Screen View
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name_surf, game_name_rect)

        #Score message
        score_message = test_font.render('Your current score: '+ str(score) , False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (screen_x/2, 330))
        if score != 0:
            screen.blit(score_message, score_message_rect)
        else: #If user does not have a score or has just started
            screen.blit(instructions_surf, instructions_rect)
            screen.blit(instructions_surf, instructions_rect)

    pygame.display.update()
    clock.tick(60)
