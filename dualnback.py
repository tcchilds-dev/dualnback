import pygame
from pygame.locals import *
import random
from pygame.math import Vector2
import sys

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

class GameButton:
    ...

class Main:
    ...

pygame.init()

DISPLAYSURF = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 80)
game_active = True
grid = Grid()

""" SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100) """

level_surface = game_font.render("n = 1", True, (255,255,255))
level_surface_rect = level_surface.get_rect(center = (400,50))

position_btn = pygame.Surface((340,200))
position_btn.fill(pygame.Color("white"))
position_text = game_font.render("POSITION", True, (0,0,0))
position_text_rect = position_text.get_rect(center = (200,675))

sound_btn = pygame.Surface((340,200))
sound_btn.fill(pygame.Color("white"))
sound_text = game_font.render("SOUND", True, (0,0,0))
sound_text_rect = sound_text.get_rect(center = (600,675))

main_game = Main()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    if game_active:
        ...
    else:
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
            game_active = True
    
    if game_active: # playing a level
        DISPLAYSURF.blit(grid.grid_top_left, (170,80))
        DISPLAYSURF.blit(grid.grid_top_center, (330,80))
        DISPLAYSURF.blit(grid.grid_top_right, (490,80))
        DISPLAYSURF.blit(grid.grid_mid_left, (170,240))
        DISPLAYSURF.blit(grid.grid_mid_center, (330,240))
        DISPLAYSURF.blit(grid.grid_mid_right, (490,240))
        DISPLAYSURF.blit(grid.grid_bot_left, (170,400))
        DISPLAYSURF.blit(grid.grid_bot_center, (330,400))
        DISPLAYSURF.blit(grid.grid_bot_right, (490,400))

        DISPLAYSURF.blit(level_surface, level_surface_rect)

        DISPLAYSURF.blit(position_btn, (30, 575))
        DISPLAYSURF.blit(position_text, position_text_rect)
        DISPLAYSURF.blit(sound_btn, (430, 575))
        DISPLAYSURF.blit(sound_text, sound_text_rect)

        print(pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(60)
    else: # menu between levels
        for event in pygame.event.get():
            if event.type == K_SPACE:
                game_active = True


