"""
game.py - Core game logic and state management for CyberSnake
"""

import json
import os
import random
from typing import List, Optional, Tuple
from constants import (
    DIFFICULTIES,
    GRID_SIZE,
    HIGHSCORE_FILE,
    POINTS_APPLE,
    POINTS_GOLDEN,
    POINTS_BONUS_COMBO,
    POWERUP_DURATION_TICKS,
    TYPE_APPLE,
    TYPE_GOLDEN,
    TYPE_SPEED,
    TYPE_SLOW,
    TYPE_CUT,
)


class GameState:
    """Encapsulates the complete logical state of the CyberSnake game."""

    def __init__(self):
        self.difficulty_name = "Normal"
        self.high_score = self.load_high_score()
        self.is_new_high_score = False
        self.reset_game()

    def reset_game(self):
        """Resets the gameplay session to initial state."""
        mid = GRID_SIZE // 2
        # Snake initial segments (moving right)
        self.snake: List[Tuple[int, int]] = [
            (mid, mid),
            (mid - 1, mid),
            (mid - 2, mid),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow_pending = 0

        # Score & Combo
        self.score = 0
        self.combo = 1
        self.combo_timer = 0
        self.is_new_high_score = False

        # Status: 'MENU', 'PLAYING', 'PAUSED', 'GAME_OVER'
        self.status = "MENU"

        # Food & Power-ups
        self.apple: Tuple[int, int] = (0, 0)
        self.special_food: Optional[dict] = None

        # Active Power-up Buff timers
        self.speed_boost_ticks = 0
        self.slow_mo_ticks = 0

        # Spawn initial apple
        self.spawn_apple()

    @property
    def difficulty_config(self) -> dict:
        return DIFFICULTIES[self.difficulty_name]

    def set_difficulty(self, diff_name: str):
        """Sets difficulty mode if valid."""
        if diff_name in DIFFICULTIES:
            self.difficulty_name = diff_name

    def load_high_score(self) -> int:
        """Loads persistent high score from highscore.json."""
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return int(data.get("high_score", 0))
            except Exception:
                return 0
        return 0

    def save_high_score(self):
        """Saves persistent high score to highscore.json."""
        try:
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f, indent=2)
        except Exception:
            pass

    def change_direction(self, dx: int, dy: int):
        """Buffers direction change, preventing 180-degree instant reversal."""
        current_dx, current_dy = self.direction
        # Cannot immediately turn back into oneself
        if (dx, dy) != (-current_dx, -current_dy):
            self.next_direction = (dx, dy)

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """Finds all grid cells unoccupied by snake or active special food."""
        occupied = set(self.snake)
        if self.special_food:
            occupied.add((self.special_food["x"], self.special_food["y"]))
        if self.apple:
            occupied.add(self.apple)

        empty = [
            (x, y)
            for x in range(GRID_SIZE)
            for y in range(GRID_SIZE)
            if (x, y) not in occupied
        ]
        return empty

    def spawn_apple(self):
        """Places a normal red apple on a free cell."""
        empty = self.get_empty_positions()
        if empty:
            self.apple = random.choice(empty)

    def try_spawn_special(self):
        """Randomly generates special food/power-up if space is available."""
        if self.special_food is not None:
            return

        # 35% chance to trigger special food when an apple is eaten
        if random.random() < 0.38:
            empty = self.get_empty_positions()
            if not empty:
                return

            x, y = random.choice(empty)
            types = [TYPE_GOLDEN, TYPE_SPEED, TYPE_SLOW, TYPE_CUT]
            weights = [0.45, 0.20, 0.20, 0.15]
            chosen_type = random.choices(types, weights=weights, k=1)[0]

            self.special_food = {
                "x": x,
                "y": y,
                "type": chosen_type,
                "ticks_left": 55,  # Timed countdown before disappearance
            }

    def update_tick(self) -> dict:
        """
        Executes one game clock tick.
        Returns an event dict describing what happened (e.g. food eaten, game over).
        """
        event = {
            "game_over": False,
            "eaten": None,
            "points_earned": 0,
            "combo_active": self.combo > 1,
            "powerup_activated": None,
            "pos": None,
        }

        if self.status != "PLAYING":
            return event

        # Decrement combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 1

        # Decrement active power-up timers
        if self.speed_boost_ticks > 0:
            self.speed_boost_ticks -= 1
        if self.slow_mo_ticks > 0:
            self.slow_mo_ticks -= 1

        # Decrement special food countdown
        if self.special_food is not None:
            self.special_food["ticks_left"] -= 1
            if self.special_food["ticks_left"] <= 0:
                self.special_food = None

        # Apply buffered direction
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall Collision / Wrap-around
        wrap_walls = self.difficulty_config["wrap_walls"]
        if wrap_walls:
            new_head = (new_head[0] % GRID_SIZE, new_head[1] % GRID_SIZE)
        else:
            if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
                self.status = "GAME_OVER"
                event["game_over"] = True
                return event

        # Self-collision check (excluding the tail if we aren't growing this tick)
        body_to_check = self.snake[:-1] if self.grow_pending == 0 else self.snake
        if new_head in body_to_check:
            self.status = "GAME_OVER"
            event["game_over"] = True
            return event

        # Advance snake head
        self.snake.insert(0, new_head)
        event["pos"] = new_head

        # Check collision with normal apple
        if new_head == self.apple:
            points = POINTS_APPLE + (self.combo - 1) * POINTS_BONUS_COMBO
            self.score += points
            self.grow_pending += 1
            self.combo += 1
            self.combo_timer = 30  # Fresh combo window

            event["eaten"] = TYPE_APPLE
            event["points_earned"] = points

            self.spawn_apple()
            self.try_spawn_special()

        # Check collision with special food
        elif self.special_food and new_head == (self.special_food["x"], self.special_food["y"]):
            sp_type = self.special_food["type"]
            event["eaten"] = sp_type

            if sp_type == TYPE_GOLDEN:
                points = POINTS_GOLDEN + (self.combo - 1) * POINTS_BONUS_COMBO
                self.score += points
                self.grow_pending += 2
                self.combo += 2
                self.combo_timer = 35
                event["points_earned"] = points

            elif sp_type == TYPE_SPEED:
                self.speed_boost_ticks = POWERUP_DURATION_TICKS
                self.slow_mo_ticks = 0
                event["powerup_activated"] = TYPE_SPEED

            elif sp_type == TYPE_SLOW:
                self.slow_mo_ticks = POWERUP_DURATION_TICKS
                self.speed_boost_ticks = 0
                event["powerup_activated"] = TYPE_SLOW

            elif sp_type == TYPE_CUT:
                # Trims up to 3 segments from tail (minimum snake length: 2)
                cut_count = min(3, max(0, len(self.snake) - 3))
                if cut_count > 0:
                    self.snake = self.snake[:-cut_count]
                event["powerup_activated"] = TYPE_CUT

            self.special_food = None

        # Manage tail segment removal
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.snake.pop()

        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.is_new_high_score = True
            self.save_high_score()

        return event

    def get_current_tick_delay(self) -> int:
        """Calculates current tick delay in milliseconds, adjusting for active buffs."""
        base_ms = self.difficulty_config["speed_ms"]
        if self.speed_boost_ticks > 0:
            return max(35, int(base_ms * 0.65))  # Much faster
        if self.slow_mo_ticks > 0:
            return int(base_ms * 1.55)           # Slow motion
        return base_ms
