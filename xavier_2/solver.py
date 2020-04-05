import time
from typing import List

from xavier_2 import parser
from xavier_2.matrix import State


def format_res(input: List[List[bool]]):
    for line in input:
        el = ['X' if c == State.FILLED else ' ' for c in line]
        print(''.join(el))


# Algo is the same as Xavier_1 except:
#  - lines are sorted from least to most permutations to lower the nb of searches done
#  - column comparison is done by checking the proposition against the list of possible columns
#     -> this makes it more readable but way slower than xavier_1
#              -> 8s for 15x15 (vs 0.76s for Xavier_1 and 0.1s for nico)
#              -> 898s for 25x25 (vs 103s for Xavier_1 and 5s for nico)

if __name__ == '__main__':
    filename = '../testFiles/test2.txt'
    start_time = time.time()
    matrix = parser.parser(filename)
    elapsed_time1 = time.time() - start_time
    print('Ellapse1:', elapsed_time1)
    res = matrix.compute()
    elapsed_time2 = time.time() - start_time
    print('Ellapse2:', elapsed_time2)
    format_res(res)