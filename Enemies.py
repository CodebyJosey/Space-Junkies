import sys, time, random
from sprites import *

# TODO: Enemy HP toevoegen

class Enemies:
    def __init__(self):
        self.randx = random.randint(10, WIDTH - 15)
        self.randy = random.randint(10, int(HEIGHT * 2/3))
        self.img = random.choice((enemy_surf))
        self.enemy = self.img.get_rect(center=(self.randx, self.randy))
        self.choice_x = random.choice(("+", "-", "0"))
        self.choice_y = random.choice(("+", "-", "0"))


    def move(self):
        if self.choice_x == "+":
            self.enemy.x += 1
        elif self.choice_x == "-":
            self.enemy.x -= 1

        if self.choice_y == "+":
            self.enemy.y += 1
        elif self.choice_y == "-":
            self.enemy.y -= 1

        if self.enemy.right >= WIDTH or self.enemy.bottom >= HEIGHT:
            self.choice_x = random.choice(("-", "0"))
            self.choice_y = random.choice(("-", "0"))
        elif self.enemy.left <= 0 or self.enemy.top <= 0:
            self.choice_x = random.choice(("+", "0"))
            self.choice_y = random.choice(("+", "0"))


    def collision(self, collider) -> bool:
        if self.enemy.colliderect(collider):
            return bool(True)


    def draw(self, surface):
        self.move()
        surface.blit(self.img, (self.enemy))
