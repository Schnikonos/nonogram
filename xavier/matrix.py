from typing import List, Tuple

class Constraint:
    list: List[int]

    def __init__(self):
        self.list = []


class Line:
    line: List[bool]

    def __init__(self, size=0):
        self.line = [False] * size


class Possibilities:
    size: int
    constraint: Constraint
    possibility: List[List[bool]]

    def __init__(self, size: int, constraint: Constraint):
        self.constraint = constraint
        self.size = size

        if min_space(self.constraint.list) > self.size:
            raise Exception('Not feasible !')
        self.possibility = get_possibilities(constraint.list, size)


def min_space(constraint: List[int]) -> int:
    return sum(constraint) + len(constraint) - 1


def get_possibilities(constraint: List[int], size: int) -> List[List[bool]]:
    if len(constraint) == 0:
        return [[False] * size]
    remaining = size - min_space(constraint)
    res = []
    base_c = [True] * constraint[0] if len(constraint) == 1 else [True] * constraint[0] + [False]
    for i in range(remaining + 1):
        base = [False] * i + base_c
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

    possibilities: List[Possibilities]

    def __init__(self):
        self.col_constraints = []
        self.line_constraints = []
        self.possibilities = []

    def init(self):
        for line in self.line_constraints:
            self.possibilities.append(Possibilities(len(self.col_constraints), line))

    def check_cols(self, p_indexes: List[int]) -> bool:
        current_possibility = [self.possibilities[i].possibility[index] for (i, index) in enumerate(p_indexes)]

        columns = [[] for x in range(len(self.col_constraints))]
        for l in current_possibility:
            for j, c in enumerate(columns):
                c.append(l[j])

        for (constraint, col) in zip(self.col_constraints, columns):
            cnt_list, used = count(col, len(self.line_constraints) == len(p_indexes))
            for (cst, cnt) in zip(constraint.list, cnt_list):
                if cst != cnt:
                    return False
            cnt_rest = min_space(constraint.list[len(cnt_list):])
            if len(self.line_constraints) - used < cnt_rest:
                return False
        return True

    def evaluate(self, p_indexes: List[int]) -> Tuple[bool, List[int]]:
        # print(p_indexes)
        if not self.check_cols(p_indexes):
            return False, []

        if len(p_indexes) == len(self.line_constraints):
            return True, p_indexes

        for i in range(len(self.possibilities[len(p_indexes)].possibility)):
            ok, res = self.evaluate(p_indexes + [i])
            if ok:
                return True, res
        return False, []

    def compute(self) -> List[List[bool]]:
        ok, p_indexes = self.evaluate([])
        res = []
        for i, index in enumerate(p_indexes):
            res.append(self.possibilities[i].possibility[index])
        return res


def count(col: List[bool], is_final: bool) -> Tuple[List[int], int]:
    res = []
    index = 0
    current = 0
    for c in col:
        if c:
            current += 1
        elif current > 0:
            res.append(current)
            index += current + 1
            current = 0
        else:
            index += 1

    if is_final and current > 0:
        res.append(current)
        index += current
    return res, index

