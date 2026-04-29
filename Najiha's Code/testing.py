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

# ===================== GAME STATE =====================
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


# ===================== UI HELPERS =====================
def draw_text_center(text, font, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    screen.blit(img, rect)


def draw_box(text, rect, color=(255, 255, 255), text_color=(0, 0, 0), font=font_small):
    pygame.draw.rect(screen, color, rect, border_radius=15)
    img = font.render(text, True, text_color)
    screen.blit(img, img.get_rect(center=rect.center))


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

            # -------- START --------
            if scene == 1 and start_btn and start_btn.collidepoint(mx, my):
                scene = 2

            # -------- STORY --------
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

            # -------- PLAY --------
            elif scene == 4 and play_btn and play_btn.collidepoint(mx, my):
                scene = 5
                current_order = generate_order(selected_level)
                player_choice = {}
                order_count = 0
                timer = 10

            # -------- GAME --------
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
        start_btn = pygame.Rect(WIDTH//2 - 150, 650, 300, 80)
        draw_box("START", start_btn)

    # ===================== SCENE 2 =====================
    elif scene == 2:
        draw_text_center("STORY", font_big, 300)
        draw_text_center("Welcome to Ice Cream Game!", font_medium, 450)
        next_btn = pygame.Rect(WIDTH//2 - 150, 700, 300, 80)
        draw_box("NEXT", next_btn)

    # ===================== LEVEL SELECT =====================
    elif scene == 3:
        draw_text_center("SELECT LEVEL", font_big, 200)

        box_w, box_h = 350, 80
        gap = 25
        start_y = HEIGHT // 2 - 150

        level1_btn = level2_btn = level3_btn = None

        for i in range(1, max_levels + 1):

            rect = pygame.Rect(
                WIDTH//2 - box_w//2,
                start_y + (i-1)*(box_h + gap),
                box_w,
                box_h
            )

            if i <= unlocked_level:
                draw_box(f"LEVEL {i}", rect)
            else:
                draw_box(f"LEVEL {i} LOCKED", rect, (120,120,120), (255,255,255))

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

        play_btn = pygame.Rect(WIDTH//2 - 150, 700, 300, 80)
        draw_box("PLAY", play_btn)

    # ===================== GAME =====================
    elif scene == 5:

        draw_text_center(f"LEVEL {selected_level}", font_small, 100)
        draw_text_center("ORDER", font_medium, 200)

        y = 260
        for k, v in current_order.items():
            draw_text_center(f"{k}: {v}", font_small, y)
            y += 40

        draw_text_center("YOUR CHOICE", font_medium, 400)

        y = 460
        for k, v in player_choice.items():
            draw_text_center(f"{k}: {v}", font_small, y)
            y += 40

        buttons = []

        # FLAVOURS
        for i, f in enumerate(flavours):
            rect = pygame.Rect(200 + i*200, 800, 180, 60)
            draw_box(f, rect)
            buttons.append(("flavour", f, rect))

        # TOPPING
        if selected_level >= 2:
            for i, t in enumerate(toppings):
                rect = pygame.Rect(200 + i*200, 900, 180, 60)
                draw_box(t, rect, (200,200,255))
                buttons.append(("topping", t, rect))

        # CONTAINER
        if selected_level >= 3:
            for i, c in enumerate(containers):
                rect = pygame.Rect(200 + i*200, 1000, 180, 60)
                draw_box(c, rect, (200,255,200))
                buttons.append(("container", c, rect))

        # TIMER
        timer -= dt
        draw_text_center(f"Time: {int(timer)}", font_medium, 650)

        # CHECK
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
        draw_text_center("RESULT", font_big, 180)
        draw_text_center(f"Score: {order_count}/{max_orders}", font_medium, 280)

        box_w, box_h = 350, 80
        gap = 25
        x = WIDTH//2 - box_w//2
        y = 420

        replay_btn = pygame.Rect(x, y, box_w, box_h)
        draw_box("PLAY AGAIN", replay_btn)

        home_btn = pygame.Rect(x, y + (box_h + gap), box_w, box_h)
        draw_box("HOME", home_btn)

        next_btn_result = None

        if order_count >= max_orders and selected_level < max_levels:
            next_btn_result = pygame.Rect(x, y + 2*(box_h + gap), box_w, box_h)
            draw_box("NEXT LEVEL", next_btn_result, (200,255,200))

    pygame.display.flip()

pygame.quit()
sys.exit()