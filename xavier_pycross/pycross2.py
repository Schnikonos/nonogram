import time
from enum import Enum
from itertools import product
from typing import List, Callable

from xavier_pycross.parser import parse


class State(Enum):
    NA = 0
    EMPTY = 1
    FILLED = 2


class Cell:
    state: State

    def __init__(self, state: State = State.NA):
        self.state = state

    def __str__(self):
        if self.state == State.NA:
            return '?'
        return 'X' if self.state == State.FILLED else ' '


def _get_line_combs(line_len: int, remaining_def: List[int], wrk_line=None, separator=None) -> List[List[Cell]]:
    if wrk_line is None:
        wrk_line = []
    if separator is None:
        separator = []

    remaining_len = line_len - len(wrk_line)
    if not remaining_def:
        return [(wrk_line + [Cell(State.EMPTY) for _ in range(remaining_len)])]

    block = remaining_def.pop(0)
    move_range = (remaining_len
                  - block
                  - len(separator)
                  - sum(remaining_def)
                  - len(remaining_def)
                  + 1)

    res = []
    for i in range(move_range):
        res += _get_line_combs(
            line_len,
            remaining_def,
            wrk_line + separator + [Cell(State.EMPTY) for _ in range(i)] + [Cell(State.FILLED) for _ in range(block)],
            [Cell(State.EMPTY)]
        )

    remaining_def.insert(0, block)
    return res


class Line:
    definition: List[int]
    combinations: List[List[Cell]]

    def __init__(self, line_len: int, definition: List[int]):
        self.definition = definition
        self.combinations = _get_line_combs(line_len, self.definition)


class Lines:
    length: int
    defs: List[Line]

    def __init__(self, length: int, lines_def: List[List[int]]):
        self.length = length
        self.defs = [Line(length, l) for l in lines_def]

    def filter(self, matrix: List[List[Cell]], get_line: Callable[[int, List[List[Cell]]], List[Cell]]) -> bool:
        old_combs = 0
        new_combs = 0

        def check_line(current_line: List[Cell], pattern: List[Cell]):
            return all(map(lambda c, p: p.state == State.NA or p.state == c.state, current_line, pattern))

        for i, row_comb in enumerate(self.defs):
            old_combs += len(row_comb.combinations)
            row_comb.combinations = [row for row in row_comb.combinations if check_line(row, get_line(i, matrix))]
            new_combs += len(row_comb.combinations)
        return old_combs != new_combs


def _get_global_state(index: int, combinations: List[List[Cell]]) -> State:
    c = combinations[0][index]
    if all(map(lambda x: x[index].state == c.state, combinations)):
        return c.state
    return State.NA


class Picross:
    rows: Lines
    cols: Lines
    matrix: List[List[Cell]]

    def __init__(self, row_def: List[List[int]], col_def: List[List[int]]):
        self.rows = Lines(len(col_def), row_def)
        self.cols = Lines(len(row_def), col_def)
        self.matrix = [[Cell() for _ in range(len(col_def))] for _ in range(len(row_def))]

    def resolve(self):
        rows_change, cols_change = True, True
        while rows_change or cols_change:
            for i, j in product(range(self.rows.length), range(self.cols.length)):
                if self.matrix[i][j].state == State.NA:
                    self.matrix[i][j].state = _get_global_state(j, self.rows.defs[i].combinations)

                if self.matrix[i][j].state == State.NA:
                    self.matrix[i][j].state = _get_global_state(i, self.cols.defs[j].combinations)

            rows_change = self.rows.filter(self.matrix, lambda i, matrix: matrix[i])
            cols_change = self.cols.filter(self.matrix, lambda i, matrix: [r[i] for r in matrix])


if __name__ == "__main__":
    start_time = time.perf_counter()
    (line, cols) = parse('../testFiles/test4.txt')
    pic = Picross(line, cols)
    # pic = Picross([[1,1],[2,1],[2],[3],[3]],[[4],[4],[2],[1],[2]])
    #    pic = Picross([[2,1],[1,3],[3],[4],[1,2],[1,5],[2,7],[2,5],[1,4],[2,4]],
    #                 [[1,5],[3,2,1],[2,1],[6],[2,1,5],[1,1,5],[5],[4],[1,2],[1,1]])
    #    pic = Picross([[2,6],[5],[4],[1,3,2],[3,3,2],[4,2],[3,1,3],[4,1,6],[10,1],[1,6,1],[1,4,1],[1,4,2],[1,4],[8,2],[11]],
    #                 [[1,9],[1,5,1],[7,2],[1,1,3,2],[2,7],[2,7],[3,7],[4,8],[5,1,2],[3,3,1],[1,1,1],[3,1,2],[2,2,2],[5],[5]])
    #    pic = Picross([[8,4],[2,5,3],[1,2,4],[3,4,1,1],[4,2,5],[4,3,2,2],[8,2],[6,1,1,3],[6,1,3],[6,8,1],[7,1,4],[4,3,1],[5,1],[5],[3,5],[6,3],[1,2,8,3],[13],[1,9],[9]],
    #                 [[5,4,1,1],[2,8,1],[1,8,1],[2,7],[3,12],[3,11],[2,2,6],[2,3,9],[3,1,6],[5,3,4],[4,1,2],[5,4,4],[1,1,3,4,5],[8,5],[1,2,5],[1,3],[4],[1,1,4],[1,1,1,4],[1,1,1,2,3]])
    # pic = Picross(
    #     [[4, 5, 1, 5], [4, 5, 5], [3, 2, 5, 2, 1], [3, 4, 3], [3, 3, 5, 3], [3, 1, 3, 3, 3], [9, 1, 1, 1, 2], [1, 4, 1],
    #      [4, 3], [3, 3], [1, 7, 3], [1, 10, 3], [1, 11, 3], [1, 1, 5, 3], [1, 1, 1, 1, 2], [3, 2, 7, 1, 2], [2, 1, 8],
    #      [3, 4, 1, 4, 3], [3, 6, 2, 1], [1, 3, 2, 4], [4, 5, 6], [6, 3, 8], [8, 2, 6], [6, 2, 3, 7], [4, 1, 1, 5, 5]],
    #     [[5, 4, 4], [5, 5, 4], [7, 6, 2, 5], [2, 3, 5], [3, 4], [1, 1, 1, 5], [1, 3, 7, 1], [3, 3, 3, 1, 1, 5],
    #      [2, 4, 3, 5, 1], [3, 8, 4], [3, 9, 4, 1], [5, 4, 1, 1, 1], [5, 4, 3, 3], [4, 4, 4, 3], [4, 3, 3, 2], [1, 3, 3],
    #      [5], [1, 2, 1], [1, 5, 3], [1, 9], [3, 1, 5], [2, 3, 2, 6], [2, 3, 6, 6], [2, 4, 8, 6], [2, 5, 5, 4, 2]])
    #     pic = Picross(
    #         [[1, 3], [1, 2, 2], [3, 3], [5, 1], [5, 2, 6], [11, 2, 4], [10, 7], [9, 3], [9, 2], [9, 1], [8, 2], [8, 3, 1],
    #          [9, 4, 1], [9, 5, 2], [8, 2, 2, 1], [8, 4, 1], [8, 1], [8, 1], [8, 1, 2], [9, 1, 2, 3], [9, 1, 2, 3],
    #          [9, 1, 2, 3], [11, 1, 2, 2, 3], [12, 3, 2], [1, 6, 1, 2, 3], [1, 2, 4, 6], [1, 2, 2, 5, 2], [1, 9], [2, 8, 1],
    #          [1, 10], [3, 8, 1], [4, 9], [4, 5, 1], [5, 1, 4, 3], [8, 3, 5], [10, 1, 8], [11, 14], [12, 2, 15], [13, 16, 1],
    #          [16, 12, 1, 2], [16, 11, 4], [14, 3, 14], [15, 2, 13], [13, 4, 12], [13, 16], [17], [15]],
    #         [[5], [10], [2, 16], [10, 16], [12, 16], [16, 13], [18, 14], [20, 13], [23, 12], [1, 23, 12], [24, 11],
    #          [2, 22, 10], [1, 2, 9, 3, 9], [3, 6, 4, 2, 9], [7, 1, 2, 8], [2, 2, 3, 2, 4, 3], [1, 5, 4, 1, 3, 2, 2],
    #          [2, 3, 1, 1, 2, 2, 4], [1, 5, 1, 3, 6], [1, 4, 3, 8], [1, 2, 2, 3, 5, 1], [1, 4, 18], [2, 2, 9, 9], [2, 10, 9],
    #          [1, 9, 10], [2, 9, 11], [2, 8, 12], [3, 3, 5, 12], [4, 2, 3, 1, 14], [5, 2, 6, 11], [4, 5, 4, 4], [9, 10],
    #          [2, 2, 5], [7], [1, 3]])
    pic.resolve()
    print('durée:', time.perf_counter() - start_time)
    for line in pic.matrix:
        print(''.join(map(str, line)))
