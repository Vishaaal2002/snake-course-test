"""
main.py - Entry point for CyberSnake: Neon Blitz
Run with:
    python main.py
"""

import tkinter as tk
from ui import CyberSnakeUI


def main():
    """Initializes the Tk window and runs the CyberSnake game loop."""
    root = tk.Tk()
    app = CyberSnakeUI(root)
    # Perform initial render pass
    app.render()
    root.mainloop()


if __name__ == "__main__":
    main()
