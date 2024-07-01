import pygame
from GraphicsUtil import WHITE, YELLOW, SIZE_17, SIZE_20, SIZE_30, INFINITY_FONT, draw_arrow, draw_vert_dashed_line
from Constants import G, HEIGHT
from Mass import Mass

graph_center_y = HEIGHT / 2 

class Graph:
    def __init__(
            self, 
            window: pygame.Surface, 
            step: float, 
            color: tuple, 
            positive: bool, 
            starting_planet, 
            m_graph: bool, 
            m: int = 1, 
            X_AXIS_START = (900, graph_center_y - 125),
            GRAPH_WIDTH: int = 250, 
            GRAPH_HEIGHT: int = 250,
            ):
        self.window = window
        self.X_AXIS_START = X_AXIS_START
        self.GRAPH_WIDTH = GRAPH_WIDTH 
        self.GRAPH_HEIGHT = GRAPH_HEIGHT 
        self.Y_AXIS_START = (X_AXIS_START[0], graph_center_y - self.GRAPH_HEIGHT / 2 if not positive else graph_center_y + self.GRAPH_HEIGHT / 2)
        self.X_AXIS_END = (X_AXIS_START[0] + self.GRAPH_WIDTH, X_AXIS_START[1])
        self.Y_AXIS_END = (self.Y_AXIS_START[0], self.Y_AXIS_START[1] + (self.GRAPH_HEIGHT if not positive else - self.GRAPH_HEIGHT))
        self.points = [] # Array storing points currently plotted on the graph
        self.color = color
        self.step = step # Pixel step for each frame of movement
        self.positive = positive # Positive or negative graph
        self.m = m # Mass of point mass (m)
        self.m_graph = m_graph # whether the graph is for an equation that includes the mass of point mass (m)
        self.update_for_current_planet_or_mass(starting_planet, self.m)



    # Updates numerical values stored in graph object if the point mass's mass or the current "planet" is changed
    def update_for_current_planet_or_mass(
            self, 
            current_planet: Mass, 
            current_mass: int
        ): 
        if self.m_graph:
            self.m = current_mass
        self.M = current_planet.mass
        self.R = current_planet.R
        self.rmax = current_planet.rmax # Maximum distance that the point mass can travel (planet dependent, affects graph clarity)
        self.current_r = self.R
        self.current_grav_x = (G * self.M * self.m / self.R) if not self.positive else (G * self.M * self.m / self.R ** 2) # Value of the gravitational quantity
        self.displayed_grav_x = self.current_grav_x
        self.x_scale = (self.rmax - self.R) / (230 - self.GRAPH_WIDTH / 8)
        self.y_scale = self.current_grav_x / 230
        self.r_step = self.step * self.x_scale

    # Draws a tick on the graph's x-axis
    def draw_x_tick(self, x_pos, text):
        infinity = text == "∞"
        pygame.draw.line(self.window, WHITE, (self.X_AXIS_START[0] + x_pos, self.X_AXIS_END[1] + (10 if self.positive else -10)), (self.X_AXIS_START[0] + x_pos, self.X_AXIS_END[1]), 2)
        tick_label = SIZE_20.render(text, 1, WHITE) if not infinity else INFINITY_FONT.render(text, 1, WHITE)
        self.window.blit(tick_label, (self.X_AXIS_START[0] + x_pos - tick_label.get_width() / 2 + (0 if not infinity else 1), self.X_AXIS_START[1] + (1 if self.positive else -1)*(tick_label.get_height() / 2 + (0 if self.positive else 25) + (-8 if self.positive and infinity else 0))))

    # Draws a tick on the graph's y-axis
    def draw_y_tick(self, y_pos, text):
        point_on_y_axis = self.Y_AXIS_START[1] + (-1 if self.positive else 1) * y_pos
        pygame.draw.line(self.window, WHITE, (self.X_AXIS_START[0] - 10, point_on_y_axis), (self.X_AXIS_START[0], point_on_y_axis), 2)
        tick_label = SIZE_20.render(text, 1, WHITE)
        self.window.blit(tick_label, (self.X_AXIS_START[0] - tick_label.get_width() - 20, point_on_y_axis - tick_label.get_height() / 2))

    # Draw the graph's skeleton
    def draw_graph(self, y_axis_variable):

        # Draw x and y-axes + labels
        draw_arrow(self.window, pygame.Vector2(self.X_AXIS_START), pygame.Vector2(self.X_AXIS_END), WHITE) # x-axis
        draw_arrow(self.window, pygame.Vector2(self.Y_AXIS_START), pygame.Vector2(self.Y_AXIS_END), WHITE) # y-axis
        x_axis_label = SIZE_30.render("r", 1, WHITE)
        y_axis_label = SIZE_30.render(y_axis_variable, 1, WHITE)
        self.window.blit(x_axis_label, (self.X_AXIS_END[0] + 20 - x_axis_label.get_width()/2, self.X_AXIS_END[1] 
                                        - x_axis_label.get_height()/2 - 5))
        self.window.blit(y_axis_label, (self.Y_AXIS_END[0] - y_axis_label.get_width()/2, self.Y_AXIS_END[1] - y_axis_label.get_height()/2 
                                        + (-1 if self.positive else 1) * 20))

        # Draw line to indicate where the surface of M is
        top_of_dashed_line = self.Y_AXIS_END[1] if self.positive else self.Y_AXIS_START[1]
        bottom_of_dashed_line = self.Y_AXIS_START[1] if self.positive else self.Y_AXIS_END[1]
        draw_vert_dashed_line(self.window, self.X_AXIS_START[0] + self.GRAPH_WIDTH / 8, 3, 3, top_of_dashed_line, bottom_of_dashed_line)

        # Draw ticks on the axes
        self.draw_x_tick(0, "0")
        self.draw_x_tick(230, "∞")
        self.draw_x_tick(self.GRAPH_WIDTH / 8, "R")
        self.draw_y_tick(230, y_axis_variable + ("min" if not self.positive else "max"))
        self.draw_y_tick(0, "0")
    
    # Plots points on the graph
    def draw_graph_point(self, moving, units):

        # Adds a point to the points array if point mass is moving (arrow keys being pressed)
        if moving:

            # Enforces limits on either end for r
            if (self.current_r <= self.rmax and self.r_step > 0) or (self.current_r >= self.R and self.r_step < 0):

                # Calculates the current gravitational quantity's value (differs if a force or energy calculation)
                self.current_grav_x = (G * self.M * self.m / self.current_r) if not self.positive else (G * self.M * self.m / self.current_r ** 2)
                self.max_grav_x = (G * self.M * self.m / self.R) if not self.positive else (G * self.M * self.m / self.R ** 2)
                
                # Enforces a limit on the current gravitational quantity's value
                if self.current_grav_x > self.max_grav_x:
                    self.current_grav_x = self.max_grav_x
                self.displayed_grav_x = (1 if self.positive else -1) * self.current_grav_x

                # Converts r and gravitational quantity value into an (x, y) coordinate that is added to the points array
                self.current_x_plot = self.current_r / self.x_scale - self.R / self.x_scale + self.X_AXIS_START[0] + self.GRAPH_WIDTH / 8
                self.current_y_plot = self.X_AXIS_START[1] + (-1 if self.positive else 1) * (self.current_grav_x / self.y_scale)
                if self.current_x_plot >= (self.X_AXIS_START[0] + 250 / 8) and self.current_x_plot <= (self.X_AXIS_START[0] + 230):
                    self.points.append((self.current_x_plot, self.current_y_plot))

                # Updates r
                self.current_r += self.r_step
                if self.current_r < self.R:
                    self.current_r = self.R

        # Plots the current point with a circle
        if hasattr(self, "current_x_plot"):        
            pygame.draw.circle(self.window, self.color, (self.current_x_plot, self.current_y_plot), 5)
            self.draw_x_tick(self.current_r / self.x_scale - self.R / self.x_scale + self.GRAPH_WIDTH / 8, "P")
            if self.current_r >= self.rmax:
                self.displayed_grav_x = 0.0
            self.displayed_grav_x_string = (
                "{:.2e}".format(self.displayed_grav_x) if (self.displayed_grav_x < 0.1 or self.displayed_grav_x > 100) 
                else "{:.2f}".format(self.displayed_grav_x)
            )
            self.grav_x_label = SIZE_17.render((self.displayed_grav_x_string if self.current_r < self.rmax else "0") + " " + units, 1, self.color)
            self.window.blit(self.grav_x_label, (self.current_x_plot - self.grav_x_label.get_width() / 2, self.current_y_plot - self.grav_x_label.get_height() / 2 + (-1 if self.positive else 1) * 20))
        
        # Draws the graph's curve using the points array
        if len(self.points) >= 2:
            pygame.draw.lines(self.window, self.color, False, self.points, 4)

    # Writes the caption for the graph based on the current graph's concept and the current plotted point's value
    def draw_graph_caption(self, current_concept, mass_string, planet_name):
        force = current_concept.type_of_concept == "force"

        displayed_grav_x_string = (
            "{:.2e} ".format(abs(self.displayed_grav_x)) if (self.displayed_grav_x < 0.1 or self.displayed_grav_x > 100) 
            else "{:.2f} ".format(self.displayed_grav_x)
        )
        caption_line1_string = "The " + mass_string + " kg point mass " + ("feels a " if force else "needs ") +  (displayed_grav_x_string if self.displayed_grav_x !=0 else "0 ") + current_concept.units[0]
        caption_line1 = SIZE_17.render(caption_line1_string, 1, WHITE)
        bottom_of_graph = self.Y_AXIS_START[1] if self.positive else self.Y_AXIS_END[1]
        self.window.blit(caption_line1, ((self.X_AXIS_END[0] + self.X_AXIS_START[0]) / 2 - caption_line1.get_width() / 2, bottom_of_graph + 42))

        caption_line2_string = "gravitational force at point P due" if force else "to escape " + planet_name + "'s gravitational field"
        caption_line2 = SIZE_17.render(caption_line2_string, 1, WHITE)
        self.window.blit(caption_line2, ((self.X_AXIS_END[0] + self.X_AXIS_START[0]) / 2 - caption_line2.get_width() / 2, bottom_of_graph + 42 + caption_line1.get_height()))

        caption_line3_string = "to " + planet_name + "'s gravitational field." if force else "from point P."
        caption_line3 = SIZE_17.render(caption_line3_string, 1, WHITE)
        self.window.blit(caption_line3, ((self.X_AXIS_END[0] + self.X_AXIS_START[0]) / 2 - caption_line3.get_width() / 2, bottom_of_graph + 42 + caption_line1.get_height() + caption_line2.get_height()))
        
        equation_caption = SIZE_20.render(current_concept.equation, 1, YELLOW)
        self.window.blit(equation_caption, ((self.X_AXIS_END[0] - equation_caption.get_width() / 2 - 40, self.Y_AXIS_END[1] - 10)))