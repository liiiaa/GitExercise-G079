from cmath import rect

import pygame
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_DIR,'..', 'Assets')
WIDTH, HEIGHT = 1920, 1200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def load_assets():
    assets = {}
    try:
        logo = pygame.image.load(os.path.join(ASSETS_PATH, 'Game Logo.png')).convert_alpha()
        assets['logo'] = pygame.transform.smoothscale(logo, (600, 600))

        start_img = pygame.image.load(os.path.join(ASSETS_PATH, 'Start button.png')).convert_alpha()
        assets['start_button'] = pygame.transform.smoothscale(start_img, (400, 150))

        return assets
    except Exception as e:
        print(f"Error loading assets: {e}. Please check the filename in the assets folder.")
        return None

def draw_button_img(screen, rect, image, is_hovered):
    if is_hovered:
        surf = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        surf.set_alpha(150)  
        surf.blit(image, (0, 0))
        screen.blit(surf, (rect.x, rect.y))
    else:
        screen.blit(image, (rect.x, rect.y))
    
def test_ui():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1200))
    pygame.display.set_caption("A Scoop of Spring - UI Test")
    all_assets = load_assets()
    start_button_rect = pygame.Rect(760, 700, 400, 150)
    logo_position = (660, 150)

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = start_button_rect.collidepoint(mouse_pos)

        if all_assets:
            if 'logo' in all_assets:
                screen.blit(all_assets['logo'], logo_position)

            if 'start_button' in all_assets:
                draw_button_img(screen, start_button_rect, all_assets['start_button'], is_hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered:
                    print("Start button is clicked!")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    test_ui()