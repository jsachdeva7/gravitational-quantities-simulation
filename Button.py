import pygame
from GraphicsUtil import SIZE_14

class Button:
    def __init__(self, text, base_color, active_color, hover_color, border_radius = 10, equation = "", units = "", type_of_concept = "", button_font = SIZE_14, h_padding = 20, v_padding = 5):
        self.text = text
        self.base_color = base_color
        self.active_color = active_color
        self.hover_color = hover_color
        self.hover = False
        self.active = False
        self.h_padding = h_padding
        self.v_padding = v_padding
        self.button_font = button_font
        self.button_text = button_font.render(self.text, 1, self.base_color)
        self.button_width = self.button_text.get_width() + self.h_padding
        self.button_height = self.button_text.get_height() + self.v_padding
        self.border_radius = border_radius
        self.equation = equation
        self.units = units
        self.type_of_concept = type_of_concept # string
        
    def draw(self, position, window):
        current_color = self.base_color if not (self.active or self.hover) else (self.active_color if self.active else self.hover_color)
        self.button_text = self.button_font.render(self.text, 1, current_color)
        self.rect = pygame.Rect(position[0], position[1], self.button_width, self.button_height)
        pygame.draw.rect(window, current_color, self.rect, 1, self.border_radius)
        window.blit(self.button_text, (position[0] + self.h_padding / 2, position[1] + self.v_padding / 2 + 1))

    def is_hovered(self, mouse_pos):
        self.hover = True if self.rect.collidepoint(mouse_pos) else False
        return self.hover
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
            else:
                return False