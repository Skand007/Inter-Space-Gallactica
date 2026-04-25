import pygame
from settings import (
    WIDTH,
    HEIGHT,
    WHITE,
    CYAN,
    MAGENTA,
    DARK_GREY,
    TITLE_FONT_NAME,
    UI_FONT_NAME,
    CRT_LINE_COLOR,
)
from utils.loader import load_image


class Starfield:
    def __init__(self, num_stars=80):
        import random

        self.stars = []
        for _ in range(num_stars):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            speed = random.uniform(0.5, 2.0)
            self.stars.append([x, y, speed])

    def update(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > HEIGHT:
                star[1] = 0

    def draw(self, surface):
        for x, y, _ in self.stars:
            surface.fill(WHITE, (int(x), int(y), 2, 2))


def draw_crt_overlay(surface):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(overlay, CRT_LINE_COLOR, (0, y), (WIDTH, y))
    surface.blit(overlay, (0, 0))


def get_font(size, bold=False):
    return pygame.font.SysFont(TITLE_FONT_NAME if bold else UI_FONT_NAME, size, bold=bold)


def show_start_screen(win, clock):
    starfield = Starfield()
    title_font = get_font(60, bold=True)
    subtitle_font = get_font(24)
    flash_font = get_font(28, bold=True)

    bg = load_image("space.png", size=(WIDTH, HEIGHT))

    flash_timer = 0
    flash_visible = True

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                if event.key == pygame.K_c:
                    return "controls"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        starfield.update()

        win.blit(bg, (0, 0))
        starfield.draw(win)

        title_surf = title_font.render("INTER-SPACE GALLACTICA", True, CYAN)
        win.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 4))

        subtitle_surf = subtitle_font.render("Retro Two-Player Space Duel", True, WHITE)
        win.blit(
            subtitle_surf,
            (WIDTH // 2 - subtitle_surf.get_width() // 2, HEIGHT // 4 + 70),
        )

        flash_timer += 1
        if flash_timer % 40 == 0:
            flash_visible = not flash_visible

        if flash_visible:
            flash_surf = flash_font.render("PRESS ENTER TO START", True, MAGENTA)
            win.blit(
                flash_surf,
                (WIDTH // 2 - flash_surf.get_width() // 2, HEIGHT // 2 + 40),
            )

        controls_surf = subtitle_font.render("Press C for Controls • ESC to Quit", True, WHITE)
        win.blit(
            controls_surf,
            (WIDTH // 2 - controls_surf.get_width() // 2, HEIGHT - 80),
        )

        draw_crt_overlay(win)
        pygame.display.update()


def show_controls_screen(win, clock):
    starfield = Starfield()
    title_font = get_font(40, bold=True)
    text_font = get_font(22)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    return

        starfield.update()
        win.fill(DARK_GREY)
        starfield.draw(win)

        title_surf = title_font.render("CONTROLS", True, CYAN)
        win.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 40))

        lines = [
            "PLAYER 1 (LEFT):",
            "  Move: W A S D",
            "  Shoot: TAB",
            "",
            "PLAYER 2 (RIGHT):",
            "  Move: Arrow Keys",
            "  Shoot: ENTER",
            "",
            "GAMEPAD (if connected):",
            "  Left stick / D-pad: Move",
            "  A / Cross: Shoot",
            "",
            "Press ENTER / ESC to return",
        ]

        y = 120
        for line in lines:
            surf = text_font.render(line, True, WHITE)
            win.blit(surf, (80, y))
            y += 30

        draw_crt_overlay(win)
        pygame.display.update()


def name_input_screen(win, clock, player_index: int):
    title_font = get_font(36, bold=True)
    text_font = get_font(26)
    info_font = get_font(18)

    name = ""
    max_len = 12
    cursor_visible = True
    cursor_timer = 0

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "YELLOW" if player_index == 1 else "RED"
                    return name
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    ch = event.unicode
                    if ch.isalpha() and len(name) < max_len:
                        name += ch.upper()

        cursor_timer += 1
        if cursor_timer % 30 == 0:
            cursor_visible = not cursor_visible

        win.fill((0, 0, 0))

        title_surf = title_font.render(f"ENTER PLAYER {player_index} NAME", True, CYAN)
        win.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 4))

        display_name = name
        if cursor_visible:
            display_name += "_"

        name_surf = text_font.render(display_name, True, WHITE)
        win.blit(
            name_surf,
            (WIDTH // 2 - name_surf.get_width() // 2, HEIGHT // 2),
        )

        info_surf = info_font.render("UPPERCASE • MAX 12 CHARS • ENTER TO CONFIRM • ESC TO QUIT", True, MAGENTA)
        win.blit(
            info_surf,
            (WIDTH // 2 - info_surf.get_width() // 2, HEIGHT - 80),
        )

        pygame.display.update()


def show_game_over_screen(win, clock, winner_name, p1_name, p2_name,
                          p1_points_match, p2_points_match,
                          scores_dict):
    title_font = get_font(50, bold=True)
    text_font = get_font(24)

    running = True
    flash_timer = 0
    flash_visible = True

    p1_stats = scores_dict.get(p1_name, {"wins": 0, "points": 0})
    p2_stats = scores_dict.get(p2_name, {"wins": 0, "points": 0})

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        win.fill((0, 0, 0))

        title_surf = title_font.render("GAME OVER", True, MAGENTA)
        win.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 60))

        winner_surf = text_font.render(f"WINNER: {winner_name}", True, CYAN)
        win.blit(winner_surf, (WIDTH // 2 - winner_surf.get_width() // 2, 130))

        y = 190
        lines = [
            f"{p1_name} - Match Points: {p1_points_match} • Total Wins: {p1_stats['wins']} • Total Points: {p1_stats['points']}",
            f"{p2_name} - Match Points: {p2_points_match} • Total Wins: {p2_stats['wins']} • Total Points: {p2_stats['points']}",
        ]
        for line in lines:
            surf = text_font.render(line, True, WHITE)
            win.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
            y += 40

        flash_timer += 1
        if flash_timer % 40 == 0:
            flash_visible = not flash_visible

        if flash_visible:
            prompt_surf = text_font.render("Press ENTER to Restart • ESC to Quit", True, WHITE)
            win.blit(
                prompt_surf,
                (WIDTH // 2 - prompt_surf.get_width() // 2, HEIGHT - 120),
            )

        draw_crt_overlay(win)
        pygame.display.update()
