import pygame
import os
from damage_popup import DamagePopup
from piece import Piece

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

# === BOARD CLASS ===
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.setup()

    def setup(self):
        # Simplified setup for demo (add full setup if needed)
        for i in range(COLS):
            self.grid[1][i] = Piece('p', 'b', BASE_DIR, SQ_SIZE, screen, hp=2)
            self.grid[6][i] = Piece('p', 'w', BASE_DIR, SQ_SIZE, screen, hp=2)
        self.grid[0][0] = Piece('r', 'b', BASE_DIR, SQ_SIZE, screen, hp=5)
        self.grid[0][7] = Piece('r', 'b', BASE_DIR, SQ_SIZE, screen, hp=5)
        self.grid[7][0] = Piece('r', 'w', BASE_DIR, SQ_SIZE, screen, hp=5)
        self.grid[7][7] = Piece('r', 'w', BASE_DIR, SQ_SIZE, screen, hp=5)

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
