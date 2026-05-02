import pygame
import sys
import os

# --- INITIALIZATION ---
pygame.init()
SCREEN_W, SCREEN_H = 1920, 1200
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.DOUBLEBUF)
pygame.display.set_caption("A Scoop of Spring")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40, bold=True)

# --- PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_PATH = os.path.join(PARENT_DIR, "Assets", "Main Game Assets")

def load_img(name, size):
    path = os.path.join(ASSETS_PATH, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size); surf.fill((255, 0, 255)); return surf

# --- ASSETS ---
bg_img = load_img("Game Background.png", (SCREEN_W, SCREEN_H))
cone_bowl_img = load_img("Cone_bowl.png", (220, 150))
cup_station_img = load_img("Cup.png", (150, 300))
RESET_RECT = pygame.Rect(1680, 1080, 200, 70)

BLENDER_BASE_POS = (1750, 350)
CUP_STATION_POS = (100, 380)
CONE_STATION_POS = (250, 480)
TUB_SIZE = (220, 160)

TOPPING_STATIONS = {
    "cream":    {"file": "Cream_bottle.png", "spawn": "Cream.png", "pos": (1200, 520), "size": (100, 280)},
    "milk":     {"file": "Milk.png",         "spawn": "Milk.png",  "pos": (1400, 550), "size": (150, 250)},
    "sprinkles":{"file": "Sprinkles_bowl.png","spawn": "Sprinkles.png", "pos": (1180, 750), "size": (200, 140)},
    "cherry":   {"file": "Cherry_bowl.png",   "spawn": "Cherry.png",    "pos": (1380, 750), "size": (200, 140)}
}

FLAVORS = ["vanilla", "strawberry", "mango", "chocolate", "chocomint", "coffee"]
FLAVOR_POS = [(250, 620), (500, 620), (750, 620), (250, 820), (500, 820), (750, 820)]

class Draggable:
    def __init__(self, name, filename, size, pos, type="item"):
        self.name = name
        self.image = load_img(filename, size)
        self.rect = self.image.get_rect(center=pos)
        self.dragging = True
        self.type = type
        self.liquid_flavor = None
        self.has_milk = False
        self.has_scoop = False
        self.is_blended = False
        # Parenting system
        self.attached_scoop = None
        self.attached_toppings = []

class Scoop:
    def __init__(self, flavor, pos):
        self.flavor = flavor
        # Increased size from 220,180 to 260,210
        self.image = load_img(f"{flavor.capitalize()}_scoop.png", (260, 210))
        self.rect = self.image.get_rect(center=pos)
        self.dragging = True
        self.locked_in_blender = False

# --- OBJECTS ---
blender = Draggable("Blender", "Blender.png", (300, 550), BLENDER_BASE_POS, "blender")
blender.dragging = False
active_scoops = []
held_item = None
placed_base = None

def reset_game():
    global active_scoops, held_item, placed_base
    active_scoops, held_item, placed_base = [], None, None
    blender.is_blended = False; blender.has_milk = False; blender.has_scoop = False
    blender.liquid_flavor = None; blender.rect.center = BLENDER_BASE_POS

# --- LOOP ---
while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if RESET_RECT.collidepoint(mouse_pos): reset_game()

            # 1. Blender
            if blender.rect.collidepoint(mouse_pos):
                if blender.has_milk and blender.has_scoop and not blender.is_blended:
                    blender.is_blended = True
                elif blender.is_blended:
                    blender.dragging = True
            
            
            elif placed_base and placed_base.rect.collidepoint(mouse_pos):
                placed_base.dragging = True
                held_item = placed_base

            # 3. Spawn Items
            else:
                if pygame.Rect(CUP_STATION_POS, (150, 300)).collidepoint(mouse_pos):
                    held_item = Draggable("Cup", "Cup.png", (200, 300), mouse_pos, "base")
                elif pygame.Rect(CONE_STATION_POS, (220, 150)).collidepoint(mouse_pos):
                    held_item = Draggable("Cone", "Cone.png", (180, 320), mouse_pos, "base")
                
                for i, f in enumerate(FLAVORS):
                    if pygame.Rect(FLAVOR_POS[i], TUB_SIZE).collidepoint(mouse_pos):
                        active_scoops.append(Scoop(f, mouse_pos))

                for t_name, d in TOPPING_STATIONS.items():
                    if pygame.Rect(d["pos"], d["size"]).collidepoint(mouse_pos):
                        held_item = Draggable(t_name, d["spawn"], (120, 120), mouse_pos, "topping")

        if event.type == pygame.MOUSEBUTTONUP:
            if blender.dragging:
                if placed_base and placed_base.name == "Cup" and blender.rect.colliderect(placed_base.rect):
                    placed_base.liquid_flavor = blender.liquid_flavor
                    blender.is_blended = False; blender.has_milk = False; blender.has_scoop = False
                blender.dragging = False; blender.rect.center = BLENDER_BASE_POS
            
            if held_item:
                if held_item.name == "milk" and held_item.rect.colliderect(blender.rect):
                    blender.has_milk = True
                    held_item = None
                elif held_item.type == "base":
                    placed_base = held_item
                    held_item.dragging = False
                    held_item = None
                elif held_item.type == "topping" and placed_base and held_item.rect.colliderect(placed_base.rect):
                    
                    placed_base.attached_toppings.append(held_item)
                    held_item.dragging = False
                    held_item = None
                else:
                    held_item = None

            for s in active_scoops[:]:
                if s.dragging:
                    s.dragging = False
                    if s.rect.colliderect(blender.rect) and not blender.is_blended:
                        blender.has_scoop = True; blender.liquid_flavor = s.flavor
                        s.locked_in_blender = True
                        s.rect.center = (blender.rect.centerx, blender.rect.centery + 100)
                    elif placed_base and s.rect.colliderect(placed_base.rect):
                        # Attach scoop to base
                        placed_base.attached_scoop = s
                        active_scoops.remove(s)
                    else:
                        active_scoops.remove(s)

    
    if blender.dragging: blender.rect.center = mouse_pos
    if held_item: held_item.rect.center = mouse_pos
    for s in active_scoops:
        if s.dragging: s.rect.center = mouse_pos
        
    if placed_base:
        if placed_base.dragging: placed_base.rect.center = mouse_pos
        # Scoop Follow 
        if placed_base.attached_scoop:
            placed_base.attached_scoop.rect.midbottom = (placed_base.rect.centerx, placed_base.rect.top + 140)
        # Toppings Follow
        for i, t in enumerate(placed_base.attached_toppings):
            t.rect.midbottom = (placed_base.rect.centerx, placed_base.rect.top + 40 - (i*10))

    # --- DRAW ---
    screen.blit(bg_img, (0, 0))
    screen.blit(cone_bowl_img, CONE_STATION_POS)
    screen.blit(cup_station_img, CUP_STATION_POS)
    for i, f in enumerate(FLAVORS):
        screen.blit(load_img(f"{f.capitalize()}_tub.png", TUB_SIZE), FLAVOR_POS[i])
    for t, d in TOPPING_STATIONS.items():
        screen.blit(load_img(d["file"], d["size"]), d["pos"])

    # Reset Button
    pygame.draw.rect(screen, (220, 60, 60), RESET_RECT, border_radius=10)
    screen.blit(font.render("RESET", True, (255, 255, 255)), (RESET_RECT.x + 45, RESET_RECT.y + 12))

    # Draw Food Base
    if placed_base:
        screen.blit(placed_base.image, placed_base.rect)
        if placed_base.name == "Cup" and placed_base.liquid_flavor:
            liq = load_img(f"{placed_base.liquid_flavor.capitalize()}_liq.png", (160, 220))
            screen.blit(liq, (placed_base.rect.x + 20, placed_base.rect.y + 40))
        # Draw Attached Scoop
        if placed_base.attached_scoop:
            screen.blit(placed_base.attached_scoop.image, placed_base.attached_scoop.rect)
        # Draw Attached Toppings
        for t in placed_base.attached_toppings:
            screen.blit(t.image, t.rect)

    # Blender Liquid Logic
    for s in active_scoops:
        if s.locked_in_blender and not blender.is_blended:
            screen.blit(s.image, s.rect)
    
    # Show Liquid inside blender if blended
    if blender.is_blended and blender.liquid_flavor:
        b_liq = load_img(f"{blender.liquid_flavor.capitalize()}_liq.png", (220, 280))
        screen.blit(b_liq, (blender.rect.x + 40, blender.rect.y + 150))

    screen.blit(blender.image, blender.rect)

    # Floating UI/Held items
    for s in active_scoops:
        if not s.locked_in_blender: screen.blit(s.image, s.rect)
    if held_item: screen.blit(held_item.image, held_item.rect)

    pygame.display.flip()
    clock.tick(60)