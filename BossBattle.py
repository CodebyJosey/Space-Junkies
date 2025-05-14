import sys, time, random
from sprites import *
from health import Health

class Boss:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.health = Health(WIDTH / 2 - 100, 0, 200, 15, 500 * (1 + (difficulty / 10)))
        self.img = pg.image.load("./sprites/boss.png")
        self.boss = pg.rect.Rect(WIDTH / 2 - 185, HEIGHT / 6, 370, 185)
        self.choice_x = random.choice(("+", "-"))
        self.choice_y = random.choice(("+", "-", "0"))
        self.bullet1 = None
        self.bullet2 = None
        self.ticks = 0


    def boss_collision(self, collider) -> bool:
        if self.boss.colliderect(collider):
            return True
        
    def bullet_collision(self, collider) -> bool:
        if self.bullet1 is not None:
            if self.bullet1.colliderect(collider):
                return True
            elif self.bullet2.colliderect(collider):
                return True
            else:
                return False


    def shoot(self):
        if self.bullet1 is None:
            self.bullet1 = pg.Rect(self.boss.centerx - 40, self.boss.bottom - 30, 6.67, 13.33)
        if self.bullet2 is None:
            self.bullet2 = pg.Rect(self.boss.centerx + 40, self.boss.bottom - 30, 6.67, 13.33)
        
        if self.bullet1 is not None:
            self.bullet1.y += 7 * (1 + (self.difficulty / 10))
            if self.bullet1.y > HEIGHT:
                self.bullet1 = None

        if self.bullet2 is not None:
            self.bullet2.y += 7 * (1 + (self.difficulty / 10))
            if self.bullet2.y > HEIGHT:
                self.bullet2 = None
                self.ticks = 0

        return self.bullet1, self.bullet2


    def movement(self):
        if self.choice_x == "+":
            self.boss.x += 1 * (1 + (self.difficulty / 10))
        elif self.choice_x == "-":
            self.boss.x -= 1 * (1 + (self.difficulty / 10))

        if self.choice_y == "+":
            self.boss.y += 1 * (1 + (self.difficulty / 10))
        elif self.choice_y == "-":
            self.boss.y -= 1 * (1 + (self.difficulty / 10))

        if self.boss.right >= WIDTH or self.boss.bottom >= HEIGHT/2:
            self.choice_x = random.choice(("-", "0"))
            self.choice_y = random.choice(("-", "0"))
        elif self.boss.left <= 0 or self.boss.top <= 0:
            self.choice_x = random.choice(("+", "0"))
            self.choice_y = random.choice(("+", "0"))

        
    def draw(self, surface):
        self.health.draw(surface)
        surface.blit(self.img, (self.boss.x, self.boss.y - 92.5))
        pg.draw.rect(screen, "red", self.bullet1) if self.bullet1 else None
        pg.draw.rect(screen, "red", self.bullet2) if self.bullet2 else None
    

    def events(self, surface):
        self.ticks += 1
        if self.ticks >= (150 / self.difficulty):
            self.shoot()
        self.draw(surface)
        self.movement()


if __name__ == '__main__':
    def main():
        boss = Boss(2)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(), sys.exit()
            screen.fill("darkblue")

            boss.events(screen)
            boss.health.hp -= 0.5

            pg.display.update()
            clock.tick(60)

    main()
