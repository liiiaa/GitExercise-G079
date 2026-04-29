import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1920, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Scoop of Spring")

font_big = pygame.font.SysFont(None, 100)
font_medium = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

# ===================== GAME DATA =====================
scene = 1
selected_level = 1

max_levels = 3
unlocked_level = 1

flavours = ["Vanilla Ice Cream", "Chocolate Milkshake", "Strawberry Ice Cream", "Choco Mint Ice Cream"]
toppings = ["Sprinkles", "Choco chips"]
containers = ["Cone", "Cup"]

current_order = {}
player_choice = {}

order_count = 0
max_orders = 3
timer = 10

buttons = []

start_btn = next_btn = None
level1_btn = level2_btn = level3_btn = None
play_btn = replay_btn = home_btn = next_btn_result = None


# ===================== FUNCTIONS =====================
def draw_text_center(text, font, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    screen.blit(img, rect)


def draw_button(text, y):
    rect = pygame.Rect(WIDTH // 2 - 150, y, 300, 80)
    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=15)
    draw_text_center(text, font_small, y + 40, (0, 0, 0))
    return rect


def generate_order(level):
    order = {"flavour": random.choice(flavours)}
    if level >= 2:
        order["topping"] = random.choice(toppings)
    if level >= 3:
        order["container"] = random.choice(containers)
    return order


# ===================== GAME LOOP =====================
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((30, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # -------- SCENE 1 --------
            if scene == 1 and start_btn and start_btn.collidepoint(mx, my):
                scene = 2

            # -------- SCENE 2 --------
            elif scene == 2 and next_btn and next_btn.collidepoint(mx, my):
                scene = 3

            # -------- LEVEL SELECT --------
            elif scene == 3:

                if level1_btn and level1_btn.collidepoint(mx, my):
                    selected_level = 1
                    scene = 4

                elif level2_btn and level2_btn.collidepoint(mx, my) and unlocked_level >= 2:
                    selected_level = 2
                    scene = 4

                elif level3_btn and level3_btn.collidepoint(mx, my) and unlocked_level >= 3:
                    selected_level = 3
                    scene = 4

            # -------- START GAME --------
            elif scene == 4 and play_btn and play_btn.collidepoint(mx, my):
                scene = 5
                current_order = generate_order(selected_level)
                player_choice = {}
                order_count = 0
                timer = 10

            # -------- GAME CLICK --------
            elif scene == 5:
                for b_type, value, rect in buttons:
                    if rect.collidepoint(mx, my):
                        player_choice[b_type] = value

            # -------- RESULT --------
            elif scene == 6:
                if replay_btn and replay_btn.collidepoint(mx, my):
                    scene = 3

                elif home_btn and home_btn.collidepoint(mx, my):
                    scene = 1

                elif next_btn_result and next_btn_result.collidepoint(mx, my):
                    selected_level += 1
                    scene = 4

    # ===================== SCENE 1 =====================
    if scene == 1:
        draw_text_center("A Scoop of Spring", font_big, 400)
        draw_text_center("Welcome!", font_medium, 500)
        start_btn = draw_button("START", 650)

    # ===================== SCENE 2 =====================
    elif scene == 2:
        draw_text_center("STORY", font_big, 300)
        draw_text_center("bla bla bla story game", font_medium, 450)
        next_btn = draw_button("NEXT", 700)

    # ===================== LEVEL SELECT =====================
    elif scene == 3:
        draw_text_center("SELECT LEVEL", font_big, 250)

        box_w, box_h = 300, 80
        gap = 30
        start_y = 400

        level1_btn = level2_btn = level3_btn = None

        for i in range(1, max_levels + 1):
            y = start_y + (i - 1) * (box_h + gap)
            rect = pygame.Rect(WIDTH // 2 - box_w // 2, y, box_w, box_h)

            if i <= unlocked_level:
                pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=15)
                text = font_small.render(f"LEVEL {i}", True, (0, 0, 0))
            else:
                pygame.draw.rect(screen, (120, 120, 120), rect, border_radius=15)
                text = font_small.render(f"LEVEL {i} LOCKED", True, (255, 255, 255))

            screen.blit(text, text.get_rect(center=rect.center))

            if i == 1:
                level1_btn = rect
            elif i == 2:
                level2_btn = rect
            elif i == 3:
                level3_btn = rect

    # ===================== PRE GAME =====================
    elif scene == 4:
        draw_text_center(f"LEVEL {selected_level}", font_big, 350)
        draw_text_center("Get Ready!", font_medium, 500)
        play_btn = draw_button("PLAY", 700)

    # ===================== GAME =====================
    elif scene == 5:
        draw_text_center(f"LEVEL {selected_level}", font_small, 100)
        draw_text_center("ORDER:", font_medium, 200)

        y_pos = 260
        for key, value in current_order.items():
            draw_text_center(f"{key}: {value}", font_small, y_pos)
            y_pos += 40

        draw_text_center("YOUR CHOICE:", font_medium, 400)

        y_pos = 460
        for key, value in player_choice.items():
            draw_text_center(f"{key}: {value}", font_small, y_pos)
            y_pos += 40

        buttons = []

        # FLAVOURS
        for i, f in enumerate(flavours):
            rect = pygame.Rect(200 + i * 200, 800, 150, 60)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            screen.blit(font_small.render(f, True, (0, 0, 0)), rect.center)
            buttons.append(("flavour", f, rect))

        # TOPPING
        if selected_level >= 2:
            for i, t in enumerate(toppings):
                rect = pygame.Rect(200 + i * 200, 900, 150, 60)
                pygame.draw.rect(screen, (200, 200, 255), rect)
                screen.blit(font_small.render(t, True, (0, 0, 0)), rect.center)
                buttons.append(("topping", t, rect))

        # CONTAINER
        if selected_level >= 3:
            for i, c in enumerate(containers):
                rect = pygame.Rect(200 + i * 200, 1000, 150, 60)
                pygame.draw.rect(screen, (200, 255, 200), rect)
                screen.blit(font_small.render(c, True, (0, 0, 0)), rect.center)
                buttons.append(("container", c, rect))

        # TIMER
        timer -= dt
        draw_text_center(f"Time: {int(timer)}", font_medium, 700)

        # CHECK WIN
        if player_choice == current_order and len(player_choice) == len(current_order):
            order_count += 1
            current_order = generate_order(selected_level)
            player_choice = {}
            timer = 10

            if order_count >= max_orders:
                if selected_level == unlocked_level and unlocked_level < max_levels:
                    unlocked_level += 1
                scene = 6

        if timer <= 0:
            scene = 6

    # ===================== RESULT =====================
    elif scene == 6:
        draw_text_center("RESULT", font_big, 200)
        draw_text_center(f"Score: {order_count}/{max_orders}", font_medium, 320)

        box_w, box_h = 350, 80
        gap = 30

        replay_btn = pygame.Rect(WIDTH // 2 - box_w // 2, 450, box_w, box_h)
        pygame.draw.rect(screen, (255, 255, 255), replay_btn, border_radius=15)
        draw_text_center("PLAY AGAIN", font_small, 490, (0, 0, 0))

        home_btn = pygame.Rect(WIDTH // 2 - box_w // 2, 450 + box_h + gap, box_w, box_h)
        pygame.draw.rect(screen, (255, 255, 255), home_btn, border_radius=15)
        draw_text_center("HOME", font_small, 570, (0, 0, 0))

        next_btn_result = None

        if order_count >= max_orders and selected_level < max_levels:
            next_btn_result = pygame.Rect(WIDTH // 2 - box_w // 2, 450 + 2 * (box_h + gap), box_w, box_h)
            pygame.draw.rect(screen, (200, 255, 200), next_btn_result, border_radius=15)
            draw_text_center("NEXT LEVEL", font_small, 650, (0, 0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()