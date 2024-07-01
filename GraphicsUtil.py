import pygame
pygame.font.init()
from Constants import HEIGHT

WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
SPACE_BLACK = (20, 20, 20)
RED = (250, 128, 114)
JUPITER_BROWN = (184, 131, 84)
SUN_ORANGE = (255, 111, 0)
MOON_YELLOW = (246, 241, 213)
BLUE = (86, 161, 252)
YELLOW = (255, 200, 97)
LIGHT_YELLOW = (255, 234, 191)
ALDEBARAN_RED = (227, 51, 16)
BETELGEUSE_RED = (255, 193, 104)
PROXIMA_BROWN = (181, 110, 4)

SIZE_38 = pygame.font.Font("cmunss.ttf", 38)
SIZE_30 = pygame.font.Font("cmunss.ttf", 30)
SIZE_25 = pygame.font.Font("cmunss.ttf", 25)
SIZE_20 = pygame.font.Font("cmunss.ttf", 20)
INFINITY_FONT = pygame.font.SysFont("comicsans", 20)
SIZE_17 = pygame.font.Font("cmunss.ttf", 17)
SIZE_14 = pygame.font.Font("cmunss.ttf", 14)
SIZE_11 = pygame.font.Font("cmunss.ttf", 11)

def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 1,
        head_width: int = 10,
        head_height: int = 10,
    ):
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)

def draw_vert_dashed_line(window, x, dash_length, dash_space_between, start_y, end_y):
    current_y = start_y
    while current_y < end_y:
        pygame.draw.line(window, WHITE, (x, current_y), (x, current_y + dash_length - 1), 1)
        current_y += (dash_length + dash_space_between)
            
def draw_line_graph(window, point_p_x, y):
    GRAPH_WIDTH = 750
    AXIS_START_X = 100
    AXIS_END_X = 825
    Y = y

    pygame.draw.line(window, WHITE, (AXIS_START_X, Y), (AXIS_END_X, Y), 2)
    
    def draw_tick(x_pos, text):
        infinity = text == "∞"
        pygame.draw.line(window, WHITE, (AXIS_START_X + x_pos, Y + 10), (AXIS_START_X + x_pos, Y), 2)
        tick_label = SIZE_20.render(text, 1, WHITE) if not infinity else INFINITY_FONT.render(text, 1, WHITE)
        window.blit(tick_label, (AXIS_START_X + x_pos - tick_label.get_width() / 2, Y + tick_label.get_height() / 2 - (0 if not infinity else 5)))

    draw_tick(0, "0")
    draw_tick(60, "R")
    draw_tick(point_p_x - 100, "P")
    draw_tick(AXIS_END_X - AXIS_START_X, "∞")

def draw_zig_zag(window, start: tuple, end: tuple, height: int, no_zig_zags):
    start_x = start[0]
    end_x = end[0]
    y_avg = start[1]
    max_y = y_avg - height / 2
    min_y = max_y + height
    quarter_x_step = (end_x - start_x) / (no_zig_zags * 4 - 2)
    current_start = (start_x, y_avg)
    for i in range(no_zig_zags * 2):
        if i == 0:
            current_end = (current_start[0] + quarter_x_step, max_y)
        elif i == (no_zig_zags * 2 - 1):
            current_end = (current_start[0] + quarter_x_step, y_avg)
        elif i % 2 == 0:
            current_end = (current_start[0] + 2 * quarter_x_step, max_y)
        elif i % 2 == 1:
            current_end = (current_start[0] + 2 * quarter_x_step, min_y)
        pygame.draw.line(window, WHITE, current_start, current_end, 2)
        current_start = current_end
