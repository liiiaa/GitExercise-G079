import pygame
import sys
import random
import os

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Scoop of Spring")

# PATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

# LINK W LIA'S CODE
sys.path.append(os.path.join(PROJECT_DIR, "Lia's codes"))

from ui_layout import load_assets
from ui_layout_screen2 import (
    load_assets as load_level_assets,
    draw_level_selection_ui,
    get_level_ui_layout
)

from sound import play_music, play_sound_effect
from timing import start_level, update_timer, get_time, is_time_up
from score import calculate_score, get_score, reset_score

# MUSIC / SOUND PATHS
MUSIC_FOLDER = os.path.join(PROJECT_DIR, "Sound Tracks")

MENU_MUSIC = os.path.join(MUSIC_FOLDER, "mainmenu.mp3")
GAMEPLAY_MUSIC = os.path.join(MUSIC_FOLDER, "gameplay.mp3")
CORRECT_SOUND = os.path.join(MUSIC_FOLDER, "correct.mp3")
WRONG_SOUND = os.path.join(MUSIC_FOLDER, "wrong.mp3")
LEVEL_COMPLETE_SOUND = os.path.join(MUSIC_FOLDER, "level_complete.mp3")

play_music(MENU_MUSIC)

# Load Game Background
game_bg = pygame.image.load(
    os.path.join(PROJECT_DIR, "Assets", "Main Game Assets", "Game Background.png")
).convert()
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# Load UI Assets
ui_assets = load_assets()
level_assets = load_level_assets()

# Load Next Button
next_btn_img = pygame.image.load(
    os.path.join(PROJECT_DIR, "Assets", "Buttons Assets", "Next button.png")
).convert_alpha()
next_btn_img = pygame.transform.scale(next_btn_img, (320, 160))

# Load Start Button
start_button_img = pygame.image.load(
    os.path.join(PROJECT_DIR, "Assets", "Buttons Assets", "Start button.png")
).convert_alpha()
start_button_img = pygame.transform.scale(start_button_img, (320, 160))

# Load Character
char_img = pygame.image.load(
    os.path.join(PROJECT_DIR, "Assets", "Main Game Assets", "char_smile.png")
).convert_alpha()
char_img = pygame.transform.scale(char_img, (330, 300))

current_page = 0

# Fonts
font_big = pygame.font.SysFont(None, 100)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 40)

# UI Config
BOX_W = 320
BOX_H = 75
BOX_GAP = 15
CENTER_X = WIDTH // 2

# Game
scene = 1
selected_level = 1

max_levels = 5
unlocked_level = 1

flavours = ["Vanilla", "Chocolate", "Strawberry", "Choco Mint"]
toppings = ["Sprinkles", "Choco chips"]
containers = ["Cone", "Cup"]

milkshake_flavours = ["Oreo", "Caramel", "Matcha"]
creams = ["Whipped Cream", "Chocolate Cream"]

current_order = {}
player_choice = {}

order_count = 0
max_orders = 3
result_text = ""

buttons = []

start_btn = None
next_btn = None
next_btn_rect = None
start_btn_rect = None
replay_btn = None
home_btn = None
next_btn_result = None


def draw_text_center(text, font, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    screen.blit(img, rect)


def draw_box(text, rect, color=(255, 255, 255), text_color=(0, 0, 0), font=font_small):
    pygame.draw.rect(screen, color, rect, border_radius=18)

    img = font.render(text, True, text_color)
    text_rect = img.get_rect(center=rect.center)

    if text_rect.width > rect.width - 20:
        font2 = pygame.font.SysFont(None, 30)
        img = font2.render(text, True, text_color)
        text_rect = img.get_rect(center=rect.center)

    screen.blit(img, text_rect)


def generate_order(level):
    if level >= 4:
        order = {"milkshake": random.choice(milkshake_flavours)}

        if level >= 5:
            order["cream"] = random.choice(creams)

        return order

    order = {"flavour": random.choice(flavours)}

    if level >= 2:
        order["topping"] = random.choice(toppings)

    if level >= 3:
        order["container"] = random.choice(containers)

    return order


running = True

while running:
    dt = clock.tick(60) / 1000
    screen.fill((30, 30, 40))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if scene == 1 and start_btn and start_btn.collidepoint(mx, my):
                scene = 2

            elif scene == 2 and next_btn_rect and next_btn_rect.collidepoint(mx, my):
                scene = 3

            elif scene == 3:
                layout = get_level_ui_layout()
                start_level_num = (current_page * 4) + 1

                for i in range(4):
                    clicked_level = start_level_num + i

                    if clicked_level > max_levels:
                        continue

                    if layout[f"slot_{i}"].collidepoint(mx, my):
                        if clicked_level <= unlocked_level:
                            selected_level = clicked_level
                            scene = 4

                total_pages = (max_levels - 1) // 4

                if layout["next_btn"].collidepoint(mx, my):
                    if current_page < total_pages:
                        current_page += 1

                if layout["prev_btn"].collidepoint(mx, my):
                    if current_page > 0:
                        current_page -= 1

            elif scene == 4 and start_btn_rect and start_btn_rect.collidepoint(mx, my):
                play_music(GAMEPLAY_MUSIC)

                scene = 5
                current_order = generate_order(selected_level)
                player_choice = {}
                order_count = 0
                result_text = ""

                reset_score()
                start_level(selected_level)

            elif scene == 5:
                for b_type, value, rect in buttons:
                    if rect.collidepoint(mx, my):
                        player_choice[b_type] = value

            elif scene == 6:
                if replay_btn and replay_btn.collidepoint(mx, my):
                    play_music(MENU_MUSIC)
                    scene = 3

                elif home_btn and home_btn.collidepoint(mx, my):
                    play_music(MENU_MUSIC)
                    scene = 1

                elif next_btn_result and next_btn_result.collidepoint(mx, my):
                    selected_level += 1
                    scene = 4

    # SCENE 1 START SCREEN
    if scene == 1:
        logo_rect = ui_assets["logo"].get_rect(center=(WIDTH // 2, 350))
        start_button_rect = ui_assets["start_button"].get_rect(center=(WIDTH // 2, 620))

        screen.blit(ui_assets["background"], (0, 0))
        screen.blit(ui_assets["logo"], logo_rect)

        if start_button_rect.collidepoint(mouse_pos):
            hover_surf = ui_assets["start_button"].copy()
            hover_surf.fill((255, 255, 255, 50), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(hover_surf, start_button_rect)
        else:
            screen.blit(ui_assets["start_button"], start_button_rect)

        start_btn = start_button_rect

    # SCENE 2 STORY
    elif scene == 2:
        screen.blit(ui_assets["background"], (0, 0))

        draw_text_center("STORY", font_big, 100)
        draw_text_center("Spring has arrived in Bloomberry Town!", font_medium, 220)
        draw_text_center("A young girl opened her dream Ice Cream Shop", font_medium, 300)
        draw_text_center("to spread happiness through sweet treats.", font_medium, 380)
        draw_text_center("Help her serve every customer before the ice cream melts!", font_medium, 460)

        next_btn_rect = next_btn_img.get_rect(center=(WIDTH // 2, 620))
        screen.blit(next_btn_img, next_btn_rect)

    # SCENE 3 LEVEL SELECT
    elif scene == 3:
        if level_assets and "background" in level_assets:
            screen.blit(level_assets["background"], (0, 0))

        draw_level_selection_ui(
            screen,
            level_assets,
            mouse_pos,
            current_page
        )

    # SCENE 4 READY
    elif scene == 4:
        screen.blit(game_bg, (0, 0))

        draw_text_center(f"LEVEL {selected_level}", font_big, 200)
        draw_text_center("Get Ready!", font_medium, 270)

        start_btn_rect = start_button_img.get_rect(center=(WIDTH // 2, 500))
        screen.blit(start_button_img, start_btn_rect)

    # SCENE 5 GAME
    elif scene == 5:
        update_timer(dt)

        screen.blit(game_bg, (0, 0))
        screen.blit(char_img, (WIDTH - 400, 30))

        draw_text_center(f"LEVEL {selected_level}", font_big, 80)
        draw_text_center(f"Score: {get_score()}", font_small, 130)

        if selected_level >= 4:
            draw_text_center("MILKSHAKE ORDER", font_medium, 170)
        else:
            draw_text_center("ORDER", font_medium, 170)

        y = 220
        for k, v in current_order.items():
            draw_text_center(f"{k}: {v}", font_small, y)
            y += 40

        draw_text_center("YOUR CHOICE", font_medium, y + 40)

        y_choice = y + 80
        for k, v in player_choice.items():
            draw_text_center(f"{k}: {v}", font_small, y_choice)
            y_choice += 40

        buttons = []
        base_y = 500

        if selected_level <= 3:
            for i, f in enumerate(flavours):
                rect = pygame.Rect(150 + i * 220, base_y, 160, 60)
                draw_box(f, rect)
                buttons.append(("flavour", f, rect))

        if 2 <= selected_level <= 3:
            for i, t in enumerate(toppings):
                rect = pygame.Rect(150 + i * 220, base_y + 80, 160, 60)
                draw_box(t, rect, (200, 200, 255))
                buttons.append(("topping", t, rect))

        if selected_level == 3:
            for i, c in enumerate(containers):
                rect = pygame.Rect(150 + i * 220, base_y + 160, 160, 60)
                draw_box(c, rect, (200, 255, 200))
                buttons.append(("container", c, rect))

        if selected_level >= 4:
            for i, m in enumerate(milkshake_flavours):
                rect = pygame.Rect(180 + i * 250, base_y, 180, 60)
                draw_box(m, rect, (255, 220, 200))
                buttons.append(("milkshake", m, rect))

        if selected_level >= 5:
            for i, c in enumerate(creams):
                rect = pygame.Rect(250 + i * 300, base_y + 90, 220, 60)
                draw_box(c, rect, (255, 240, 200))
                buttons.append(("cream", c, rect))

        if selected_level == 1:
            timer_y = base_y + 90
        elif selected_level == 2:
            timer_y = base_y + 170
        elif selected_level == 3:
            timer_y = base_y + 250
        elif selected_level == 4:
            timer_y = base_y + 170
        else:
            timer_y = base_y + 260

        draw_text_center(f"Time: {get_time()}", font_medium, timer_y)
        draw_text_center(result_text, font_small, timer_y + 40)

        if player_choice == current_order and len(player_choice) == len(current_order):
            play_sound_effect(CORRECT_SOUND)

            order_count += 1
            result_text = calculate_score(True, get_time())

            current_order = generate_order(selected_level)
            player_choice = {}

            if order_count >= max_orders:
                play_sound_effect(LEVEL_COMPLETE_SOUND)

                if selected_level == unlocked_level and unlocked_level < max_levels:
                    unlocked_level += 1

                scene = 6

        elif len(player_choice) == len(current_order):
            play_sound_effect(WRONG_SOUND)

            result_text = calculate_score(False, get_time())
            player_choice = {}

        if is_time_up():
            scene = 6

    # SCENE 6 RESULT
    elif scene == 6:
        screen.blit(ui_assets["background"], (0, 0))

        draw_text_center("RESULT", font_big, 110)
        draw_text_center(f"Orders: {order_count}/{max_orders}", font_medium, 170)
        draw_text_center(f"Score: {get_score()}", font_medium, 220)

        start_y = 300

        replay_btn = pygame.Rect(CENTER_X - BOX_W // 2, start_y, BOX_W, BOX_H)
        draw_box("PLAY AGAIN", replay_btn)

        home_btn = pygame.Rect(CENTER_X - BOX_W // 2, start_y + 110, BOX_W, BOX_H)
        draw_box("HOME", home_btn)

        next_btn_result = None

        if order_count >= max_orders and selected_level < max_levels:
            next_btn_result = pygame.Rect(CENTER_X - BOX_W // 2, start_y + 220, BOX_W, BOX_H)
            draw_box("NEXT LEVEL", next_btn_result, (200, 255, 200))

    pygame.display.flip()

pygame.quit()
sys.exit()