import pygame
from GraphicsUtil import WHITE, SIZE_17, SIZE_25, INFINITY_FONT

class Mass:    
    def __init__(
            self, 
            x: float, 
            y: float, 
            radius: int, 
            mass: int, 
            color: tuple,
            name: str,
            rmax: float,
            R: float,
        ):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.name = name
        self.R = R
        self.rmax = rmax

    def draw_mass(self, window):
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius)

class PointMass(Mass):
    def __init__(
            self, 
            x: float, 
            y: float, 
            radius: int, 
            mass: int, 
            color: tuple,
            tracker: bool, 
            name: str,
        ):
        super().__init__(x, y, radius, mass, color, name, 0, 0)
        self.starting_x = x
        self.tracker = tracker

    def draw_mass(
            self, 
            window: pygame.Surface, 
            r: float, 
            rmax: float, 
            m: float
        ):
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius)
        if not self.tracker:
            point_mass_label = SIZE_25.render(str(m) + " kg", 1, WHITE)
            infinity = r >= rmax
            if infinity:
                r_string1 = "r = "
                r_string2 = "∞"
                r_string3 = " m" 
                r_label1 = SIZE_17.render(r_string1, 1, WHITE)
                r_label2 = INFINITY_FONT.render(r_string2, 1, WHITE)
                r_label3 = SIZE_17.render(r_string3, 1, WHITE)
                total_length = r_label1.get_width() + r_label2.get_width() + r_label3.get_width()
                start = self.x - total_length / 2
                window.blit(r_label1, (start, self.y + self.radius / 2 + 10 + point_mass_label.get_height()))
                window.blit(r_label2, (start + r_label1.get_width(), self.y + self.radius / 2 + 5 + point_mass_label.get_height()))
                window.blit(r_label3, (start + r_label1.get_width() + r_label2.get_width(), self.y + self.radius / 2 + 10 + point_mass_label.get_height()))
            else:
                if r <= self.R:
                    r_string = "r = {:.2e} m".format(self.R)
                else:
                    r_string = "r = {:.2e} m".format(r)
                r_label = SIZE_17.render(r_string, 1, WHITE)
                window.blit(r_label, (self.x - r_label.get_width() / 2, self.y + self.radius / 2 + 10 + point_mass_label.get_height()))

    def move_point_mass(
            self, 
            starting_pos: int, 
            infinity_pos: int, 
            step: float
        ):

        # Enforces restrictions on the left and right of the point mass's movement
        if (self.x < infinity_pos and step > 0) or (self.x > starting_pos and step < 0):
            self.x += step




