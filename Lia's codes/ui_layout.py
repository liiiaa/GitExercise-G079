from cmath import rect

import pygame
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_DIR, '..', 'Assets')
SUB_FOLDER = "Buttons Assets"
WIDTH, HEIGHT = 1920, 1200

def load_assets():
    assets = {}
    try:
        assets['background'] = pygame.image.load(os.path.join(ASSETS_PATH, 'Background.png')).convert_alpha()
        
        logo = pygame.image.load(os.path.join(ASSETS_PATH, 'Game Logo.png')).convert_alpha()
        assets['logo'] = pygame.transform.smoothscale(logo, (900, 900))

        start_img = pygame.image.load(os.path.join(ASSETS_PATH, SUB_FOLDER, 'Start button.png')).convert_alpha()
        assets['start_button'] = pygame.transform.smoothscale(start_img, (500, 250))

        return assets
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_ui():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A Scoop of Spring")
    
    all_assets = load_assets()
    if not all_assets:
        return

    logo_rect = all_assets['logo'].get_rect(center=(WIDTH // 2, 450))
    start_button_rect = all_assets['start_button'].get_rect(center=(WIDTH // 2, 900))

    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill((255, 253, 240))
        
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = start_button_rect.collidepoint(mouse_pos)

        screen.blit(all_assets['background'], (0, 0))
        screen.blit(all_assets['logo'], logo_rect)

        if is_hovered:
            hover_surf = all_assets['start_button'].copy()
            hover_surf.fill((255, 255, 255, 50), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(hover_surf, start_button_rect)
        else:
            screen.blit(all_assets['start_button'], start_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered:
                    print("Start button clicked!")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    test_ui()