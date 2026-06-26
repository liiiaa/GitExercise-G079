import pygame
import subprocess
import sys
import os
print(
    "READING LEVEL FROM:",
    os.path.abspath("current_level.txt")
)
import random
import game_data

# ==================================================
# INITIALIZATION
# ==================================================
pygame.init()

SCREEN_W, SCREEN_H = 1920, 1080
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

# link w aliya's codes
sys.path.append(os.path.join(PARENT_DIR, "Aliya's codes"))

from sound import play_music, play_sound_effect
from score import calculate_score, get_score, reset_score
from timing import start_level, update_timer, get_time, is_time_up

MUSIC_FOLDER = os.path.join(PARENT_DIR, "Sound Tracks")

GAMEPLAY_MUSIC = os.path.join(MUSIC_FOLDER, "gameplay.mp3")
CORRECT_SOUND = os.path.join(MUSIC_FOLDER, "correct.mp3")
WRONG_SOUND = os.path.join(MUSIC_FOLDER, "wrong.mp3")
LEVEL_COMPLETE_SOUND = os.path.join(MUSIC_FOLDER, "level_complete.mp3")

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
exit_btn_img = load_img("Exit.png", (200, 100))
guide_btn_img = load_img("Instruction.png", (200, 100))

guide_screen_img = load_img(
    "Instruction2.png",
    (SCREEN_W, SCREEN_H)
)


RESET_RECT = pygame.Rect(1680, 900, 200, 70)
SERVE_BUTTON_RECT = pygame.Rect(60, 900, 200, 70)
SERVE_ZONE_RECT = pygame.Rect(760, 400, 400, 400)
EXIT_BUTTON_RECT = pygame.Rect(20, 60, 100, 100)
GUIDE_BUTTON_RECT = pygame.Rect(140, 60, 100, 100)

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

ALL_FLAVOR_POS = {
    "vanilla": (250, 620),
    "strawberry": (500, 620),
    "mango": (750, 620),
    "chocolate": (250, 820),
    "chocomint": (500, 820),
    "coffee": (750, 820)
}

try:
    with open("current_level.txt", "r") as f:
        CURRENT_LEVEL = int(f.read().strip())
except:
    CURRENT_LEVEL = 1
    print("CURRENT LEVEL FILE READ =", CURRENT_LEVEL)

LEVEL_UNLOCKS = {
    1: {
        "flavors": ["vanilla", "chocolate"],
        "toppings": [],
        "cups": False,
        "milkshakes": False,
        "combo": False
    },

    2: {
        "flavors": ["vanilla", "chocolate", "strawberry", "chocomint"],
        "toppings": ["cherry"],
        "cups": False,
        "milkshakes": False,
        "combo": False
    },

    3: {
        "flavors": ["vanilla", "chocolate", "strawberry", "chocomint", "mango", "coffee"],
        "toppings": ["cherry", "sprinkles"],
        "cups": False,
        "milkshakes": False,
        "combo": False
    },

    4: {
        "flavors": ["vanilla", "chocolate", "strawberry", "chocomint", "mango", "coffee"],
        "toppings": ["cherry", "sprinkles", "cream", "milk"],
        "cups": True,
        "milkshakes": True,
        "combo": False
    },

    5: {
        "flavors": ["vanilla", "chocolate", "strawberry", "chocomint", "mango", "coffee"],
        "toppings": ["cherry", "sprinkles", "cream", "milk"],
        "cups": True,
        "milkshakes": True,
        "combo": True
    }
}

orders_completed = 0

def refresh_level():
    global FLAVORS

    FLAVORS = LEVEL_UNLOCKS[CURRENT_LEVEL]["flavors"]
refresh_level()

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
    def show(self, message, duration=15):
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

    
    if CURRENT_LEVEL == 5:

        base1 = random.choice(["Cone", "Cup"])
        base2 = random.choice(["Cone", "Cup"])

        flavor1 = random.choice(FLAVORS)
        flavor2 = random.choice(FLAVORS)

        current_order = {
            "combo": True,

            "item1": {
                "base": base1,
                "flavor": flavor1
            },

            "item2": {
                "base": base2,
                "flavor": flavor2
            }
        }
        

        order_string = (
            f"One {flavor1} {base1} and "
            f"{flavor2} {base2} please!"
        )

        chat_bubble.show(order_string)

        return

    if LEVEL_UNLOCKS[CURRENT_LEVEL]["cups"]:
     base = random.choice(["Cup", "Cone"])
    else:
     base = "Cone"
    flavor = random.choice(FLAVORS)
    toppings = []
    if base == "Cup":

        if "cream" in LEVEL_UNLOCKS[CURRENT_LEVEL]["toppings"]:
            if random.random() > 0.5:
                toppings.append("cream")

        order_string = (
            f"A {flavor} milkshake"
            f"{' with cream' if 'cream' in toppings else ''}!"
    )
    else:
        if "sprinkles" in LEVEL_UNLOCKS[CURRENT_LEVEL]["toppings"]:
             if random.random() > 0.4:
                toppings.append("sprinkles")

        if "cherry" in LEVEL_UNLOCKS[CURRENT_LEVEL]["toppings"]:
             if random.random() > 0.4:
                 toppings.append("cherry")
        top_str = " and ".join(toppings) if toppings else "no toppings"
        order_string = f"One {flavor} cone with {top_str} please!"
    current_order = {"base": base, "flavor": flavor, "toppings": sorted(toppings)}
    chat_bubble.show(order_string)

def check_service():
    global current_order, orders_completed

    print("SERVE CLICKED")
    print("CURRENT LEVEL =", CURRENT_LEVEL)
    print("CURRENT ORDER =", current_order)

    # ==========================
    # LEVEL 5 COMBO ORDERS
    # ==========================
    if CURRENT_LEVEL == 5 and current_order.get("combo"):

        served_items = []

        for item in placed_items:
            if SERVE_ZONE_RECT.colliderect(item.rect):
                served_items.append(item)

        if len(served_items) != 2:
            chat_bubble.show("Serve BOTH items together please!")
            return

        item_data = []

        for item in served_items:

            flavor = (
                item.liquid_flavor
                if item.name == "Cup"
                else (
                    item.attached_scoop.flavor
                    if item.attached_scoop
                    else None
                )
            )

            item_data.append({
                "base": item.name,
                "flavor": flavor
            })

        expected = [
            current_order["item1"],
            current_order["item2"]
        ]

        if sorted(item_data, key=str) == sorted(expected, key=str):
            play_sound_effect(CORRECT_SOUND)
            calculate_score(True, get_time())

            chat_bubble.show("Amazing! Thank you!")

            for item in served_items:
                if item in placed_items:
                    placed_items.remove(item)

            orders_completed += 1

            if orders_completed >= 3:
                play_sound_effect(LEVEL_COMPLETE_SOUND)
                pygame.time.set_timer(
                    pygame.USEREVENT + 3,
                    2500
                )
                
            pygame.time.set_timer(pygame.USEREVENT + 1, 2500)

        else:
            play_sound_effect(WRONG_SOUND)
            calculate_score(False, get_time())
            chat_bubble.show(
                f"Incorrect... I wanted: {order_string}",
                duration=5
            )

        return

    # ==========================
    # NORMAL ORDERS (LEVELS 1-4)
    # ==========================
    served_item = None

    for item in placed_items:
        if SERVE_ZONE_RECT.colliderect(item.rect):
            served_item = item
            break

    if not served_item:
        chat_bubble.show("Drop it in the middle area!")
        return

    actual_flavor = (
        served_item.liquid_flavor
        if served_item.name == "Cup"
        else (
            served_item.attached_scoop.flavor
            if served_item.attached_scoop
            else None
        )
    )

    actual_toppings = sorted(
        [t.name for t in served_item.attached_toppings]
    )

    if (
        served_item.name == current_order["base"]
        and actual_flavor == current_order["flavor"]
        and actual_toppings == current_order["toppings"]
    ):
        play_sound_effect(CORRECT_SOUND)
        calculate_score(True, get_time())

        chat_bubble.show("Yummy! Thank you!")

        if served_item in placed_items:
            placed_items.remove(served_item)

        orders_completed += 1

        if orders_completed >= 3:
            play_sound_effect(LEVEL_COMPLETE_SOUND)
            pygame.time.set_timer(
                    pygame.USEREVENT + 3,
                    2500
                )

        pygame.time.set_timer(
            pygame.USEREVENT + 1,
            2500
        )

    else:
        play_sound_effect(WRONG_SOUND)
        calculate_score(False, get_time())
        chat_bubble.show(
            f"Incorrect... I wanted: {order_string}",
            duration=5
        )
        
def show_completion_screen():
    global CURRENT_LEVEL, orders_completed

    button_rect = pygame.Rect(
        SCREEN_W // 2 - 150,
        SCREEN_H // 2 + 80,
        300,
        80
    )

    level_select_rect = pygame.Rect(
        SCREEN_W // 2 - 150,
        SCREEN_H // 2 + 180,
        300,
        80)

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if level_select_rect.collidepoint(event.pos):

                    SAVE_PATH = os.path.join(
                        os.path.dirname(__file__),
                        "save.txt"
                    )

                    if CURRENT_LEVEL < 5:
                        unlocked = CURRENT_LEVEL + 1

                        if unlocked > game_data.UNLOCKED_LEVEL:
                            game_data.UNLOCKED_LEVEL = unlocked

                        with open(SAVE_PATH, "w") as f:
                            f.write(str(game_data.UNLOCKED_LEVEL))

                        print("SAVED UNLOCKED LEVEL =", game_data.UNLOCKED_LEVEL)

                    print("LEVEL SELECT CLICKED")
                    return "LEVEL_SELECT"
                
                if button_rect.collidepoint(event.pos):

                    if CURRENT_LEVEL == 5:
                        pygame.quit()
                        sys.exit()

                    CURRENT_LEVEL += 1

                    with open("current_level.txt", "w") as f:
                        f.write(str(CURRENT_LEVEL))

                    game_data.CURRENT_LEVEL = CURRENT_LEVEL

                    if CURRENT_LEVEL > game_data.UNLOCKED_LEVEL:
                        game_data.UNLOCKED_LEVEL = CURRENT_LEVEL

                    SAVE_PATH = os.path.join(
                        os.path.dirname(__file__),
                        "save.txt"
                    )

                    with open(SAVE_PATH, "w") as f:
                        f.write(str(game_data.UNLOCKED_LEVEL))


                    refresh_level() 

                    orders_completed = 0

                    reset_items_only()

                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)

                    pygame.event.clear(pygame.USEREVENT + 1)
                    pygame.event.clear(pygame.USEREVENT + 2)

                    pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

                    running = False

        screen.fill((255, 240, 220))

        title = pygame.font.SysFont(
            "Comic Sans MS",
            80,
            bold=True
        ).render(
            "LEVEL COMPLETE!",
            True,
            (255, 120, 120)
        )

        level_text = font.render(
            f"Level {CURRENT_LEVEL} cleared!",
            True,
            (80, 50, 20)
        )

        unlock_text = font.render(
            "New items unlocked!",
            True,
            (80, 50, 20)
        )

        screen.blit(
            title,
            (
                SCREEN_W // 2 - title.get_width() // 2,
                250
            )
        )

        screen.blit(
            level_text,
            (
                SCREEN_W // 2 - level_text.get_width() // 2,
                400
            )
        )

        screen.blit(
            unlock_text,
            (
                SCREEN_W // 2 - unlock_text.get_width() // 2,
                450
            )
        )

        pygame.draw.rect(
            screen,
            (120, 220, 120),
            button_rect,
            border_radius=20)

        if CURRENT_LEVEL == 5:
            button_text = font.render(
                "FINISH GAME",
                True,
                (255,255,255)
            )
        else:
            button_text = font.render(
                "NEXT LEVEL",
                True,
                (255,255,255)
            )

        screen.blit(
            button_text,
            (
                button_rect.centerx - button_text.get_width() // 2,
                button_rect.centery - button_text.get_height() // 2
            )
        )
        pygame.draw.rect(
            screen,
            (120, 120, 220),
            level_select_rect,
            border_radius=20)

        level_select_text = font.render(
            "LEVEL SELECT",
            True,
            (255, 255, 255))

        screen.blit(
            level_select_text,
            (
                level_select_rect.centerx - level_select_text.get_width() // 2,
                level_select_rect.centery - level_select_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

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

play_music(GAMEPLAY_MUSIC)
reset_score()
start_level(CURRENT_LEVEL)

generate_order()

show_guide = False
go_to_main_menu = False
running = True
go_to_level_select = False
time_up_triggered = False

while running:
    dt = clock.tick(60) / 1000
    update_timer(dt)
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            if GUIDE_BUTTON_RECT.collidepoint(mouse_pos):
                show_guide = not show_guide

            if EXIT_BUTTON_RECT.collidepoint(mouse_pos):
                go_to_main_menu = True
                running = False

            if RESET_RECT.collidepoint(mouse_pos): reset_items_only()

            if SERVE_BUTTON_RECT.collidepoint(mouse_pos) and customer.visible:
                result = check_service()

                if result == "LEVEL_SELECT":
                    go_to_level_select = True
                    running = False
            
            if blender.rect.collidepoint(mouse_pos):
                if blender.has_milk and blender.has_scoop and not blender.is_blended: blender.is_blended = True
                elif blender.is_blended: blender.dragging = True; held_item = blender
            for name, b in bottles.items():

                if name == "milk" and CURRENT_LEVEL < 4:
                    continue

                if name == "cream" and CURRENT_LEVEL < 4:
                    continue
                if b.rect.collidepoint(mouse_pos):
                     b.dragging = True; held_item = b
            for name, bowl in bowls.items():

                if name not in LEVEL_UNLOCKS[CURRENT_LEVEL]["toppings"]:
                    continue

                if bowl["rect"].collidepoint(mouse_pos):
                    info = TOPPING_STATIONS[name]
                    held_item = Draggable(name, info["spawn"], info["spawn_size"], mouse_pos, "topping_drag"); held_item.dragging = True
            for item in placed_items:
                if item.rect.collidepoint(mouse_pos): item.dragging = True; held_item = item
            if not held_item:
                if LEVEL_UNLOCKS[CURRENT_LEVEL]["cups"] and pygame.Rect(CUP_STATION_POS, (150, 300)).collidepoint(mouse_pos):
                    held_item = Draggable("Cup", "Cup.png", (200, 300), mouse_pos, "base"); held_item.dragging = True
                elif pygame.Rect(CONE_STATION_POS, (220, 150)).collidepoint(mouse_pos):
                    held_item = Draggable("Cone", "Cone.png", (180, 320), mouse_pos, "base"); held_item.dragging = True
                for f in FLAVORS:
                     if pygame.Rect(ALL_FLAVOR_POS[f], TUB_SIZE).collidepoint(mouse_pos):
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
            print("USEREvENT 1 FIRED")
            customer.visible = False
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

        if event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            generate_order()

        if event.type == pygame.USEREVENT + 3:
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)

            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)

            pygame.event.clear(pygame.USEREVENT + 1)
            pygame.event.clear(pygame.USEREVENT + 2)

            result = show_completion_screen()

            if result == "LEVEL_SELECT":
                go_to_level_select = True
                running = False

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
    screen.blit(cone_bowl_img, CONE_STATION_POS)

    if LEVEL_UNLOCKS[CURRENT_LEVEL]["cups"]:
        screen.blit(cup_station_img, CUP_STATION_POS)
    for f in FLAVORS:
        screen.blit(
         load_img(f"{f.capitalize()}_tub.png", TUB_SIZE),
         ALL_FLAVOR_POS[f]
    )
    for name, bowl in bowls.items():

        if name not in LEVEL_UNLOCKS[CURRENT_LEVEL]["toppings"]:
         continue

        screen.blit(bowl["img"], bowl["rect"])

    for name, b in bottles.items():

        if name == "milk" and CURRENT_LEVEL < 4:
         continue

        if name == "cream" and CURRENT_LEVEL < 4:
         continue

        if not b.dragging:
         screen.blit(b.image, b.rect)
    
    pygame.draw.rect(screen, (220, 60, 60), RESET_RECT, border_radius=15)
    screen.blit(font.render("RESET", True, (255, 255, 255)), (RESET_RECT.x + 50, RESET_RECT.y + 15))
    pygame.draw.rect(screen, (100, 200, 100), SERVE_BUTTON_RECT, border_radius=15)
    screen.blit(font.render("SERVE", True, (255, 255, 255)), (SERVE_BUTTON_RECT.x + 50, SERVE_BUTTON_RECT.y + 15))

    score_text = font.render(f"Score: {get_score()}", True, (139, 69, 19))
    time_text = font.render(f"Time: {get_time()}", True, (139, 69, 19))
    
    screen.blit(score_text, (830, 180))
    screen.blit(time_text, (830, 220))

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
    if CURRENT_LEVEL >= 4:
        if not blender.dragging:
            screen.blit(blender.image, blender.rect)

    for s in active_scoops:
        if not s.locked_in_blender: screen.blit(s.image, s.rect)
    if held_item:
        if held_item.type == "base": draw_treat(held_item)
        else: screen.blit(held_item.image, held_item.rect)

    screen.blit(exit_btn_img, EXIT_BUTTON_RECT.topleft)
    screen.blit(guide_btn_img, GUIDE_BUTTON_RECT.topleft)

    if show_guide:
        screen.blit(guide_screen_img, (0,0))

    if is_time_up() and not time_up_triggered:
        chat_bubble.show("Time's up!")
        pygame.time.set_timer(pygame.USEREVENT + 3, 100)
        time_up_triggered = True

    pygame.display.flip()

    
pygame.quit()

if go_to_main_menu:

    menu_path = os.path.join(
        os.path.dirname(__file__), "c:\\Users\\user\\MiniITProject\\GitExercise-G079\\Lia's codes\\MAIN(FINAL)"
    )

    subprocess.run(
        [sys.executable, menu_path]
    )

if go_to_level_select:
    ui_path = os.path.join(
        os.path.dirname(__file__),
        "ui_layout_screen2.py"
    )

    subprocess.run([sys.executable, ui_path])

pygame.quit()
sys.exit()