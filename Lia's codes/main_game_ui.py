import pygame
import sys
import os

# ==================================================
# INITIALIZATION
# ==================================================
pygame.init()

SCREEN_W, SCREEN_H = 1280, 720
BASE_W, BASE_H = 1920, 1200

SCALE_X = SCREEN_W / BASE_W
SCALE_Y = SCREEN_H / BASE_H

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.DOUBLEBUF)
pygame.display.set_caption("A Scoop of Spring")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40, bold=True)

# ==================================================
# PATHS & LOADER
# ==================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_PATH = os.path.join(PARENT_DIR, "Assets", "Main Game Assets")

def load_img(name, size):
    path = os.path.join(ASSETS_PATH, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill((255, 0, 255))
        return surf

# ==================================================
# SCALING HELPERS
# ==================================================
def scale(pos):
    x, y = pos
    return (int(x * SCALE_X), int(y * SCALE_Y))

def scale_rect(rect):
    return pygame.Rect(
        int(rect.x * SCALE_X),
        int(rect.y * SCALE_Y),
        int(rect.width * SCALE_X),
        int(rect.height * SCALE_Y)
    )

# ==================================================
# ASSETS
# ==================================================
bg_img = load_img("Game Background.png", (SCREEN_W, SCREEN_H))

cone_bowl_img = load_img("Cone_bowl.png", (int(220*SCALE_X), int(150*SCALE_Y)))
cup_station_img = load_img("Cup.png", (int(150*SCALE_X), int(300*SCALE_Y)))
milk_liq_img = load_img("Milk_liq.png", (int(220*SCALE_X), int(280*SCALE_Y)))
char_smile_img = load_img("Char_smile.png", (int(420*SCALE_X), int(380*SCALE_Y)))
char_talk_img = load_img("Char_talk.png", (int(420*SCALE_X), int(380*SCALE_Y)))
chat_bubble_base = load_img("Chat_bubble.png", (350, 150))

# ==================================================
# CONSTANTS (SCALED)
# ==================================================
RESET_RECT = scale_rect(pygame.Rect(1680, 1080, 200, 70))

BLENDER_BASE_POS = scale((1750, 350))
CUP_STATION_POS = scale((100, 380))
CONE_STATION_POS = scale((250, 480))

SERVE_BUTTON_RECT = scale_rect(pygame.Rect(860, 1080, 200, 70))
SERVE_ZONE_RECT = scale_rect(pygame.Rect(760, 400, 400, 400))

TUB_SIZE = (int(220*SCALE_X), int(160*SCALE_Y))

# ==================================================
# TOPPING STATIONS (FIXED)
# ==================================================
TOPPING_STATIONS = {
    "cream": {
        "type": "bottle",
        "file": "Cream_bottle.png",
        "spawn": "Cream.png",
        "pos": scale((1200, 950)),
        "size": (int(100*SCALE_X), int(280*SCALE_Y)),
        "spawn_size": (int(160*SCALE_X), int(140*SCALE_Y)),
        "offset": int(90*SCALE_Y)
    }
}

# ==================================================
# FLAVORS
# ==================================================
FLAVORS = ["vanilla", "strawberry", "mango", "chocolate", "chocomint", "coffee"]

FLAVOR_POS = [
    scale((250, 620)), scale((500, 620)), scale((750, 620)),
    scale((250, 820)), scale((500, 820)), scale((750, 820))
]

# ==================================================
# CLASSES
# ==================================================
class Character:
    def __init__(self, x, y, sprite_smile, sprite_talk):
        self.x, self.y = x, y
        self.sprite_smile, self.sprite_talk = sprite_smile, sprite_talk
        self.current_sprite = sprite_smile
        self.is_talking, self.talk_timer, self.anim_timer = False, 0, 0
    def update(self, dt):
        if self.is_talking:
            self.talk_timer -= dt
            self.anim_timer += dt
            if self.anim_timer >= 0.2:
                self.anim_timer = 0
                self.current_sprite = self.sprite_talk if self.current_sprite == self.sprite_smile else self.sprite_smile
            if self.talk_timer <= 0:
                self.is_talking = False; self.current_sprite = self.sprite_smile
    def draw(self, screen): screen.blit(self.current_sprite, (self.x, self.y))

class ChatBubble:
    def __init__(self, speaker, bubble_img, font):
        self.speaker, self.bubble_img, self.font = speaker, bubble_img, font
        self.text, self.active, self.timer = "", False, 0
    def show(self, message, duration=3):
        self.text, self.active, self.timer = message, True, duration
        self.speaker.is_talking = True; self.speaker.talk_timer = duration
    def update(self, dt):
        if self.active:
            self.timer -= dt
            if self.timer <= 0: self.active = False
    def draw(self, screen):
        if not self.active: return
        text_surf = self.font.render(self.text, True, (60, 60, 60))
        bx, by = self.speaker.x + 160 - text_surf.get_width() // 2, self.speaker.y - 80
        bubble_scaled = pygame.transform.scale(self.bubble_img, (text_surf.get_width() + 60, text_surf.get_height() + 40))
        screen.blit(bubble_scaled, (bx, by))
        screen.blit(text_surf, (bx + 30, by + 20))

class Draggable:
    def __init__(self, name, filename, size, pos, type="item"):
        self.name, self.image = name, load_img(filename, size)
        self.rect = self.image.get_rect(center=pos)
        self.start_pos, self.dragging, self.type = pos, False, type
        self.liquid_flavor, self.has_milk, self.has_scoop, self.is_blended = None, False, False, False
        self.attached_scoop, self.attached_toppings = None, []

class Scoop:
    def __init__(self, flavor, pos):
        self.flavor = flavor
        self.image = load_img(f"{flavor.capitalize()}_scoop.png", (300, 240))
        self.rect = self.image.get_rect(center=pos)
        self.dragging, self.locked_in_blender = True, False

# ==================================================
# OBJECTS & RESET
# ==================================================
customer = Character(100, 160, char_smile_img, char_talk_img)
chat_bubble = ChatBubble(customer, chat_bubble_base, font)
blender = Draggable("Blender", "Blender.png", (300, 550), BLENDER_BASE_POS, "blender")

bottles = {}
bowls = {}
for name, data in TOPPING_STATIONS.items():
    if data["type"] == "bottle":
        bottles[name] = Draggable(name, data["file"], data["size"], data["pos"], "bottle")
    else:
        img = load_img(data["file"], data["size"])
        bowls[name] = {"img": img, "rect": img.get_rect(center=data["pos"])}

active_scoops, placed_items, held_item = [], [], None

def reset_game():
    global active_scoops, placed_items, held_item
    active_scoops, placed_items, held_item = [], [], None
    blender.has_milk, blender.has_scoop, blender.is_blended = False, False, False
    blender.liquid_flavor, blender.rect.center = None, BLENDER_BASE_POS
    for b in bottles.values(): b.rect.center = b.start_pos
    chat_bubble.show("Hi! Get your scoop! ✨")

reset_game()

# ==================================================
# GAME LOOP
# ==================================================
while True:
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if RESET_RECT.collidepoint(mouse_pos): reset_game()
            
            if blender.rect.collidepoint(mouse_pos):
                if blender.has_milk and blender.has_scoop and not blender.is_blended: blender.is_blended = True
                elif blender.is_blended: blender.dragging = True; held_item = blender
            
            for b in bottles.values():
                if b.rect.collidepoint(mouse_pos): b.dragging = True; held_item = b
            
            for name, bowl in bowls.items():
                if bowl["rect"].collidepoint(mouse_pos):
                    info = TOPPING_STATIONS[name]
                    held_item = Draggable(name, info["spawn"], info["spawn_size"], mouse_pos, "topping_drag")
                    held_item.dragging = True
            
            for item in placed_items:
                if item.rect.collidepoint(mouse_pos): item.dragging = True; held_item = item
            
            if not held_item:
                if pygame.Rect(CUP_STATION_POS, (150, 300)).collidepoint(mouse_pos):
                    held_item = Draggable("Cup", "Cup.png", (200, 300), mouse_pos, "base"); held_item.dragging = True
                elif pygame.Rect(CONE_STATION_POS, (220, 150)).collidepoint(mouse_pos):
                    held_item = Draggable("Cone", "Cone.png", (180, 320), mouse_pos, "base"); held_item.dragging = True
                for i, f in enumerate(FLAVORS):
                    if pygame.Rect(FLAVOR_POS[i], TUB_SIZE).collidepoint(mouse_pos):
                        active_scoops.append(Scoop(f, mouse_pos))

        if event.type == pygame.MOUSEBUTTONUP:
            if held_item:
                is_topping_type = held_item.type in ["bottle", "topping_drag"]
                if is_topping_type:
                    if held_item.name == "milk":
                        if held_item.rect.colliderect(blender.rect): blender.has_milk = True
                    else:
                        for target in placed_items:
                            if held_item.rect.colliderect(target.rect):
                                if not any(t.name == held_item.name for t in target.attached_toppings):
                                    can_add = (held_item.name == "cream" and target.name == "Cup" and target.liquid_flavor) or \
                                              (held_item.name in ["cherry", "sprinkles"] and target.attached_scoop)
                                    if can_add:
                                        info = TOPPING_STATIONS[held_item.name]
                                        new_t = Draggable(held_item.name, info["spawn"], info["spawn_size"], target.rect.center, "topping")
                                        target.attached_toppings.append(new_t)
                    
                    if held_item.type == "bottle":
                        held_item.dragging = False; held_item.rect.center = held_item.start_pos
                    held_item = None
                
                elif held_item.name == "Blender":
                    for target in placed_items:
                        if target.name == "Cup" and held_item.rect.colliderect(target.rect):
                            target.liquid_flavor = blender.liquid_flavor
                            active_scoops = [s for s in active_scoops if not s.locked_in_blender]
                            blender.has_milk, blender.has_scoop, blender.is_blended = False, False, False
                    held_item.dragging = False; held_item.rect.center = BLENDER_BASE_POS; held_item = None
                
                elif held_item.type == "base":
                    if held_item not in placed_items: placed_items.append(held_item)
                    held_item.dragging = False; held_item = None
            
            for s in active_scoops[:]:
                if s.dragging:
                    s.dragging = False
                    if s.rect.colliderect(blender.rect) and not blender.is_blended and not blender.has_scoop:
                        blender.has_scoop = True; blender.liquid_flavor = s.flavor; s.locked_in_blender = True
                        s.rect.center = (blender.rect.centerx, blender.rect.centery + 20)
                    else:
                        for target in placed_items:
                            if target.name == "Cone" and s.rect.colliderect(target.rect) and target.attached_scoop is None:
                                target.attached_scoop = s; active_scoops.remove(s); break
                        if s in active_scoops: active_scoops.remove(s)

    # --- UPDATES ---
    if held_item: held_item.rect.center = mouse_pos
    for s in active_scoops:
        if s.dragging: s.rect.center = mouse_pos
    
    update_list = placed_items + ([held_item] if held_item and held_item.type == "base" else [])
    for item in update_list:
        if item.attached_scoop:
            item.attached_scoop.rect.center = (item.rect.centerx, item.rect.top + (50 if item.name == "Cone" else 90))
        
        for t in item.attached_toppings:
            offset = TOPPING_STATIONS[t.name]["offset"]
            anchor_y = item.rect.top if (item.name == "Cup" and t.name == "cream") else (item.attached_scoop.rect.top if item.attached_scoop else item.rect.top)
            t.rect.center = (item.rect.centerx, anchor_y + offset)

    # --- DRAWING ---
    screen.blit(bg_img, (0, 0))
    customer.update(dt); customer.draw(screen); chat_bubble.update(dt); chat_bubble.draw(screen)
    screen.blit(cone_bowl_img, CONE_STATION_POS); screen.blit(cup_station_img, CUP_STATION_POS)
    
    for i, f in enumerate(FLAVORS):
        screen.blit(load_img(f"{f.capitalize()}_tub.png", TUB_SIZE), FLAVOR_POS[i])
    
    for bowl in bowls.values(): screen.blit(bowl["img"], bowl["rect"])
    for b in bottles.values():
        if not b.dragging: screen.blit(b.image, b.rect)
    
    pygame.draw.rect(screen, (220, 60, 60), RESET_RECT, border_radius=10)
    screen.blit(font.render("RESET", True, (255, 255, 255)), (RESET_RECT.x + 40, RESET_RECT.y + 10))

    # Helper function to draw treating logic consistently for static and dragged items
    def draw_treat(treat):
        if treat.name == "Cup":
            if treat.liquid_flavor:
                liq = load_img(f"{treat.liquid_flavor.capitalize()}_liq.png", (150, 200))
                screen.blit(liq, (treat.rect.x + 25, treat.rect.y + 65))
            # Sort toppings (draw Sprinkles before Cherry)
            sorted_t = sorted(treat.attached_toppings, key=lambda x: TOPPING_STATIONS[x.name]["offset"], reverse=True)
            for t in sorted_t: screen.blit(t.image, t.rect)
            screen.blit(treat.image, treat.rect)
        else:
            screen.blit(treat.image, treat.rect)
            if treat.attached_scoop: screen.blit(treat.attached_scoop.image, treat.attached_scoop.rect)
            sorted_t = sorted(treat.attached_toppings, key=lambda x: TOPPING_STATIONS[x.name]["offset"], reverse=True)
            for t in sorted_t: screen.blit(t.image, t.rect)

    # Draw static placed items
    for item in placed_items:
        if item != held_item: draw_treat(item)

    # Blender drawing...
    if blender.has_milk and not blender.is_blended:
        screen.blit(milk_liq_img, (blender.rect.x + 40, blender.rect.y + 150))
    if blender.has_scoop and not blender.is_blended:
        for s in active_scoops:
            if s.locked_in_blender: screen.blit(s.image, s.rect)
    if blender.is_blended and blender.liquid_flavor:
        blend_liq = load_img(f"{blender.liquid_flavor.capitalize()}_liq.png", (220, 280))
        screen.blit(blend_liq, (blender.rect.x + 40, blender.rect.y + 150))
    if not blender.dragging: screen.blit(blender.image, blender.rect)
    for s in active_scoops:
        if not s.locked_in_blender: screen.blit(s.image, s.rect)

    # Draw the held item on top
    if held_item:
        if held_item.type == "base":
            draw_treat(held_item)
        else:
            screen.blit(held_item.image, held_item.rect)

    pygame.display.flip()