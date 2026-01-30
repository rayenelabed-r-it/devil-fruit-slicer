import pygame
import random
import math
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
ORANGE = (243, 156, 18)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)

# Get the directory where images are stored
IMAGES_DIR = "/mnt/user-data/uploads"

# Fruit definitions with image paths
FRUITS = [
    {'name': 'Purple Devil Fruit', 'image': '596e67f8f559d2865824bb7554d0ea3b.jpg', 'color': (147, 112, 219), 'key': pygame.K_p, 'letter': 'P'},
    {'name': 'Fire Devil Fruit', 'image': '858dacd62efdb4774784e9dbebe174f3.jpg', 'color': (255, 140, 0), 'key': pygame.K_f, 'letter': 'F'},
    {'name': 'Heart Devil Fruit', 'image': '1113a891663c7a600ac4536c94554a1d.jpg', 'color': (255, 71, 87), 'key': pygame.K_h, 'letter': 'H'},
    {'name': 'Blue Devil Fruit', 'image': 'téléchargement.png', 'color': (100, 149, 237), 'key': pygame.K_b, 'letter': 'B'},
]

SPECIAL_ITEMS = [
    {'name': 'Ice Cube', 'image': '9f542496ae8dbf45ed1983b2e0aa2ab1.jpg', 'color': (135, 206, 235), 'key': pygame.K_i, 'letter': 'I', 'type': 'ice'},
    {'name': 'Bomb', 'image': 'e9a1f569a0005ff14f58fdfbdf5ede68.jpg', 'color': (44, 62, 80), 'key': pygame.K_x, 'letter': 'X', 'type': 'bomb'},
]


class ImageCache:
    """Cache for loading and storing fruit images"""
    def __init__(self):
        self.images = {}
        self.load_images()
    
    def load_images(self):
        """Load all fruit images"""
        all_items = FRUITS + SPECIAL_ITEMS
        
        for item in all_items:
            if 'image' in item:
                try:
                    image_path = os.path.join(IMAGES_DIR, item['image'])
                    original_image = pygame.image.load(image_path)
                    # Scale to reasonable size
                    scaled_image = pygame.transform.smoothscale(original_image, (80, 80))
                    self.images[item['name']] = scaled_image
                    print(f"✓ Loaded: {item['name']}")
                except Exception as e:
                    print(f"✗ Error loading {item['name']}: {e}")
                    # Create fallback colored circle
                    surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                    pygame.draw.circle(surf, item['color'], (40, 40), 35)
                    self.images[item['name']] = surf
    
    def get_image(self, name):
        """Get cached image"""
        return self.images.get(name)


class Fruit:
    def __init__(self, fruit_data, x, y, image_cache):
        self.data = fruit_data
        self.start_x = x
        self.x = x
        self.y = y
        
        # Physics for parabolic arc (like real fruit ninja!)
        self.velocity_y = random.uniform(-12, -18)  # Initial upward velocity (negative = up)
        self.velocity_x = random.uniform(-4, 4)  # Horizontal velocity
        self.gravity = 0.5  # Gravity pulls down
        
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-8, 8)
        self.size = 80
        self.sliced = False
        self.slice_time = 0
        self.image_cache = image_cache
        
        # Get the base image
        self.base_image = image_cache.get_image(fruit_data['name'])
        
    def update(self, frozen=False):
        if not frozen and not self.sliced:
            # Apply gravity to create parabolic arc
            self.velocity_y += self.gravity  # Gravity accelerates downward
            self.y += self.velocity_y  # Update vertical position
            self.x += self.velocity_x  # Update horizontal position
            self.rotation += self.rotation_speed  # Rotate fruit
            
    def draw(self, screen, font):
        if self.sliced:
            # Slice animation
            elapsed = pygame.time.get_ticks() - self.slice_time
            alpha = max(0, 255 - (elapsed * 255 // 500))
            scale = 1 + (elapsed / 500)
            
            if alpha > 0 and self.base_image:
                # Scale and rotate
                size = int(self.size * scale)
                rotated = pygame.transform.rotate(self.base_image, self.rotation)
                scaled = pygame.transform.smoothscale(rotated, (size, size))
                
                # Apply alpha
                scaled.set_alpha(alpha)
                
                # Draw glow effect
                for i in range(3):
                    glow_size = size + (3 - i) * 15
                    glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                    glow_alpha = alpha // (i + 2)
                    color_with_alpha = (*self.data['color'], glow_alpha)
                    pygame.draw.circle(glow_surf, color_with_alpha, (glow_size // 2, glow_size // 2), glow_size // 2)
                    screen.blit(glow_surf, (self.x - glow_size // 2, self.y - glow_size // 2))
                
                # Draw sliced fruit
                rect = scaled.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(scaled, rect)
            
            return elapsed < 500
        else:
            # Draw rotating fruit
            if self.base_image:
                # Outer glow
                glow_surf = pygame.Surface((self.size + 30, self.size + 30), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*self.data['color'], 80), (self.size // 2 + 15, self.size // 2 + 15), self.size // 2 + 15)
                screen.blit(glow_surf, (self.x - self.size // 2 - 15, self.y - self.size // 2 - 15))
                
                # Rotate image
                rotated_image = pygame.transform.rotate(self.base_image, self.rotation)
                rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(rotated_image, rect)
                
                # Letter label below fruit
                letter_surface = font.render(self.data['letter'], True, WHITE)
                letter_rect = letter_surface.get_rect(center=(int(self.x), int(self.y) + 50))
                
                # Letter background with special styling for bomb/ice
                bg_size = 35
                bg_rect = pygame.Rect(0, 0, bg_size, bg_size)
                bg_rect.center = letter_rect.center
                
                if self.data.get('type') == 'bomb':
                    # Red warning for bomb
                    pygame.draw.rect(screen, RED, bg_rect, border_radius=8)
                    pygame.draw.rect(screen, (150, 0, 0), bg_rect, 3, border_radius=8)
                elif self.data.get('type') == 'ice':
                    # Blue glow for ice
                    pygame.draw.rect(screen, (173, 216, 230), bg_rect, border_radius=8)
                    pygame.draw.rect(screen, self.data['color'], bg_rect, 3, border_radius=8)
                else:
                    # Normal fruit
                    pygame.draw.rect(screen, BLACK, bg_rect, border_radius=8)
                    pygame.draw.rect(screen, self.data['color'], bg_rect, 3, border_radius=8)
                
                screen.blit(letter_surface, letter_rect)
            
            return True
    
    def is_missed(self):
        # Fruit is missed if it falls below screen
        return self.y > SCREEN_HEIGHT + self.size and not self.sliced


class ParticleEffect:
    def __init__(self, x, y, color):
        self.particles = []
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 255,
                'color': color,
                'size': random.randint(3, 7)
            })
    
    def update(self):
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.3  # Gravity
            p['life'] -= 5
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def draw(self, screen):
        for p in self.particles:
            alpha = max(0, p['life'])
            color = (*p['color'], alpha)
            surf = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (p['size'], p['size']), p['size'])
            screen.blit(surf, (int(p['x']), int(p['y'])))
    
    def is_finished(self):
        return len(self.particles) == 0


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Devil Fruit Slicer")
        self.clock = pygame.time.Clock()
        
        # Load images
        print("Loading Devil Fruit images...")
        self.image_cache = ImageCache()
        print("All images loaded!\n")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 90)
        self.large_font = pygame.font.Font(None, 56)
        self.medium_font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 28)
        self.letter_font = pygame.font.Font(None, 32)
        
        # Game state
        self.state = 'menu'  # menu, playing, gameover
        self.score = 0
        self.strikes = 0
        self.combo = 0
        self.combo_display_time = 0
        self.frozen_time = 0
        
        self.fruits = []
        self.particles = []
        self.spawn_timer = 0
        self.spawn_interval = 1200  # milliseconds
        
        # Animation variables
        self.menu_pulse = 0
        self.strike_shake = [0, 0, 0]
        
    def reset_game(self):
        self.score = 0
        self.strikes = 0
        self.combo = 0
        self.combo_display_time = 0
        self.frozen_time = 0
        self.fruits = []
        self.particles = []
        self.spawn_timer = pygame.time.get_ticks()
        
    def spawn_fruit(self):
        # 20% chance for special item
        if random.random() < 0.2:
            fruit_data = random.choice(SPECIAL_ITEMS)
        else:
            fruit_data = random.choice(FRUITS)
        
        # Spawn from bottom at random horizontal position
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = SCREEN_HEIGHT + 50
        
        self.fruits.append(Fruit(fruit_data, x, y, self.image_cache))
    
    def slice_fruits(self, key):
        sliced_count = 0
        sliced_fruits = []
        
        for fruit in self.fruits:
            if fruit.data['key'] == key and not fruit.sliced:
                fruit.sliced = True
                fruit.slice_time = pygame.time.get_ticks()
                sliced_fruits.append(fruit)
                sliced_count += 1
                
                # Create particle effect
                self.particles.append(ParticleEffect(fruit.x, fruit.y, fruit.data['color']))
        
        if sliced_count > 0:
            # Check for bombs
            bombs = [f for f in sliced_fruits if f.data.get('type') == 'bomb']
            if bombs:
                self.state = 'gameover'
                # Big explosion effect
                for bomb in bombs:
                    for _ in range(3):
                        self.particles.append(ParticleEffect(bomb.x, bomb.y, RED))
                return
            
            # Check for ice
            ice = [f for f in sliced_fruits if f.data.get('type') == 'ice']
            if ice:
                self.frozen_time = pygame.time.get_ticks() + 4000  # 4 seconds freeze
            
            # Count regular fruits
            regular_fruits = [f for f in sliced_fruits if 'type' not in f.data]
            
            if regular_fruits:
                if sliced_count == 1:
                    self.score += 1
                else:
                    self.score += sliced_count
                    self.combo = sliced_count
                    self.combo_display_time = pygame.time.get_ticks()
    
    def draw_cloud(self, screen, x, y, width, height):
        # Draw a simple cloud
        pygame.draw.ellipse(screen, WHITE, (x, y + height // 3, width // 3, height // 2))
        pygame.draw.ellipse(screen, WHITE, (x + width // 3, y, width // 2, height))
        pygame.draw.ellipse(screen, WHITE, (x + width // 2, y + height // 3, width // 2, height // 2))
    
    def draw_menu(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw clouds
        for i in range(5):
            cloud_x = (i * 250 + (pygame.time.get_ticks() // 50) % 250) % SCREEN_WIDTH
            self.draw_cloud(self.screen, cloud_x, 100 + i * 80, 120, 60)
        
        # Title
        title_text = "DEVIL FRUIT"
        subtitle_text = "SLICER"
        
        # Animated glow
        glow_intensity = abs(math.sin(pygame.time.get_ticks() / 500)) * 20
        
        # Draw title with outline and glow
        title_surf = self.title_font.render(title_text, True, ORANGE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 120))
        
        # Glow effect
        for offset in range(10, 0, -2):
            glow_color = (255, int(165 + glow_intensity), 0)
            glow_surf = self.title_font.render(title_text, True, glow_color)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 3, 120 + 3))
            self.screen.blit(glow_surf, glow_rect)
        
        # Outline
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3)]:
            outline_surf = self.title_font.render(title_text, True, (211, 84, 0))
            outline_rect = outline_surf.get_rect(center=(SCREEN_WIDTH // 2 + dx, 120 + dy))
            self.screen.blit(outline_surf, outline_rect)
        
        self.screen.blit(title_surf, title_rect)
        
        # Subtitle
        subtitle_surf = self.title_font.render(subtitle_text, True, ORANGE)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3)]:
            outline_surf = self.title_font.render(subtitle_text, True, (211, 84, 0))
            outline_rect = outline_surf.get_rect(center=(SCREEN_WIDTH // 2 + dx, 200 + dy))
            self.screen.blit(outline_surf, outline_rect)
        
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        # Instructions
        instructions = [
            "Tapez la lettre sur chaque Devil Fruit!",
            "",
            "P, F, H, B = Devil Fruits (+1 point)",
            "Tranchez plusieurs en même temps = Combo!",
            "X = Bombe (Game Over instantané!)",
            "I = Glaçon (Gel du temps 4 secondes)",
            "Ratez 3 fruits = Game Over",
            "",
        ]
        
        y = 280
        for line in instructions:
            if line:
                text_surf = self.small_font.render(line, True, BLACK)
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text_surf, text_rect)
            y += 32
        
        # Pulsing "Press SPACE"
        pulse = abs(math.sin(pygame.time.get_ticks() / 300))
        start_text = self.large_font.render("Appuyez sur ESPACE", True, (255, int(pulse * 255), 0))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(start_text, start_rect)
    
    def draw_playing(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw clouds
        for i in range(5):
            cloud_x = (i * 250 + (pygame.time.get_ticks() // 50) % 250) % SCREEN_WIDTH
            self.draw_cloud(self.screen, cloud_x, 50 + i * 80, 120, 60)
        
        # Draw score
        score_bg = pygame.Rect(20, 20, 200, 100)
        pygame.draw.rect(self.screen, ORANGE, score_bg, border_radius=15)
        pygame.draw.rect(self.screen, (211, 84, 0), score_bg, 4, border_radius=15)
        
        score_label = self.small_font.render("SCORE", True, WHITE)
        score_value = self.large_font.render(f"{self.score:04d}", True, WHITE)
        self.screen.blit(score_label, (score_bg.centerx - score_label.get_width() // 2, score_bg.y + 15))
        self.screen.blit(score_value, (score_bg.centerx - score_value.get_width() // 2, score_bg.y + 45))
        
        # Draw strikes
        strike_x = SCREEN_WIDTH - 220
        strike_y = 20
        
        for i in range(3):
            x_offset = self.strike_shake[i]
            strike_rect = pygame.Rect(strike_x + i * 60 + x_offset, strike_y, 50, 50)
            
            if i < self.strikes:
                pygame.draw.rect(self.screen, RED, strike_rect, border_radius=10)
                # Draw X
                pygame.draw.line(self.screen, WHITE, 
                               (strike_rect.left + 10, strike_rect.top + 10),
                               (strike_rect.right - 10, strike_rect.bottom - 10), 5)
                pygame.draw.line(self.screen, WHITE,
                               (strike_rect.right - 10, strike_rect.top + 10),
                               (strike_rect.left + 10, strike_rect.bottom - 10), 5)
            else:
                pygame.draw.rect(self.screen, WHITE, strike_rect, 3, border_radius=10)
        
        # Frozen time indicator
        if self.frozen_time > pygame.time.get_ticks():
            frozen_bg = pygame.Rect(SCREEN_WIDTH // 2 - 120, 20, 240, 60)
            pygame.draw.rect(self.screen, (173, 216, 230), frozen_bg, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, frozen_bg, 3, border_radius=10)
            
            frozen_text = self.medium_font.render("❄️ TEMPS GELÉ ❄️", True, (0, 0, 139))
            self.screen.blit(frozen_text, (frozen_bg.centerx - frozen_text.get_width() // 2, frozen_bg.y + 15))
        
        # Draw combo
        if self.combo > 1 and pygame.time.get_ticks() - self.combo_display_time < 1500:
            combo_scale = 1 + 0.3 * math.sin((pygame.time.get_ticks() - self.combo_display_time) / 100)
            combo_text = self.large_font.render(f"COMBO x{self.combo}!", True, YELLOW)
            combo_size = (int(combo_text.get_width() * combo_scale), int(combo_text.get_height() * combo_scale))
            combo_scaled = pygame.transform.scale(combo_text, combo_size)
            combo_rect = combo_scaled.get_rect(center=(SCREEN_WIDTH // 2, 150))
            
            # Draw outline
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                outline_text = self.large_font.render(f"COMBO x{self.combo}!", True, ORANGE)
                outline_scaled = pygame.transform.scale(outline_text, combo_size)
                outline_rect = outline_scaled.get_rect(center=(SCREEN_WIDTH // 2 + dx, 150 + dy))
                self.screen.blit(outline_scaled, outline_rect)
            
            self.screen.blit(combo_scaled, combo_rect)
        
        # Draw fruits
        frozen = self.frozen_time > pygame.time.get_ticks()
        self.fruits = [f for f in self.fruits if f.draw(self.screen, self.letter_font)]
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
    def draw_gameover(self):
        self.screen.fill(SKY_BLUE)
        
        # Draw clouds
        for i in range(5):
            cloud_x = (i * 250 + (pygame.time.get_ticks() // 50) % 250) % SCREEN_WIDTH
            self.draw_cloud(self.screen, cloud_x, 50 + i * 80, 120, 60)
        
        # Game Over text
        gameover_text = self.title_font.render("GAME OVER", True, RED)
        gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        
        # Outline
        for dx, dy in [(-4, -4), (-4, 4), (4, -4), (4, 4)]:
            outline_surf = self.title_font.render("GAME OVER", True, (150, 0, 0))
            outline_rect = outline_surf.get_rect(center=(SCREEN_WIDTH // 2 + dx, 180 + dy))
            self.screen.blit(outline_surf, outline_rect)
        
        self.screen.blit(gameover_text, gameover_rect)
        
        # Final score
        score_text = self.large_font.render(f"Score Final: {self.score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # Restart prompt
        pulse = abs(math.sin(pygame.time.get_ticks() / 300))
        restart_text = self.medium_font.render("ESPACE pour rejouer", True, (0, int(pulse * 200), 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(restart_text, restart_rect)
        
        # Press ESC to quit
        quit_text = self.small_font.render("ESC pour quitter", True, BLACK)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 460))
        self.screen.blit(quit_text, quit_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.state == 'menu':
                    if event.key == pygame.K_SPACE:
                        self.state = 'playing'
                        self.reset_game()
                
                elif self.state == 'playing':
                    # Try to slice fruits
                    self.slice_fruits(event.key)
                
                elif self.state == 'gameover':
                    if event.key == pygame.K_SPACE:
                        self.state = 'menu'
        
        return True
    
    def update(self):
        if self.state == 'playing':
            # Spawn fruits
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_timer > self.spawn_interval:
                if not (self.frozen_time > current_time):
                    self.spawn_fruit()
                    self.spawn_timer = current_time
            
            # Update fruits
            frozen = self.frozen_time > current_time
            for fruit in self.fruits:
                fruit.update(frozen)
            
            # Check for missed fruits (fruits that fell below screen)
            missed = [f for f in self.fruits if f.is_missed() and 'type' not in f.data]
            if missed:
                self.strikes += len(missed)
                # Shake effect for strikes
                for i in range(min(len(missed), 3)):
                    if self.strikes - len(missed) + i < 3:
                        self.strike_shake[self.strikes - len(missed) + i] = 5
                
                if self.strikes >= 3:
                    self.state = 'gameover'
            
            # Remove missed fruits
            self.fruits = [f for f in self.fruits if not f.is_missed()]
            
            # Update particles
            for particle in self.particles:
                particle.update()
            self.particles = [p for p in self.particles if not p.is_finished()]
            
            # Update strike shake
            for i in range(3):
                if self.strike_shake[i] > 0:
                    self.strike_shake[i] -= 1
    
    def draw(self):
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'playing':
            self.draw_playing()
        elif self.state == 'gameover':
            self.draw_gameover()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
