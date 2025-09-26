import pygame
from pygame.locals import * # type: ignore
import random
from pygame.math import Vector2
import sys

pygame.init()

DISPLAYSURF = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 80)
level_active = False

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

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    if level_active:
        ...
    else:
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
            level_active = True
    
    if level_active: # playing a level
        Grid.draw()
        level_text.draw()
        posbtn.draw()
        sndbtn.draw()

        print(pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(60)
    else: # menu between levels
        for event in pygame.event.get():
            if event.type == K_SPACE:
                level_active = True


