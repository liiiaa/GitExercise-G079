import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1920, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Scoop of Spring")

# Fonts
font_big = pygame.font.SysFont(None, 100)
font_medium = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

# UI Config
BOX_W = 420
BOX_H = 85
BOX_GAP = 25
CENTER_X = WIDTH // 2

# Game
scene = 1
selected_level = 1

max_levels = 3
unlocked_level = 1

flavours = ["Vanilla", "Chocolate", "Strawberry", "Choco Mint"]
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


# Function
def draw_text_center(text, font, y, color=(255,255,255)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    screen.blit(img, rect)


def draw_box(text, rect, color=(255,255,255), text_color=(0,0,0), font=font_small):
    pygame.draw.rect(screen, color, rect, border_radius=18)

    img = font.render(text, True, text_color)
    text_rect = img.get_rect(center=rect.center)

    # shrink the text
    if text_rect.width > rect.width - 20:
        font2 = pygame.font.SysFont(None, 30)
        img = font2.render(text, True, text_color)
        text_rect = img.get_rect(center=rect.center)

    screen.blit(img, text_rect)


def generate_order(level):
    order = {"flavour": random.choice(flavours)}
    if level >= 2:
        order["topping"] = random.choice(toppings)
    if level >= 3:
        order["container"] = random.choice(containers)
    return order


# Loop
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((30, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Scene 1 
            if scene == 1 and start_btn and start_btn.collidepoint(mx, my):
                scene = 2

            # Scene 2
            elif scene == 2 and next_btn and next_btn.collidepoint(mx, my):
                scene = 3

            # Scene 3 (Level Select)
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

            # Scene 4 (Start Level)
            elif scene == 4 and play_btn and play_btn.collidepoint(mx, my):
                scene = 5
                current_order = generate_order(selected_level)
                player_choice = {}
                order_count = 0
                timer = 10

            # Scene 5 (Game Scene)
            elif scene == 5:
                for b_type, value, rect in buttons:
                    if rect.collidepoint(mx, my):
                        player_choice[b_type] = value

            # Scene 6 (Result Screen)
            elif scene == 6:

                if replay_btn and replay_btn.collidepoint(mx, my):
                    scene = 3

                elif home_btn and home_btn.collidepoint(mx, my):
                    scene = 1

                elif next_btn_result and next_btn_result.collidepoint(mx, my):
                    selected_level += 1
                    scene = 4

    # Scene 1
    if scene == 1:
        draw_text_center("A Scoop of Spring", font_big, 380)
        draw_text_center("Welcome!", font_medium, 480)

        start_btn = pygame.Rect(CENTER_X - BOX_W//2, 650, BOX_W, BOX_H)
        draw_box("START", start_btn)

    # Scene 2
    elif scene == 2:
        draw_text_center("STORY", font_big, 300)
        draw_text_center("bla bla bla bla", font_medium, 450)

        next_btn = pygame.Rect(CENTER_X - BOX_W//2, 700, BOX_W, BOX_H)
        draw_box("NEXT", next_btn)

    # Scene 3 (Level Select)
    elif scene == 3:
        draw_text_center("SELECT LEVEL", font_big, 180)

        start_y = HEIGHT//2 - 150

        level1_btn = level2_btn = level3_btn = None

        for i in range(1, max_levels+1):

            rect = pygame.Rect(
                CENTER_X - BOX_W//2,
                start_y + (i-1)*(BOX_H + BOX_GAP),
                BOX_W,
                BOX_H
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

    # Scene 4 (Start Level)
    elif scene == 4:
        draw_text_center(f"LEVEL {selected_level}", font_big, 350)
        draw_text_center("Get Ready!", font_medium, 500)

        play_btn = pygame.Rect(CENTER_X - BOX_W//2, 700, BOX_W, BOX_H)
        draw_box("PLAY", play_btn)

    # Scene 5 (Game Scene)
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

        base_y = 750

        # Flavours
        for i, f in enumerate(flavours):
            rect = pygame.Rect(200 + i*180, base_y, 160, 60)
            draw_box(f, rect)
            buttons.append(("flavour", f, rect))

        # Toppings
        if selected_level >= 2:
            for i, t in enumerate(toppings):
                rect = pygame.Rect(200 + i*180, base_y+100, 160, 60)
                draw_box(t, rect, (200,200,255))
                buttons.append(("topping", t, rect))

        # Containers
        if selected_level >= 3:
            for i, c in enumerate(containers):
                rect = pygame.Rect(200 + i*180, base_y+200, 160, 60)
                draw_box(c, rect, (200,255,200))
                buttons.append(("container", c, rect))

        timer -= dt
        draw_text_center(f"Time: {int(timer)}", font_medium, 650)

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

    # Scene 6 (Result Screen)
    elif scene == 6:
        draw_text_center("RESULT", font_big, 180)
        draw_text_center(f"Score: {order_count}/{max_orders}", font_medium, 280)

        start_y = 420

        replay_btn = pygame.Rect(CENTER_X - BOX_W//2, start_y, BOX_W, BOX_H)
        draw_box("PLAY AGAIN", replay_btn)

        home_btn = pygame.Rect(CENTER_X - BOX_W//2, start_y + 110, BOX_W, BOX_H)
        draw_box("HOME", home_btn)

        next_btn_result = None

        if order_count >= max_orders and selected_level < max_levels:
            next_btn_result = pygame.Rect(CENTER_X - BOX_W//2, start_y + 220, BOX_W, BOX_H)
            draw_box("NEXT LEVEL", next_btn_result, (200,255,200))

    pygame.display.flip()

pygame.quit()
sys.exit()