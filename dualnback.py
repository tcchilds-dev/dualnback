import pygame
from pygame.locals import *
import random
import sys
import asyncio
import edge_tts
import os

# -------------------- CONFIG --------------------
WINDOW_SIZE = (800, 800)
ROUND_DURATION = 3000   # total length of round (ms)
FLASH_DURATION = 500    # how long block is visible (ms)
LETTERS = ["C", "H", "K", "L", "Q", "R", "S", "T"]  # Jaeggi set
VOICE = "en-US-JennyNeural"
SPEECH_FOLDER = "speech_cache"

# -------------------- INIT --------------------
pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
background = pygame.Surface((800,800))
background.fill(pygame.Color("black"))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 80)

# -------------------- EDGE-TTS --------------------
async def gen_speech(letter: str, out_file: str):
    """Generate a spoken letter using edge-tts and save to file."""
    if not os.path.exists(out_file):
        comm = edge_tts.Communicate(letter, VOICE)
        await comm.save(out_file)

def ensure_speech_files():
    """Pre-generate speech files for all letters."""
    if not os.path.exists(SPEECH_FOLDER):
        os.makedirs(SPEECH_FOLDER)
    for letter in LETTERS:
        fname = os.path.join(SPEECH_FOLDER, f"{letter}.mp3")
        if not os.path.exists(fname):
            asyncio.run(gen_speech(letter, fname))

def load_sounds():
    """Load all pre-generated sounds into a dict."""
    sounds = {}
    for letter in LETTERS:
        fname = os.path.join(SPEECH_FOLDER, f"{letter}.mp3")
        sounds[letter] = pygame.mixer.Sound(fname)
    return sounds

# -------------------- CLASSES --------------------
class Grid:
    cell_size = 140
    positions = [
        (170, 80), (330, 80), (490, 80),
        (170, 240), (330, 240), (490, 240),
        (170, 400), (330, 400), (490, 400)
    ]
    surface = pygame.Surface((cell_size, cell_size))
    surface.fill(pygame.Color("white"))

    @staticmethod
    def draw():
        for idx, pos in enumerate(Grid.positions):
            DISPLAYSURF.blit(Grid.surface, pos)

class Flash:
    surface = pygame.Surface((140, 140))
    surface.fill(pygame.Color("red"))
    current_pos = random.choice(Grid.positions)
    current_letter = random.choice(LETTERS)

    @staticmethod
    def set_pos():
        Flash.current_pos = random.choice(Grid.positions)
    
    @staticmethod
    def set_letter():
        Flash.current_letter = random.choice(LETTERS)
    
    @staticmethod
    def draw():
        DISPLAYSURF.blit(Flash.surface, Flash.current_pos)

class Button:
    def __init__(self, center, label, color="white", text_color="black"):
        self.surface = pygame.Surface((340, 200))
        self.base_color = pygame.Color(color)
        self.text_color = text_color
        self.surfrect = self.surface.get_rect(center=center)
        self.text = game_font.render(label, True, text_color)
        self.text_rect = self.text.get_rect(center=center)
        self.pressed = False

    def update(self, mouse_pos):
        if self.pressed:
            self.surface.fill(pygame.Color("green"))
        elif self.surfrect.collidepoint(mouse_pos):
            self.surface.fill(pygame.Color("lightgrey"))
        else:
            self.surface.fill(self.base_color)

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.surfrect)
        DISPLAYSURF.blit(self.text, self.text_rect)

class LevelText:
    def __init__(self, text="n = 1", color=(255,255,255)):
        self.font = game_font
        self._text = text
        self._color = color
        self.surface = self.font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(center=(400, 50))

    @property
    def text(self): return self._text
    @text.setter
    def text(self, new_string):
        self._text = new_string
        self.surface = self.font.render(self._text, True, self._color)

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.rect)

class ScoreBoard:
    ...

# -------------------- MAIN GAME --------------------
def main():
    # --- Generate & load sounds ---
    ensure_speech_files()
    sounds = load_sounds()

    # --- Game state ---
    level = 1
    rounds_in_level = level + 20
    round_count = 0
    round_start = pygame.time.get_ticks()
    level_active = False
    sound_played = False

    # --- Score ---
    pos_history = []
    letter_history = []
    correct = 0
    missed = 0
    mistakes = 0

    # --- UI ---
    posbtn = Button((200, 675), "POSITION")
    sndbtn = Button((600, 675), "SOUND")
    level_text = LevelText(f"n = {level}")

    while True:

        # --- Quit ---
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # --- Begin level ---
            if not level_active and event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    level_active = True
                    round_count = 0
                    round_start = pygame.time.get_ticks()
                    correct = 0
                    missed = 0
                    mistakes = 0
                    pos_history.clear()
                    letter_history.clear()

            # --- Button functionality ---
            if level_active and event.type == pygame.MOUSEBUTTONDOWN:
                if posbtn.surfrect.collidepoint(event.pos):
                    posbtn.pressed = True
                if sndbtn.surfrect.collidepoint(event.pos):
                    sndbtn.pressed = True

        mouse_pos = pygame.mouse.get_pos()
        posbtn.update(mouse_pos)
        sndbtn.update(mouse_pos)

        # --- Draw background ---
        DISPLAYSURF.blit(background, (0,0))

        # --- Level ---
        if level_active:
            now = pygame.time.get_ticks()
            elapsed = now - round_start
            posbtn.draw()
            sndbtn.draw()
            level_text.draw()

            if elapsed < FLASH_DURATION:
                Grid.draw()
                Flash.draw()
                if not sound_played:
                    sounds[Flash.current_letter].play()
                    sound_played = True
            else:
                Grid.draw()

            # --- Round end ---
            if elapsed >= ROUND_DURATION:
                round_count += 1
                round_start = now

                # --- Score check (if enough history) ---
                if round_count > level:
                    # check position n-back
                    if Flash.current_pos == pos_history[-level]:
                        if posbtn.pressed: correct += 1
                        else: missed += 1
                    else:
                        if posbtn.pressed: mistakes += 1
                    # check letter n-back
                    if Flash.current_letter == letter_history[-level]:
                        if sndbtn.pressed: correct += 1
                        else: missed += 1
                    else:
                        if sndbtn.pressed: mistakes += 1
                
                # --- Update history ---
                pos_history.append(Flash.current_pos)
                letter_history.append(Flash.current_letter)
                
                # --- New round setup ---
                Flash.set_pos()
                Flash.set_letter()
                sound_played = False
                posbtn.pressed = False
                sndbtn.pressed = False                

                # --- End of level check ---
                if round_count >= rounds_in_level:
                    level_active = False
                    print(f"Correct: {correct}\nMissed: {missed}\nMistakes: {mistakes}")
                    if correct >= ((correct + missed)*0.8) and mistakes < 4:
                        level += 1
                        print("Proceeding to next level.")
                    else:
                        print("Score not high enough to proceed.")
                    rounds_in_level = level + 20
                    level_text.text = f"n = {level}"

        # --- UI ---
        pygame.display.update()
        clock.tick(60)

# -------------------- RUN --------------------
if __name__ == "__main__":
    main()
