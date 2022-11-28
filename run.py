from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import collections
import random

# Encoding that will store all of your constraints
E = Encoding()


TETRIMINOS = {
    'I': (
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (1, 0), (2, 0), (3, 0))
    ),
    'O': (
        ((0, 0), (0, 1), (1, 0), (1, 1)),
    ),
    'J': (
        ((0, 0), (0, 1), (0, 2), (1, 2)),
        ((0, 1), (1, 1), (2, 0), (2, 1)),
        ((0, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (0, 1), (1, 0), (2, 0))
    ),
    'L': (
        ((0, 0), (0, 1), (0, 2), (1, 0)),
        ((0, 0), (0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 0), (1, 1), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (2, 2))
    ),
    'S': (
        ((0, 1), (0, 2), (1, 0), (1, 1)),
        ((0, 0), (1, 0), (1, 1), (2, 1))
    ),
    'Z': (
        ((0, 0), (0, 1), (1, 1), (1, 2)),
        ((0, 1), (1, 0), (1, 1), (2, 0))
    ),
    'T': (
        ((0, 0), (0, 1), (0, 2), (1, 1)),
        ((0, 1), (1, 0), (1, 1), (2, 1)),
        ((0, 1), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (1, 0), (1, 1), (2, 0))
    )
}


COLUMNS = 2
ROWS = 3
PIECE_SIZE = 4
ROUNDS = 1

PIECES = ('I', 'O', 'J', 'L', 'S', 'Z', 'T')
PIECES_BY_ROUND = [random.choice(PIECES) for _ in range(ROUNDS)]
print(f'Piece Order: {PIECES_BY_ROUND}')


@proposition(E)
class TetrisPiece:
    def __init__(self, piece, rotation, x, y, time):
        self.piece = piece
        self.rotation = rotation
        self.x = x
        self.y = y
        self.time = time

    def __repr__(self):
        return f'{self.piece}_{self.rotation} {self.x, self.y} R{self.time}'


@proposition(E)
class Cell:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def __repr__(self):
        return f'{self.x, self.y} R{self.time}'


cells_by_cell = collections.defaultdict(list)
cells_by_time = collections.defaultdict(list)
all_cell_props = []
for x in range(ROWS + PIECE_SIZE - 1):
    for y in range(COLUMNS + PIECE_SIZE - 1):
        for time in range(ROUNDS):
            cell_prop = Cell(x, y, time)
            cells_by_cell[(x, y)].append(cell_prop)
            cells_by_time[time].append(cell_prop)
            all_cell_props.append(cell_prop)

pieces_by_time = collections.defaultdict(list)
pieces_by_cell = collections.defaultdict(list)
all_piece_props = []
for x in range(ROWS):
    for y in range(COLUMNS):
        for time, piece in enumerate(PIECES_BY_ROUND):
            for i in range(len(TETRIMINOS[piece])):
                piece_prop = TetrisPiece(piece, i, x, y, time)
                pieces_by_time[time].append(piece_prop)
                pieces_by_cell[(x, y)].append(piece_prop)
                all_piece_props.append(piece_prop)

for piece_props in pieces_by_time.values():
    constraint.add_exactly_one(E, *piece_props)

for piece_prop in all_piece_props:
    rotation = TETRIMINOS[piece_prop.piece][piece_prop.rotation]
    cells = ((piece_prop.x + dx, piece_prop.y + dy) for dx, dy in rotation)
    if all(x != ROWS - 1 for x, _ in cells):
        if piece_prop.time:
            constraint.add_at_least_one(
                E, *(cells_by_cell[(x + 1, y)][time - 1] for x, y in cells))
        else:
            E.add_constraint(~piece_prop)

    for x, y in cells:
        for time in range(piece_prop.time):
            for r in range(x + 1):
                E.add_constraint(piece_prop >> (~cells_by_cell[(r, y)][time]))
        for time in range(piece_prop.time, ROUNDS):
            E.add_constraint(piece_prop >> cells_by_cell[(x, y)][time])

for (x, y), cell_props in cells_by_cell.items():
    if x < 0 or x >= ROWS or y < 0 or y >= COLUMNS:
        constraint.add_none_of(E, *cell_props)

for time, cell_props in cells_by_time.items():
    if (time + 1) * PIECE_SIZE < ROWS * COLUMNS:
        constraint.add_at_most_k(E, (time + 1) * PIECE_SIZE, *cell_props)
    else:
        break

# Don't compile until you're finished adding all your constraints!
E = E.compile()
# After compilation (and only after), you can check some of the properties
# of your model:
print(f'\nSatisfiable: {E.satisfiable()}')
# print(f'# Solutions: {count_solutions(T)}')
print(f'Solution: {E.solve()}')
print("Variable likelihoods:")
