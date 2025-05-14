import pygame as pg

pg.init()

WIDTH, HEIGHT = 625, 625

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Shooter")

# Filename JSON
filename: str = 'spacejunkies.json'

# Sounds
shot = pg.mixer.Sound("./sprites/shot_fire.mp3")
bg_music = pg.mixer.Sound("./sprites/bg_music.mp3")
menu_sound = pg.mixer.Sound("./sprites/menu_sound.mp3")
pause_music = pg.mixer.Sound("./sprites/pause_music.mp3")

# Fonts
font = pg.font.Font("./sprites/font.otf", 20)

# Pictures
bg = pg.transform.scale(pg.image.load("./sprites/bg.png"), (WIDTH, HEIGHT))
logo = pg.transform.scale_by(pg.image.load("./sprites/space_junkies.png"), 0.8)
logo_rect = logo.get_rect(center=(WIDTH / 2, 100))

# Enemies
enemy1 = pg.transform.scale_by(pg.image.load("./sprites/enemy1.png"), 0.75)
enemy2 = pg.transform.scale_by(pg.image.load("./sprites/enemy2.png"), 0.75)
enemy3 = pg.transform.scale_by(pg.image.load("./sprites/enemy3.png"), 0.75)
enemy_surf = [enemy1, enemy2, enemy3]