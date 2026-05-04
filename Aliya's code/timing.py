# level 1 - 60 sec, lvl 2 - 45 sec, lvl 3 (final level) - 30 sec
level_times = {
    1: 60,
    2: 45,
    3: 30
}

timer = 0


def start_level(level):
    global timer
    timer = level_times.get(level, 60)  # default 60 if level not found


def update_timer(dt):
    global timer
    timer -= dt
    if timer < 0:
        timer = 0


def get_time():
    return int(timer)


def is_time_up():
    return timer <= 0