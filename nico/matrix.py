from enum import Enum
from typing import List


class State(Enum):
    NA = 0
    FILLED = 1
    EMPTY = 2


class Constraint:
    list: List[int]

    def __init__(self):
        self.list = []


class CellState:
    filled: int
    empty: int

    def __init__(self):
        self.empty = 0
        self.filled = 0

    def reinit(self):
        self.empty = 0
        self.filled = 0

    def get_state(self) -> State:
        if self.filled > 0 and self.empty == 0:
            return State.FILLED
        elif self.filled == 0 and self.empty > 0:
            return State.FILLED
        else:
            return State.NA


class Cell:
    state_x: CellState
    state_y: CellState

    global_state: State

    def __init__(self):
        self.state_x = CellState()
        self.state_y = CellState()
        self.global_state = State.NA

    def reset(self, is_col: bool):
        if is_col:
            self.state_y = CellState()
        else:
            self.state_x = CellState()

    def add_state(self, state: State, is_col: bool) -> bool:
        cell_state = self.state_y if is_col else self.state_x
        other_state = self.state_x if is_col else self.state_y
        if (state == State.FILLED and other_state.filled == 0 and other_state.empty > 0) \
            or (state == State.EMPTY and other_state.empty == 0 and other_state.filled > 0):
            return False
        if state == State.FILLED:
            cell_state.filled += 1
        else:
            cell_state.empty += 1
        return True

    def compute_state(self, is_col: bool) -> bool:
        if self.global_state != State.NA:
            return False
        cell_state = self.state_y if is_col else self.state_x
        if cell_state.empty > 0 and cell_state.filled == 0:
            self.global_state = State.EMPTY
            return True
        elif cell_state.filled > 0 and cell_state.empty == 0:
            self.global_state = State.FILLED
            return True
        return False

    def __str__(self):
        if self.global_state == State.FILLED:
            return 'X'
        elif self.global_state == State.EMPTY:
            return ' '
        else:
            return 'O'


class HasChanged:
    x_has_changed: bool
    y_has_changed: bool

    def reset(self, is_col: bool):
        if is_col:
            self.y_has_changed = False
        else:
            self.x_has_changed = False

    def no_changes(self):
        return hasattr(self, 'x_has_changed') and not self.x_has_changed \
               and hasattr(self, 'y_has_changed') and not self.y_has_changed

    def has_changed(self, is_col: bool):
        if is_col:
            self.y_has_changed = True
        else:
            self.x_has_changed = True


class Possibilities:
    size: int
    constraint: Constraint
    possibility: List[List[State]]

    def __init__(self, size: int, constraint: Constraint):
        self.constraint = constraint
        self.size = size

        if min_space(self.constraint.list) > self.size:
            raise Exception('Not feasible !')
        self.possibility = get_possibilities(constraint.list, size)


def min_space(constraint: List[int]) -> int:
    return sum(constraint) + len(constraint) - 1


def get_possibilities(constraint: List[int], size: int) -> List[List[State]]:
    if len(constraint) == 0:
        return [[State.EMPTY] * size]
    remaining = size - min_space(constraint)
    res = []
    base_c = [State.FILLED] * constraint[0] if len(constraint) == 1 else [State.FILLED] * constraint[0] + [State.EMPTY]
    for i in range(remaining + 1):
        base = [State.EMPTY] * i + base_c
        rest = get_possibilities(constraint[1:], size - len(base))
        for r in rest:
            res.append(base + r)
    return res


def parse_str(line: str) -> Constraint:
    res = Constraint()
    res.list = [int(s) for s in line.split()]
    return res


class Matrix:
    col_constraints: List[Constraint]
    line_constraints: List[Constraint]

    line_possibilities: List[Possibilities]
    col_possibilities: List[Possibilities]

    matrix_line: List[List[Cell]]  # Cell[i,j]
    matrix_col: List[List[Cell]]  # Cell[j,i]
    has_changed: HasChanged

    def __init__(self):
        self.col_constraints = []
        self.line_constraints = []
        self.line_possibilities = []
        self.col_possibilities = []
        self.has_changed = HasChanged()

    def init(self):
        for line in self.line_constraints:
            self.line_possibilities.append(Possibilities(len(self.col_constraints), line))
        for col in self.col_constraints:
            self.col_possibilities.append(Possibilities(len(self.col_constraints), col))

        self.matrix_line = [[Cell() for _ in range(len(self.col_constraints))] for _ in range(len(self.line_constraints))]
        self.matrix_col = [[Cell() for _ in range(len(self.line_constraints))] for _ in range(len(self.col_constraints))]
        for i, line in enumerate(self.matrix_line):
            for j, cell in enumerate(line):
                self.matrix_col[j][i] = cell

    def evaluate(self, is_col: bool):
        list_possibilities = self.col_possibilities if is_col else self.line_possibilities
        matrix = self.matrix_col if is_col else self.matrix_line
        self.has_changed.reset(is_col)

        for possibilities, list_cells in zip(list_possibilities, matrix):
            for cell in list_cells:
                cell.reset(is_col)
            new_list_possibility = []
            for possibility in possibilities.possibility:
                possibility_ok = True
                for state, cell in zip(possibility, list_cells):
                    is_ok = cell.add_state(state, is_col)
                    if not is_ok:
                        self.has_changed.has_changed(is_col)
                        possibility_ok = False
                        break
                if possibility_ok:
                    new_list_possibility.append(possibility)

            if len(new_list_possibility) != len(possibilities.possibility):
                possibilities.possibility = new_list_possibility

            for cell in list_cells:
                has_changed = cell.compute_state(is_col)
                if has_changed:
                    self.has_changed.has_changed(is_col)

    def compute(self):
        while not self.has_changed.no_changes():
            self.evaluate(False)
            self.evaluate(True)
        self.draw()

    def draw(self):
        for line in self.matrix_line:
            print("".join([cell.__str__() for cell in line]))
