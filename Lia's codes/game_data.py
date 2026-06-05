import os

CURRENT_LEVEL = 1

SAVE_PATH = os.path.join(
    os.path.dirname(__file__),
    "save.txt"
)

try:
    with open(SAVE_PATH, "r") as f:
        UNLOCKED_LEVEL = int(f.read().strip())
except:
    UNLOCKED_LEVEL = 1