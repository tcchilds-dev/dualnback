import pygame
from pygame.locals import * # type: ignore
from pygame.math import Vector2
import pyttsx3
import random
import sys

pygame.init()

sound = pyttsx3.init()
sound.setProperty("rate", 120)
sound.startLoop(False)

DISPLAYSURF = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 80)
level_active = False

round_duration = 3000 # total length of round in ms
flash_duration = 500 # how long the block is visible in ms

round_count = 0
round_start = pygame.time.get_ticks()

class Grid:
    grid_top_left = pygame.Surface((140,140))
    grid_top_left.fill(pygame.Color("white"))

    grid_top_center = pygame.Surface((140,140))
    grid_top_center.fill(pygame.Color("white"))

    grid_top_right = pygame.Surface((140,140))
    grid_top_right.fill(pygame.Color("white"))

    grid_mid_left = pygame.Surface((140,140))
    grid_mid_left.fill(pygame.Color("white"))

    grid_mid_center = pygame.Surface((140,140))
    grid_mid_center.fill(pygame.Color("white"))

    grid_mid_right = pygame.Surface((140,140))
    grid_mid_right.fill(pygame.Color("white"))

    grid_bot_left = pygame.Surface((140,140))
    grid_bot_left.fill(pygame.Color("white"))

    grid_bot_center = pygame.Surface((140,140))
    grid_bot_center.fill(pygame.Color("white"))

    grid_bot_right = pygame.Surface((140,140))
    grid_bot_right.fill(pygame.Color("white"))

    @staticmethod
    def draw():
        DISPLAYSURF.blit(Grid.grid_top_left, (170,80))
        DISPLAYSURF.blit(Grid.grid_top_center, (330,80))
        DISPLAYSURF.blit(Grid.grid_top_right, (490,80))
        DISPLAYSURF.blit(Grid.grid_mid_left, (170,240))
        DISPLAYSURF.blit(Grid.grid_mid_center, (330,240))
        DISPLAYSURF.blit(Grid.grid_mid_right, (490,240))
        DISPLAYSURF.blit(Grid.grid_bot_left, (170,400))
        DISPLAYSURF.blit(Grid.grid_bot_center, (330,400))
        DISPLAYSURF.blit(Grid.grid_bot_right, (490,400))

class Flash:
    surface = pygame.Surface((140,140))
    surface.fill(pygame.Color("red"))
    positions = [(170,80), (330,80), (490,80),
                 (170,240), (330,240), (490,240),
                 (170,400), (330,400), (490,400)]
    current_pos = random.choice(positions)
    letters = ["C", "H", "K", "L", "Q", "R", "S", "T"]
    current_letter = random.choice(letters)

    @staticmethod
    def set_pos():
        Flash.current_pos = random.choice(Flash.positions)
    
    @staticmethod
    def draw():
        DISPLAYSURF.blit(Flash.surface, Flash.current_pos)

    @staticmethod
    def set_letter():
        Flash.current_letter = random.choice(Flash.letters)

    @staticmethod
    def say_letter(letter):
        sound.say(letter)
        sound.iterate()

class PositionButton:

    def __init__(self, color="white", text_color="black"):
        self.surface = pygame.Surface((340,200))
        self.color = self.surface.fill(pygame.Color(color))
        self.text = game_font.render("POSITION", True, text_color)
        self.rect = self.text.get_rect(center = (200,675))

    def draw(self):
        DISPLAYSURF.blit(self.surface, (30, 575))
        DISPLAYSURF.blit(self.text, self.rect)

class SoundButton:
    
    def __init__(self, color="white", text_color="black"):
        self.surface = pygame.Surface((340,200))
        self.color = self.surface.fill(pygame.Color(color))
        self.text = game_font.render("SOUND", True, text_color)
        self.rect = self.text.get_rect(center = (600,675))

    def draw(self):
        DISPLAYSURF.blit(self.surface, (430, 575))
        DISPLAYSURF.blit(self.text, self.rect)

class LevelText:

    def __init__(self, font=game_font, text="n = 1", color=(255,255,255)):
        self.font = font 
        self._text = text
        self._color = color
        self.surface = font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(center = (400,50))

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, new_string):
        self._text = new_string
    
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_value):
        self._color = new_value

    def draw(self):
        DISPLAYSURF.blit(level_text.surface, level_text.rect)

""" SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100) """

level_text = LevelText()
posbtn = PositionButton()
sndbtn = SoundButton()
sound_played = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sound.endLoop()
            pygame.quit()
            sys.exit()
    
    if not level_active and event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_SPACE, pygame.K_RETURN): 
            level_active = True
            round_count = 0
            round_start = pygame.time.get_ticks()
            show_block = True
            # pick first position
            current_pos = random.choice([...])
    
    if level_active:
        now = pygame.time.get_ticks()
        elapsed = now - round_start

        if elapsed < flash_duration:
            # phase 1: block visible
            Grid.draw()
            Flash.draw()
            if not sound_played:
                Flash.say_letter(Flash.current_letter)
                sound_played = True
        else:
            # phase 2: hide block
            Grid.draw()
        
        if elapsed >= round_duration:
            # advance to next round
            round_count += 1
            round_start = now
            # pick a new position for next round
            Flash.set_pos()
            Flash.set_letter()
            sound_played = False

        level_text.draw()
        posbtn.draw()
        sndbtn.draw()
        print(pygame.mouse.get_pos()) # just for testing
        sound.iterate()
        pygame.display.update()
        clock.tick(60)