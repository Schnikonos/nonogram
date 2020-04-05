from enum import Enum
from typing import List, Tuple


class State(Enum):
    NA = 0
    FILLED = 1
    EMPTY = 2


class Constraint:
    list: List[int]

    def __init__(self):
        self.list = []


def count_state(states: List[State], state_type: State) -> int:
    return sum([1 if e == state_type else 0 for e in states])


class Possibilities:
    size: int
    constraint: Constraint
    possibility: List[List[State]]
    index: int
    value: int

    nb_blank: int
    nb_filled: int

    def __init__(self, size: int, constraint: Constraint, index: int):
        self.constraint = constraint
        self.size = size
        self.index = index

        if min_space(self.constraint.list) > self.size:
            raise Exception('Not feasible !')
        self.possibility = get_possibilities(constraint.list, size)

        self.value = len(self.possibility)  # used to define where to start -> the lower the value, the better
        self.nb_blank = count_state(self.possibility[0], State.EMPTY)
        self.nb_filled = count_state(self.possibility[0], State.FILLED)


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

    def __init__(self):
        self.col_constraints = []
        self.line_constraints = []
        self.line_possibilities = []
        self.col_possibilities = []
        self.sorted_line_possibilities = []
        self.sorted_column_possibilities = []

    def init(self):
        for (i, line) in enumerate(self.line_constraints):
            self.line_possibilities.append(Possibilities(len(self.col_constraints), line, i))
        for (j, col) in enumerate(self.col_constraints):
            self.col_possibilities.append(Possibilities(len(self.col_constraints), col, j))

        self.sorted_line_possibilities = sorted(self.line_possibilities, key=lambda x: x.value)
        self.sorted_column_possibilities = sorted(self.col_possibilities, key=lambda x: x.value)

    def check_cols(self, p_indexes: List[int]) -> bool:
        current_possibility = [[State.NA] * len(self.col_constraints) for _ in range(len(self.line_constraints))]
        for i, index in enumerate(p_indexes):
            current_possibility[self.sorted_line_possibilities[i].index] = self.sorted_line_possibilities[i].possibility[index]

        # rewrite line possibility as column
        columns: List[List[State]] = [[State.NA] * len(self.line_constraints) for _ in range(len(self.col_constraints))]
        for i, l in enumerate(current_possibility):
            for j, c in enumerate(columns):
                c[i] = l[j]

        # first level check -> verify that possibility doesn't go over limits
        for suggestion, constraint in zip(columns, self.col_possibilities):
            if count_state(suggestion, State.FILLED) > constraint.nb_filled \
               or count_state(suggestion, State.EMPTY) > constraint.nb_blank:
                return False

        # check if there is a match among the column possibilities
        for column in self.sorted_column_possibilities:
            column_possible = False
            for c_p in column.possibility:
                if self.is_match(c_p, columns[column.index], p_indexes):
                    column_possible = True
                    break
            if not column_possible:
                return False
        return True

    def evaluate(self, p_indexes: List[int]) -> Tuple[bool, List[int]]:
        if not self.check_cols(p_indexes):
            return False, []

        if len(p_indexes) == len(self.line_constraints):
            return True, p_indexes

        for i in range(len(self.sorted_line_possibilities[len(p_indexes)].possibility)):
            ok, res = self.evaluate(p_indexes + [i])
            if ok:
                return True, res
        return False, []

    def compute(self) -> List[List[State]]:
        ok, p_indexes = self.evaluate([])
        res = [[]] * len(self.line_constraints)
        for i, index in enumerate(p_indexes):
            res[self.sorted_line_possibilities[i].index] = self.sorted_line_possibilities[i].possibility[index]
        return res

    def is_match(self, a: List[State], b: List[State], p_indexes: List[int]) -> bool:
        for index in range(len(p_indexes)):
            i = self.sorted_line_possibilities[index].index
            if a[i] != b[i]:
                return False
        return True
