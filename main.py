import pygame as pg
import sys
import random
import json
from icecream import ic
from sprites import *
from Enemies import Enemies
from GameMenu import GameMenu
from BossBattle import Boss

pg.init()


def get_user_information() -> dict:
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print("File was not found")


def write_to_json(file_content):
    try:
        with open(filename, 'w') as json_file:
            json.dump(file_content, json_file, indent=4)
    except FileNotFoundError:
        print("File was not found")
    

class Main():
    def __init__(self):
        # » Pygame initializatie
        self.screen = screen
        pg.display.set_icon(logo)

        # » Player initializatie
        self.player = pg.transform.scale_by(pg.image.load("./sprites/spaceship.png"), 0.5)
        self.player_rect = self.player.get_rect(center=(WIDTH / 2, HEIGHT - 70))

        # » Booleans
        self.is_paused: bool = False
        self.shot_fired: bool = False

        # » Prestaties
        self.score: int = 0
        self.highscore: int = 0
        self.difficulty: int = 1

        # » Opponents
        self.enemies: list[Enemies] = [Enemies() for _ in range(random.randint(2, 6))]
        self.bosses: list[Boss] = []
        self.bullet = None

        # » Username variabelen
        self.user_input_box = pg.Rect(WIDTH / 2 - 150, HEIGHT / 2 - 25, 10, 50)
        self.color_inactive = pg.Color('gray72')
        self.color_active = pg.Color('gray92')
        self.color = self.color_inactive
        self.active: bool = False
        self.text_input: str = ''
        self.username: str = ''

        self.get_username()

    def movement(self, rect, speed: float = 4.5) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            rect.x += 0 if rect.right + speed >= WIDTH else speed

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            rect.x -= 0 if rect.left - speed <= 0 else speed

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            rect.y += 0 if rect.bottom + speed >= HEIGHT else speed
        
        if keys[pg.K_UP] or keys[pg.K_w]:
            rect.y -= 0 if rect.top - speed <= 0 else speed

    def get_username(self) -> None:
        pg.display.set_caption("Space Junkies")

        while True:
            screen.fill("black")
            screen.blit(bg, (0, 0))
            screen.blit(logo, logo_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(), sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.user_input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                
                if event.type == pg.KEYDOWN:
                 if self.active:
                    if event.key == pg.K_RETURN:
                        ic(self.text_input)
                        self.username = self.text_input
                        self.text_input = ''
                        self.user_information = get_user_information()
                        if self.username in self.user_information.keys():
                            self.highscore = self.user_information[self.username]["highscore"]
                            self.score = self.user_information[self.username]["score"]
                            self.enemies = [Enemies() for _ in range(self.user_information[self.username]["enemies"])]
                            self.difficulty = self.user_information[self.username]["difficulty"]

                        self.start_death_screen("start")

                    elif event.key == pg.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    else:
                        self.text_input += event.unicode

            self.txt_surface = font.render(self.text_input, True, self.color)
            self.user_input_box.w = max(300, self.txt_surface.get_width()+10)

            self.user_txt_surface = font.render("Enter your username", True, self.color) 
            self.user_txt_rect = self.user_txt_surface.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))

            screen.blit(self.user_txt_surface, self.user_txt_rect)
            screen.blit(self.txt_surface, (self.user_input_box.x+5, self.user_input_box.y+5))
            pg.draw.rect(screen, self.color, self.user_input_box, 2)
            pg.display.update()
            clock.tick(60)

    def save_game(self):
        self.user_information[self.username] = {
            "highscore": self.highscore,
            "score": self.score,
            "enemies": len(self.enemies),
            "difficulty": self.difficulty
        }

        write_to_json(self.user_information)


    def start_death_screen(self, choice: str = "start") -> None:
        pg.display.set_caption("Space Junkies")

        if choice == "start":
            choice_button = font.render("Press enter to start", True, "white")
        elif choice == "death":
            choice_button = font.render("Press enter to try again", True, "white")
        choice_rect = choice_button.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        while True:
            screen.fill("black")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(), sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.restart() if choice == "death" else None
                        self.run()

            screen.blit(bg, (0, 0))
            screen.blit(logo, logo_rect)
            screen.blit(choice_button, choice_rect)

            pg.display.update()
            clock.tick(60)


    def pause(self) -> None:
        pg.display.set_caption("Space Junkies => Game Paused")
        while True:
            pause_music.play()
            menu = GameMenu(self.screen)
            if menu.events() == 'Resume':
                pause_music.stop()
                break
            if menu.events() == 'Quit':
                pause_music.stop()
                menu.quit()
            if menu.events() == 'Restart':
                pause_music.stop()
                self.score = 0
                self.bullet = None
                self.enemies = [Enemies() for _ in range(random.randint(2, 6))]
                break
            if menu.events() == 'Save':
                self.save_game()
                pg.quit(), sys.exit()
            
            pg.display.update()
            clock.tick(60)


    def restart(self) -> None:
        self.score = 0
        self.bullet = None
        self.enemies = [Enemies() for _ in range(random.randint(2, 6))]
        self.player_rect.center = (WIDTH / 2, HEIGHT - 70)


    def draw(self) -> None:
        screen.fill("black")
        screen.blit(bg, (0, 0))
        pg.draw.rect(screen, "yellow", self.bullet) if self.bullet else None    
        screen.blit(self.player, (self.player_rect))
        for enemy in self.enemies:
            enemy.draw(self.screen)
        screen.blit(font.render(f"Score: {self.score}", True, "white"), (0, 0))
        screen.blit(font.render(f"Highscore: {self.highscore}", True, "white"), (0, 25))


    def bullets(self) -> None:
        if not self.shot_fired:
            shot.play()
            self.shot_fired = True
        self.bullet.y -= 12.5

        for enemy in self.enemies:
            if enemy.collision(self.bullet):
                self.enemies.remove(enemy)
                self.score += 1
                self.bullet = None
                for _ in range(random.randint(1, 2)):
                    self.enemies.append(Enemies())
                break
        
        if self.bullet is not None:
            if self.bullet.y < 0:
                self.bullet = None
                self.shot_fired = False


    def boss_fight(self) -> None:
        if self.bullet is not None:
            if self.boss_class.boss_collision(self.bullet):
                self.boss_class.health.hp -= random.randint(10, 50)
                self.bullet = None

        if self.boss_class.bullet_collision(self.player_rect):
            self.start_death_screen("death")

        if self.boss_class.health.hp <= 0:
            return 'Death'

    # » Main loop
    def run(self) -> None:
        pg.display.set_caption("Space Junkies")

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(), sys.exit()

            keys = pg.key.get_pressed()

            if keys[pg.K_ESCAPE] or keys[pg.K_p]:
                self.pause()  # Open het pauzemenu

            if keys[pg.K_SPACE] and self.bullet is None:
                self.bullet = pg.Rect(self.player_rect.centerx - 5, self.player_rect.top, 6.67, 13.33)

            self.draw()
            self.movement(self.player_rect)


            if self.bullet is not None:
                self.bullets()

            for enemy in self.enemies: 
                if enemy.collision(self.player_rect):
                    self.start_death_screen("death")


            if self.score % 25 >= 0 and self.score % 25 <= 3 and self.score > 3:
                if len(self.bosses) == 0:
                    self.amount_enemies = len(self.enemies)
                    self.enemies = []

                    self.boss_class = Boss(self.difficulty)
                    self.bosses = [self.boss_class]

                self.boss_class.events(screen)
                self.boss_fight()

                if self.boss_fight() == 'Death':
                    self.difficulty += 1
                    self.score += 10
                    self.bosses = []
                    self.enemies = [Enemies() for _ in range(self.amount_enemies)]

            self.highscore = self.score if self.score > self.highscore else self.highscore

            pg.display.update()
            clock.tick(60)


if __name__ == '__main__':
    Main()
