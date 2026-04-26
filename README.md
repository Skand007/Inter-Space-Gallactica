# 🎮 Inter‑Space Gallactica — Retro Arcade Edition

A fast‑paced, two‑player retro space duel built with **Python + Pygame**, redesigned with a modular architecture and a full arcade presentation.

## ✨ Features

- 🚀 Two‑player local space duel
- 🧑‍🚀 Player name input (retro screen, uppercase, blinking cursor)
- 🏆 Per‑player stats stored in `scores.json`:
  - `wins`
  - `points` (total hits across all matches)
- 🎨 Retro visuals:
  - Animated starfield background
  - CRT scanline overlay
  - Flashing “PRESS ENTER TO START”
  - Pixel‑style fonts (Courier New)
- 🔊 Retro SFX (shots + hits)
- 🎮 Keyboard + optional gamepad support
- 📦 Cross‑platform desktop (macOS / Windows / Linux)

---

## 🕹️ Controls

### 🟡 Player 1 (Left)

- Move: **W A S D**
- Shoot: **TAB**

### 🔴 Player 2 (Right)

- Move: **Arrow Keys**
- Shoot: **ENTER**

### 🎮 Gamepad (optional, if connected)

- Move: Left stick / D‑pad
- Shoot: Button A / Cross

---

## 🔁 Flow

1. Start screen
2. Press **ENTER** → Start Game
3. Enter **PLAYER 1 NAME** (uppercase, max 12 chars)
4. Enter **PLAYER 2 NAME**
5. Play match
6. Game Over screen:
   - Shows winner
   - Shows match points
   - Shows cumulative stats from `scores.json`
7. Press **ENTER** → back to menu  
   Press **ESC** → quit

---

## 📸 Screenshots
Home screen layout
![Start Screen](SS_home.png)

Gameplay showcase
![Gameplay](SS_game.png)

Game in action showcase
![Action](SS_action.png)

---

## 📦 Requirements

### ✅ Supported Python Versions (IMPORTANT)
Pygame does NOT support Python 3.14 yet.  
If you use Python 3.14, the game will crash with:
NotImplementedError: mixer module not available

### ✔ Use one of these supported versions:
- Python 3.11 (recommended)
- Python 3.12
- Python 3.10
- Python 3.9

### ❌ Not supported:
- Python 3.13 (partial, unstable)
- Python 3.14 (mixer/audio completely broken)

---

## 📦 Installation & Running

### 1. Install a supported Python version
Check your Python version:
python3 --version

If it shows 3.14.x, install Python 3.11 instead.

macOS (Homebrew):
brew install python@3.11

### 2. Create a virtual environment (recommended)
python3.11 -m venv game_venv
source game_venv/bin/activate

### 3. Install dependencies
pip install pygame

### 4. Run the game
python main.py
or
python3 main.py
