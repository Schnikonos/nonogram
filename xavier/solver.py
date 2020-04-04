import time
from typing import List

from xavier import parser
from xavier.matrix import State


def format_res(input: List[List[bool]]):
    for line in input:
        el = ['X' if c == State.FILLED else ' ' for c in line]
        print(''.join(el))


if __name__ == '__main__':
    filename = '../testFiles/test.txt'
    start_time = time.time()
    matrix = parser.parser(filename)
    elapsed_time1 = time.time() - start_time
    print('Ellapse1:', elapsed_time1)
    res = matrix.compute()
    elapsed_time2 = time.time() - start_time
    print('Ellapse2:', elapsed_time2)
    format_res(res)