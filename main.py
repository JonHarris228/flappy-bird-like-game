import pygame
import random
import math
import base64
from pygame import mixer

# Pygame innit
pygame.init()

# Technical vars
fps = 60
win_width, win_height = 720, 480
spr_width, spr_height = 100, 75
die = pygame.USEREVENT + 1

# Gameplay vars
grav = 0.25

# Set window
win = pygame.display.set_mode((win_width, win_height))

# Load sprite
ship_sprite = pygame.image.load('Assets/Ship.png')
wall_bot_sprite = pygame.image.load('Assets/Wall_bot.png')
wall_top_sprite = pygame.image.load('Assets/Wall_top.png')
rocket_sprite = pygame.image.load('Assets/Rocket.png')
back_ground_sprite = pygame.image.load('Assets/Background.png')
tap_start_sprite = pygame.image.load('Assets/Start.png')
beck_house_sprite = pygame.image.load('Assets/Back_house.png')
end_screen_sprite = pygame.image.load('Assets/End_screen.png')
button_sprite = pygame.image.load('Assets/Button_restart.png')


class Technical:
    def __init__(self):
        self.hit_box = None
        self.alpha = 150
        self.start_tap = False
        self.move_stop = True

        self.tap_start = pygame.Surface((win_width, win_height), pygame.SRCALPHA, 32)
        self.tap_start = self.tap_start.convert_alpha()
        self.tap_start.set_alpha(150)
        self.size = 0
        self.size_d = 1

        self.background_s = pygame.Surface((win_width, win_height), pygame.SRCALPHA, 32)
        self.background_s = self.background_s.convert_alpha()
        self.background_s.set_alpha(150)

        self.back_house_s = pygame.Surface((win_width, win_height), pygame.SRCALPHA, 32)
        self.back_house_s = self.back_house_s.convert_alpha()
        self.back_house_s.set_alpha(180)
        self.move = 0

        self.score_s = pygame.Surface((win_width, win_height), pygame.SRCALPHA, 32)
        self.score_s = self.score_s.convert_alpha()
        self.score_s.set_alpha(120)
        self.font_score = pygame.font.Font('Assets/fff-forward.regular.ttf', 100)

        self.end_s = pygame.Surface((win_width, win_height), pygame.SRCALPHA, 32)
        self.end_s = self.end_s.convert_alpha()
        self.font_current_score = pygame.font.Font('Assets/fff-forward.regular.ttf', 40)
        self.font_best_score = pygame.font.Font('Assets/fff-forward.regular.ttf', 15)

    def pre_start_draw(self):
        self.tap_start.fill((0, 0, 0, 0))
        if self.size >= 30:
            self.size_d = -1
        elif self.size <= -30:
            self.size_d = 1
        self.size += self.size_d * 0.5

        x = tap_start_sprite.get_width()
        y = tap_start_sprite.get_height()
        division = y / x
        sprite = pygame.transform.scale(tap_start_sprite, (x + self.size, y + self.size * division))

        self.tap_start.blit(sprite, (win_width / 2 - sprite.get_width() / 2,
                                     win_height / 2 - sprite.get_height() / 2))
        win.blit(self.tap_start, (0, 0))

    def on_tap(self):
        self.alpha -= 15
        self.tap_start.set_alpha(self.alpha)
        self.pre_start_draw()

    def background(self):
        self.background_s.blit(back_ground_sprite, (0, 0))
        win.blit(self.background_s, (0, 0))

    def back_house_loop(self):
        if self.move == -1200:
            self.move = 0
        else:
            self.move -= 3

    def back_house_draw(self):
        self.back_house_s.fill((0, 0, 0, 0))
        self.back_house_s.blit(beck_house_sprite, (self.move, 500 - 138))
        self.back_house_s.blit(beck_house_sprite, (self.move + 1200, 500 - 138))
        win.blit(self.back_house_s, (0, 0))

    def end_screen_draw(self, ship):
        best_score = base64.b64decode(open("Assets/bin", 'r').read()).decode('utf-8')
        best_score = best_score[len('Best score:'): best_score.find('end')]
        self.end_s.fill((0, 0, 0, 70))
        self.end_s.blit(end_screen_sprite, (225, 125))

        img = self.font_current_score.render('Score: {}'.format(ship.score), True, (0, 0, 0))
        self.end_s.blit(img, (225 + 225 - img.get_width() / 2, 125 + 90 - img.get_height() / 2))
        img = self.font_best_score.render('Best score: {}'.format(best_score), True, (50, 50, 50))
        self.end_s.blit(img, (225 + 225 - img.get_width() / 2, 125 + 40 - img.get_height() / 2))

        self.hit_box = pygame.Rect(225 + 225 - button_sprite.get_width() / 2,
                                   125 + 175 - button_sprite.get_height() / 2,
                                   button_sprite.get_width(), button_sprite.get_height())

        self.end_s.blit(button_sprite, self.hit_box)
        win.blit(self.end_s, (0, 0))

    def score_draw(self, score):
        self.score_s.fill((0, 0, 0, 0))

        img = self.font_score.render(score, True, (0, 0, 0))
        self.score_s.blit(img, (win_width / 2 - img.get_width() / 2,
                                win_height / 4 - img.get_height() / 2))
        win.blit(self.score_s, (0, 0))


class Ship:
    def __init__(self):
        self.ship_hit_box = pygame.Rect(200, 250, spr_width - 25, spr_height - 35)
        self.y_speed = 0
        self.rotation = 0
        self.score = 0

    def loop(self):
        self.ship_move()
        self.rotation = self.y_speed * 4

    def ship_move(self):
        self.y_speed -= grav
        self.ship_hit_box.y -= self.y_speed

    def draw(self):
        sprite_copy = pygame.transform.rotate(ship_sprite, self.rotation)
        win.blit(sprite_copy, (self.ship_hit_box.x - int((sprite_copy.get_width() / 2) - 40),
                               self.ship_hit_box.y - int((sprite_copy.get_height() / 2) - 10)))


class WallBuild:
    def __init__(self, x):
        self.rocket_allow = False
        self.score = 0
        sp_top = pygame.Rect(900 + x, random.randint(-350, -175), 168, 400)
        sp_bot = pygame.Rect(900 + x, sp_top.y + 750, 168, 400)
        score_hit_box = pygame.Rect(sp_bot.x + 168, sp_bot.y - 200, 1, 250)

        self.sp_top = sp_top
        self.sp_bot = sp_bot
        self.score_hit_box = score_hit_box
        self.score_ind = True

    def loop(self):
        sp_top = self.sp_top
        sp_bot = self.sp_bot
        score_hit_box = self.score_hit_box

        if sp_top.x >= -168:
            sp_top.x -= 5
        elif sp_top.x < -168 and self.score % 5 != 0:
            sp_top.x = 900
            sp_top.y = random.randint(-350, -175)
            self.score_ind = True
        else:
            sp_top.x = -200

        if self.score_ind:
            score_hit_box.x = sp_bot.x
        else:
            score_hit_box.x = -100

        sp_bot.x = sp_top.x
        sp_bot.y = sp_top.y + 625
        score_hit_box.y = sp_bot.y - 200

    def draw(self, sprite_top, sprite_bot):
        sp_top = self.sp_top
        sp_bot = self.sp_bot
        win.blit(sprite_top, (sp_top.x, sp_top.y))
        win.blit(sprite_bot, (sp_bot.x, sp_bot.y))


class EnemyRocket:
    def __init__(self, ship_hit_box):
        self.difference_x = None
        self.difference_y = None
        self.hit_box = pygame.Rect(2000, 250, 20, 20)
        self.total_diff = 0
        self.speed = 0
        self.rotation = 0
        self.ship_hit_box = ship_hit_box

    def loop(self, variable):
        self.difference_x = abs(self.ship_hit_box.x - self.hit_box.x + 50)
        self.difference_y = self.ship_hit_box.y - self.hit_box.y + 37

        hypotenuse = math.sqrt(self.difference_x ** 2 + self.difference_y ** 2)
        sinus = self.difference_y / hypotenuse
        if self.difference_y < 0:
            self.speed = abs(sinus * variable)
        else:
            self.speed = -abs(sinus * variable)

        self.hit_box.y -= self.speed
        self.rotation = -self.speed * 2
        self.hit_box.x -= variable

    def draw(self):
        sprite_copy = pygame.transform.rotate(rocket_sprite, self.rotation)
        win.blit(sprite_copy, (self.hit_box.x - int((sprite_copy.get_width() / 2) - 40),
                               self.hit_box.y - int((sprite_copy.get_height() / 2) - 10)))


class Particles:
    def __init__(self):
        self.particles = []

    def loop(self):
        self.delete()
        if self.particles:
            for particles in self.particles:
                particles[0][0] += particles[1]/2
                particles[1] -= particles[2]
                pygame.draw.circle(win, (150, 150, 150), particles[0], int(particles[1]))

    def add(self, pos):
        particles = [[pos.x + rocket_sprite.get_width() + 5,
                      pos.y + rocket_sprite.get_height()/2], 7, 0.3]
        self.particles.append(particles)

    def delete(self):
        particles_copy = [particles for particles in self.particles if particles[1] > 0.2]
        self.particles = particles_copy


# Main loop
def main():
    par = Particles()
    # Music
    mixer.music.load('Assets/SadSvit.mp3')
    mixer.music.set_volume(0.03)
    mixer.music.play()
    cloak = pygame.time.Clock()
    # Main True and argument of start
    run = True
    # Plane create
    ship = Ship()
    # Wall create
    first_wall = WallBuild(0)
    second_wall = WallBuild(500)
    # Enemy rocket create
    enemy_rocket = EnemyRocket(ship.ship_hit_box)

    technical = Technical()

    while run:
        # FPS limitation
        cloak.tick(fps)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            technical.start_tap = True
        if technical.start_tap and technical.move_stop:
            # Plain main loom
            ship.loop()
            # Wall main loop
            first_wall.loop()
            second_wall.loop()

            # Rocket main loop
            if ship.score % 10 == 0 and first_wall.rocket_allow:
                enemy_rocket.loop(5 + ship.score / 10)
                if enemy_rocket.hit_box.x <= -150:
                    first_wall = WallBuild(0)
                    second_wall = WallBuild(500)

                    enemy_rocket = EnemyRocket(ship.ship_hit_box)

        # Background builds
        if technical.move_stop: technical.back_house_loop()
        walls = {'first': first_wall,
                 'second': second_wall}

        par.add(enemy_rocket.hit_box)
        # Def draw
        draw(ship, walls, enemy_rocket, technical, par)

        # Collision plane with walls
        ship_hit_box = ship.ship_hit_box
        if ship_hit_box.colliderect(first_wall.sp_top) or ship_hit_box.colliderect(first_wall.sp_bot) or \
                ship_hit_box.colliderect(second_wall.sp_top) or ship_hit_box.colliderect(second_wall.sp_bot):
            pygame.event.post(pygame.event.Event(die))
        # Collision plane with top and bot
        if ship_hit_box.y < 0 or ship_hit_box.y > 500:
            pygame.event.post(pygame.event.Event(die))
        # Collision plane with rocket
        if ship_hit_box.colliderect(enemy_rocket.hit_box):
            pygame.event.post(pygame.event.Event(die))
        # Score detection
        if ship_hit_box.colliderect(first_wall.score_hit_box):
            first_wall.score_ind = False
            first_wall.rocket_allow = True
            ship.score += 1
            first_wall.score += 1

        if ship_hit_box.colliderect(second_wall.score_hit_box):
            second_wall.score_ind = False
            ship.score += 1
            second_wall.score += 1

        # Main event check
        for event in pygame.event.get():
            # Quit from game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Die in game
            if event.type == die:
                if technical.move_stop: mixer.Sound('Assets/Explosion.wav').play().set_volume(0.07)
                technical.move_stop = False
                best_score = base64.b64decode(open("Assets/bin", 'r').read()).decode('utf-8')
                best_score = int(best_score[len('Best score:'): best_score.find('end')])
                if ship.score > best_score:
                    open("Assets/bin", 'w').write(
                        (base64.b64encode(('Best score:{}end'.format(ship.score)).encode())).decode('utf-8'))
            # Restart button
            try:
                if event.type == pygame.MOUSEBUTTONDOWN and technical.hit_box.collidepoint(pygame.mouse.get_pos()):
                    run = False
                    main()
            except: pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship.y_speed = 25 * grav
                    if technical.move_stop: mixer.Sound('Assets/Jump.wav').play().set_volume(0.07)


# Draw/display update
def draw(ship, walls, enemy_rocket, technical, par):
    win.fill((255, 255, 255))
    #
    technical.background()
    # Tap to start  bar
    if technical.start_tap is False:
        technical.pre_start_draw()
    elif technical.start_tap is True and technical.alpha != 0:
        technical.on_tap()
    if technical.start_tap:
        text = str(ship.score)
        technical.score_draw(text)

    # Back house render
    technical.back_house_draw()
    # Plane draw
    ship.draw()
    # Walls draw
    first_wall = walls['first']
    second_wall = walls['second']
    first_wall.draw(wall_top_sprite, wall_bot_sprite)
    second_wall.draw(wall_top_sprite, wall_bot_sprite)
    #
    par.loop()
    # Enemy rocket draw
    enemy_rocket.draw()
    # End screen
    if technical.move_stop is False:
        technical.end_screen_draw(ship)
    # Display update
    pygame.display.update()


if __name__ == '__main__':
    try:
        file = open('Assets/bin', 'x')
        file.write((base64.b64encode(b'Best score:0end')).decode('utf-8'))
        file.close()
    except:
        pass
    main()
