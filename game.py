import pygame
from settings import (
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK,
    RED,
    YELLOW,
    FPS,
    VEL,
    BULLET_VEL,
    MAX_BULLETS,
    SPACESHIP_WIDTH,
    SPACESHIP_HEIGHT,
)
from loader import load_image, load_sound


def init_gamepad():
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        return pygame.joystick.Joystick(0)
    return None


def run_game(win, clock, p1_name: str, p2_name: str):
    space_bg = load_image("space.png", size=(WIDTH, HEIGHT))
    yellow_ship_img = load_image(
        "spaceship_yellow.png",
        size=(SPACESHIP_WIDTH, SPACESHIP_HEIGHT),
        rotate=90,
    )
    red_ship_img = load_image(
        "spaceship_red.png",
        size=(SPACESHIP_WIDTH, SPACESHIP_HEIGHT),
        rotate=270,
    )
    bullet_hit_sound = load_sound("Grenade.mp3")
    bullet_fire_sound = load_sound("Silencer.wav")

    hud_font = pygame.font.SysFont("couriernew", 24, bold=True)

    border = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

    yellow = pygame.Rect(
        50,
        HEIGHT // 2 - SPACESHIP_HEIGHT // 2,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
    )
    red = pygame.Rect(
        WIDTH - SPACESHIP_WIDTH - 50,
        HEIGHT // 2 - SPACESHIP_HEIGHT // 2,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
    )

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    p1_points = 0
    p2_points = 0

    gamepad = init_gamepad()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return None, p1_points, p2_points
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return None, p1_points, p2_points

                # Player 1 shoot (TAB)
                if event.key == pygame.K_TAB and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()

                # Player 2 shoot (ENTER)
                if event.key == pygame.K_RETURN and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x,
                        red.y + red.height // 2 - 2,
                        10,
                        5,
                    )
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

        # Gamepad input (for Player 2)
        if gamepad is not None:
            axis_x = gamepad.get_axis(0)
            axis_y = gamepad.get_axis(1)

            if axis_x < -0.3 and red.x - VEL > border.x + border.width:
                red.x -= VEL
            if axis_x > 0.3 and red.x + VEL + red.width < WIDTH:
                red.x += VEL
            if axis_y < -0.3 and red.y - VEL > 0:
                red.y -= VEL
            if axis_y > 0.3 and red.y + VEL + red.height < HEIGHT - 15:
                red.y += VEL

            if gamepad.get_button(0):
                if len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x,
                        red.y + red.height // 2 - 2,
                        10,
                        5,
                    )
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

        keys_pressed = pygame.key.get_pressed()
        # Player 1 movement
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < border.x:
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
            yellow.y += VEL

        # Player 2 movement
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > border.x + border.width:
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
            red.y += VEL

        # Bullets
        for bullet in yellow_bullets[:]:
            bullet.x += BULLET_VEL
            if red.colliderect(bullet):
                yellow_bullets.remove(bullet)
                bullet_hit_sound.play()
                red_health -= 1
                p1_points += 1
            elif bullet.x > WIDTH:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets[:]:
            bullet.x -= BULLET_VEL
            if yellow.colliderect(bullet):
                red_bullets.remove(bullet)
                bullet_hit_sound.play()
                yellow_health -= 1
                p2_points += 1
            elif bullet.x < 0:
                red_bullets.remove(bullet)

        # Check win
        if red_health <= 0:
            return p1_name, p1_points, p2_points
        if yellow_health <= 0:
            return p2_name, p1_points, p2_points

        # Draw
        win.blit(space_bg, (0, 0))
        pygame.draw.rect(win, BLACK, border)

        p1_text = hud_font.render(f"{p1_name}: {p1_points}", True, YELLOW)
        p2_text = hud_font.render(f"{p2_name}: {p2_points}", True, RED)

        win.blit(p1_text, (20, 10))
        win.blit(p2_text, (WIDTH - p2_text.get_width() - 20, 10))

        win.blit(yellow_ship_img, (yellow.x, yellow.y))
        win.blit(red_ship_img, (red.x, red.y))

        for bullet in yellow_bullets:
            pygame.draw.rect(win, YELLOW, bullet)
        for bullet in red_bullets:
            pygame.draw.rect(win, RED, bullet)

        pygame.display.update()
