import pygame
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_DIR,'..', 'Assets')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def load_assets():
    assets = {}
    try:
        logo = pygame.image.load(os.path.join(ASSETS_PATH, 'Game Logo.png')).convert_alpha()
        assets['logo'] = pygame.transform.smoothscale(logo, (300, 300))

        start_img = pygame.image.load(os.path.join(ASSETS_PATH, 'Start button.png')).convert_alpha()
        assets['start_button'] = pygame.transform.smoothscale(start_img, (220, 80))

        return assets
    except Exception as e:
        print(f"Error loading assets: {e}. Please check the filename in the assets folder.")
        return None

def draw_button_img(screen, rect, image, is_hovered):
    screen.blit(image, (rect.x, rect.y))

    if is_hovered:
        glow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        glow_surface.fill((255, 255, 255, 100))
        screen.blit(glow_surface, (rect.x, rect.y))

def test_ui():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("A Scoop of Spring - UI Test")
    all_assets = load_assets()
    start_button_rect = pygame.Rect(290,400,220,80)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = start_button_rect.collidepoint(mouse_pos)

        if all_assets:
            if 'logo' in all_assets:
                screen.blit(all_assets['logo'], (250, 50))

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