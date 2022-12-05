import pygame
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import collections


class Visualizer:
    WIDTH, HEIGHT = 1100, 800
    PAD = 0.25
    ADJ = (-1, 0), (1, 0), (0, -1), (0, 1)
    PIECE_COLOURS = (
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (89, 38, 78), (67, 198, 8),
        (4, 200, 200), (127, 127, 200), (255, 128, 0)
    )
    BG_COLOUR = 0, 0, 0
    LINE_COLOUR = 127, 127, 127
    LINE_THICKNESS = 3

    def __init__(self, solution, rows, columns, tetriminos):
        self.surface = pygame.display.set_mode(
            (Visualizer.WIDTH, Visualizer.HEIGHT)
        )
        self.surface.fill(Visualizer.BG_COLOUR)
        self.cell_size = min(
            (Visualizer.WIDTH * (1 - Visualizer.PAD)) / columns,
            (Visualizer.HEIGHT * (1 - Visualizer.PAD)) / rows
        )
        self.top_magin = (Visualizer.HEIGHT - (self.cell_size * rows)) / 2
        self.left_margin = (Visualizer.WIDTH - (self.cell_size * columns)) / 2
        self.rows = rows
        self.columns = columns
        self.solution = solution
        self.tetriminos = tetriminos

    def draw_grid(self, cell_colours):
        for i in range(self.rows):
            for j in range(self.columns):
                left = self.left_margin + j*self.cell_size
                right = left + self.cell_size
                top = self.top_magin + i*self.cell_size
                bottom = top + self.cell_size
                pygame.draw.rect(
                    self.surface,
                    cell_colours[(i, j)],
                    (left, top, self.cell_size, self.cell_size),
                )
                pygame.draw.line(
                    self.surface,
                    Visualizer.LINE_COLOUR,
                    (left, top),
                    (right, top),
                    Visualizer.LINE_THICKNESS
                )
                pygame.draw.line(
                    self.surface,
                    Visualizer.LINE_COLOUR,
                    (left, top),
                    (left, bottom),
                    Visualizer.LINE_THICKNESS
                )
                pygame.draw.line(
                    self.surface,
                    Visualizer.LINE_COLOUR,
                    (right, top),
                    (right, bottom),
                    Visualizer.LINE_THICKNESS
                )
                pygame.draw.line(
                    self.surface,
                    Visualizer.LINE_COLOUR,
                    (left, bottom),
                    (right, bottom),
                    Visualizer.LINE_THICKNESS
                )
        pygame.display.update()

    def get_cell_colours(self, piece_colours=None):
        if piece_colours is None:
            piece_colours = self.get_piece_colours()
        cell_colours = collections.defaultdict(lambda: Visualizer.BG_COLOUR)
        for piece, colour in piece_colours.items():
            for dx, dy in self.tetriminos[piece.piece][piece.rotation]:
                cell_colours[(piece.x + dx, piece.y + dy)] = colour
        return cell_colours

    def get_piece_colours(self):
        cells_by_piece = collections.defaultdict(set)
        for prop, isTrue in self.solution.items():
            if not isTrue:
                continue
            try:
                for dx, dy in self.tetriminos[prop.piece][prop.rotation]:
                    cells_by_piece[prop].add((prop.x + dx, prop.y + dy))
            except AttributeError:
                continue

        graph = collections.defaultdict(list)
        for piece0, cells0 in cells_by_piece.items():
            for piece1, cells1 in cells_by_piece.items():
                if piece0.time >= piece1.time:
                    continue
                flag = False
                for x0, y0 in cells0:
                    for dx, dy in Visualizer.ADJ:
                        if (x0 + dx, y0 + dy) in cells1:
                            graph[piece0].append(piece1)
                            graph[piece1].append(piece0)
                            flag = True
                            break
                    if flag:
                        break
        colours = {}
        for piece in cells_by_piece:
            neighbors = graph[piece]
            used = {colours[nei] for nei in neighbors if nei in colours}
            for colour in Visualizer.PIECE_COLOURS:
                if colour not in used:
                    colours[piece] = colour
                    break
        return colours


def visualize(solution, rows, columns, tetriminos):
    visualizer = Visualizer(solution, rows, columns, tetriminos)
    visualizer.draw_grid(visualizer.get_cell_colours())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
