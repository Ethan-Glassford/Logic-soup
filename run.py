from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import collections
import random
# import visualize
import itertools
import operator

E = Encoding()


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

# Create proposition for a single cell
# If true the cell is occupied/blocked by a piece


@proposition(E)
class Cell:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

    def __repr__(self):
        return f'{self.x, self.y} R{self.time}'


# Encoding that will store all of your constraints
if __name__ == '__main__':

    # CONSTANTS
    # With (0,0) in the top-left corner blocks a piece takes up are based on where it is from the 0,0 corner
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

    ROWS = 2
    COLUMNS = 4
    PIECE_SIZE = 4
    ROUNDS = 2
    PIECES = ('I', 'O', 'J', 'L', 'S', 'Z', 'T')

    # Randomize order of incoming pieces
    PIECES_BY_ROUND = [random.choice(PIECES) for _ in range(ROUNDS)]
    PIECES_BY_ROUND = ['O', 'O']
    print(f'Piece Order: {PIECES_BY_ROUND}')

    # Represent a general tetriino piece
    # Type of piece, orientation, location and what round piece is in play in.

    # Each key is defaulted to an empty list
    cells_by_cell = collections.defaultdict(list)
    cells_by_time = collections.defaultdict(list)

    all_cell_props = []
    for x in range(ROWS + PIECE_SIZE - 1):  # loop through every cell
        for y in range(COLUMNS + PIECE_SIZE - 1):  # loop through every cell
            for time in range(ROUNDS):  # Loop through every round
                # Creating a proposition for each cell,
                cell_prop = Cell(x, y, time)
                cells_by_cell[(x, y)].append(cell_prop)
                cells_by_time[time].append(cell_prop)
                all_cell_props.append(cell_prop)

    pieces_by_time = collections.defaultdict(list)
    pieces_by_cell = collections.defaultdict(list)
    all_piece_props = []
    for x in range(ROWS):
        for y in range(COLUMNS):
            # Loop through round specific piece
            for time, piece in enumerate(PIECES_BY_ROUND):
                # Loop through orientation
                for i in range(len(TETRIMINOS[piece])):
                    # Create proposition for each cell
                    piece_prop = TetrisPiece(piece, i, x, y, time)
                    pieces_by_time[time].append(piece_prop)
                    pieces_by_cell[(x, y)].append(piece_prop)
                    all_piece_props.append(piece_prop)

    # CONSTRAINTS

    # There must be exactly one piece placed in a round.
    for piece_props in pieces_by_time.values():
        constraint.add_exactly_one(E, *piece_props)

    # For all piece propositions, when they are placed ina  location they will then occupy those cells.
    for piece_prop in all_piece_props:
        rotation = TETRIMINOS[piece_prop.piece][piece_prop.rotation]
        cells = [(piece_prop.x + dx, piece_prop.y + dy) for dx, dy in rotation]
        # If there is no cell touching the bottom, it must be checked
        if all(x < ROWS - 1 for x, _ in cells):
            if piece_prop.time:  # If this is not round 1
                below = (cells_by_cell[(x + 1, y)][time - 1] for x, y in cells)
                at_least_one = itertools.accumulate(below, operator.or_)
                # There must be a piece for the current to fall onto
                E.add_constraint(piece_prop >> at_least_one)
            else:
                E.add_constraint(~piece_prop)

        # Check every cell
        for x, y in cells:
            # For all previous rounds
            if piece_prop.time:
                for r in range(x + 1):
                    # If there are occupied cells above or in the same cell, the atempted placement is invalid.
                    E.add_constraint(piece_prop >> (
                        ~cells_by_cell[(r, y)][piece_prop.time - 1]))
            # For this and future rounds, this cell will be occupied
            for time in range(piece_prop.time, ROUNDS):
                E.add_constraint(piece_prop >> cells_by_cell[(x, y)][time])

    # Ensure out of bound cells can not pieces placed in them
    for (x, y), cell_props in cells_by_cell.items():
        if x < 0 or x >= ROWS or y < 0 or y >= COLUMNS:
            constraint.add_none_of(E, *cell_props)

    # For a cell to be occupied, there must be a actual piece placed in the location
    for time, cell_props in cells_by_time.items():
        # Each piece must take up PIECE_SIZE cells
        if (time + 1) * PIECE_SIZE < ROWS * COLUMNS:
            # Check each round for correct number of cells occupied.
            constraint.add_at_most_k(E, (time + 1) * PIECE_SIZE, *cell_props)
        else:
            break

    # Don't compile until you're finished adding all your constraints!
    E = E.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print(f'\nSatisfiable: {E.satisfiable()}')
    # print(f'# Solutions: {count_solutions(E)}')
    solution = E.solve()
    print(f'Solution: {solution}')
    # visualize.visualize(solution, ROWS, COLUMNS, TETRIMINOS)
