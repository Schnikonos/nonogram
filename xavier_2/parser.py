from typing import Dict, Tuple, List

from xavier_2.matrix import Matrix, parse_str


def parser(filename: str) -> Matrix:
    res = Matrix()
    with open(filename) as fp:
        lines = fp.readlines()

        constraint = res.col_constraints
        for line in lines:
            if line.startswith('#'):
                constraint = res.line_constraints
                continue
            constraint.append(parse_str(line))

    res.init()
    return res
