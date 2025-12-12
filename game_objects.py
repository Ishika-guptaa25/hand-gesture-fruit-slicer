import random
import pygame
import config
import os
import math

# Helper to load assets if present
def load_image(name, size):
    path = os.path.join(config.ASSETS_DIR, config.FRUIT_IMAGES.get(name, ""))
    if os.path.isfile(path):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, (size, size))
        return img
    return None


class Particle:
    def __init__(self, x, y, color, vx, vy, life):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = life
        self.age = 0

    def update(self):
        self.age += 1
        self.vy += 0.2  # gravity on particles
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        alpha = max(0, 255 - int((self.age / self.life) * 255))
        surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        surf.fill((*self.color, alpha))
        screen.blit(surf, (int(self.x), int(self.y)))

    def is_dead(self):
        return self.age >= self.life


class Fruit:
    def __init__(self, x, y, fruit_data, screen_width, screen_height, size=config.FRUIT_SIZE):
        self.x = x
        self.y = y
        self.data = fruit_data
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size

        # physics
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-18, -12)
        self.rotation = random.uniform(-8, 8)
        self.angle = 0

        # state
        self.is_sliced = False
        self.slice_time = 0
        self.is_bomb = (fruit_data['name'] == 'bomb')
        self.is_special = fruit_data.get('special', False)

        # visual asset (if provided)
        self.image = load_image(fruit_data['name'], self.size)

        # fallback color and text
        self.color = fruit_data.get('color', (200, 200, 200))
        self.text = fruit_data.get('text', '?')

    def update(self):
        if not self.is_sliced:
            self.vy += config.GRAVITY
            self.x += self.vx
            self.y += self.vy
            self.angle = (self.angle + self.rotation) % 360
        else:
            self.slice_time += 1
            # sliced fruits fall apart
            self.x += self.vx * 0.5
            self.y += self.vy * 0.5
            self.angle += self.rotation * 2

    def draw(self, screen, font):
        if not self.is_sliced:
            if self.image:
                rotated = pygame.transform.rotate(self.image, self.angle)
                rect = rotated.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(rotated, rect)
            else:
                # draw circle and emoji text fallback
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
                txt = font.render(self.text, True, config.WHITE)
                txt_rect = txt.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(txt, txt_rect)
        else:
            # show two halves (fallback)
            if self.image:
                # draw smaller rotated halves (simple effect)
                left = pygame.transform.rotate(self.image, self.angle + 20)
                right = pygame.transform.rotate(self.image, self.angle - 20)
                screen.blit(left, (int(self.x - 20), int(self.y)))
                screen.blit(right, (int(self.x + 20), int(self.y)))
            else:
                txt_l = font.render(self.text, True, config.WHITE)
                txt_r = font.render(self.text, True, config.WHITE)
                screen.blit(txt_l, (int(self.x - 20), int(self.y)))
                screen.blit(txt_r, (int(self.x + 20), int(self.y)))

    def is_off_screen(self):
        return self.y > self.screen_height + 120 or self.x < -200 or self.x > self.screen_width + 200

    def check_collision(self, finger_x, finger_y, threshold=55):
        if self.is_sliced:
            return False
        distance = ((self.x - finger_x) ** 2 + (self.y - finger_y) ** 2) ** 0.5
        return distance < threshold

    def slice(self):
        self.is_sliced = True
        return self.data.get('points', 0)


class Trail:
    def __init__(self, max_points=25):
        self.points = []  # [x,y,alpha]
        self.max_points = max_points

    def add_point(self, x, y):
        self.points.append([x, y, 255])
        if len(self.points) > self.max_points:
            self.points.pop(0)

    def update(self):
        for p in self.points:
            p[2] -= 12
        self.points = [p for p in self.points if p[2] > 0]

    def draw(self, screen):
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                a = self.points[i][2]
                width = int(12 * (i / len(self.points))) + 2
                s = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(s, (255, 0, 200, a), (self.points[i][0], self.points[i][1]),
                                 (self.points[i + 1][0], self.points[i + 1][1]), width)
                screen.blit(s, (0, 0))
