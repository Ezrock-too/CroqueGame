import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Croque Hunter")

# Load the background image
background_img = pygame.image.load("images/background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
player_img = pygame.image.load("images/player.png")
enemy_img = pygame.image.load("images/enemy.png")
bullet_img = pygame.image.load("images/bullet.png")
powerup_img = pygame.image.load("images/powerup.png")

# Scale images
player_img = pygame.transform.scale(player_img, (100, 150))
enemy_img = pygame.transform.scale(enemy_img, (100, 100))
bullet_img = pygame.transform.scale(bullet_img, (30, 50))
powerup_img = pygame.transform.scale(powerup_img, (100, 100))

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5
bullet_speed = 10
enemy_speed = 3
enemy_spawn_delay = 80
powerup_spawn_delay = 120
score = 0
speed_boost_duration = 100  # Duration of the speed boost in frames (60 frames per second)
game_over = False  # Variable to track whether the game is over
message_end_time = pygame.time.get_ticks() + 3000
current_time = pygame.time.get_ticks()

# Create sprite groups
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(player_x, player_y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += player_speed
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        self.rect.y += enemy_speed
        if self.rect.y > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = powerup_img
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def update(self):
        self.rect.y += enemy_speed
        if self.rect.y > HEIGHT:
            self.kill()

# Create player object
player = Player()
speed_boost_timer = 0  # Timer for tracking the duration of the speed boost

# Game loop
clock = pygame.time.Clock()
while True:
    screen.blit(background_img, (0, 0))  # Blit the background image
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Spawn enemies
    if random.randint(0, enemy_spawn_delay) == 0:
        enemy = Enemy()
        enemies.add(enemy)

    # Spawn power-up
    if random.randint(0, powerup_spawn_delay) == 0:
        powerup = Powerup()
        powerups.add(powerup)

    # Update sprites
    if not game_over:
        player.update()
        bullets.update()
        enemies.update()
        powerups.update()

    # Check for collisions
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for enemy in collisions.keys():
        score += 1

    collisions = pygame.sprite.groupcollide(powerups, bullets, True, True)
    for enemy in collisions.keys():
        score -= 1

    # Check for player-enemy collisions
    if not game_over and pygame.sprite.spritecollide(player, enemies, True):
        game_over = True  # Game over if player is hit by an enemy

    # Check for power-up collisions
    powerup_collisions = pygame.sprite.spritecollide(player, powerups, True)
    if powerup_collisions:
        score += 2
        player_speed += 2  # Increase player speed
        speed_boost_timer = speed_boost_duration  # Set the speed boost timer

    # Decrement speed boost timer
    if speed_boost_timer > 0:
        speed_boost_timer -= 1
        if speed_boost_timer == 0:
            player_speed -= 2  # Restore player speed after the boost ends

    # Draw sprites
    bullets.draw(screen)
    enemies.draw(screen)
    powerups.draw(screen)
    screen.blit(player.image, player.rect)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        # Display game over text and final score
        game_over_text = font.render("Game Over! Final Score: " + str(score), True, RED)
        screen.fill(0)
        if current_time < message_end_time:
            screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))

    pygame.display.flip()
    clock.tick(60)
