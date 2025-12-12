import cv2
import pygame
import random
import sys
import math
import os
import time
from hand_detector import HandDetector
from game_objects import Fruit, Trail, Particle
import config

# Create assets folder if missing (no files required)
if not os.path.isdir(config.ASSETS_DIR):
    os.makedirs(config.ASSETS_DIR, exist_ok=True)

class FruitNinjaGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("AI Fruit Ninja - Upgraded")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.Font(None, 84)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_mono = pygame.font.SysFont("consolas", 22)

        # Game state
        self.score = 0
        self.high_score = 0
        self.lives = config.INITIAL_LIVES
        self.state = "menu"  # menu, playing, paused, game_over
        self.difficulty = "Normal"

        # Objects
        self.fruits = []
        self.trail = Trail()
        self.particles = []
        self.frame_count = 0

        # Hand / camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.detector = HandDetector(max_hands=1, detection_con=0.7, smooth=True)

        self.finger_x = config.SCREEN_WIDTH // 2
        self.finger_y = config.SCREEN_HEIGHT // 2
        self.finger_speed = 0.0

        # combo tracking
        self.last_slice_time = 0
        self.combo_count = 0
        self.combo_message_time = 0

        # sounds (optional)
        self.sounds = {}
        self.load_sounds()

        # background music (optional)
        # pygame.mixer.music.load(os.path.join(config.ASSETS_DIR, config.SOUNDS.get("music")))
        # pygame.mixer.music.play(-1)

    def load_sounds(self):
        # loads if asset present; graceful fallback
        try:
            slice_path = os.path.join(config.ASSETS_DIR, config.SOUNDS.get("slice", ""))
            bomb_path = os.path.join(config.ASSETS_DIR, config.SOUNDS.get("bomb", ""))
            if os.path.isfile(slice_path):
                self.sounds['slice'] = pygame.mixer.Sound(slice_path)
            if os.path.isfile(bomb_path):
                self.sounds['bomb'] = pygame.mixer.Sound(bomb_path)
        except Exception as e:
            print("Sound load error:", e)

    def spawn_fruit(self):
        # difficulty adjustments
        d = config.DIFFICULTY.get(self.difficulty, config.DIFFICULTY["Normal"])
        if random.random() < config.SPECIAL_PROBABILITY:
            # special fruit: golden or freeze
            special = random.choice(['golden', 'freeze'])
            if special == 'golden':
                data = {'name': 'golden', 'color': (255, 200, 50), 'points': 50, 'text': '🌟', 'special': True}
            else:
                data = {'name': 'freeze', 'color': (180, 230, 255), 'points': 5, 'text': '❄️', 'special': True}
        else:
            if random.random() < d['bomb_prob']:
                data = {'name': 'bomb', 'color': (30, 30, 30), 'points': -20, 'text': '💣'}
            else:
                # pick regular fruit and default points
                data = random.choice([
                    {'name': 'apple', 'color': (255, 0, 0), 'points': 10, 'text': '🍎'},
                    {'name': 'orange', 'color': (255, 165, 0), 'points': 10, 'text': '🍊'},
                    {'name': 'watermelon', 'color': (255, 105, 180), 'points': 15, 'text': '🍉'},
                    {'name': 'banana', 'color': (255, 255, 0), 'points': 10, 'text': '🍌'},
                    {'name': 'grapes', 'color': (128, 0, 128), 'points': 15, 'text': '🍇'},
                    {'name': 'strawberry', 'color': (255, 20, 147), 'points': 10, 'text': '🍓'},
                    {'name': 'kiwi', 'color': (50, 205, 50), 'points': 10, 'text': '🥝'},
                ])
        x = random.randint(120, config.SCREEN_WIDTH - 120)
        y = config.SCREEN_HEIGHT + 80
        fruit = Fruit(x, y, data, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, size=config.FRUIT_SIZE)
        self.fruits.append(fruit)

    def handle_camera(self):
        success, img = self.cap.read()
        if not success:
            return

        # Flip and process
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (640, 480))
        img = self.detector.find_hands(img, draw=True)
        self.detector.find_position(img, draw=False)

        sx, sy, spd = self.detector.get_index_finger_position()
        if sx is not None:
            cam_w, cam_h = 640, 480
            self.finger_x = int(sx * config.SCREEN_WIDTH / cam_w)
            self.finger_y = int(sy * config.SCREEN_HEIGHT / cam_h)
            self.finger_speed = spd / 30.0
            self.trail.add_point(self.finger_x, self.finger_y)

        # Convert to pygame surface
        preview_w, preview_h = config.CAM_PREVIEW_SIZE
        x, y = config.CAM_PREVIEW_POS

        cam_small = cv2.resize(img, (preview_w, preview_h))
        cam_small = cv2.cvtColor(cam_small, cv2.COLOR_BGR2RGB)
        cam_small = cam_small.swapaxes(0, 1)

        surf = pygame.surfarray.make_surface(cam_small)

        # Neon frame
        frame_rect = pygame.Rect(x - 4, y - 4, preview_w + 8, preview_h + 8)
        pygame.draw.rect(self.screen, (255, 0, 255), frame_rect, width=3, border_radius=6)

        # Draw camera last
        self.screen.blit(surf, (x, y))

    def spawn_logic(self):
        d = config.DIFFICULTY[self.difficulty]
        if self.frame_count % d['spawn_rate'] == 0:
            self.spawn_fruit()

    def update_game(self):
        self.frame_count += 1
        self.spawn_logic()

        # Update fruits
        for fruit in self.fruits[:]:
            fruit.update()

            # collision detection based on speed threshold and movement
            if not fruit.is_sliced:
                # check movement-based slicing (finger must be moving quickly)
                if self.finger_speed > config.SLICE_SPEED_THRESHOLD:
                    if fruit.check_collision(self.finger_x, self.finger_y):
                        points = fruit.slice()
                        # play slice sound
                        if 'slice' in self.sounds:
                            self.sounds['slice'].play()

                        # particles
                        self.create_particles(fruit.x, fruit.y, fruit.color)

                        # bomb behavior
                        if fruit.is_bomb:
                            # bomb explosion: stronger penalty + sound + flash
                            if 'bomb' in self.sounds:
                                self.sounds['bomb'].play()
                            self.lives -= 1
                            # flash / screen shake simple implementation:
                            self.flash_red()
                            if self.lives <= 0:
                                self.state = "game_over"
                        else:
                            # special fruit handling
                            if fruit.data.get('name') == 'golden':
                                self.score += points
                                self.combo_count = 0  # reset or maybe extra behavior
                                self.combo_message_time = pygame.time.get_ticks()
                            elif fruit.data.get('name') == 'freeze':
                                self.score += points
                                # slow motion effect for a short duration
                                self.slow_motion(180)  # frames
                            else:
                                # normal fruit
                                self.score += points

                            # combo handling
                            now_ms = pygame.time.get_ticks()
                            if now_ms - self.last_slice_time <= config.COMBO_WINDOW_MS:
                                self.combo_count += 1
                                # apply bonus for combos >=2
                                if self.combo_count >= 2:
                                    self.score += config.COMBO_BONUS
                                    self.combo_message_time = now_ms
                            else:
                                self.combo_count = 1
                            self.last_slice_time = now_ms

            # remove off-screen fruits
            if fruit.is_off_screen():
                if not fruit.is_sliced and not fruit.is_bomb:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.state = "game_over"
                try:
                    self.fruits.remove(fruit)
                except ValueError:
                    pass

            # remove sliced fruits after animation
            if fruit.is_sliced and fruit.slice_time > 30:
                try:
                    self.fruits.remove(fruit)
                except ValueError:
                    pass

        # update trail and particles
        self.trail.update()
        for p in self.particles[:]:
            p.update()
            if p.is_dead():
                self.particles.remove(p)

        # high score
        if self.score > self.high_score:
            self.high_score = self.score

    def draw_game(self):
        # --- Draw background FIRST ---
        self.draw_background()

        # --- Trails ---
        self.trail.draw(self.screen)

        # --- Fruits ---
        for fruit in self.fruits:
            fruit.draw(self.screen, self.font_medium)

        # --- Particles ---
        for p in self.particles:
            p.draw(self.screen)

        # --- Finger cursor ---
        pygame.draw.circle(self.screen, config.NEON, (self.finger_x, self.finger_y), 14, 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.finger_x, self.finger_y), 6)

        # --- Score ---
        score_text = self.font_large.render(f"Score: {self.score}", True, config.WHITE)
        self.screen.blit(score_text, (20, 14))

        # --- High Score ---
        high_text = self.font_small.render(f"High: {self.high_score}", True, config.YELLOW)
        self.screen.blit(high_text, (22, 86))

        # --- Lives ---
        for i in range(self.lives):
            heart = self.font_medium.render("❤️", True, config.RED)
            self.screen.blit(heart, (22 + i * 48, 120))

        # --- Combo ---
        if pygame.time.get_ticks() - self.combo_message_time < config.COMBO_TEXT_DURATION_MS:
            combo_txt = self.font_medium.render(f"COMBO x{self.combo_count}!", True, config.YELLOW)
            self.screen.blit(combo_txt, (config.SCREEN_WIDTH // 2 - combo_txt.get_width() // 2, 40))

        # --- CAMERA ALWAYS LAST (IMPORTANT FIX!!) ---
        self.handle_camera()

    def draw_background(self):
        # simple vertical gradient
        top = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        for i in range(config.SCREEN_HEIGHT):
            ratio = i / config.SCREEN_HEIGHT
            r = int(config.BLUE[0] * (1 - ratio) + config.WHITE[0] * ratio)
            g = int(config.BLUE[1] * (1 - ratio) + config.WHITE[1] * ratio)
            b = int(config.BLUE[2] * (1 - ratio) + config.WHITE[2] * ratio)
            pygame.draw.line(top, (r, g, b), (0, i), (config.SCREEN_WIDTH, i))
        self.screen.blit(top, (0, 0))

    def create_particles(self, x, y, color):
        for _ in range(config.PARTICLE_COUNT):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(1, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            p = Particle(x, y, color, vx, vy, config.PARTICLE_LIFETIME)
            self.particles.append(p)

    def flash_red(self):
        # quick red flash overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((255, 10, 10))
        self.screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(80)

    def slow_motion(self, frames=120):
        # simple slow motion effect: reduce spawn rate and gravity temporarily
        prev = config.DIFFICULTY[self.difficulty].copy()
        config.DIFFICULTY[self.difficulty]['spawn_rate'] *= 2
        config.DIFFICULTY[self.difficulty]['gravity'] *= 0.6
        # schedule revert after frames
        revert_frame = self.frame_count + frames

        # We'll store a simple tuple to revert later
        self._slow_motion_revert = (revert_frame, prev)

    def check_slow_motion_revert(self):
        if hasattr(self, "_slow_motion_revert"):
            revert_frame, prev = self._slow_motion_revert
            if self.frame_count >= revert_frame:
                config.DIFFICULTY[self.difficulty] = prev
                delattr = hasattr(self, "_slow_motion_revert")
                if delattr:
                    del self._slow_motion_revert

    def draw_menu(self):
        self.screen.fill((45, 40, 80))
        title = self.font_large.render("AI FRUIT NINJA", True, config.WHITE)
        self.screen.blit(title, (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        subtitle = self.font_medium.render("Hand Gesture Control", True, config.YELLOW)
        self.screen.blit(subtitle, (config.SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 170))

        instr = self.font_small.render("Press SPACE to Start | D to change difficulty | Q to Quit", True, config.WHITE)
        self.screen.blit(instr, (config.SCREEN_WIDTH // 2 - instr.get_width() // 2, 260))

        diff = self.font_medium.render(f"Difficulty: {self.difficulty}", True, config.NEON)
        self.screen.blit(diff, (config.SCREEN_WIDTH // 2 - diff.get_width() // 2, 340))

    def draw_game_over(self):
        self.screen.fill((60, 0, 0))
        g = self.font_large.render("GAME OVER", True, config.WHITE)
        self.screen.blit(g, (config.SCREEN_WIDTH // 2 - g.get_width() // 2, 140))
        s = self.font_medium.render(f"Final Score: {self.score}", True, config.YELLOW)
        self.screen.blit(s, (config.SCREEN_WIDTH // 2 - s.get_width() // 2, 260))
        h = self.font_medium.render(f"High Score: {self.high_score}", True, config.GREEN)
        self.screen.blit(h, (config.SCREEN_WIDTH // 2 - h.get_width() // 2, 330))
        r = self.font_small.render("Press R to Restart or Q to Quit", True, config.WHITE)
        self.screen.blit(r, (config.SCREEN_WIDTH // 2 - r.get_width() // 2, 420))

    def reset_game(self):
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.fruits = []
        self.frame_count = 0
        self.state = "playing"
        self.particles = []
        self.trail = Trail()
        self.last_slice_time = 0
        self.combo_count = 0

    def toggle_difficulty(self):
        keys = list(config.DIFFICULTY.keys())
        idx = keys.index(self.difficulty)
        idx = (idx + 1) % len(keys)
        self.difficulty = keys[idx]

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(config.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "menu":
                        self.reset_game()
                    elif event.key == pygame.K_r and self.state == "game_over":
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_p and self.state == "playing":
                        self.state = "paused"
                    elif event.key == pygame.K_p and self.state == "paused":
                        self.state = "playing"
                    elif event.key == pygame.K_d and self.state == "menu":
                        self.toggle_difficulty()

            # camera & input
            self.handle_camera()

            # game update/draw
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing":
                self.update_game()
                self.check_slow_motion_revert()
                self.draw_game()
            elif self.state == "paused":
                self.draw_game()
                p = self.font_large.render("PAUSED", True, config.YELLOW)
                self.screen.blit(p, (config.SCREEN_WIDTH // 2 - p.get_width() // 2, config.SCREEN_HEIGHT // 2))
            elif self.state == "game_over":
                self.draw_game_over()

            pygame.display.flip()

        # cleanup
        self.cap.release()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = FruitNinjaGame()
    game.run()
