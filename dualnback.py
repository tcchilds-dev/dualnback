import pygame
from pygame.locals import * # type: ignore
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

# -------------------- THEME --------------------
tom_black = (36,40,59)
tom_darker = (32,35,51)
tom_charcoal = (20,22,31)
tom_grey = (64,69,91)
tom_button_grey = (48,52,69)
tom_yellow = (224,175,104)
tom_red = (247,118,142)
tom_green = (158,206,106)
tom_indigo = (122,162,247)
tom_purple = (187,154,247)
tom_blue = (113,146,166)

# -------------------- INIT --------------------
pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
background = pygame.Surface((800,800))
background.fill((tom_black))
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
    surface.fill((tom_grey))

    @staticmethod
    def draw():
        for idx, pos in enumerate(Grid.positions):
            DISPLAYSURF.blit(Grid.surface, pos)

class Flash:
    surface = pygame.Surface((140, 140))
    surface.fill((tom_red))
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
    def __init__(self, center, label, text_color=(tom_charcoal)):
        self.size = (340,160)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.base_color = (tom_darker)
        self.text_color = text_color
        self.surfrect = self.surface.get_rect(center=center)
        self.text = game_font.render(label, True, text_color)
        self.text_rect = self.text.get_rect(center=center)
        self.pressed = False

    def update(self, mouse_pos):
        if self.pressed:
            fill_color = (tom_indigo)
        elif self.surfrect.collidepoint(mouse_pos):
            fill_color = (tom_button_grey)
        else:
            fill_color = self.base_color
        
        # Clear surface
        self.surface.fill((0,0,0,0))
        
        rect = self.surface.get_rect()

        # --- Draw main rounded rect ---
        pygame.draw.rect(
            self.surface,
            fill_color,
            rect,
            border_radius=50
        )

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.surfrect)
        DISPLAYSURF.blit(self.text, self.text_rect)

class StartButton:
    def __init__(self, center, label, text_color=(tom_charcoal)):
        self.size = (340,160)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.base_color = (tom_darker)
        self.text_color = text_color
        self.surfrect = self.surface.get_rect(center=center)
        self.text = game_font.render(label, True, text_color)
        self.text_rect = self.text.get_rect(center=center)
    
    def update(self, mouse_pos):
        if self.surfrect.collidepoint(mouse_pos):
            fill_color = (tom_button_grey)
        else:
            fill_color = self.base_color
        
        # Clear surface
        self.surface.fill((0,0,0,0))
        
        rect = self.surface.get_rect()
        
        # --- Draw main rounded rect ---
        pygame.draw.rect(
            self.surface,
            fill_color,
            rect,
            border_radius=50
        )
    
    def draw(self):
        DISPLAYSURF.blit(self.surface, self.surfrect)
        DISPLAYSURF.blit(self.text, self.text_rect)

class LevelText:
    def __init__(self, text="n = 1", color=(tom_purple)):
        self.font = game_font
        self._text = text
        self._color = color
        self.surface = self.font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(center=(400, 40))

    @property
    def text(self): return self._text

    @text.setter
    def text(self, new_string):
        self._text = new_string
        self.surface = self.font.render(self._text, True, self._color)

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.rect)

class ScoreBoard:
    def __init__(self, text, center_pos=(0,0), color=(tom_yellow)):
        self.font = pygame.font.Font(None, 50)
        self._text = text
        self._color = color
        self.surface = self.font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(center=center_pos)
    
    @property
    def text(self): return self._text

    @text.setter
    def text(self, new_string):
        self._text = new_string
        self.surface = self.font.render(self._text, True, self._color)
    
    @property
    def color(self): return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color
        self.surface = self.font.render(self._text, True, self._color)

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.rect)

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
    correct: int = 0
    missed: int = 0
    mistakes: int = 0

    # --- UI ---
    correct_text = ScoreBoard(f"Correct: {correct}", (400,160))
    missed_text = ScoreBoard(f"Missed: {missed}", (400,240))
    mistakes_text = ScoreBoard(f"Mistakes: {mistakes}", (400,320))
    result_text = ScoreBoard("", (335,675))
    strtbtn = StartButton((400,480), "Start")
    posbtn = Button((200,675), "POSITION")
    sndbtn = Button((600,675), "SOUND")
    level_text = LevelText(f"n = {level}")

    while True:

        # --- Quit ---
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # --- Begin level ---
            if not level_active and event.type == pygame.MOUSEBUTTONDOWN:
                if strtbtn.surfrect.collidepoint(event.pos):
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

        # --- Mouse hover ---
        mouse_pos = pygame.mouse.get_pos()
        posbtn.update(mouse_pos)
        sndbtn.update(mouse_pos)
        strtbtn.update(mouse_pos)

        # --- Draw background ---
        DISPLAYSURF.blit(background, (0,0))

        # -- Results mode ---
        if not level_active:
            correct_text.draw()
            missed_text.draw()
            mistakes_text.draw()
            level_text.draw()
            result_text.draw()
            strtbtn.draw()

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
                    
                    # --- Update scoreboard text surfaces ---
                    correct_text.text = f"Correct: {correct}"
                    missed_text.text = f"Missed: {missed}"
                    mistakes_text.text = f"Mistakes: {mistakes}"

                    if correct >= ((correct + missed)*0.8) and mistakes < 4:
                        level += 1
                        result_text.text = "PASSED".strip()
                        result_text.color = tom_green
                        print("Proceeding to next level.")
                    else:
                        result_text.text = "FAILED".strip()
                        result_text.color = tom_red
                        print("Score not high enough to proceed.")
                    rounds_in_level = level + 20
                    level_text.text = f"n = {level}"

        # --- UI ---
        pygame.display.update()
        clock.tick(60)

# -------------------- RUN --------------------
if __name__ == "__main__":
    main()
