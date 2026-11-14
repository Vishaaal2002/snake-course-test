"""
sound.py - Non-blocking retro sound synthesizer for CyberSnake
Uses Windows winsound in background threads with safe fallbacks.
"""

import sys
import threading
import time

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


class SoundManager:
    """Manages retro chiptune sound effects asynchronously."""

    def __init__(self):
        self.muted = False
        self._is_supported = HAS_WINSOUND and sys.platform.startswith("win")

    def toggle_mute(self) -> bool:
        """Toggles sound on or off. Returns new mute state."""
        self.muted = not self.muted
        if not self.muted:
            self.play_click()
        return self.muted

    def _play_async(self, tone_sequence):
        """Runs a sequence of (frequency, duration_ms) tones in a daemon thread."""
        if self.muted or not self._is_supported:
            return

        def worker():
            try:
                for freq, duration in tone_sequence:
                    winsound.Beep(int(freq), int(duration))
            except Exception:
                pass  # Ignore hardware/audio busy errors silently

        threading.Thread(target=worker, daemon=True).start()

    def play_apple(self):
        """Crisp high-pitch chirp for eating a regular apple."""
        self._play_async([(1200, 35)])

    def play_golden(self):
        """Ascending triumphant chime for special golden food."""
        self._play_async([(900, 35), (1350, 40), (1800, 60)])

    def play_powerup(self):
        """Energizing double chirp for speed or buff activation."""
        self._play_async([(1400, 40), (2000, 60)])

    def play_shrink(self):
        """Playful double pip for snake body trim powerup."""
        self._play_async([(1600, 30), (1100, 45)])

    def play_game_over(self):
        """Descending retro failure tone when snake crashes."""
        self._play_async([(500, 90), (380, 110), (260, 220)])

    def play_click(self):
        """Subtle blip for UI navigation or toggles."""
        self._play_async([(880, 25)])
