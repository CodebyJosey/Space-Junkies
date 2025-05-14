import pygame as pg
import sys
from sprites import *

pg.init()

class GameMenu():
    def __init__(self, surface):
        self.surface = surface


    def resume(self) -> str:
        return 'Resume'


    def restart(self):
        return 'Restart'


    def save_game(self):
        return 'Save'


    def quit(self):
        pg.quit(), sys.exit()

    def draw(self, surface) -> None:
        surface.blit(logo, logo_rect)

        # Resume button
        self.resume_button = font.render("Resume game", True, "white")
        self.resume_rect = self.resume_button.get_rect(center=(WIDTH / 2, 250))
        surface.blit(self.resume_button, self.resume_rect)

        # Restart button
        self.restart_button = font.render("Restart game", True, "white")
        self.restart_rect = self.restart_button.get_rect(center=(WIDTH / 2, 300))
        surface.blit(self.restart_button, self.restart_rect)

        # Save game button
        self.save_button = font.render("Save game", True, "white")
        self.save_rect = self.save_button.get_rect(center=(WIDTH / 2, 350))
        surface.blit(self.save_button, self.save_rect)

        # Quit button
        self.quit_button = font.render("Quit game", True, "white")
        self.quit_rect = self.quit_button.get_rect(center=(WIDTH / 2, 400))
        surface.blit(self.quit_button, self.quit_rect)


    def events(self):
        mouse = pg.mouse.get_pos()
        self.draw(self.surface)

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.resume_rect.collidepoint(mouse):
                    return self.resume()

                if self.quit_rect.collidepoint(mouse):
                    self.quit()

                if self.restart_rect.collidepoint(mouse):
                    return self.restart()

                if self.save_rect.collidepoint(mouse):
                    return self.save_game()


def main() -> None:
    is_paused = False
    pg.display.set_caption("Game Menu tester")
    while not is_paused:
        screen.fill("black")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(), sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    is_paused = True

        pg.display.update()
        clock.tick(60)


    while is_paused:
        screen.fill("black")
        menu = GameMenu(screen)
        menu.events()

        pg.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
