import pygame
import os

# === PIECE CLASS ===
class Piece:
    def __init__(self, name, color, BASE_DIR, SQ_SIZE, screen, hp=1):
        self.name = name  # 'p', 'r', 'n', etc.
        self.color = color  # 'w' or 'b'
        self.hp = hp
        self.max_hp = hp  # Store initial as max_hp
        self.sq_size = SQ_SIZE
        self.screen = screen
        filename = f"{color}{name}".lower() + ".png"
        path = os.path.join(BASE_DIR, "assets", filename)
        self.image = pygame.transform.scale(pygame.image.load(path), (SQ_SIZE, SQ_SIZE))

    def draw(self, row, col):
        x = col * self.sq_size
        y = row * self.sq_size
        self.screen.blit(self.image, (x, y))

        # Draw HP bar only if damaged
        if self.hp < self.max_hp:
            bar_width = self.sq_size  * 0.8
            bar_height = 6
            bar_x = x + (self.sq_size  - bar_width) / 2
            bar_y = y + self.sq_size  - bar_height - 2  # 2 px above bottom

            # Background (red)
            pygame.draw.rect(self.screen, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))

            # Foreground (green) — proportional
            hp_ratio = max(self.hp, 0) / self.max_hp
            pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))