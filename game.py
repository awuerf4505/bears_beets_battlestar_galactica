#!/usr/bin/env python3

import json
import pygame
import sys
import random

pygame.mixer.pre_init()
pygame.init()

# Window settings
TITLE = "Bears, Beets, Battlestar Galactica"
SIZE = (640, 640)
WIDTH = 640
HEIGHT = 640
FPS = 60
GRID_SIZE = 64
screen = pygame.display.set_mode(SIZE)

# Options
sound_on = True
music_on = True

# Controls
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
UP = pygame.K_UP
DOWN = pygame.K_DOWN
JUMP = pygame.K_SPACE
PAUSE = pygame.K_p
UNPAUSE = pygame.K_u
MUTEM = pygame.K_m
MUTES = pygame.K_s
# Levels
levels = ["levels/world-1.json",
          "levels/world-2.json",
          "levels/world-3.json",
          "levels/world-4.json"]

# Colors
TRANSPARENT = (0, 0, 0, 0)
DARK_BLUE = (16, 86, 103)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
FONT_SMN = pygame.font.Font("assets/fonts/galacticstormcondital.ttf", 28)
FONT_SM = pygame.font.Font("assets/fonts/galacticstormcondital.ttf", 35)
FONT_SMP = pygame.font.Font("assets/fonts/galacticstormcondital.ttf", 18)
FONT_SMT = pygame.font.Font("assets/fonts/galacticstorm.ttf", 39)
FONT_MD = pygame.font.Font("assets/fonts/Galactic-Bold.ttf", 64)
FONT_LG = pygame.font.Font("assets/fonts/thats_super.ttf", 32)

# Helper functions
def load_image(file_path):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))

    return img

def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
    if sound_on:
        if maxtime == 0:
            sound.play(loops, maxtime, fade_ms)
        else:
            sound.play(loops, maxtime, fade_ms)
    
def play_music():
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()        
stars = []
for n in range(500):
    x = random.randrange(0, 640)
    y = random.randrange(0, 640)
    r = random.randrange(1, 5)
    stars.append([x, y, r, r])
    
# Images
hero_walk1 = load_image("assets/character/normal.png")
hero_walk2 = load_image("assets/character/moving.png")
hero_jump = load_image("assets/character/moving.png")
hero_idle = load_image("assets/character/normal.png")
hero_images = {"run": [hero_walk1, hero_walk2],
               "jump": hero_jump,
               "idle": hero_idle}

block_images = {"TL": load_image("assets/tiles/top_left.png"),
                "FL": load_image("assets/tiles/floor_stone.png"),
                "TM": load_image("assets/tiles/middle_stone.png"),
                "TR": load_image("assets/tiles/top_right.png"),
                "ER": load_image("assets/tiles/top_right.png"),
                "EL": load_image("assets/tiles/top_left.png"),
                "TP": load_image("assets/tiles/top_stone.png"),
                "CN": load_image("assets/tiles/end_stone.png"),
                "LF": load_image("assets/tiles/alone_stone.png"),
                "SP": load_image("assets/tiles/top_stone.png"),
                "TL2": load_image("assets/tiles/top_left2.png"),
                "FL2": load_image("assets/tiles/floor_stone2.png"),
                "TM2": load_image("assets/tiles/middle_stone2.png"),
                "TR2": load_image("assets/tiles/top_right2.png"),
                "ER2": load_image("assets/tiles/top_right2.png"),
                "EL2": load_image("assets/tiles/top_left2.png"),
                "TP2": load_image("assets/tiles/top_stone2.png"),
                "CN2": load_image("assets/tiles/end_stone2.png"),
                "LF2": load_image("assets/tiles/alone_stone2.png"),
                "SP2": load_image("assets/tiles/top_stone2.png"),
                "GR" : load_image("assets/tiles/grass.png"),
                "DR": load_image("assets/tiles/dirt.png")}

player_img = load_image("assets/character/normal.png")
sound_img = load_image("assets/sounds/sound_on.png")
music_img = load_image("assets/sounds/music_on.png")
nosound_img = load_image("assets/sounds/sound_off.png")
nomusic_img = load_image("assets/sounds/music_off.png")
coin_img = load_image("assets/items/beet.png")
thing_img = load_image("assets/items/beet_basket.png")
magic_img = load_image("assets/items/magic.png")
heart_img = load_image("assets/items/heart.png")
oneup_img = load_image("assets/items/first_aid.png")
onedown_img = load_image("assets/items/one_down.png")
flag_img = load_image("assets/items/flag.png")
flagpole_img = load_image("assets/items/flagpole.png")
mini_img = load_image("assets/items/mini.png")
monster_img1 = load_image("assets/enemies/monster-1.png")
monster_img2 = load_image("assets/enemies/monster-2.png")
monster_images = [monster_img1, monster_img2]

bullet_img = load_image("assets/items/beet.png")

bear_img1 = load_image("assets/enemies/bear-1.png")
bear_img2 = load_image("assets/enemies/bear-2.png")
bear_images = [bear_img1, bear_img2]

float_img1 = load_image("assets/items/float-1.png")
float_images = [float_img1]

# Sounds
JUMP_SOUND = pygame.mixer.Sound("assets/sounds/jump.wav")
COIN_SOUND = pygame.mixer.Sound("assets/sounds/Pickup_Coin4.wav")
POWERUP_SOUND = pygame.mixer.Sound("assets/sounds/powerup.wav")
HURT_SOUND = pygame.mixer.Sound("assets/sounds/The_Schrute_Scream.wav")
DIE_SOUND = pygame.mixer.Sound("assets/sounds/bad.wav")
LEVELUP_SOUND = pygame.mixer.Sound("assets/sounds/powerup.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/The_Schrute_Scream.wav")
MAGIC_SOUND = pygame.mixer.Sound("assets/sounds/mGIC.wav")
WIN_SOUND = pygame.mixer.Sound("assets/sounds/mGIC.wav")

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

    def apply_gravity(self, level):
        self.vy += level.gravity
        self.vy = min(self.vy, level.terminal_velocity)

class Block(Entity):

    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Character(Entity):

    def __init__(self, images):
        super().__init__(0, 0, images['idle'])

        self.image_idle = images['idle']
        self.images_run_right = images['run']
        self.images_run_left = [pygame.transform.flip(img, 1, 0) for img in self.images_run_right]
        self.image_jump_right = images['jump']
        self.image_jump_left = pygame.transform.flip(self.image_jump_right, 1, 0)

        self.running_images = self.images_run_right
        self.image_index = 0
        self.steps = 0

        self.speed = 5
        self.jump_power = 20

        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.on_ground = True

        self.coin = 0
        self.score = 0
        self.lives = 3
        self.hearts = 3
        self.max_hearts = 3
        self.invincibility = 0

    def move_left(self):
        self.vx = -self.speed
        self.facing_right = False

    def move_right(self):
        self.vx = self.speed
        self.facing_right = True
        
    def move_right_fast(self):
        self.vx = self.speed * 5
        self.facing_right = True

    def move_left_fast(self):
        self.vx = -self.speed * 5
        self.facing_right = False

    def stop(self):
        self.vx = 0

    def jump(self, blocks):
        self.rect.y += 1

        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power
            play_sound(JUMP_SOUND)

        self.rect.y -= 1

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.on_ground = False
        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0
            
    def process_coins(self, coins):
        hit_list = pygame.sprite.spritecollide(self, coins, True)

        for coin in hit_list:
            play_sound(COIN_SOUND)
            self.score += coin.value
            self.coin += coin.value
        if self.score >= 10:
            self.lives += 1
            self.score = 0
                
    def process_things(self, things):
        hit_list = pygame.sprite.spritecollide(self, things, True)

        for things in hit_list:
            play_sound(COIN_SOUND)
            self.score += things.value

    def process_mini(self, mini):
        hit_list = pygame.sprite.spritecollide(self, mini, True)

        for mini in hit_list:
            play_sound(COIN_SOUND)
            self.max_hearts += 1
                     
    def process_magic(self, magic):
        hit_list = pygame.sprite.spritecollide(self, magic, True)

        if len(hit_list) > 0 and self.invincibility == 0:
            self.invincibility = int(0.75 * FPS)
            self.lives -= 1
            play_sound(MAGIC_SOUND)


    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)

        if len(hit_list) > 0 and self.invincibility == 0:
            play_sound(HURT_SOUND)
            self.hearts -= 1
            self.invincibility = int(0.75 * FPS)
            
    def process_powerups(self, powerups):
        hit_list = pygame.sprite.spritecollide(self, powerups, True)

        for p in hit_list:
            play_sound(POWERUP_SOUND)
            p.apply(self)

    def check_flag(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.flag, False)

        if len(hit_list) > 0:
            level.completed = True
            play_sound(LEVELUP_SOUND)

    def set_image(self):
        if self.on_ground:
            if self.vx != 0:
                if self.facing_right:
                    self.running_images = self.images_run_right
                else:
                    self.running_images = self.images_run_left

                self.steps = (self.steps + 1) % self.speed # Works well with 2 images, try lower number if more frames are in animation

                if self.steps == 0:
                    self.image_index = (self.image_index + 1) % len(self.running_images)
                    self.image = self.running_images[self.image_index]
            else:
                self.image = self.image_idle
        else:
            if self.facing_right:
                self.image = self.image_jump_right
            else:
                self.image = self.image_jump_left

    def die(self):
        self.lives -= 1

        if self.lives > 0:
            play_sound(DIE_SOUND)
        else:
            play_sound(GAMEOVER_SOUND)

    def respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.hearts = self.max_hearts
        self.invincibility = 0

    def update(self, level):
        self.process_enemies(level.enemies)
        self.apply_gravity(level)
        self.move_and_process_blocks(level.blocks)
        self.check_world_boundaries(level)
        self.set_image()

        if self.hearts > 0:
            self.process_coins(level.coins)
            self.process_magic(level.magic)
            self.process_things(level.things)
            self.process_mini(level.mini)
            self.process_powerups(level.powerups)
            self.check_flag(level)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            self.die()

class Coin(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 2

class Thing(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 5
        
class Magic(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Mini(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
                     
class Enemy(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images_left = images
        self.images_right = [pygame.transform.flip(img, 1, 0) for img in images]
        self.current_images = self.images_left
        self.image_index = 0
        self.steps = 0

    def reverse(self):
        self.vx *= -1

        if self.vx < 0:
            self.current_images = self.images_left
        else:
            self.current_images = self.images_right

        self.image = self.current_images[self.image_index]

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.reverse()

    def move_and_process_blocks(self):
        if self.vy < 0:
            sprite.kill()

    def set_images(self):
        if self.steps == 0:
            self.image = self.current_images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.current_images)

        self.steps = (self.steps + 1) % 20 # Nothing significant about 20. It just seems to work okay.

    def is_near(self, hero):
        return abs(self.rect.x - hero.rect.x) < 2 * WIDTH

    def update(self, level, hero):
        if self.is_near(hero):
            self.apply_gravity(level)
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_images()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = self.start_vx
        self.vy = self.start_vy
        self.image = self.images_left[0]
        self.steps = 0

class Bear(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        reverse = False
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True
        
        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0
                
class Monster(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    
    def move_and_process_blocks(self, blocks):
        reverse = False

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.vy >= 0:
                self.rect.bottom = block.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.vx < 0 and self.rect.left >= block.rect.left:
                    reverse = False

            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

        if reverse:
            self.reverse()
            
class Float(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        reverse = False
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

class OneUp(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.lives += 1

class OneDown(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.score -= 1

class Heart(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.hearts += 1
        character.hearts = max(character.hearts, character.max_hearts)

class Flag(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class Level():

    def __init__(self, file_path):
        self.starting_blocks = []
        self.starting_enemies = []
        self.starting_coins = []
        self.starting_magic = []
        self.starting_things = []
        self.starting_mini = []
        self.starting_powerups = []
        self.starting_flag = []

        
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.magic = pygame.sprite.Group()
        self.things = pygame.sprite.Group()
        self.mini = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()

        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        with open(file_path, 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.name = map_data['name']
        self.width = map_data['width'] * GRID_SIZE
        self.height = map_data['height'] * GRID_SIZE
        self.start_x = map_data['start'][0] * GRID_SIZE
        self.start_y = map_data['start'][1] * GRID_SIZE


        for item in map_data['blocks']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = block_images[item[2]]
            self.starting_blocks.append(Block(x, y, img))

        for item in map_data['bears']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Bear(x, y, bear_images))
            
        for item in map_data['monsters']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Monster(x, y, monster_images))

        for item in map_data['float']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Float(x, y, float_images))
            
        for item in map_data['coins']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_coins.append(Coin(x, y, coin_img))
            
        for item in map_data['magic']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_magic.append(Magic(x, y, magic_img))
            
        for item in map_data['things']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_things.append(Thing(x, y, thing_img))
                     
        for item in map_data['mini']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_mini.append(Mini(x, y, mini_img))
                     
        for item in map_data['oneups']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(OneUp(x, y, oneup_img))
            
        for item in map_data['onedown']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(OneDown(x, y, onedown_img))

        for item in map_data['hearts']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Heart(x, y, heart_img))

        for i, item in enumerate(map_data['flag']):
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE

            if i == 0:
                img = flag_img
            else:
                img = flagpole_img
            self.starting_flag.append(Flag(x, y, img))

        self.background_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.scenery_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

        if map_data['background-color'] != "":
            self.background_layer.fill(map_data['background-color'])

        if map_data['background-img'] != "":
            background_img = pygame.image.load(map_data['background-img'])

            if map_data['background-fill-y']:
                h = background_img.get_height()
                w = int(background_img.get_width() * HEIGHT / h)
                background_img = pygame.transform.scale(background_img, (w, HEIGHT))

            if "top" in map_data['background-position']:
                start_y = 0
            elif "bottom" in map_data['background-position']:
                start_y = self.height - background_img.get_height()

            if map_data['background-repeat-x']:
                for x in range(0, self.width, background_img.get_width()):
                    self.background_layer.blit(background_img, [x, start_y])
            else:
                self.background_layer.blit(background_img, [0, start_y])

        if map_data['scenery-img'] != "":
            scenery_img = pygame.image.load(map_data['scenery-img'])

            if map_data['scenery-fill-y']:
                h = scenery_img.get_height()
                w = int(scenery_img.get_width() * HEIGHT / h)
                scenery_img = pygame.transform.scale(scenery_img, (w, HEIGHT))

            if "top" in map_data['scenery-position']:
                start_y = 0
            elif "bottom" in map_data['scenery-position']:
                start_y = self.height - scenery_img.get_height()

            if map_data['scenery-repeat-x']:
                for x in range(0, self.width, scenery_img.get_width()):
                    self.scenery_layer.blit(scenery_img, [x, start_y])
            else:
                self.scenery_layer.blit(scenery_img, [0, start_y])

        pygame.mixer.music.load(map_data['music'])

        self.gravity = map_data['gravity']
        self.terminal_velocity = map_data['terminal-velocity']

        self.completed = False

        self.blocks.add(self.starting_blocks)
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.magic.add(self.starting_magic)
        self.things.add(self.starting_things)
        self.mini.add(self.starting_mini)
        self.powerups.add(self.starting_powerups)
        self.flag.add(self.starting_flag)

        self.active_sprites.add(self.coins, self.things, self.mini, self.magic, self.enemies, self.powerups)
        self.inactive_sprites.add(self.blocks, self.flag)

        self.inactive_sprites.draw(self.inactive_layer)

    def reset(self):
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.magic.add(self.starting_magic)
        self.things.add(self.starting_things)
        self.mini.add(self.starting_mini)
        self.powerups.add(self.starting_powerups)

        self.active_sprites.add(self.coins, self.magic, self.things, self.mini, self.enemies, self.powerups)

        for e in self.enemies:
            e.reset()

class Game():

    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5
    VICTORY = 6

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.done = False

        self.reset()

    def start(self):
        self.level = Level(levels[self.current_level])
        self.level.reset()
        self.hero.respawn(self.level)

    def advance(self):
        self.current_level += 1
        self.start()
        self.stage = Game.START

    def reset(self):
        self.hero = Character(hero_images)
        self.current_level = 0
        self.start()
        self.stage = Game.SPLASH

    def display_splash(self, surface):
        line1 = FONT_SMT.render(TITLE, 1, WHITE)
        line2 = FONT_SM.render("Press P to play.", 1, WHITE)
        line3 = FONT_SMN.render("Made by: Alison W.", 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        x3 = WIDTH / 2 - line3.get_width() / 2;
        y3 = y2 + line1.get_height() + 10;
        
        screen.fill(BLACK)
        for s in stars:
            pygame.draw.ellipse(screen, WHITE, s)
        pygame.draw.rect(screen, DARK_BLUE, [x1-8, y1-16, 700, 150])
        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))
        surface.blit(line3, (x3, y3))

    def display_message(self, surface, primary_text, secondary_text):
        line1 = FONT_MD.render(primary_text, 1, WHITE)
        line2 = FONT_SM.render(secondary_text, 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_stats(self, surface):
        level_text = FONT_SM.render(str(self.level.name), 1, WHITE)
        hearts_text = FONT_SM.render("Hearts: " + str(self.hero.hearts) + "/" + str(self.hero.max_hearts), 1, WHITE)
        lives_text = FONT_SM.render(" / " + str(self.hero.lives), 1, WHITE)
        score_text = FONT_SM.render("Score: " + str(self.hero.score), 1, WHITE)
        coin_text = FONT_SM.render("Coins: " + str(self.hero.coin), 1, WHITE)
        pause_text = FONT_SMP.render("Press P to Pause " , 1, WHITE)
        

        surface.blit(score_text, (WIDTH - score_text.get_width() - 32, 32))

        surface.blit(level_text, (32, 32))
        surface.blit(hearts_text, (32, 64))
        surface.blit(player_img, (16, 71))
        surface.blit(lives_text, (64, 96))
        surface.blit(coin_text, (32, 128))
        surface.blit(pause_text, (WIDTH - score_text.get_width() - 32, 64))
        if sound_on == True:
            surface.blit(sound_img, (32, 576))
        else:
            surface.blit(nosound_img, (32, 576))
            

        if music_on == True:
            
            surface.blit(music_img, (96, 576))
            
        else:
            surface.blit(nomusic_img, (96, 576))
            pygame.mixer.music.stop()

    def display_credits(self, surface):
        line1 = FONT_SMT.render(TITLE, 1, WHITE)
        score_text2 = FONT_SM.render("Final Score: " + str(self.hero.score), 1, WHITE)
        coin_text2 = FONT_SM.render("Total Coins: " + str(self.hero.coin), 1, WHITE)
        lives_text2 = FONT_SM.render("Lives Left: " + str(self.hero.lives), 1, WHITE)
        line2 = FONT_SMT.render("Press R to restart.", 1, WHITE)
        line3 = FONT_SMN.render("Made by: Alison W.", 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - score_text2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        x3 = WIDTH / 2 - coin_text2.get_width() / 2;
        y3 = y2 + line1.get_height() + 10;

        x4 = WIDTH / 2 -lives_text2.get_width() / 2;
        y4 = y3 + line1.get_height() + 10;

        x5 = WIDTH / 2 - line2.get_width() / 2;
        y5 = y4 + line1.get_height() + 10;
        
        x6 = WIDTH / 2 - line3.get_width() / 2;
        y6 = y5 + line1.get_height() + 10;        
        screen.fill(BLACK)
        for s in stars:
            pygame.draw.ellipse(screen, WHITE, s)
        pygame.draw.rect(screen, DARK_BLUE, [x1-8, y1-16, 700, 300])
        surface.blit(line1, (x1, y1))
        surface.blit(score_text2, (x2, y2))
        surface.blit(coin_text2, (x3, y3))
        surface.blit(lives_text2, (x4, y4))
        surface.blit(line2, (x5, y5))
        surface.blit(line3, (x6, y6))


    def process_events(self):
        global music_on
        global sound_on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                play_sound(WIN_SOUND)

            elif event.type == pygame.KEYDOWN:
                if self.stage == Game.SPLASH or self.stage == Game.START or self.stage == Game.PAUSED:
                    self.stage = Game.PLAYING
                    play_music()

                elif self.stage == Game.PLAYING:
                    if event.key == JUMP:
                        self.hero.jump(self.level.blocks)
                    if event.key == MUTEM:
                        music_on = not music_on
                    if event.key == MUTES:
                        sound_on = not sound_on
                    if event.key == PAUSE:
                        self.stage = Game.PAUSED
                        self.hero.jump(self.level.blocks)
                    else:
                        self.stage = Game.PLAYING
                elif self.stage == Game.LEVEL_COMPLETED:
                    self.advance()

                elif self.stage == Game.VICTORY or self.stage == Game.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset()

        pressed = pygame.key.get_pressed()

        if self.stage == Game.PLAYING:
            if pressed[LEFT]:
                self.hero.move_left()
            elif pressed[RIGHT]:
                self.hero.move_right()
            elif pressed [UP]:
                self.hero.move_right_fast()
            elif pressed [DOWN]:
                self.hero.move_left_fast()
            else:
                self.hero.stop()

    def update(self):
        if self.stage == Game.PLAYING:
            self.hero.update(self.level)
            self.level.enemies.update(self.level, self.hero)

        if self.level.completed:
            if self.current_level < len(levels) - 1:
                self.stage = Game.LEVEL_COMPLETED
            else:
                self.stage = Game.VICTORY
            pygame.mixer.music.stop()

        elif self.hero.lives == 0:
            self.stage = Game.GAME_OVER
            pygame.mixer.music.stop()

        elif self.hero.hearts == 0:
            self.level.reset()
            self.hero.respawn(self.level)

    def calculate_offset(self):
        x = -1 * self.hero.rect.centerx + WIDTH / 2

        if self.hero.rect.centerx < WIDTH / 2:
            x = 0
        elif self.hero.rect.centerx > self.level.width - WIDTH / 2:
            x = -1 * self.level.width + WIDTH

        return x, 0

    def draw(self):
        offset_x, offset_y = self.calculate_offset()

        self.level.active_layer.fill(TRANSPARENT)
        self.level.active_sprites.draw(self.level.active_layer)

        if self.hero.invincibility % 3 < 2:
            self.level.active_layer.blit(self.hero.image, [self.hero.rect.x, self.hero.rect.y])

        self.window.blit(self.level.background_layer, [offset_x / 3, offset_y])
        self.window.blit(self.level.scenery_layer, [offset_x / 2, offset_y])
        self.window.blit(self.level.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.level.active_layer, [offset_x, offset_y])

        self.display_stats(self.window)

        if self.stage == Game.SPLASH:
            self.display_splash(self.window)
        elif self.stage == Game.START:
            self.display_message(self.window, "Ready?!!!", "Press any key to start.")
        elif self.stage == Game.PAUSED:
            self.display_message(self.window, "PAUSED", "Press any key to contintue playing.")
        elif self.stage == Game.LEVEL_COMPLETED:
            self.display_message(self.window, "Level Complete", "Press any key to continue.")
        elif self.stage == Game.VICTORY:
            self.display_credits(self.window)
        elif self.stage == Game.GAME_OVER:
            self.display_message(self.window, "Game Over", "Press 'R' to restart.")

        pygame.display.flip()

    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.start()
    game.loop()
    pygame.quit()
    sys.exit()
