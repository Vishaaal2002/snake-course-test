# 🐍 CyberSnake: Neon Blitz

> A modern, vibrant neon arcade snake game built in pure Python with **zero external dependencies**!

---

## ⚡ Quick Start (Run in 5 Seconds)

You do **not** need to install any external libraries (`pip install` is not required!). The game uses Python's built-in standard library (`tkinter`).

### Method 1: Just Double-Click (Easiest on Windows)
Double-click the **[`run.bat`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/run.bat)** file in this folder.

### Method 2: From the Terminal / PowerShell
Open your terminal inside this folder and run:

```bash
python main.py
```

---

## 🎮 Game Controls

| Key | Action |
| :--- | :--- |
| **`W` / `↑`** | Move **UP** |
| **`S` / `↓`** | Move **DOWN** |
| **`A` / `←`** | Move **LEFT** |
| **`D` / `→`** | Move **RIGHT** |
| **`Space`** or **`Enter`** | Start Game / Pause / Resume / Restart |
| **`P`** | Pause / Unpause |
| **`R`** | Restart Match instantly |
| **`M`** | Toggle Sound (Mute / Unmute) |
| **`1`** | Select **Casual Mode** (Wall wrap-around, relaxed speed) |
| **`2`** | Select **Classic Mode** (Solid walls, standard speed) |
| **`3`** | Select **Insane Mode** (Super fast, hardcore challenge) |

---

## 🍎 Food & Power-Up Items

As you play, special timed bonus items will randomly materialize on the grid. Collect them before they vanish!

| Icon | Item | Effect |
| :---: | :--- | :--- |
| 🍎 | **Neon Apple** | **+10 Points**. Grows snake by 1 segment and feeds your combo meter. |
| ⭐ | **Golden Star** | **+35 Points**. Timed radiant treat! Awards double combo bonus and grows snake by 2 segments. |
| ⚡ | **Speed Surge** | **Power-up**. Boosts snake velocity to hyper speed for a massive adrenaline rush! |
| ❄️ | **Chill Freeze** | **Power-up**. Slows down time by 50% for 6 seconds, giving you precision steering. |
| ✂️ | **Tail Trimmer** | **Power-up**. Instantly trims up to 3 segments off your tail, escaping tight spots! |

---

## 🔥 Combo & High Score System

- **Combos**: Eating apples in quick succession activates the **Combo Multiplier** (`x2`, `x3`, etc.), rewarding bonus points for every subsequent fruit!
- **Persistent High Scores**: Your highest score is automatically saved to [`highscore.json`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/highscore.json) so your record is preserved between sessions.

---

## 🛠️ How to Customize (Great for Learning Python!)

All game settings are centralized in **[`constants.py`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/constants.py)**. You can easily tweak the game to your liking:

### 1. Change the Game Speed
Open [`constants.py`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/constants.py#L48-L64) and edit the `speed_ms` values:
```python
DIFFICULTIES = {
    "Easy":   {"speed_ms": 110, ...},  # Lower number = faster
    "Normal": {"speed_ms": 80,  ...},
    "Hard":   {"speed_ms": 50,  ...}
}
```

### 2. Change Snake or Board Colors
Check lines 15–45 in [`constants.py`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/constants.py#L15-L45) to customize your color palette (using standard HEX codes):
```python
COLOR_SNAKE_HEAD = "#38bdf8"       # Your favorite neon color
COLOR_BG_BOARD   = "#0d1322"       # Background grid tone
```

### 3. Change Board Size
In [`constants.py`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/constants.py#L6-L10):
```python
GRID_SIZE = 24  # Change grid dimensions (e.g. 20, 24, or 30)
CELL_SIZE = 25  # Pixel size per square
```

---

## 📂 Project Architecture

```
Gemini Course/
│
├── main.py          # Launcher script and Tkinter initialization
├── constants.py     # Central configuration (colors, speeds, points, grid)
├── game.py          # Core engine (movement, collisions, powerups, scoring)
├── ui.py            # Canvas renderer, animations, HUD, and input handling
├── sound.py         # Asynchronous retro chiptune audio synthesizer
├── particles.py     # Particle spark effects and floating text popups
├── highscore.json   # Persistent high score data file
├── run.bat          # 1-click Windows desktop launcher
└── README.md        # Comprehensive game guide and instructions
```

---

## ❓ Troubleshooting & FAQ

<details>
<summary><b>1. Does this require any third-party installation (like Pygame)?</b></summary>

No! The game is built completely on top of Python's standard library. As long as you have Python 3 installed, it works immediately out of the box.
</details>

<details>
<summary><b>2. How does the sound work?</b></summary>

The game generates retro chiptune sound effects through Windows `winsound.Beep` running on background daemon threads, ensuring smooth 60 FPS gameplay without audio stutter. Press **`M`** at any time to mute or unmute.
</details>

<details>
<summary><b>3. How do I reset my High Score?</b></summary>

Open [`highscore.json`](file:///C:/Users/Vishaal/OneDrive/Pictures/Desktop/Gemini%20Course/highscore.json) and set `"high_score": 0`, or delete the file entirely.
</details>

---

*Enjoy the game! Press **Space** to start slithering!* 🕹️
