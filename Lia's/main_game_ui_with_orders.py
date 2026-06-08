import pygame
import sys
import os
import random

# ==================================================
# INITIALIZATION
# ==================================================
pygame.init()
SCREEN_W, SCREEN_H = 1920, 1200
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.DOUBLEBUF)
pygame.display.set_caption("A Scoop of Spring")
clock = pygame.time.Clock()

try:
    font = pygame.font.SysFont("Comic Sans MS", 25, bold=True)
except:
    font = pygame.font.SysFont("Arial", 25, bold=True)

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
        surf = pygame.Surface(size); surf.fill((255, 0, 255)); return surf

# ==================================================
# ASSETS & CONSTANTS
# ==================================================
bg_img = load_img("Game Background.png", (SCREEN_W, SCREEN_H))
cone_bowl_img = load_img("Cone_bowl.png", (220, 150))
cup_station_img = load_img("Cup.png", (150, 300))
milk_liq_img = load_img("Milk_liq.png", (220, 280))
char_smile_img = load_img("Char_smile.png", (420, 380))
char_talk_img = load_img("Char_talk.png", (420, 380))

RESET_RECT = pygame.Rect(1680, 1080, 200, 70)
SERVE_BUTTON_RECT = pygame.Rect(860, 1080, 200, 70)
SERVE_ZONE_RECT = pygame.Rect(760, 400, 400, 400)

BLENDER_BASE_POS = (1750, 350)
CUP_STATION_POS = (100, 380)
CONE_STATION_POS = (250, 480)
TUB_SIZE = (220, 160)

TOPPING_STATIONS = {
    "cream":    {"type": "bottle", "file": "Cream_bottle.png", "spawn": "Cream.png", "pos": (1200, 950), "size": (100, 280), "spawn_size": (160, 140), "offset": 90},
    "milk":     {"type": "bottle", "file": "Milk.png",         "spawn": "Milk.png",  "pos": (1400, 950), "size": (150, 250), "spawn_size": (100, 100), "offset": 0},
    "sprinkles":{"type": "bowl",   "file": "Sprinkles_bowl.png","spawn": "Sprinkles.png", "pos": (1180, 750), "size": (200, 140), "spawn_size": (120, 90), "offset": 100},
    "cherry":   {"type": "bowl",   "file": "Cherry_bowl.png",   "spawn": "Cherry.png",    "pos": (1380, 750), "size": (200, 140), "spawn_size": (80, 80), "offset": 30}
}

FLAVORS = ["vanilla", "strawberry", "mango", "chocolate", "chocomint", "coffee"]
FLAVOR_POS = [(250, 620), (500, 620), (750, 620), (250, 820), (500, 820), (750, 820)]

# ==================================================
# CLASSES
# ==================================================
class Character:
    def __init__(self, x, y, sprite_smile, sprite_talk):
        self.x, self.y = x, y
        self.sprite_smile, self.sprite_talk = sprite_smile, sprite_talk
        self.current_sprite = sprite_smile
        self.visible = False
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
    def draw(self, screen):
        if self.visible: screen.blit(self.current_sprite, (self.x, self.y))

class ChatBubble:
    def __init__(self, speaker, font):
        self.speaker, self.font = speaker, font
        self.text, self.active, self.timer = "", False, 0
    def show(self, message, duration=5):
        self.text, self.active, self.timer = message, True, duration
        self.speaker.is_talking = True; self.speaker.talk_timer = duration
    def update(self, dt):
        if self.active:
            self.timer -= dt
            if self.timer <= 0: self.active = False
    def draw(self, screen):
        if not self.active or not self.speaker.visible: return
        text_surf = self.font.render(self.text, True, (80, 50, 20)) 
        
        
        bubble_w = text_surf.get_width() + 40
        bubble_h = text_surf.get_height() + 20
        bx, by = self.speaker.x - 50, self.speaker.y - 60
        
        pygame.draw.rect(screen, (255, 255, 255), (bx, by, bubble_w, bubble_h), border_radius=15)
        pygame.draw.rect(screen, (220, 220, 220), (bx, by, bubble_w, bubble_h), 2, border_radius=15)
        screen.blit(text_surf, (bx + 20, by + 10))

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
# GAME LOGIC
# ==================================================
customer = Character(1100, 160, char_smile_img, char_talk_img)
chat_bubble = ChatBubble(customer, font)
current_order = None
order_string = ""

def generate_order():
    global current_order, order_string
    customer.visible = True
    base = random.choice(["Cup", "Cone"])
    flavor = random.choice(FLAVORS)
    toppings = []
    if base == "Cup":
        if random.random() > 0.5: toppings.append("cream")
        order_string = f"A {flavor} milkshake{' with cream' if 'cream' in toppings else ''}!"
    else:
        if random.random() > 0.4: toppings.append("sprinkles")
        if random.random() > 0.4: toppings.append("cherry")
        top_str = " and ".join(toppings) if toppings else "no toppings"
        order_string = f"One {flavor} cone with {top_str}!"
    current_order = {"base": base, "flavor": flavor, "toppings": sorted(toppings)}
    chat_bubble.show(order_string)

def check_service():
    global current_order
    served_item = None
    for item in placed_items:
        if SERVE_ZONE_RECT.colliderect(item.rect):
            served_item = item; break
    
    if not served_item:
        chat_bubble.show("Drop it in the middle area!"); return

    actual_flavor = served_item.liquid_flavor if served_item.name == "Cup" else (served_item.attached_scoop.flavor if served_item.attached_scoop else None)
    actual_toppings = sorted([t.name for t in served_item.attached_toppings])
    
    if (served_item.name == current_order["base"] and actual_flavor == current_order["flavor"] and actual_toppings == current_order["toppings"]):
        chat_bubble.show("Yummy! Thank you! ✨")
        placed_items.remove(served_item)
        pygame.time.set_timer(pygame.USEREVENT + 1, 2500)
    else:
        chat_bubble.show(f"Incorrect... I wanted: {order_string}", duration=5)

# ==================================================
# MAIN LOOP SETUP
# ==================================================
blender = Draggable("Blender", "Blender.png", (300, 550), BLENDER_BASE_POS, "blender")
bottles = {n: Draggable(n, d["file"], d["size"], d["pos"], "bottle") for n, d in TOPPING_STATIONS.items() if d["type"]=="bottle"}
bowls = {n: {"img": load_img(d["file"], d["size"]), "rect": load_img(d["file"], d["size"]).get_rect(center=d["pos"])} for n, d in TOPPING_STATIONS.items() if d["type"]=="bowl"}
active_scoops, placed_items, held_item = [], [], None

def reset_items_only():
    global active_scoops, placed_items, held_item
    active_scoops, placed_items, held_item = [], [], None
    blender.has_milk, blender.has_scoop, blender.is_blended = False, False, False
    blender.liquid_flavor, blender.rect.center = None, BLENDER_BASE_POS
    for b in bottles.values(): b.rect.center = b.start_pos

generate_order()

while True:
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if RESET_RECT.collidepoint(mouse_pos): reset_items_only()
            if SERVE_BUTTON_RECT.collidepoint(mouse_pos) and customer.visible: check_service()
            
            if blender.rect.collidepoint(mouse_pos):
                if blender.has_milk and blender.has_scoop and not blender.is_blended: blender.is_blended = True
                elif blender.is_blended: blender.dragging = True; held_item = blender
            for b in bottles.values():
                if b.rect.collidepoint(mouse_pos): b.dragging = True; held_item = b
            for name, bowl in bowls.items():
                if bowl["rect"].collidepoint(mouse_pos):
                    info = TOPPING_STATIONS[name]
                    held_item = Draggable(name, info["spawn"], info["spawn_size"], mouse_pos, "topping_drag"); held_item.dragging = True
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
                if held_item.type in ["bottle", "topping_drag"]:
                    if held_item.name == "milk" and held_item.rect.colliderect(blender.rect): blender.has_milk = True
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
                    if held_item.type == "bottle": held_item.rect.center = held_item.start_pos
                    held_item.dragging = False; held_item = None
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

        if event.type == pygame.USEREVENT + 1:
            customer.visible = False; pygame.time.set_timer(pygame.USEREVENT + 1, 0); pygame.time.set_timer(pygame.USEREVENT + 2, 2000)
        if event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0); generate_order()

    # --- POSITION UPDATES ---
    if held_item: held_item.rect.center = mouse_pos
    for s in active_scoops:
        if s.dragging: s.rect.center = mouse_pos
    for item in placed_items + ([held_item] if held_item and held_item.type == "base" else []):
        if item.attached_scoop: item.attached_scoop.rect.center = (item.rect.centerx, item.rect.top + (50 if item.name == "Cone" else 90))
        for t in item.attached_toppings:
            anchor_y = item.rect.top if (item.name == "Cup" and t.name == "cream") else (item.attached_scoop.rect.top if item.attached_scoop else item.rect.top)
            t.rect.center = (item.rect.centerx, anchor_y + TOPPING_STATIONS[t.name]["offset"])

    # --- DRAWING ---
    screen.blit(bg_img, (0, 0))
    customer.update(dt); customer.draw(screen); chat_bubble.update(dt); chat_bubble.draw(screen)
    
    screen.blit(cone_bowl_img, CONE_STATION_POS); screen.blit(cup_station_img, CUP_STATION_POS)
    for i, f in enumerate(FLAVORS): screen.blit(load_img(f"{f.capitalize()}_tub.png", TUB_SIZE), FLAVOR_POS[i])
    for bowl in bowls.values(): screen.blit(bowl["img"], bowl["rect"])
    for b in bottles.values(): 
        if not b.dragging: screen.blit(b.image, b.rect)
    
    pygame.draw.rect(screen, (220, 60, 60), RESET_RECT, border_radius=15)
    screen.blit(font.render("RESET", True, (255, 255, 255)), (RESET_RECT.x + 50, RESET_RECT.y + 15))
    pygame.draw.rect(screen, (100, 200, 100), SERVE_BUTTON_RECT, border_radius=15)
    screen.blit(font.render("SERVE", True, (255, 255, 255)), (SERVE_BUTTON_RECT.x + 50, SERVE_BUTTON_RECT.y + 15))

    def draw_treat(treat):
        if treat.name == "Cup":
            if treat.liquid_flavor:
                liq = load_img(f"{treat.liquid_flavor.capitalize()}_liq.png", (150, 200)); screen.blit(liq, (treat.rect.x + 25, treat.rect.y + 65))
            for t in sorted(treat.attached_toppings, key=lambda x: TOPPING_STATIONS[x.name]["offset"], reverse=True): screen.blit(t.image, t.rect)
            screen.blit(treat.image, treat.rect)
        else:
            screen.blit(treat.image, treat.rect)
            if treat.attached_scoop: screen.blit(treat.attached_scoop.image, treat.attached_scoop.rect)
            for t in sorted(treat.attached_toppings, key=lambda x: TOPPING_STATIONS[x.name]["offset"], reverse=True): screen.blit(t.image, t.rect)

    for item in placed_items:
        if item != held_item: draw_treat(item)

    if blender.has_milk and not blender.is_blended: screen.blit(milk_liq_img, (blender.rect.x + 40, blender.rect.y + 150))
    if blender.has_scoop and not blender.is_blended:
        for s in active_scoops:
            if s.locked_in_blender: screen.blit(s.image, s.rect)
    if blender.is_blended and blender.liquid_flavor:
        blend_liq = load_img(f"{blender.liquid_flavor.capitalize()}_liq.png", (220, 280)); screen.blit(blend_liq, (blender.rect.x + 40, blender.rect.y + 150))
    if not blender.dragging: screen.blit(blender.image, blender.rect)

    for s in active_scoops:
        if not s.locked_in_blender: screen.blit(s.image, s.rect)
    if held_item:
        if held_item.type == "base": draw_treat(held_item)
        else: screen.blit(held_item.image, held_item.rect)

    pygame.display.flip()