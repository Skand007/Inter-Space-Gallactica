import os
import sys
import subprocess

# Auto-install pygame if missing
def ensure_pygame():
    try:
        import pygame  # noqa: F401
    except ImportError:
        print("Pygame not found. Installing pygame...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pygame"])
        print("Pygame installed successfully. Restarting game...")
        os.execv(sys.executable, [sys.executable] + sys.argv)


ensure_pygame()
import pygame

from settings import WIDTH, HEIGHT, TITLE
from ui import (
    show_start_screen,
    show_controls_screen,
    name_input_screen,
    show_game_over_screen,
)
from game import run_game
from loader import load_scores, save_scores, ensure_scores_file


def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    ensure_scores_file()
    scores = load_scores()

    running = True
    while running:

        # ⭐ Start Screen
        action = show_start_screen(win, clock)

        if action == "quit":
            running = False
            break

        if action == "controls":
            show_controls_screen(win, clock)
            continue

        if action == "start":
            # ⭐ Player 1 Name
            p1_name = name_input_screen(win, clock, 1)
            if p1_name is None:
                running = False
                break

            # ⭐ Player 2 Name
            p2_name = name_input_screen(win, clock, 2)
            if p2_name is None:
                running = False
                break

            # ⭐ Run Game
            winner, p1_points_match, p2_points_match = run_game(
                win, clock, p1_name, p2_name
            )

            if winner is None:
                running = False
                break

            # ⭐ Update Scores
            for name, pts in [(p1_name, p1_points_match), (p2_name, p2_points_match)]:
                if name not in scores:
                    scores[name] = {"wins": 0, "points": 0}
                scores[name]["points"] += pts

            if winner not in scores:
                scores[winner] = {"wins": 0, "points": 0}
            scores[winner]["wins"] += 1

            save_scores(scores)

            # ⭐ Game Over Screen
            post_action = show_game_over_screen(
                win,
                clock,
                winner,
                p1_name,
                p2_name,
                p1_points_match,
                p2_points_match,
                scores,
            )

            if post_action == "quit":
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
