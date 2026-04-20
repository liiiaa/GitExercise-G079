import pygame
import os

WIDTH, HEIGHT = 1920, 1080
ASSETS_PATH = os.path.join("GitExercise", "Assets") 
SUB_FOLDER = "Levels Assets" 

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
        assets['scoop_images'] = []
        for filename in my_files:
            path = os.path.join(ASSETS_PATH, SUB_FOLDER, filename)
            img = pygame.image.load(path).convert_alpha()
            assets['scoop_images'].append(pygame.transform.smoothscale(img, (400, 400)))
            
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

    for btn_key, label in [('prev_btn', 'BACK'), ('next_btn', 'NEXT')]:
        btn_rect = layout[btn_key]
        color = (180, 180, 180) if btn_rect.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, btn_rect, border_radius=20)
        btn_text = assets['btn_font'].render(label, True, (255, 255, 255))
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))


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
        screen.fill((40, 40, 40)) 
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