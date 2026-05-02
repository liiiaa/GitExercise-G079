import pygame
import sys
import random
from order import generate_order

pygame.init()

WIDTH, HEIGHT = 1920, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Scoop of Spring")

font_big = pygame.font.SysFont(None, 100)
font_medium = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

scene = 1


current_order = generate_order()

timer = 10  # testing
clock = pygame.time.Clock()



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
    screen.fill((30, 30, 40))  # background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # SCENE 1 BUTTON
            if scene == 1 and start_btn.collidepoint(mx, my):
                scene = 2

            # SCENE 2 NEXT
            elif scene == 2 and next_btn.collidepoint(mx, my):
                scene = 3

            # SCENE 3 START GAME
            elif scene == 3 and play_btn.collidepoint(mx, my):
                scene = 4

        if event.type == pygame.KEYDOWN:
            if scene == 4:
                current_order = generate_order()
                timer = 10


    if scene == 1:
        draw_text_center("A Scoop of Spring", font_big, 400)
        draw_text_center("Welcome!", font_medium, 500)

        start_btn = draw_button("START", 650)


    elif scene == 2:
        draw_text_center("STORY", font_big, 300)
        draw_text_center("bla bla bla", font_medium, 450)
        draw_text_center("bla bla", font_medium, 520)

        next_btn = draw_button("NEXT", 700)


    elif scene == 3:
        draw_text_center("LEVEL 1", font_big, 350)
        draw_text_center("Get Ready!", font_medium, 500)

        play_btn = draw_button("PLAY", 700)


    elif scene == 4:
        timer -= clock.get_time() / 1000
        draw_text_center("GAMEPLAY", font_big, 200)

        draw_text_center("Customer Order:", font_medium, 350)
        order_text = f"{current_order['flavor']} with {', '.join(current_order['toppings'])}"
        draw_text_center(order_text, font_medium, 420)

        draw_text_center("Press ANY KEY to complete order", font_small, 550)

        # testing
        timer -= 0.02
        draw_text_center(f"Time Left: {int(timer)}", font_medium, 650)

        if timer <= 0:
            timer = 0
            draw_text_center("FAILED! Time Up!", font_medium, 750, (255, 100, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()                                   