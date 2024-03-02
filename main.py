import pygame
from sys import exit

WIDTH = 1200
HEIGHT = 800
CELL_SIZE = 30
FPS = 10


def get_grid():
    for height in range(CELL_SIZE, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (127, 130, 130), (0, height), (WIDTH, height), width=2)
    for width in range(CELL_SIZE, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (127, 130, 130), (width, 0), (width, HEIGHT), width=2)


def are_adjacent(x1, y1, x2, y2):
    right_offset_x = abs(x1 - x2) in [CELL_SIZE, 0]
    right_offset_y = abs(y1 - y2) in [CELL_SIZE, 0]
    return right_offset_x and right_offset_y


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def detect_neighbours(self, cells):
        adjacent_cells_amount = 0
        for cell in cells:
            if cell == self:
                continue
            if are_adjacent(self.x, self.y, cell.x, cell.y):
                adjacent_cells_amount += 1

        return adjacent_cells_amount

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"(x: {self.x} y: {self.y})"

    def draw(self):
        pygame.draw.rect(
            screen, (0, 0, 0), pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        )


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")

alive_cells = pygame.sprite.Group()
new_alive_cells = pygame.sprite.Group()
init_cells = []
start = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if not len(init_cells) == 0 and event.key == pygame.K_RETURN:
                alive_cells = pygame.sprite.Group()
                alive_cells.add(*init_cells)
                start = True
            elif event.key == pygame.K_r:
                start = False
                init_cells = []
                alive_cells = pygame.sprite.Group()
        if len(alive_cells) == 0 and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            cell_x = mouse_pos[0] // CELL_SIZE * CELL_SIZE
            cell_y = mouse_pos[1] // CELL_SIZE * CELL_SIZE
            chosen_cell = Cell(cell_x, cell_y)
            if chosen_cell not in init_cells:
                init_cells.append(chosen_cell)
            else:
                init_cells.remove(chosen_cell)

    screen.fill((186, 204, 214))

    if start:
        for cell in alive_cells:
            neighbours_amount = cell.detect_neighbours(alive_cells)
            if neighbours_amount == 2:
                new_alive_cells.add(cell)

        for height in range(0, HEIGHT, CELL_SIZE):
            for width in range(0, WIDTH, CELL_SIZE):
                new_cell = Cell(width, height)
                if new_cell.detect_neighbours(alive_cells) == 3:
                    new_alive_cells.add(new_cell)

        for cell in set(new_alive_cells):
            cell.draw()

        alive_cells = new_alive_cells.copy()
        new_alive_cells = pygame.sprite.Group()
    else:
        for cell in set(init_cells):
            cell.draw()

    get_grid()

    pygame.display.flip()
    clock.tick(FPS)
