from typing import List, Tuple


def parse(filename: str) -> Tuple[List[List[int]], List[List[int]]]:
    res_l = []
    res_c = []
    current = res_l
    with open(filename) as fp:
        lines = fp.readlines()
        for line in lines:
            if line.startswith('#'):
                current = res_c
                continue
            current.append([int(i) for i in line.split(' ')])
    return res_l, res_c

