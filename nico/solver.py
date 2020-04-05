import time
from typing import List

from nico import parser


# Here list of possibilities will tell the probability a cell is matched / not matched
# If proba is absolute for column -> remove lines possibilities that do not match (+ reset proba for next turn)
# Same if proba is absolute for line -> remove column possibilities that do not match
# If no new cell has been resolved after 2 loops,
from nico.matrix import compute

if __name__ == '__main__':
    filename = '../testFiles/test2.txt'
    start_time = time.time()
    matrix = parser.parser(filename)
    elapsed_time1 = time.time() - start_time
    print('Ellapse1:', elapsed_time1)
    res = compute(matrix)
    elapsed_time2 = time.time() - start_time
    print('Ellapse2:', elapsed_time2)