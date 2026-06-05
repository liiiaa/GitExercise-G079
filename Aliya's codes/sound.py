import pygame

pygame.mixer.init()

current_music = None


def play_music(file, volume=0.4, loop=True):
    global current_music

    if current_music != file:
        pygame.mixer.music.stop()
        print("Loading:", file)
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(volume)

        loops = -1 if loop else 0
        pygame.mixer.music.play(loops)

        current_music = file


def stop_music():
    pygame.mixer.music.stop()