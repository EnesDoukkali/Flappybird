import pygame
import random
import math
import numpy as np
from pygame import gfxdraw

# Initialisierung
pygame.init()
pygame.mixer.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Farben
BLUE = (135, 206, 235)  # Himmelsfarbe
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_GRAY = (220, 220, 220)

# Generiere Bilder
def create_bird_images():
    images = []
    for i in range(3):
        surf = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, YELLOW, (0, 0, 40, 30))
        pygame.draw.circle(surf, BLACK, (30, 10 + i * 2), 5)
        pygame.draw.polygon(surf, ORANGE, [(40, 15), (50, 15 + i), (40, 20)])
        images.append(surf)
    return images

def create_pipe_image():
    surf = pygame.Surface((70, height), pygame.SRCALPHA)
    pygame.draw.rect(surf, GREEN, (0, 0, 70, height))
    pygame.draw.rect(surf, (0, 100, 0), (0, 0, 5, height))
    pygame.draw.rect(surf, (0, 200, 0), (65, 0, 5, height))
    return surf

def create_background():
    surf = pygame.Surface((width, height))
    surf.fill(BLUE)
    return surf

def create_ground():
    surf = pygame.Surface((width, 100))
    surf.fill((100, 80, 0))
    for i in range(100):
        grass_height = random.randint(1, 5)
        pygame.draw.line(surf, GREEN, (i * 8, 0), (i * 8, grass_height))
    return surf

# Wolkenklasse für schöne Wolken
class Cloud:
    def __init__(self):
        self.x = random.randint(width, width + 500)
        self.y = random.randint(50, height // 2)
        self.speed = random.uniform(0.3, 0.8)
        self.image = self.generate_cloud_image()

    def generate_cloud_image(self):
        base_width = random.randint(120, 250)
        base_height = int(base_width * 0.6)
        cloud_surface = pygame.Surface((base_width, base_height), pygame.SRCALPHA)

        cloud_color = (255, 255, 255, 220)
        highlight_color = (255, 255, 255, 255)
        shadow_color = (200, 200, 200, 180)

        # Hauptform der Wolke
        ellipse_rect = pygame.Rect(0, base_height // 3, base_width, base_height // 2)
        pygame.draw.ellipse(cloud_surface, cloud_color, ellipse_rect)

        # Zusätzliche Wölbungen für mehr Struktur
        num_bumps = random.randint(3, 6)
        for _ in range(num_bumps):
            bump_width = random.randint(base_width // 4, base_width // 2)
            bump_height = random.randint(base_height // 3, base_height // 2)
            bump_x = random.randint(0, base_width - bump_width)
            bump_y = random.randint(0, base_height - bump_height)
            gfxdraw.filled_ellipse(cloud_surface, bump_x + bump_width // 2, bump_y + bump_height // 2,
                                   bump_width // 2, bump_height // 2, cloud_color)

        # Highlights hinzufügen
        for _ in range(num_bumps // 2):
            highlight_radius = random.randint(10, 30)
            highlight_x = random.randint(highlight_radius, base_width - highlight_radius)
            highlight_y = random.randint(highlight_radius, base_height - highlight_radius)
            gfxdraw.filled_circle(cloud_surface, highlight_x, highlight_y, highlight_radius, highlight_color)

        # Schatten hinzufügen
        shadow_ellipse_rect = pygame.Rect(base_width // 8, base_height * 2 // 3, 
                                          base_width * 3 // 4, base_height // 4)
        pygame.draw.ellipse(cloud_surface, shadow_color, shadow_ellipse_rect)

        return cloud_surface

    def update(self):
        self.x -= self.speed
        if self.x < -self.image.get_width():
            self.x = random.randint(width, width + 500)
            self.y = random.randint(50, height // 2)
            self.speed = random.uniform(0.3, 0.8)
            self.image = self.generate_cloud_image()

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

# Generiere Sounds
def create_sound(frequency, duration):
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate))
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_sample = 2**(16 - 1) - 1
    for s in range(n_samples):
        t = float(s) / sample_rate
        buf[s][0] = int(round(max_sample * math.sin(2 * math.pi * frequency * t)))
        buf[s][1] = buf[s][0]  # Left and right channel have same value
    return pygame.sndarray.make_sound(buf)

# Lade Bilder und Sounds
bird_images = create_bird_images()
pipe_image = create_pipe_image()
background_image = create_background()
ground_image = create_ground()

flap_sound = create_sound(400, 0.1)
score_sound = create_sound(600, 0.1)
hit_sound = create_sound(200, 0.2)

# Kamera
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scroll = 0

    def update(self, target):
        self.scroll = target.x - self.width // 4

# Vogel
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.velocity_x = 3
        self.gravity = 0.5
        self.lift = -9
        self.rotation = 0
        self.flap_cooldown = 0
        self.air_resistance = 0.99
        self.animation_index = 0
        self.animation_speed = 0.1
        self.rect = pygame.Rect(x, y, 34, 24)

    def apply_lift(self):
        if self.flap_cooldown == 0:
            self.velocity_y = self.lift
            self.flap_cooldown = 10
            flap_sound.play()

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.x += self.velocity_x
        self.velocity_y *= self.air_resistance
        self.rotation = -math.atan2(self.velocity_y, 3) * 180 / math.pi
        if self.flap_cooldown > 0:
            self.flap_cooldown -= 1
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen, camera):
        self.animation_index = (self.animation_index + self.animation_speed) % len(bird_images)
        bird_surf = bird_images[int(self.animation_index)]
        rotated_bird = pygame.transform.rotate(bird_surf, self.rotation)
        screen.blit(rotated_bird, (self.x - camera.scroll - rotated_bird.get_width() // 2, 
                                   self.y - rotated_bird.get_height() // 2))

    def check_collision(self, pipe):
        top_pipe_rect = pygame.Rect(pipe.x, 0, pipe.width, pipe.top)
        bottom_pipe_rect = pygame.Rect(pipe.x, pipe.top + pipe.gap, pipe.width, height - pipe.top - pipe.gap)
        return self.rect.colliderect(top_pipe_rect) or self.rect.colliderect(bottom_pipe_rect)

# Röhren
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top = random.randint(50, height - 200)
        self.gap = 180
        self.width = 70
        self.passed = False

    def draw(self, screen, camera):
        screen.blit(pipe_image, (self.x - camera.scroll, self.top - height))
        screen.blit(pipe_image, (self.x - camera.scroll, self.top + self.gap))

# Spiel-Variablen
bird = Bird(50, height // 2)
camera = Camera(width, height)
pipes = [Pipe(width + i * 300) for i in range(3)]
clouds = [Cloud() for _ in range(6)]  # Erstelle 6 Wolken am Anfang
score = 0
high_score = 0
game_state = "start"
difficulty = 1

# Hintergrund
def draw_background(screen, camera):
    rel_scroll = camera.scroll % width
    screen.blit(background_image, (-rel_scroll, 0))
    screen.blit(background_image, (-rel_scroll + width, 0))
    rel_ground_scroll = camera.scroll % width
    screen.blit(ground_image, (-rel_ground_scroll, height - ground_image.get_height()))
    screen.blit(ground_image, (-rel_ground_scroll + width, height - ground_image.get_height()))

# Text anzeigen
def show_text(text, size, x, y, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Spielschleife
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start":
                    game_state = "play"
                    bird = Bird(50, height // 2)
                    pipes = [Pipe(width + i * 300) for i in range(3)]
                    clouds = [Cloud() for _ in range(6)]  # Neue Wolken generieren
                    score = 0
                    difficulty = 1
                elif game_state == "play":
                    bird.apply_lift()
                elif game_state == "game_over":
                    game_state = "start"

    if game_state == "play":
        # Update
        bird.update()
        camera.update(bird)

        # Wolken aktualisieren
        for cloud in clouds:
            cloud.update()

        # Generate new pipes
        if pipes[-1].x - camera.scroll < width:
            pipes.append(Pipe(pipes[-1].x + 300 - difficulty * 10))

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x - camera.scroll > -pipe.width]

        # Check collision and scoring
        for pipe in pipes:
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
                score_sound.play()
                difficulty = min(difficulty + 0.1, 3)
            if bird.check_collision(pipe):
                hit_sound.play()
                game_state = "game_over"
                high_score = max(high_score, score)

        if bird.y > height - ground_image.get_height() or bird.y < 0:
            hit_sound.play()
            game_state = "game_over"
            high_score = max(high_score, score)

        # Draw
        draw_background(screen, camera)
        
        for cloud in clouds:  # Wolken zeichnen
            cloud.draw(screen)

        for pipe in pipes:
            pipe.draw(screen, camera)
        bird.draw(screen, camera)
        show_text(f"Score: {score}", 36, width // 2, 30, WHITE)

    elif game_state == "start" or game_state == "game_over":
        draw_background(screen, camera)
        if game_state == "start":
            show_text("Flappy Bird", 50, width // 2, height // 3, ORANGE)
            show_text("Press SPACE to Start", 30, width // 2, height * 2 // 3)
        else:
            show_text("Game Over", 50, width // 2, height // 3, ORANGE)
            show_text(f"Score: {score}", 40, width // 2, height // 2)
            show_text(f"High Score: {high_score}", 30, width // 2, height * 2 // 3)
            show_text("Press SPACE to Restart", 25, width // 2, height * 4 // 5)

    pygame.display.flip()
    clock.tick(60)
