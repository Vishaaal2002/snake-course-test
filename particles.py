"""
particles.py - Lightweight particle and floating text effects for CyberSnake
"""

import random
from typing import List


class Particle:
    """A single visual spark that shoots outward and decays."""

    def __init__(self, x: float, y: float, color: str, speed_mult: float = 1.0):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 6.28318)  # 0 to 2*PI
        speed = random.uniform(1.5, 4.0) * speed_mult
        import math
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.max_life = random.randint(10, 16)
        self.life = self.max_life
        self.size = random.uniform(2.5, 4.5)

    def update(self) -> bool:
        """Updates particle position and life. Returns False when dead."""
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.92  # Friction
        self.vy *= 0.92
        self.life -= 1
        return self.life > 0


class FloatingText:
    """A floating score/combo popup that drifts upward and fades out."""

    def __init__(self, x: float, y: float, text: str, color: str):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.max_life = 20
        self.life = self.max_life

    def update(self) -> bool:
        """Moves text upward. Returns False when expired."""
        self.y -= 1.2
        self.life -= 1
        return self.life > 0


class ParticleSystem:
    """Manages all active particles and floating text on the canvas."""

    def __init__(self):
        self.particles: List[Particle] = []
        self.floating_texts: List[FloatingText] = []

    def spawn_burst(self, x: float, y: float, color: str, count: int = 10):
        """Spawns an explosive burst of sparks around (x, y)."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def spawn_text(self, x: float, y: float, text: str, color: str = "#ffffff"):
        """Spawns a floating score/message text at (x, y)."""
        self.floating_texts.append(FloatingText(x, y, text, color))

    def update(self):
        """Ticks forward all active effects and prunes dead ones."""
        self.particles = [p for p in self.particles if p.update()]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]

    def clear(self):
        """Removes all active particles and texts."""
        self.particles.clear()
        self.floating_texts.clear()
