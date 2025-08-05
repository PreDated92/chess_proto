import pygame
import os
from damage_popup import DamagePopup

# Only run once, globally
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === CONFIG ===
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS
FPS = 60

# === COLORS ===
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
SELECTED_COLOR = (255, 255, 0)

# === PYGAME SETUP ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Custom Chess Engine")
clock = pygame.time.Clock()
damage_popups = []

# === PIECE CLASS ===
class Piece:
    def __init__(self, name, color, hp=1):
        self.name = name  # 'p', 'r', 'n', etc.
        self.color = color  # 'w' or 'b'
        self.hp = hp
        self.max_hp = hp  # Store initial as max_hp
        filename = f"{color}{name}".lower() + ".png"
        path = os.path.join(BASE_DIR, "assets", filename)
        self.image = pygame.transform.scale(pygame.image.load(path), (SQ_SIZE, SQ_SIZE))

    def draw(self, row, col):
        x = col * SQ_SIZE
        y = row * SQ_SIZE
        screen.blit(self.image, (x, y))

        # Draw HP bar only if damaged
        if self.hp < self.max_hp:
            bar_width = SQ_SIZE * 0.8
            bar_height = 6
            bar_x = x + (SQ_SIZE - bar_width) / 2
            bar_y = y + SQ_SIZE - bar_height - 2  # 2 px above bottom

            # Background (red)
            pygame.draw.rect(screen, (150, 0, 0), (bar_x, bar_y, bar_width, bar_height))

            # Foreground (green) — proportional
            hp_ratio = max(self.hp, 0) / self.max_hp
            pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))

# === BOARD CLASS ===
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.setup()

    def setup(self):
        # Simplified setup for demo (add full setup if needed)
        for i in range(COLS):
            self.grid[1][i] = Piece('p', 'b', hp=2)
            self.grid[6][i] = Piece('p', 'w', hp=2)
        self.grid[0][0] = Piece('r', 'b', hp=5)
        self.grid[0][7] = Piece('r', 'b', hp=5)
        self.grid[7][0] = Piece('r', 'w', hp=5)
        self.grid[7][7] = Piece('r', 'w', hp=5)

    def draw(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if (r + c) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                piece = self.grid[r][c]
                if piece:
                    piece.draw(r, c)

    def move(self, start_pos, end_pos):
        sr, sc = start_pos
        er, ec = end_pos
        piece = self.grid[sr][sc]
        target = self.grid[er][ec]
        if piece and (target is None or target.color != piece.color):
            # Optional: attack logic
            if target:
                target.hp -= 1
                # Add a popup at target's position
                screen_x = ec * SQ_SIZE + SQ_SIZE // 2
                screen_y = er * SQ_SIZE + SQ_SIZE // 4
                damage_popups.append(DamagePopup("-1", screen_x, screen_y))

                if target.hp <= 0:
                    self.grid[er][ec] = piece
                    self.grid[sr][sc] = None
                else:
                    return  # target still alive; don't move
            else:
                self.grid[er][ec] = piece
                self.grid[sr][sc] = None

# === MAIN LOOP ===
def main():
    board = Board()
    selected = None
    running = True

    while running:
        board.draw()
        if selected:
            r, c = selected
            pygame.draw.rect(screen, SELECTED_COLOR, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)

        # font = pygame.font.SysFont("Arial", 20, bold=True)
        # red = (255, 0, 0)
        # screen.blit(font.render("DEBUG", True, red), (10, 10))
        
        clock.tick(FPS)
        dt = clock.get_time() / 1000  # seconds since last frame
        for popup in damage_popups:
            popup.update(dt)
            popup.draw(screen)

        # No more drawing beyond this point
        pygame.display.flip() 
        
        # Remove finished popups
        damage_popups[:] = [p for p in damage_popups if not p.is_dead()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                row, col = my // SQ_SIZE, mx // SQ_SIZE

                if selected:
                    board.move(selected, (row, col))
                    selected = None
                else:
                    piece = board.grid[row][col]
                    if piece:
                        selected = (row, col)

    pygame.quit()

if __name__ == "__main__":
    main()
