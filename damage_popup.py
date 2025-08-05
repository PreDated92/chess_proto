import pygame

# === DAMAGE POPUP CLASS ===
class DamagePopup:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.alpha = 255

        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.color = pygame.Color("red")

    def update(self, dt):
        self.y -= 20 * dt  # float upward
        self.alpha -= 100 * dt  # fade out

    def draw(self, surface):
        if self.alpha <= 0:
            return
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(int(self.alpha))
        surface.blit(text_surf, (self.x, self.y))

    def is_dead(self):
        return self.alpha <= 0