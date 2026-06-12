import pygame
import random
import sys
import math
from collections import deque

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

# Premium Colors
BLACK = (3, 3, 15)
DARK_GREEN = (0, 180, 0)
NEON_GREEN = (0, 255, 150)
GLOW_GREEN = (0, 255, 150, 120)
RED = (255, 80, 80)
NEON_RED = (255, 100, 100)
GLOW_RED = (255, 100, 100, 140)
WHITE = (255, 255, 255)
BLUE = (70, 160, 255)
NEON_BLUE = (100, 200, 255)
GLOW_BLUE = (100, 200, 255, 100)
PURPLE = (180, 100, 255)
GLOW_PURPLE = (180, 120, 255, 80)
YELLOW = (255, 255, 120)
GOLD = (255, 220, 100)
GRID_COLOR = (25, 25, 45)
PANEL_BG = (0, 0, 0, 180)
SHINE = (255, 255, 255, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 PREMIUM STACK SNAKE")
clock = pygame.time.Clock()
font_title = pygame.font.Font(None, 42)
font_main = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 20)
font_tiny = pygame.font.Font(None, 16)

class SnakeGame:
    def __init__(self):
        self.reset()
        self.paused = False
        self.glow_surf = None
        self.create_glow_surface()
    
    def create_glow_surface(self):
        self.glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    def reset(self):
        self.snake = deque([(GRID_W//2, GRID_H//2)])
        self.direction = (0, 0)
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
        self.speed = 4
    
    def new_food(self):
        while True:
            x = random.randint(2, GRID_W-3)
            y = random.randint(2, GRID_H-3)
            if (x, y) not in self.snake:
                return (x, y)
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], 
                   head[1] + self.direction[1])
        
        if (new_head[0] < 1 or new_head[0] > GRID_W-2 or 
            new_head[1] < 1 or new_head[1] > GRID_H-2 or
            new_head in list(self.snake)[1:]):
            self.game_over = True
            return
        
        self.snake.appendleft(new_head)#STACK
        
        if new_head == self.food:
            self.score += 10
            self.food = self.new_food()
            self.speed = min(7, self.speed + 0.05)
        else:
            self.snake.pop() #QUEUE
    
    def set_direction(self, dx, dy):
        self.direction = (dx, dy)
    
    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused
    
    def draw_glow_trail(self):
        self.glow_surf.fill((0, 0, 0, 0))
        
        # Snake glow trail
        for i, (x, y) in enumerate(self.snake):  #TRAVERSING
            if i == 0:
                alpha = 180
            else:
                alpha = max(25, 120 - i * 4)
            
            glow_rect = pygame.Rect(x*CELL_SIZE-1, y*CELL_SIZE-1, CELL_SIZE+2, CELL_SIZE+2)
            glow_color = (*NEON_GREEN[:3], alpha)
            pygame.draw.ellipse(self.glow_surf, glow_color, glow_rect)
        
        # Food glow
        fx, fy = self.food
        food_glow = pygame.Rect(fx*CELL_SIZE-2, fy*CELL_SIZE-2, CELL_SIZE+4, CELL_SIZE+4)
        pygame.draw.ellipse(self.glow_surf, GLOW_RED, food_glow)
        
        screen.blit(self.glow_surf, (0, 0))
    
    def draw_premium_snake(self):
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x*CELL_SIZE+1, y*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2)
            if i == 0:
                # Premium head with eyes
                pygame.draw.ellipse(screen, NEON_GREEN, rect)
                # Eyes
                eye_size = 2
                eye_offset = 3
                left_eye = (x*CELL_SIZE + eye_offset, y*CELL_SIZE + eye_offset)
                right_eye = (x*CELL_SIZE + CELL_SIZE - eye_offset - 1, y*CELL_SIZE + eye_offset)
                pygame.draw.circle(screen, WHITE, left_eye, eye_size)
                pygame.draw.circle(screen, WHITE, right_eye, eye_size)
                pygame.draw.circle(screen, NEON_GREEN, left_eye, 1)
                pygame.draw.circle(screen, NEON_GREEN, right_eye, 1)
            else:
                color_intensity = max(40, 160 - i * 4)
                color = (0, color_intensity, min(80, color_intensity//2))
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, NEON_GREEN, rect, 1)
    
    def draw_premium_food(self, fx, fy):
        # Pulsing premium food
        pulse = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() * 0.02)
        size = int((CELL_SIZE-6) * pulse)
        offset = (CELL_SIZE - size) // 2
        food_rect = pygame.Rect(fx*CELL_SIZE+3+offset, fy*CELL_SIZE+3+offset, size, size)
        
        pygame.draw.ellipse(screen, NEON_RED, food_rect)
        pygame.draw.ellipse(screen, GOLD, food_rect, 1)
        pygame.draw.circle(screen, SHINE, food_rect.center, max(1, size//4))
    
    def draw(self):
        screen.fill(BLACK)
        
        # Animated premium grid
        t = pygame.time.get_ticks() * 0.002
        for x in range(0, WIDTH, CELL_SIZE):
            alpha = 60 + int(30 * math.sin(t + x * 0.02))
            color = (*GRID_COLOR[:3], alpha)
            pygame.draw.line(screen, color, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, CELL_SIZE):
            alpha = 60 + int(30 * math.sin(t + y * 0.02))
            color = (*GRID_COLOR[:3], alpha)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y), 1)
        
        # Glow effects FIRST
        self.draw_glow_trail()
        
        # Premium snake & food
        self.draw_premium_snake()
        self.draw_premium_food(self.food[0], self.food[1])
        
        # ✅ ORIGINAL HUD - ENHANCED
        score_label = font_small.render("Score =", True, WHITE)
        score_value = font_main.render(f"{self.score}", True, NEON_BLUE)
        screen.blit(score_label, (15, 12))
        screen.blit(score_value, (85, 8))
        
        stack_label = font_small.render("Stack =", True, WHITE)
        stack_value = font_main.render(f"{len(self.snake)}", True, NEON_GREEN)
        screen.blit(stack_label, (15, 45))
        screen.blit(stack_value, (95, 42))
        
        speed_label = font_small.render("Speed =", True, WHITE)
        speed_value = font_main.render(f"{self.speed:.1f} fps", True, GOLD)
        screen.blit(speed_label, (15, 78))
        screen.blit(speed_value, (95, 75))
        
        pause_icon = "⏸️" if self.paused else "▶️"
        pause_surf = font_tiny.render(pause_icon, True, YELLOW)
        screen.blit(pause_surf, (220, 82))
        
        # Premium Controls Panel
        panel_w, panel_h = 240, 180
        panel_x, panel_y = WIDTH - panel_w - 20, HEIGHT - panel_h - 20
        
        # Multi-layer glow
        for i in range(2):
            glow_surf = pygame.Surface((panel_w+12-i*4, panel_h+12-i*4), pygame.SRCALPHA)
            glow_alpha = 80 - i*30
            pygame.draw.rect(glow_surf, (*GLOW_BLUE[:3], glow_alpha), 
                           (6-i*2, 6-i*2, panel_w, panel_h))
            screen.blit(glow_surf, (panel_x-6+i*2, panel_y-6+i*2))
        
        # Main panel
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (10, 10, 30, 200), (0, 0, panel_w, panel_h))
        pygame.draw.rect(panel_surf, NEON_BLUE, (0, 0, panel_w, panel_h), 2)
        pygame.draw.rect(panel_surf, GOLD, (0, 0, panel_w, panel_h), 1)
        screen.blit(panel_surf, (panel_x, panel_y))
        
        # Shine gradient
        shine_surf = pygame.Surface((panel_w-12, 24), pygame.SRCALPHA)
        for i in range(24):
            alpha = int(100 * (1 - i/24))
            pygame.draw.line(shine_surf, (*WHITE[:3], alpha), (0, i), (panel_w-12, i))
        screen.blit(shine_surf, (panel_x+6, panel_y+6))
        
        # Original controls content with premium colors
        controls_content = [
            ("🎮 CONTROLS", font_main, GOLD),
            ("", None, None),
            ("Arrows = Move", font_small, WHITE),
            ("P = Pause", font_small, NEON_BLUE),
            ("R = Restart", font_small, YELLOW),
            ("Esc = Quit", font_small, RED),
            ("", None, None),
            ("📚 STACK", font_small, PURPLE),
            (f"Head: {self.snake[0]}", font_tiny, WHITE),
            (f"Size: {len(self.snake)}", font_tiny, NEON_GREEN)
        ]
        
        y_offset = 0
        for text, fnt, color in controls_content:
            if fnt is None:
                y_offset += 6
                continue
            
            txt_surf = fnt.render(text, True, color)
            screen.blit(txt_surf, (panel_x + 15, panel_y + 15 + y_offset))
            y_offset += fnt.get_height() + 3
        
        # Pulsing status indicator
        status_color = NEON_GREEN if not self.game_over and not self.paused else NEON_BLUE if self.paused else NEON_RED
        pulse_size = 4 + int(2 * math.sin(pygame.time.get_ticks() * 0.03))
        pygame.draw.circle(screen, status_color, (panel_x + panel_w - 18, panel_y + 18), pulse_size)
        
        # Pause overlay
        if self.paused:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            pause_text = font_title.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH//2 - 80, HEIGHT//2))
        
        # Game Over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((15, 0, 0))
            screen.blit(overlay, (0, 0))
            
            go_title = font_title.render("GAME OVER", True, NEON_RED)
            final_score = font_main.render(f"Score: {self.score}", True, WHITE)
            restart_msg = font_small.render("Press R to Play Again", True, GOLD)
            
            screen.blit(go_title, (WIDTH//2 - 140, HEIGHT//2 - 60))
            screen.blit(final_score, (WIDTH//2 - 80, HEIGHT//2 - 10))
            screen.blit(restart_msg, (WIDTH//2 - 130, HEIGHT//2 + 30))

def main():
    game = SnakeGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.key == pygame.K_p:
                    game.toggle_pause()
                else:
                    if event.key == pygame.K_UP: game.set_direction(0, -1)
                    elif event.key == pygame.K_DOWN: game.set_direction(0, 1)
                    elif event.key == pygame.K_LEFT: game.set_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT: game.set_direction(1, 0)
                    elif event.key == pygame.K_ESCAPE: running = False
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(game.speed)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
