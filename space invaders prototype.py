import pygame
import sys

pygame.init()

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1280

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# --- SETUP BACKGROUND & IMAGES ---
try:
    bg_image = pygame.image.load("space_bg.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # 1. Load the floor image texture
    floor_img = pygame.image.load("mars_surface.jpg").convert_alpha()
    
    # 2. Scale the floor image to perfectly fit the line area (Width: 1080, Height: 40)
    # The road spans from X=100 to X=1180, which is exactly 1080 pixels wide
    floor_img = pygame.transform.scale(floor_img, (1080, 70))
    
    # --- SETUP PLAYER ---
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img.set_colorkey((255, 255, 255))
    player_img = pygame.transform.scale(player_img, (99, 99))

    test_collider =  pygame.image.load("player.png").convert_alpha()
    
    test_collider.set_colorkey((255,255,255))
    test_collider = pygame.transform.scale(test_collider, (99,99))
    rotate_test_collider = pygame.transform.rotate(test_collider, 180)
    
except pygame.error as e:
    print(f"Asset loading error: {e}. Using placeholders instead.")
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((10, 10, 25))
    player_img = pygame.Surface((91, 91), pygame.SRCALPHA)
    pygame.draw.polygon(player_img, (0, 255, 0), [(45, 0), (0, 91), (91, 91)])
    test_collider = pygame.Surface((99, 99), pygame.SRCALPHA)
    pygame.draw.circle(test_collider, (255, 0, 0), (49, 49), 40)
    rotate_test_collider = test_collider
    
    # Fallback floor if image fails to load
    floor_img = pygame.Surface((1080, 40))
    floor_img.fill((173, 98, 66))

# Setup player positioning variables
collider_x = 640
collider_y = 100

player_x = 640
player_y = 900
player_size_width = 30  
player_speed = 265

cooldown = 850
last_bullet = 0

# --- PROJECTILE CLASS ---
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 600 


    def check_collision(self,other_sprite):
        return self.rect.colliderect(other_sprite.rect)

        
    def update(self, dt):
        self.rect.y -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()
        
            
bullet_group = pygame.sprite.Group()

clock = pygame.time.Clock()
dt = 0 

running = True
while running: 
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                    
    # 1. Handle Key Inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
        player_x += player_speed * dt

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if current_time - last_bullet >= cooldown:
            new_bullet = Bullet(player_x, player_y - 50)
            bullet_group.add(new_bullet)
            last_bullet = current_time

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        if current_time - last_bullet >= cooldown:
            new_bullet = Bullet(player_x, player_y - 50)
            bullet_group.add(new_bullet)
            last_bullet = current_time

    # 2. Enforce Road Boundaries
    if player_x < 100 + player_size_width:
        player_x = 100 + player_size_width

    if player_x > 1180 - player_size_width:
        player_x = 1180 - player_size_width

    # --- UPDATE SPRITES ---
    bullet_group.update(dt)
    for bullet in bullet_group:

        offset = (
            test_collider_rect.left - bullet.rect.left,
            test_collider_rect.top - bullet.rect.top
            )
        
        if bullet.rect.colliderect(test_collider_rect):
            print("Collision")
            bullet.kill()
            

            
    # 3. Drawing Phase
    screen.blit(bg_image, (0,0))
    
    bullet_group.draw(screen)
    
    player_rect = player_img.get_rect()
    player_rect.center = (int(player_x), int(player_y)) 
    screen.blit(player_img, player_rect)

    test_collider_rect = rotate_test_collider.get_rect()
    test_collider_rect.center = (int(collider_x), int(collider_y - 20))
    screen.blit(rotate_test_collider, test_collider_rect)
    
    # --- DRAW BORDERS & FLOORS ---
    # Draw your active Mars Surface Image right where the line used to be!
    # Placed at X=100, Y=930 so it fits nicely inside your layout frame
    

    # Side black borders & road outline
   
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, (SCREEN_HEIGHT)), 0)
    pygame.draw.rect(screen, (0, 0, 0), (1180, 0, 100, (SCREEN_HEIGHT)), 0)
    screen.blit(floor_img, (100, 970))
    #pygame.draw.rect(screen, (0,0,0), (100, 0, (SCREEN_WIDTH - 200), (SCREEN_HEIGHT)), 2)
    #pygame.draw.rect(screen, (0,0,0), (0, 970, (SCREEN_WIDTH), (SCREEN_HEIGHT)), 0)
   
    # Update Display
    pygame.display.flip()

    dt = clock.tick(120) / 1000

pygame.quit()
sys.exit()
