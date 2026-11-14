"""
ui.py - Tkinter GUI, visual rendering, HUD, and input handling for CyberSnake
"""

import math
import tkinter as tk
from tkinter import font as tkfont
from constants import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_SIZE,
    COLOR_BG_BOARD,
    COLOR_BG_HEADER,
    COLOR_BG_MAIN,
    COLOR_FOOD_APPLE,
    COLOR_FOOD_GOLDEN,
    COLOR_GRID_LINE,
    COLOR_POWERUP_CUT,
    COLOR_POWERUP_SLOW,
    COLOR_POWERUP_SPEED,
    COLOR_SNAKE_BODY_END,
    COLOR_SNAKE_BODY_START,
    COLOR_SNAKE_EYE,
    COLOR_SNAKE_HEAD,
    COLOR_SNAKE_PUPIL,
    COLOR_TEXT_ACCENT,
    COLOR_TEXT_GOLD,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_PRIMARY,
    DIFFICULTIES,
    GRID_SIZE,
    HEADER_HEIGHT,
    TOTAL_HEIGHT,
    TOTAL_WIDTH,
    TYPE_APPLE,
    TYPE_CUT,
    TYPE_GOLDEN,
    TYPE_SLOW,
    TYPE_SPEED,
)
from game import GameState
from particles import ParticleSystem
from sound import SoundManager


class CyberSnakeUI:
    """Manages the complete graphical user interface and animation loop."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CyberSnake // Neon Blitz")
        self.root.geometry(f"{TOTAL_WIDTH}x{TOTAL_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG_MAIN)

        # Center the window on user's screen
        self._center_window()

        # Engine Components
        self.game = GameState()
        self.sound = SoundManager()
        self.particles = ParticleSystem()

        # Animation states
        self.blink_state = True
        self.pulse_phase = 0.0

        # Build UI layout
        self._setup_widgets()
        self._bind_keys()

        # Start master update loops
        self._schedule_game_tick()
        self._schedule_fx_tick()
        self._schedule_blink_tick()

    def _center_window(self):
        """Centers the application window on user display."""
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        pos_x = max(0, (screen_w - TOTAL_WIDTH) // 2)
        pos_y = max(0, (screen_h - TOTAL_HEIGHT) // 2 - 20)
        self.root.geometry(f"{TOTAL_WIDTH}x{TOTAL_HEIGHT}+{pos_x}+{pos_y}")
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)
        self.root.focus_force()

    def _setup_widgets(self):
        """Constructs HUD header and main game canvas."""
        # Top HUD Bar
        self.header_frame = tk.Frame(
            self.root,
            width=TOTAL_WIDTH,
            height=HEADER_HEIGHT,
            bg=COLOR_BG_HEADER,
            highlightthickness=0,
        )
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        self.header_frame.pack_propagate(False)

        # Header elements
        self.hud_score_label = tk.Label(
            self.header_frame,
            text="SCORE: 0",
            font=("Segoe UI", 14, "bold"),
            fg=COLOR_TEXT_ACCENT,
            bg=COLOR_BG_HEADER,
        )
        self.hud_score_label.pack(side=tk.LEFT, padx=18, pady=8)

        self.hud_combo_label = tk.Label(
            self.header_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_FOOD_GOLDEN,
            bg=COLOR_BG_HEADER,
        )
        self.hud_combo_label.pack(side=tk.LEFT, padx=4, pady=8)

        # Right-side HUD elements (High Score, Audio status, Difficulty)
        self.hud_sound_label = tk.Label(
            self.header_frame,
            text="🔊 [M]",
            font=("Segoe UI", 11),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG_HEADER,
            cursor="hand2",
        )
        self.hud_sound_label.pack(side=tk.RIGHT, padx=16, pady=8)
        self.hud_sound_label.bind("<Button-1>", lambda e: self.toggle_sound())

        self.hud_diff_label = tk.Label(
            self.header_frame,
            text=f"MODE: {self.game.difficulty_name.upper()}",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG_HEADER,
        )
        self.hud_diff_label.pack(side=tk.RIGHT, padx=12, pady=8)

        self.hud_high_label = tk.Label(
            self.header_frame,
            text=f"🏆 {self.game.high_score}",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT_GOLD,
            bg=COLOR_BG_HEADER,
        )
        self.hud_high_label.pack(side=tk.RIGHT, padx=14, pady=8)

        # Main Game Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg=COLOR_BG_BOARD,
            highlightthickness=0,
            cursor="crosshair",
        )
        self.canvas.pack(side=tk.BOTTOM)

    def _bind_keys(self):
        """Binds keyboard inputs for movement, menus, sound and difficulty."""
        # Movement
        for key in ["<Up>", "<w>", "<W>"]:
            self.root.bind(key, lambda e: self._handle_input(0, -1))
        for key in ["<Down>", "<s>", "<S>"]:
            self.root.bind(key, lambda e: self._handle_input(0, 1))
        for key in ["<Left>", "<a>", "<A>"]:
            self.root.bind(key, lambda e: self._handle_input(-1, 0))
        for key in ["<Right>", "<d>", "<D>"]:
            self.root.bind(key, lambda e: self._handle_input(1, 0))

        # Controls & Toggles
        self.root.bind("<space>", lambda e: self._handle_action_button())
        self.root.bind("<Return>", lambda e: self._handle_action_button())
        self.root.bind("<p>", lambda e: self.toggle_pause())
        self.root.bind("<P>", lambda e: self.toggle_pause())
        self.root.bind("<r>", lambda e: self.restart_game())
        self.root.bind("<R>", lambda e: self.restart_game())
        self.root.bind("<m>", lambda e: self.toggle_sound())
        self.root.bind("<M>", lambda e: self.toggle_sound())

        # Difficulty shortcuts
        self.root.bind("1", lambda e: self.change_difficulty("Easy"))
        self.root.bind("2", lambda e: self.change_difficulty("Normal"))
        self.root.bind("3", lambda e: self.change_difficulty("Hard"))

    def _handle_input(self, dx: int, dy: int):
        """Processes directional key presses."""
        if self.game.status == "PLAYING":
            self.game.change_direction(dx, dy)

    def _handle_action_button(self):
        """Handles Space or Enter key depending on current state."""
        if self.game.status == "MENU":
            self.game.status = "PLAYING"
            self.sound.play_golden()
        elif self.game.status == "GAME_OVER":
            self.restart_game()
        elif self.game.status in ["PLAYING", "PAUSED"]:
            self.toggle_pause()

    def toggle_pause(self):
        """Pauses or resumes ongoing game."""
        if self.game.status == "PLAYING":
            self.game.status = "PAUSED"
            self.sound.play_click()
        elif self.game.status == "PAUSED":
            self.game.status = "PLAYING"
            self.sound.play_click()
        self.render()

    def toggle_sound(self):
        """Toggles sound on or off."""
        is_muted = self.sound.toggle_mute()
        icon = "🔇 [M]" if is_muted else "🔊 [M]"
        self.hud_sound_label.config(text=icon)

    def change_difficulty(self, diff_name: str):
        """Switches difficulty and updates HUD."""
        self.game.set_difficulty(diff_name)
        self.hud_diff_label.config(text=f"MODE: {diff_name.upper()}")
        self.sound.play_click()
        self.render()

    def restart_game(self):
        """Resets the game state and begins a new match."""
        diff = self.game.difficulty_name
        self.game.reset_game()
        self.game.set_difficulty(diff)
        self.game.status = "PLAYING"
        self.particles.clear()
        self.sound.play_click()
        self.render()

    # -------------------------------------------------------------
    # Tick Loops
    # -------------------------------------------------------------
    def _schedule_game_tick(self):
        """Executes logic steps based on game speed."""
        if self.game.status == "PLAYING":
            event = self.game.update_tick()
            self._handle_game_event(event)
            self.render()

        delay = self.game.get_current_tick_delay()
        self.root.after(delay, self._schedule_game_tick)

    def _schedule_fx_tick(self):
        """Smooth 30 FPS tick for floating text, particle dynamics, and pulsing."""
        self.pulse_phase += 0.12
        if self.pulse_phase > 6.28:
            self.pulse_phase = 0.0

        if self.game.status in ["PLAYING", "PAUSED"]:
            self.particles.update()
            self._draw_particles()

        self.root.after(33, self._schedule_fx_tick)

    def _schedule_blink_tick(self):
        """Blinks start and pause text for retro arcade aesthetic."""
        self.blink_state = not self.blink_state
        if self.game.status in ["MENU", "PAUSED"]:
            self.render()
        self.root.after(550, self._schedule_blink_tick)

    # -------------------------------------------------------------
    # Event Reactions
    # -------------------------------------------------------------
    def _handle_game_event(self, event: dict):
        """Dispatches sounds and visual particles triggered by game logic."""
        if event["game_over"]:
            self.sound.play_game_over()
            head_x, head_y = self.game.snake[0]
            cx = head_x * CELL_SIZE + CELL_SIZE // 2
            cy = head_y * CELL_SIZE + CELL_SIZE // 2
            self.particles.spawn_burst(cx, cy, "#ef4444", count=18)
            return

        if event["eaten"] == TYPE_APPLE:
            self.sound.play_apple()
            head_x, head_y = self.game.snake[0]
            cx = head_x * CELL_SIZE + CELL_SIZE // 2
            cy = head_y * CELL_SIZE + CELL_SIZE // 2
            self.particles.spawn_burst(cx, cy, COLOR_FOOD_APPLE, count=10)
            txt = f"+{event['points_earned']}"
            if event["combo_active"]:
                txt += f" (x{self.game.combo})!"
            self.particles.spawn_text(cx, cy - 8, txt, COLOR_FOOD_APPLE)

        elif event["eaten"] == TYPE_GOLDEN:
            self.sound.play_golden()
            head_x, head_y = self.game.snake[0]
            cx = head_x * CELL_SIZE + CELL_SIZE // 2
            cy = head_y * CELL_SIZE + CELL_SIZE // 2
            self.particles.spawn_burst(cx, cy, COLOR_FOOD_GOLDEN, count=16)
            self.particles.spawn_text(cx, cy - 10, f"⭐ +{event['points_earned']}!", COLOR_FOOD_GOLDEN)

        if event["powerup_activated"] == TYPE_SPEED:
            self.sound.play_powerup()
            head_x, head_y = self.game.snake[0]
            cx = head_x * CELL_SIZE + CELL_SIZE // 2
            cy = head_y * CELL_SIZE + CELL_SIZE // 2
            self.particles.spawn_burst(cx, cy, COLOR_POWERUP_SPEED, count=14)
            self.particles.spawn_text(cx, cy - 10, "⚡ SPEED BOOST!", COLOR_POWERUP_SPEED)

        elif event["powerup_activated"] == TYPE_SLOW:
            self.sound.play_powerup()
            head_x, head_y = self.game.snake[0]
            cx = head_x * CELL_SIZE + CELL_SIZE // 2
            cy = head_y * CELL_SIZE + CELL_SIZE // 2
            self.particles.spawn_burst(cx, cy, COLOR_POWERUP_SLOW, count=14)
            self.particles.spawn_text(cx, cy - 10, "❄️ SLOW MOTION!", COLOR_POWERUP_SLOW)

        elif event["powerup_activated"] == TYPE_CUT:
            self.sound.play_shrink()
            head_x, head_y = self.game.snake[0]
            cx = head_x * CELL_SIZE + CELL_SIZE // 2
            cy = head_y * CELL_SIZE + CELL_SIZE // 2
            self.particles.spawn_burst(cx, cy, COLOR_POWERUP_CUT, count=14)
            self.particles.spawn_text(cx, cy - 10, "✂️ SHRUNK!", COLOR_POWERUP_CUT)

    # -------------------------------------------------------------
    # Rendering & Drawing
    # -------------------------------------------------------------
    def render(self):
        """Draws the entire frame: HUD updates, board, snake, food, overlays."""
        # 1. Update HUD labels
        self.hud_score_label.config(text=f"SCORE: {self.game.score}")
        self.hud_high_label.config(text=f"🏆 {self.game.high_score}")

        if self.game.combo > 1:
            self.hud_combo_label.config(text=f"x{self.game.combo} COMBO 🔥")
        else:
            self.hud_combo_label.config(text="")

        # 2. Clear canvas
        self.canvas.delete("all")

        # 3. Draw grid lines
        self._draw_grid()

        # 4. Draw food & special items
        self._draw_food()

        # 5. Draw snake
        self._draw_snake()

        # 6. Draw active particles and texts
        self._draw_particles()

        # 7. Draw modal overlays based on state
        if self.game.status == "MENU":
            self._draw_menu_overlay()
        elif self.game.status == "PAUSED":
            self._draw_paused_overlay()
        elif self.game.status == "GAME_OVER":
            self._draw_game_over_overlay()

    def _draw_grid(self):
        """Draws a subtle neon grid pattern on canvas."""
        for x in range(0, BOARD_WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, BOARD_HEIGHT, fill=COLOR_GRID_LINE, width=1)
        for y in range(0, BOARD_HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, BOARD_WIDTH, y, fill=COLOR_GRID_LINE, width=1)

    def _draw_food(self):
        """Draws regular apple and any active special power-up item."""
        # Draw Normal Apple
        ax, ay = self.game.apple
        px = ax * CELL_SIZE
        py = ay * CELL_SIZE
        pad = 3
        # Apple body
        self.canvas.create_oval(
            px + pad,
            py + pad + 2,
            px + CELL_SIZE - pad,
            py + CELL_SIZE - pad + 2,
            fill=COLOR_FOOD_APPLE,
            outline="#fb7185",
            width=2,
        )
        # Apple leaf stem
        self.canvas.create_line(
            px + CELL_SIZE // 2,
            py + pad + 2,
            px + CELL_SIZE // 2 + 3,
            py + pad - 2,
            fill="#22c55e",
            width=2,
        )

        # Draw Special Food if active
        sf = self.game.special_food
        if sf:
            sx = sf["x"] * CELL_SIZE
            sy = sf["y"] * CELL_SIZE
            sp_type = sf["type"]

            # Pulsing size effect
            pulse_offset = math.sin(self.pulse_phase * 2) * 2.0
            p_pad = max(2, int(4 - pulse_offset))

            if sp_type == TYPE_GOLDEN:
                # Golden Star Diamond
                mid_x = sx + CELL_SIZE // 2
                mid_y = sy + CELL_SIZE // 2
                r = CELL_SIZE // 2 - p_pad
                points = [
                    mid_x, mid_y - r - 2,
                    mid_x + r, mid_y,
                    mid_x, mid_y + r + 2,
                    mid_x - r, mid_y,
                ]
                self.canvas.create_polygon(
                    points,
                    fill=COLOR_FOOD_GOLDEN,
                    outline="#fef08a",
                    width=2,
                )
            elif sp_type == TYPE_SPEED:
                # Purple Bolt Box
                self.canvas.create_oval(
                    sx + p_pad, sy + p_pad,
                    sx + CELL_SIZE - p_pad, sy + CELL_SIZE - p_pad,
                    fill=COLOR_POWERUP_SPEED,
                    outline="#d8b4fe",
                    width=2,
                )
                self.canvas.create_text(
                    sx + CELL_SIZE // 2,
                    sy + CELL_SIZE // 2,
                    text="⚡",
                    font=("Segoe UI", 11, "bold"),
                    fill="#ffffff",
                )
            elif sp_type == TYPE_SLOW:
                # Cyan Freeze Orb
                self.canvas.create_oval(
                    sx + p_pad, sy + p_pad,
                    sx + CELL_SIZE - p_pad, sy + CELL_SIZE - p_pad,
                    fill=COLOR_POWERUP_SLOW,
                    outline="#bae6fd",
                    width=2,
                )
                self.canvas.create_text(
                    sx + CELL_SIZE // 2,
                    sy + CELL_SIZE // 2,
                    text="❄",
                    font=("Segoe UI", 10, "bold"),
                    fill="#ffffff",
                )
            elif sp_type == TYPE_CUT:
                # Pink Shrink Scissor
                self.canvas.create_oval(
                    sx + p_pad, sy + p_pad,
                    sx + CELL_SIZE - p_pad, sy + CELL_SIZE - p_pad,
                    fill=COLOR_POWERUP_CUT,
                    outline="#fbcfe8",
                    width=2,
                )
                self.canvas.create_text(
                    sx + CELL_SIZE // 2,
                    sy + CELL_SIZE // 2,
                    text="✂",
                    font=("Segoe UI", 9, "bold"),
                    fill="#ffffff",
                )

    def _draw_snake(self):
        """Draws snake body with color gradient and head with dynamic eyes."""
        snake_len = len(self.game.snake)
        if snake_len == 0:
            return

        # Draw body segments backwards from tail to head
        for i in range(snake_len - 1, 0, -1):
            seg_x, seg_y = self.game.snake[i]
            px = seg_x * CELL_SIZE
            py = seg_y * CELL_SIZE

            # Subtle gradient color transition
            ratio = i / max(1, snake_len)
            color = self._interpolate_color(COLOR_SNAKE_BODY_START, COLOR_SNAKE_BODY_END, ratio)

            pad = 2
            self.canvas.create_rectangle(
                px + pad,
                py + pad,
                px + CELL_SIZE - pad,
                py + CELL_SIZE - pad,
                fill=color,
                outline="",
            )

        # Draw Head with glowing border
        head_x, head_y = self.game.snake[0]
        hx = head_x * CELL_SIZE
        hy = head_y * CELL_SIZE
        h_pad = 1

        self.canvas.create_rectangle(
            hx + h_pad,
            hy + h_pad,
            hx + CELL_SIZE - h_pad,
            hy + CELL_SIZE - h_pad,
            fill=COLOR_SNAKE_HEAD,
            outline="#7dd3fc",
            width=2,
        )

        # Draw Eyes facing current movement direction
        dx, dy = self.game.direction
        eye_radius = 2.5
        pupil_radius = 1.2
        cx = hx + CELL_SIZE / 2
        cy = hy + CELL_SIZE / 2

        # Eye offset positions relative to direction
        if dx == 1:  # Facing right
            eye1 = (cx + 5, cy - 5)
            eye2 = (cx + 5, cy + 5)
        elif dx == -1:  # Facing left
            eye1 = (cx - 5, cy - 5)
            eye2 = (cx - 5, cy + 5)
        elif dy == -1:  # Facing up
            eye1 = (cx - 5, cy - 5)
            eye2 = (cx + 5, cy - 5)
        else:  # Facing down
            eye1 = (cx - 5, cy + 5)
            eye2 = (cx + 5, cy + 5)

        for ex, ey in [eye1, eye2]:
            self.canvas.create_oval(
                ex - eye_radius, ey - eye_radius,
                ex + eye_radius, ey + eye_radius,
                fill=COLOR_SNAKE_EYE, outline="",
            )
            self.canvas.create_oval(
                ex + dx * 0.8 - pupil_radius,
                ey + dy * 0.8 - pupil_radius,
                ex + dx * 0.8 + pupil_radius,
                ey + dy * 0.8 + pupil_radius,
                fill=COLOR_SNAKE_PUPIL, outline="",
            )

    def _draw_particles(self):
        """Draws current particle sparks and floating score texts."""
        self.canvas.delete("fx")
        for p in self.particles.particles:
            r = p.size * (p.life / p.max_life)
            self.canvas.create_oval(
                p.x - r, p.y - r, p.x + r, p.y + r,
                fill=p.color, outline="", tags="fx"
            )

        for ft in self.particles.floating_texts:
            self.canvas.create_text(
                ft.x, ft.y,
                text=ft.text,
                font=("Segoe UI", 11, "bold"),
                fill=ft.color,
                tags="fx"
            )

    # -------------------------------------------------------------
    # Overlays (Menu, Paused, Game Over)
    # -------------------------------------------------------------
    def _draw_menu_overlay(self):
        """Draws arcade title screen."""
        cx = BOARD_WIDTH // 2
        cy = BOARD_HEIGHT // 2

        # Dark overlay
        self.canvas.create_rectangle(
            0, 0, BOARD_WIDTH, BOARD_HEIGHT,
            fill="#090d16", stipple="gray75" if self.blink_state else "gray75"
        )

        # Title
        self.canvas.create_text(
            cx, cy - 140,
            text="CYBERSNAKE",
            font=("Segoe UI", 36, "bold"),
            fill=COLOR_TEXT_ACCENT,
        )
        self.canvas.create_text(
            cx, cy - 90,
            text="⚡ NEON BLITZ ⚡",
            font=("Segoe UI", 14, "bold"),
            fill=COLOR_FOOD_GOLDEN,
        )

        # Control Info Box
        box_y = cy - 40
        self.canvas.create_rectangle(
            cx - 200, box_y, cx + 200, box_y + 130,
            fill="#111827", outline="#1e293b", width=2
        )
        info_lines = [
            ("Move / Steer", "Arrow Keys  or  W A S D"),
            ("Pause Game", "Space  or  P"),
            ("Toggle Audio", "M  (Mute / Unmute)"),
            ("Difficulty", "[1] Casual  [2] Classic  [3] Insane"),
        ]
        for idx, (label, val) in enumerate(info_lines):
            line_y = box_y + 22 + idx * 26
            self.canvas.create_text(
                cx - 180, line_y,
                text=label, font=("Segoe UI", 10, "bold"),
                fill=COLOR_TEXT_MUTED, anchor="w"
            )
            self.canvas.create_text(
                cx + 180, line_y,
                text=val, font=("Segoe UI", 10),
                fill=COLOR_TEXT_PRIMARY, anchor="e"
            )

        # Blinking Start Prompt
        if self.blink_state:
            self.canvas.create_text(
                cx, cy + 140,
                text="PRESS [SPACE] OR [ENTER] TO PLAY",
                font=("Segoe UI", 13, "bold"),
                fill="#38bdf8",
            )

        # High score reminder
        self.canvas.create_text(
            cx, cy + 180,
            text=f"Current All-Time High Score: {self.game.high_score}",
            font=("Segoe UI", 10),
            fill=COLOR_TEXT_MUTED,
        )

    def _draw_paused_overlay(self):
        """Draws pause menu."""
        cx = BOARD_WIDTH // 2
        cy = BOARD_HEIGHT // 2

        self.canvas.create_rectangle(
            0, 0, BOARD_WIDTH, BOARD_HEIGHT,
            fill="#050811", stipple="gray75"
        )
        self.canvas.create_rectangle(
            cx - 150, cy - 60, cx + 150, cy + 60,
            fill="#111827", outline="#38bdf8", width=2
        )
        self.canvas.create_text(
            cx, cy - 18,
            text="PAUSED",
            font=("Segoe UI", 24, "bold"),
            fill=COLOR_TEXT_PRIMARY,
        )
        if self.blink_state:
            self.canvas.create_text(
                cx, cy + 22,
                text="Press [SPACE] or [P] to Resume",
                font=("Segoe UI", 11),
                fill=COLOR_TEXT_ACCENT,
            )

    def _draw_game_over_overlay(self):
        """Draws game over screen with score summary and retry prompt."""
        cx = BOARD_WIDTH // 2
        cy = BOARD_HEIGHT // 2

        self.canvas.create_rectangle(
            0, 0, BOARD_WIDTH, BOARD_HEIGHT,
            fill="#050811", stipple="gray75"
        )

        card_w, card_h = 360, 260
        self.canvas.create_rectangle(
            cx - card_w // 2, cy - card_h // 2,
            cx + card_w // 2, cy + card_h // 2,
            fill="#111827", outline="#f43f5e", width=2
        )

        self.canvas.create_text(
            cx, cy - 80,
            text="GAME OVER",
            font=("Segoe UI", 26, "bold"),
            fill="#f43f5e",
        )

        # Score Summary
        self.canvas.create_text(
            cx, cy - 30,
            text=f"Final Score: {self.game.score}",
            font=("Segoe UI", 18, "bold"),
            fill=COLOR_TEXT_PRIMARY,
        )

        if self.game.is_new_high_score:
            self.canvas.create_text(
                cx, cy + 10,
                text="🎉 NEW ALL-TIME HIGH SCORE! 🎉",
                font=("Segoe UI", 12, "bold"),
                fill=COLOR_FOOD_GOLDEN,
            )
        else:
            self.canvas.create_text(
                cx, cy + 10,
                text=f"Best Score: {self.game.high_score}",
                font=("Segoe UI", 12),
                fill=COLOR_TEXT_MUTED,
            )

        # Restart instructions
        if self.blink_state:
            self.canvas.create_text(
                cx, cy + 65,
                text="PRESS [SPACE] OR [R] TO RESTART",
                font=("Segoe UI", 12, "bold"),
                fill=COLOR_TEXT_ACCENT,
            )

        self.canvas.create_text(
            cx, cy + 95,
            text="Press [1, 2, 3] to Change Difficulty",
            font=("Segoe UI", 9),
            fill=COLOR_TEXT_MUTED,
        )

    # -------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------
    def _interpolate_color(self, hex1: str, hex2: str, t: float) -> str:
        """Interpolates between two hex colors by factor t (0.0 to 1.0)."""
        t = max(0.0, min(1.0, t))
        r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
        r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"
