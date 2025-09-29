# Dual N-Back Game

## Description

This project is an implementation of the Dual N-Back cognitive task, built with Python and Pygame.
The player must remember the **position** of a red square and the **letter sound** spoken out loud, and indicate if either matches the one shown *n* steps earlier.

The game increases in difficulty as the player succeeds.

Note that the game will take a second to load the speech files on the first time running.

Features:

- Visual grid display using Pygame.
- Text-to-speech audio with Edge-TTS.
- Scoring system (correct, missed, mistakes).
- Level progression (each level has *n + 20* rounds).
- Themed UI with buttons and hover effects.

---

## How to Run

1. Clone this repository or download the project folder.
2. Install requirements:
` pip install -r requirements.txt `
3. Run the game:
` python dualnback.py `

---

## Requirements

- Python 3.10+
- Pygame
- Edge-TTS

All dependencies are listed in requirements.txt

---

## Files

- dualnback.py -- main game file
- spech_cache/ -- stores pre-generated TTS audio
- requirements.txt -- Python dependencies
- README.md -- this file

---

## Acknowledgements

- Inspired by Jaeggi et al.'s Dual N-Back task.
- Uses Microsoft's Edge-TTS for speech analysis.
