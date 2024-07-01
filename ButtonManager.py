import pygame
from GraphicsUtil import WHITE, SIZE_20, SIZE_25
from Constants import HEIGHT
from Graph import Graph
from Button import Button
from Mass import Mass, PointMass

class ButtonManager:
    def __init__(
            self, 
            window: pygame.Surface, 
            y_pos: int, 
            buttons_array: list[Button], 
            current_active: str, 
            spacing: int, 
            center_x: float,
        ):
        self.window = window
        self.y_pos = y_pos
        self.buttons_array = buttons_array
        self.num_buttons = len(self.buttons_array)
        self.current_active = current_active
        self.spacing = spacing 
        self.total_length = 0
        for button in self.buttons_array:
            self.total_length += (button.button_width + self.spacing)
        self.total_length -= self.spacing
        self.starting_x = center_x - self.total_length / 2
        self.current_x = self.starting_x
    
    def draw_buttons(self):
        self.current_x = self.starting_x
        mouse_pos = pygame.mouse.get_pos()
        self.any_hovered = False  
        for button in self.buttons_array:
            button.draw((self.current_x, self.y_pos), self.window)
            if button.is_hovered(mouse_pos):
                self.any_hovered = True
            self.current_x += (button.button_width + self.spacing)
        return self.any_hovered

    def handle_click(self, event):
        for button in self.buttons_array:
            if button.is_clicked(event):
                for btn in self.buttons_array:
                    btn.active = False
                button.active = True
                self.current_active = button.text
                new_button = button != self.current_active_object
                self.current_active_object = button
                return new_button
            
class ChangePlanetButtonManager(ButtonManager):
    def __init__(
            self, 
            window, 
            y_pos: int, 
            buttons_array: list[Button], 
            current_active: str, 
            spacing: int, 
            center_x: float, 
            planets: list[Mass]):
        super().__init__(window, y_pos, buttons_array, current_active, spacing,center_x)
        self.planets = planets
        self.current_planet = planets[0]
        self.current_planet_index = 0
        self.num_planets = len(planets)
        self.prev_button = buttons_array[0]
        self.next_button = buttons_array[1]

    def handle_click(self, event: pygame.event):
        if self.prev_button.is_clicked(event) and self.current_planet_index > 0:
            self.current_planet_index -= 1
            self.current_planet = self.planets[self.current_planet_index]
            return True
        elif self.next_button.is_clicked(event) and self.current_planet_index < self.num_planets - 1:
            self.current_planet_index += 1
            self.current_planet = self.planets[self.current_planet_index]
            return True
        return False
    
    def draw_planet_labels(self):
        planet_name_label = SIZE_25.render(self.current_planet.name, 1, WHITE)
        planet_M_label = SIZE_20.render("M = " + "{:.2e}".format(self.current_planet.mass) + " kg", 1, WHITE)
        planet_R_label = SIZE_20.render("R = " + "{:.2e}".format(self.current_planet.R) + " m", 1, WHITE)
        self.window.blit(planet_name_label, (100 - planet_name_label.get_width() / 2, HEIGHT / 2 + 82 - planet_name_label.get_height() / 2))
        self.window.blit(planet_R_label, (100 - planet_R_label.get_width() / 2, HEIGHT / 2 - planet_R_label.get_height() - 70))
        self.window.blit(planet_M_label, (100 - planet_M_label.get_width() / 2, HEIGHT / 2 - planet_M_label.get_height() - 70 - planet_R_label.get_height()))

class mChangeButtonManager(ButtonManager):
    def __init__(
            self, 
            window: pygame.Surface, 
            buttons_array: list[Button], 
            initial_m: int, 
            point_mass: PointMass
        ):
        y_pos = point_mass.y + point_mass.radius + 12
        self.m = initial_m
        self.saved_m = self.m
        self.m_label = SIZE_25.render(str(self.m) + " kg", 1, WHITE)
        self.divide_10_button = buttons_array[0]
        self.times_10_button = buttons_array[1]
        super().__init__(window, y_pos, buttons_array, "", self.m_label.get_width() + 15, point_mass.x)
        self.any_hovered = False
        self.power_of_ten = 2
        self.mass_string = "100"

    def change_to_and_from_1kg(
            self, 
            type_of_concept: str, 
            point_mass: PointMass
        ):
        if type_of_concept == "g pot" or type_of_concept == "g strength":
            self.m = 1
        else:
            self.m = self.saved_m
        point_mass.mass = self.m

    def draw_buttons(self, point_mass, type_of_concept):
        self.spacing = self.m_label.get_width() + 15
        self.starting_x = point_mass.x - self.spacing / 2 - self.divide_10_button.button_width
        if not (type_of_concept == "g pot" or type_of_concept == "g strength"):
            self.any_hovered = super().draw_buttons()

    def draw_m_label(self, point_mass):
        if self.m <= 100 and self.m >= 0.01:
            if self.m >= 1:
                self.mass_string = str(int(self.m))
            else:
                self.mass_string = str(round(self.m, abs(self.power_of_ten)))
        else:
            self.mass_string = "10^" + str(self.power_of_ten)
        self.m_label = SIZE_25.render(self.mass_string + " kg", 1, WHITE)
        self.window.blit(self.m_label,(point_mass.x - self.m_label.get_width() / 2, point_mass.y + point_mass.radius / 2 + 10))

    def handle_click(self, event):
        if self.divide_10_button.is_clicked(event):
            self.m = self.m / 10
            self.saved_m = self.saved_m / 10
            self.power_of_ten -= 1
            return True
        elif self.times_10_button.is_clicked(event):
            self.m = self.m * 10
            self.saved_m = self.saved_m * 10
            self.power_of_ten += 1
            return True
        return False
    
class GraphManager:
    def __init__(self, graphs: list[Graph]):
        self.graphs = graphs
        self.num_graphs = len(graphs)
        self.current_graph_object = self.graphs[2]   

    def change_graph_if_needed(self, type_of_concept, point_mass_tracker):
        if type_of_concept == "g strength":
            self.current_graph_object = self.graphs[0]
        elif type_of_concept == "g pot":
            self.current_graph_object = self.graphs[1]
        elif type_of_concept == "g force":
            self.current_graph_object = self.graphs[2]
        elif type_of_concept == "g pot energy":
            self.current_graph_object = self.graphs[3]
        point_mass_tracker.y = self.current_graph_object.X_AXIS_START[1]
