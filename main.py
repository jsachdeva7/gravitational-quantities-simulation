import pygame
from Graph import Graph
from Button import Button
from ButtonManager import ButtonManager, ChangePlanetButtonManager, mChangeButtonManager, GraphManager
from Mass import Mass, PointMass
from GraphicsUtil import BLUE, GRAY, JUPITER_BROWN, SUN_ORANGE, MOON_YELLOW, ALDEBARAN_RED, BETELGEUSE_RED, PROXIMA_BROWN, RED, WHITE, YELLOW, LIGHT_YELLOW, SPACE_BLACK, SIZE_11, SIZE_38, SIZE_17, draw_vert_dashed_line, draw_line_graph
from Constants import WIDTH, HEIGHT
pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
TOP = HEIGHT / 2 - 250
pygame.display.set_caption("Gravitational Quantities Visualization")
pointer_cursor = pygame.SYSTEM_CURSOR_HAND
system_cursor = pygame.SYSTEM_CURSOR_ARROW

def reset(actual_point_mass, graph_point_mass, graph, m):
    actual_point_mass.x = actual_point_mass.starting_x
    graph_point_mass.x = graph_point_mass.starting_x
    graph.current_r = graph.R
    graph.points = []
    if hasattr(graph, "current_x_plot"):
        del graph.current_x_plot

def main():
    run = True
    moving = False
    clock = pygame.time.Clock()

    # Set the initial simulation direction and speed (of the point mass). Def
    simulation_speed = 70
    simulation_time = 250 / simulation_speed
    simulation_direction = 1

    # Set the step (in pixels) of the point mass on the graph
    graph_x_step = (1130 - (900 + 250 / 8)) / (simulation_time * 60)

    # Create planet objects
    earth = Mass(100, HEIGHT / 2, 60, 5.972 * 10**24, BLUE, "Earth", 597200000, 6.371 * 10**6)
    mercury = Mass(100, HEIGHT / 2, 60, 3.285 * 10**23, GRAY, "Mercury", 231487796, 2.4397 * 10**6)
    jupiter = Mass(100, HEIGHT / 2, 60, 1.898 * 10**27, JUPITER_BROWN, "Jupiter", 7448663796, 69.911 * 10**6)
    sun = Mass(100, HEIGHT / 2, 60, 1.989 * 10**30, SUN_ORANGE, "the Sun", 81593071668, 6.9634 * 10**8)
    moon = Mass(100, HEIGHT / 2, 60, 7.34767309 * 10**22, MOON_YELLOW, "the Moon", 147760311.6, 1.74 * 10**6)
    aldebaran = Mass(100, HEIGHT / 2, 60, 3.381 * 10**30, ALDEBARAN_RED, "Aldebaran", 3014881021595, 30.701 * 10**9)
    betelgeuse = Mass(100, HEIGHT / 2, 60, 3.282 * 10**31, BETELGEUSE_RED, "Betelgeuse", 60297620431892, 617.1 * 10**9)
    proxima_centauri_b = Mass(100, HEIGHT / 2, 60, 1.2 * 5.972 * 10**24, PROXIMA_BROWN, "Proxima b", 597200000 * 1.2, 1.3 * 6.371 * 10**6)
    point_mass = PointMass(earth.x + earth.radius, HEIGHT / 2, 10, 1, RED, False, "Point Mass")
    point_mass_tracker = PointMass(900 + 250 / 8, 125, 5, 1, RED, True, "Point Mass Tracker")
    rendered_planet = earth
    planets_array = [earth, mercury, jupiter, sun, moon, aldebaran, betelgeuse, proxima_centauri_b]

    # Create buttons that allow user to cycle through planets
    prev_planet_button = Button("<", WHITE, GRAY, GRAY, 4)
    next_planet_button = Button(">", WHITE, GRAY, GRAY, 4)
    change_planet_button_array = [prev_planet_button, next_planet_button]
    change_planet_button_manager = ChangePlanetButtonManager(WINDOW, HEIGHT / 2 + 100, change_planet_button_array, "", 10, earth.x, planets_array)

    # Create buttons that allow user to change the mass of the point mass
    times_ten_button = Button("x 10", WHITE, GRAY, GRAY, button_font=SIZE_11, h_padding=10, v_padding=2)
    divide_ten_button = Button("÷10", WHITE, GRAY, GRAY, button_font=SIZE_11, h_padding=10, v_padding=2)
    change_m_button_array = [divide_ten_button, times_ten_button]
    m_change_button_manager = mChangeButtonManager(WINDOW, change_m_button_array, 100, point_mass)

    # Create the graphs for gravitational force, field strength, potential, and potential energy
    g_pot_graph = Graph(WINDOW, graph_x_step, YELLOW, False, change_planet_button_manager.current_planet, False, 1)
    g_pot_energy_graph = Graph(WINDOW, graph_x_step, YELLOW, False, change_planet_button_manager.current_planet, True, m_change_button_manager.m)
    g_strength_graph = Graph(WINDOW, graph_x_step, YELLOW, True, change_planet_button_manager.current_planet, False, 1, [900, HEIGHT / 2 + 125])
    g_force_graph = Graph(WINDOW, graph_x_step, YELLOW, True, change_planet_button_manager.current_planet, True, m_change_button_manager.m, [900, HEIGHT / 2 + 125])
    graph_array = [g_strength_graph, g_pot_graph, g_force_graph, g_pot_energy_graph]
    graph_manager = GraphManager(graph_array)
    
    # Create the buttons that allow users to switch between what concept is currently being visualized.
    g_force_button = Button("Gravitational Force", WHITE, YELLOW, LIGHT_YELLOW, 10, "F = G M m / r^2", "N", "g force")
    g_force_button.active = True
    g_strength_button = Button("Gravitational Field Strength", WHITE, YELLOW, LIGHT_YELLOW, 10, "g = G M / r^2", "N kg-1", "g strength")
    g_pot_energy_button = Button("Gravitational Potential Energy", WHITE, YELLOW, LIGHT_YELLOW, 10, "U = - G M m / r", "J", "g pot energy")
    g_pot_button = Button("Gravitational Potential", WHITE, YELLOW, LIGHT_YELLOW, 10, "V = - G M / r", "J kg-1", "g pot")
    concept_button_array = [g_force_button, g_strength_button, g_pot_energy_button, g_pot_button]
    concept_button_manager = ButtonManager(WINDOW, TOP, concept_button_array, "Gravitational Force", 20, WIDTH / 2)
    concept_button_manager.current_active_object = g_force_button
                
    while run:
        # Set refresh rate (60 Hz), set the background of the window to be black, display title + instructions
        clock.tick(60)
        WINDOW.fill(SPACE_BLACK)
        title_string = "Visualizing " + concept_button_manager.current_active
        title = SIZE_38.render(title_string, 1, WHITE)
        WINDOW.blit(title, (WIDTH / 2 - title.get_width() / 2, TOP + 31))
        instructions = SIZE_17.render("Use left and right arrow keys to move P.", 1, WHITE)
        WINDOW.blit(instructions, (WIDTH / 2 - instructions.get_width() / 2, TOP + 31 + title.get_height()))

        # Change the graph if another concept is clicked, draw graph components
        graph_manager.change_graph_if_needed(concept_button_manager.current_active_object.type_of_concept, point_mass_tracker)
        graph_manager.current_graph_object.draw_graph(concept_button_manager.current_active_object.equation[0])
        graph_manager.current_graph_object.draw_graph_point(moving, concept_button_manager.current_active_object.units)
        graph_manager.current_graph_object.draw_graph_caption(concept_button_manager.current_active_object, m_change_button_manager.mass_string, change_planet_button_manager.current_planet.name)

        # Draw each planet that should currently be rendered and their labels
        rendered_planet.draw_mass(WINDOW)
        point_mass.draw_mass(WINDOW, graph_manager.current_graph_object.current_r, graph_manager.current_graph_object.rmax, m_change_button_manager.m)
        point_mass_tracker.draw_mass(WINDOW, graph_manager.current_graph_object.current_r, graph_manager.current_graph_object.rmax, m_change_button_manager.m)
        change_planet_button_manager.draw_planet_labels()

        # Draw all buttons
        concept_button_manager.draw_buttons()
        change_planet_button_manager.draw_buttons()
        m_change_button_manager.draw_buttons(point_mass, concept_button_manager.current_active_object.type_of_concept)
        m_change_button_manager.draw_m_label(point_mass)
        if concept_button_manager.any_hovered or change_planet_button_manager.any_hovered or m_change_button_manager.any_hovered:
            pygame.mouse.set_cursor(pointer_cursor)
        else:
            pygame.mouse.set_cursor(system_cursor)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    moving = True
                    simulation_direction = 1
                    graph_manager.current_graph_object.r_step = abs(graph_manager.current_graph_object.r_step)
                elif event.key == pygame.K_LEFT:
                    moving = True
                    simulation_direction = -1
                    graph_manager.current_graph_object.r_step = -(abs(graph_manager.current_graph_object.r_step))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    moving = False
            concept_button_clicked = concept_button_manager.handle_click(event)
            planet_changed = change_planet_button_manager.handle_click(event)
            mass_changed = m_change_button_manager.handle_click(event)
            (concept_button_clicked or planet_changed or mass_changed) and reset(point_mass, point_mass_tracker, graph_manager.current_graph_object, m_change_button_manager.m)
            if planet_changed or mass_changed:
                for graph in graph_array:
                    graph.update_for_current_planet_or_mass(change_planet_button_manager.current_planet, m_change_button_manager.m)
                rendered_planet = change_planet_button_manager.current_planet

            m_change_button_manager.change_to_and_from_1kg(concept_button_manager.current_active_object.type_of_concept, point_mass)
                
        if moving:
            point_mass.move_point_mass(160, 825, simulation_direction * (825 - 160) / (simulation_time * 60))
            point_mass_tracker.move_point_mass(graph_manager.current_graph_object.X_AXIS_START[0] + 250 / 8, 1130, 
                                               simulation_direction * graph_x_step)
            
        draw_line_graph(WINDOW, point_mass.x, earth.y + 180)
        draw_vert_dashed_line(WINDOW, 825, 10, 7, HEIGHT / 2 - 150, HEIGHT / 2 + 150)

        pygame.display.update()
    pygame.quit()
    
main()