import pygame
import os

WIDTH, HEIGHT = 1920, 1080
ASSETS_PATH = os.path.join("GitExercise", "Assets") 
LEVELS_FOLDER = "Levels Assets" 
BUTTONS_FOLDER = "Buttons Assets"

def get_level_ui_layout():
    layout = {}
    
    positions = [
        (80, 50), 
        (320, 180), 
        (80, 310), 
        (320, 440)   
    ]
    
    for i in range(4):
        x, y = positions[i]
        layout[f'slot_{i}'] = pygame.Rect(x, y, 350, 350)
    
    layout['prev_btn'] = pygame.Rect(80, 850, 250, 80)
    layout['next_btn'] = pygame.Rect(380, 850, 250, 80)
    
    return layout

def load_assets():
    assets = {}
    my_files = ['Vanilla_LVL.png', 'Choco_LVL.png', 'Strawb_LVL.png', 'Mint_LVL.png']
    
    try:
        assets['background'] = pygame.image.load(os.path.join(ASSETS_PATH, 'Background.png')).convert_alpha()

        assets['scoop_images'] = []
        for filename in my_files:
            path = os.path.join(ASSETS_PATH, LEVELS_FOLDER, filename)
            img = pygame.image.load(path).convert_alpha()
            assets['scoop_images'].append(pygame.transform.smoothscale(img, (400, 400)))

        assets['back_button'] = pygame.image.load(os.path.join(ASSETS_PATH, BUTTONS_FOLDER, 'Back button.png')).convert_alpha()
        assets['back_button'] = pygame.transform.smoothscale(assets['back_button'], (350, 150))

        assets['next_button'] = pygame.image.load(os.path.join(ASSETS_PATH, BUTTONS_FOLDER, 'Next button.png')).convert_alpha()
        assets['next_button'] = pygame.transform.smoothscale(assets['next_button'], (350, 150))
            
        assets['font'] = pygame.font.SysFont('Cooper Black', 110, bold=True)
        assets['btn_font'] = pygame.font.SysFont('Cooper Black', 40, bold=True)
        return assets
    except Exception as e:
        print(f"Error: {e}")
        return None

def draw_level_selection_ui(screen, assets, mouse_pos, page):
    layout = get_level_ui_layout()
    start_level = (page * 4) + 1
    
    for i in range(4):
        level_num = start_level + i
        if level_num > 25: break

        rect = layout[f'slot_{i}']
        scoop_center = (rect.centerx, rect.centery + 10) 
        
        number_center = (scoop_center[0], scoop_center[1] - 40)

        if rect.collidepoint(mouse_pos):
            glow_size = 260 
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (200, 200, 200, 50), (0, 0, glow_size, glow_size))
            screen.blit(glow_surf, glow_surf.get_rect(center=scoop_center))

        img_idx = (level_num - 1) % len(assets['scoop_images'])
        scoop_img = assets['scoop_images'][img_idx]
        screen.blit(scoop_img, scoop_img.get_rect(center=scoop_center))

        level_text = str(level_num)
        text_surf = assets['font'].render(level_text, True, (255, 255, 255))
        outline_surf = assets['font'].render(level_text, True, (30, 30, 30))
        text_rect = text_surf.get_rect(center=number_center)

        off = 4
        screen.blit(outline_surf, (text_rect.x - off, text_rect.y - off))
        screen.blit(outline_surf, (text_rect.x + off, text_rect.y - off))
        screen.blit(outline_surf, (text_rect.x - off, text_rect.y + off))
        screen.blit(outline_surf, (text_rect.x + off, text_rect.y + off))
        screen.blit(text_surf, text_rect)

    prev_rect = layout['prev_btn']
    if prev_rect.collidepoint(mouse_pos):
        hover_surf = pygame.Surface(assets['back_button'].get_size(), pygame.SRCALPHA)
        hover_surf.set_alpha(150)
        hover_surf.blit(assets['back_button'], (0, 0))
        screen.blit(hover_surf, prev_rect.topleft)
    else:
        screen.blit(assets['back_button'], prev_rect.topleft)

    next_rect = layout['next_btn']
    if next_rect.collidepoint(mouse_pos):
        hover_surf = pygame.Surface(assets['next_button'].get_size(), pygame.SRCALPHA)
        hover_surf.set_alpha(150)
        hover_surf.blit(assets['next_button'], (0, 0))
        screen.blit(hover_surf, next_rect.topleft)
    else:
        screen.blit(assets['next_button'], next_rect.topleft)


def test_selection_ui():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level Select: 4 per page")
    clock = pygame.time.Clock()
    
    all_assets = load_assets()
    if not all_assets: return

    current_page = 0
    total_pages = 7

    running = True
    while running:
        if all_assets and 'background' in all_assets:
            screen.blit(all_assets['background'], (0, 0))
        else:
            screen.fill((50, 50, 50))
        mouse_pos = pygame.mouse.get_pos()
        layout = get_level_ui_layout()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if layout['next_btn'].collidepoint(mouse_pos):
                    if current_page < total_pages - 1:
                        current_page += 1
                
                if layout['prev_btn'].collidepoint(mouse_pos):
                    if current_page > 0:
                        current_page -= 1
                
                start_level = (current_page * 4) + 1
                for i in range(4):
                    if layout[f'slot_{i}'].collidepoint(mouse_pos):
                        clicked_level = start_level + i
                        if clicked_level <= 25:
                            print(f"Starting Level {clicked_level}!")

        draw_level_selection_ui(screen, all_assets, mouse_pos, current_page)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    test_selection_ui()