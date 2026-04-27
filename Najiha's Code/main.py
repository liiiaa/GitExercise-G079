import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1920, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Scoop of Spring")

font_big = pygame.font.SysFont(None, 100)
font_medium = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

scene = 1
selected_level = 1

orders = ["Vanilla Ice Cream", "Chocolate Milkshake", "Strawberry Ice Cream", "Choco Mint Ice Cream"]
current_order = random.choice(orders)

timer = 10
clock = pygame.time.Clock()


start_btn = None
next_btn = None
level1_btn = None
play_btn = None
replay_btn = None
home_btn = None


def draw_text_center(text, font, y, color=(255,255,255)):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    screen.blit(img, rect)

def draw_button(text, y):
    rect = pygame.Rect(WIDTH//2 - 150, y, 300, 80)
    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=15)
    draw_text_center(text, font_small, y + 40, (0,0,0))
    return rect


running = True
while running:
    screen.fill((30, 30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if scene == 1 and start_btn and start_btn.collidepoint(mx, my):
                scene = 2

            elif scene == 2 and next_btn and next_btn.collidepoint(mx, my):
                scene = 3

            elif scene == 3:
                if level1_btn and level1_btn.collidepoint(mx, my):
                    selected_level = 1
                    scene = 4

            elif scene == 4 and play_btn and play_btn.collidepoint(mx, my):
                scene = 5

            elif scene == 6:
                if replay_btn and replay_btn.collidepoint(mx, my):
                    scene = 3
                    timer = 10
                    current_order = random.choice(orders)

                elif home_btn and home_btn.collidepoint(mx, my):
                    scene = 1
                    timer = 10
                    current_order = random.choice(orders)

        
        if event.type == pygame.KEYDOWN:
            if scene == 5:
                current_order = random.choice(orders)
                timer = 10


    # SCENE 1
    if scene == 1:
        draw_text_center("A Scoop of Spring", font_big, 400)
        draw_text_center("Welcome!", font_medium, 500)
        start_btn = draw_button("START", 650)

    # SCENE 2
    elif scene == 2:
        draw_text_center("STORY", font_big, 300)
        draw_text_center("bla bla bla", font_medium, 450)
        draw_text_center("bla bla", font_medium, 520)
        next_btn = draw_button("NEXT", 700)

    # SCENE 3
    elif scene == 3:
        draw_text_center("SELECT LEVEL", font_big, 300)
        level1_btn = draw_button("LEVEL 1", 500)
        draw_text_center("LEVEL 2 (LOCKED)", font_small, 650, (150,150,150))

    # SCENE 4
    elif scene == 4:
        draw_text_center(f"LEVEL {selected_level}", font_big, 350)
        draw_text_center("Get Ready!", font_medium, 500)
        play_btn = draw_button("PLAY", 700)

    # SCENE 5 (GAMEPLAY)
    elif scene == 5:
        draw_text_center("GAMEPLAY", font_big, 200)
        draw_text_center("Customer Order:", font_medium, 350)
        draw_text_center(current_order, font_medium, 420)
        draw_text_center("Press ANY KEY to complete order", font_small, 550)

        timer -= 0.02
        draw_text_center(f"Time Left: {int(timer)}", font_medium, 650)

        if timer <= 0:
            scene = 6

    # SCENE 6 (RESULT)
    elif scene == 6:
        draw_text_center("RESULT", font_big, 300)
        draw_text_center("Score: 100", font_medium, 500)

        replay_btn = draw_button("PLAY AGAIN", 700)
        home_btn = draw_button("HOME", 820)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()                             