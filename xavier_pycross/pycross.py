import time
from typing import List, Union, Callable


class Picross:
    row_def: List[List[int]]
    col_def: List[List[int]]
    row_len: int
    col_len: int
    matrix: List[List[Union[int, str]]]
    row_comb: List[List[List[int]]]
    col_comb: List[List[List[int]]]

    def __init__(self, row_def: List[List[int]], col_def: List[List[int]]):
        self.row_def = row_def
        self.col_def = col_def
        self.row_len = len(col_def)  # length of a line = number of columns
        self.col_len = len(row_def)  # length of a column = number of lines
        self.matrix = []
        self.row_comb = []
        self.col_comb = []

    def resolve(self):
        def _get_line_combs(line_len: int, line_def: List[int]) -> List[List[int]]:
            result_list = []

            def _combine(remaining_def: List[int], wrk_line: List[Union[int, str]], separator: List[Union[int, str]]):
                remaining_len = line_len - len(wrk_line)
                if not remaining_def:
                    result_list.append((wrk_line + [0] * remaining_len))
                    return

                block = remaining_def.pop(0)
                move_range = (remaining_len
                              - block
                              - len(separator)
                              - sum(remaining_def)
                              - len(remaining_def)
                              + 1)

                for i in range(move_range):
                    _combine(remaining_def,
                             wrk_line + separator + [0] * i + [1] * block,
                             [0])

                remaining_def.insert(0, block)
                return

            _combine(line_def, [], [])
            return result_list

        def _filter_comb(lines_combinations: List[List[List[int]]],
                         matrix: List[List[Union[int, str]]],
                         get_line: Callable[[int, List[List[Union[int, str]]]], List[Union[int, str]]]) -> bool:
            old_combs = 0
            new_combs = 0

            def check_line(current_line: List[int], pattern: List[int]):
                return all(map(lambda c, p: p == '?' or p == c, current_line, pattern))

            for i, line_comb in enumerate(lines_combinations):
                old_combs += len(line_comb)
                lines_combinations[i] = [row for row in line_comb if check_line(row, get_line(i, matrix))]
                new_combs += len(lines_combinations[i])
            return old_combs != new_combs

        def _get_global_state(index: int, combinations: List[List[Union[int, str]]]) -> Union[int, str]:
            c = combinations[0][index]
            if all(map(lambda x: x[index] == c, combinations)):
                return c
            return '?'

        def _reduce():
            for i in range(self.row_len):
                for j in range(self.col_len):
                    if self.matrix[i][j] == '?':
                        self.matrix[i][j] = _get_global_state(j, self.row_comb[i])

                    if self.matrix[i][j] == '?':
                        self.matrix[i][j] = _get_global_state(i, self.col_comb[j])

            rows_change = _filter_comb(self.row_comb, self.matrix, lambda i, matrix: matrix[i])
            cols_change = _filter_comb(self.col_comb, self.matrix, lambda i, matrix: [r[i] for r in matrix])
            return rows_change or cols_change

        init_row = ['?'] * self.row_len
        self.matrix = [init_row.copy() for i in range(self.col_len)]
        self.row_comb = [_get_line_combs(self.row_len, r) for r in self.row_def]
        self.col_comb = [_get_line_combs(self.col_len, c) for c in self.col_def]

        while _reduce():
            pass
        return


if __name__ == "__main__":
    start_time = time.perf_counter()
    # pic = Picross([[1,1],[2,1],[2],[3],[3]],[[4],[4],[2],[1],[2]])
    #    pic = Picross([[2,1],[1,3],[3],[4],[1,2],[1,5],[2,7],[2,5],[1,4],[2,4]],
    #                 [[1,5],[3,2,1],[2,1],[6],[2,1,5],[1,1,5],[5],[4],[1,2],[1,1]])
    #    pic = Picross([[2,6],[5],[4],[1,3,2],[3,3,2],[4,2],[3,1,3],[4,1,6],[10,1],[1,6,1],[1,4,1],[1,4,2],[1,4],[8,2],[11]],
    #                 [[1,9],[1,5,1],[7,2],[1,1,3,2],[2,7],[2,7],[3,7],[4,8],[5,1,2],[3,3,1],[1,1,1],[3,1,2],[2,2,2],[5],[5]])
    #    pic = Picross([[8,4],[2,5,3],[1,2,4],[3,4,1,1],[4,2,5],[4,3,2,2],[8,2],[6,1,1,3],[6,1,3],[6,8,1],[7,1,4],[4,3,1],[5,1],[5],[3,5],[6,3],[1,2,8,3],[13],[1,9],[9]],
    #                 [[5,4,1,1],[2,8,1],[1,8,1],[2,7],[3,12],[3,11],[2,2,6],[2,3,9],[3,1,6],[5,3,4],[4,1,2],[5,4,4],[1,1,3,4,5],[8,5],[1,2,5],[1,3],[4],[1,1,4],[1,1,1,4],[1,1,1,2,3]])
    pic = Picross(
        [[4, 5, 1, 5], [4, 5, 5], [3, 2, 5, 2, 1], [3, 4, 3], [3, 3, 5, 3], [3, 1, 3, 3, 3], [9, 1, 1, 1, 2], [1, 4, 1],
         [4, 3], [3, 3], [1, 7, 3], [1, 10, 3], [1, 11, 3], [1, 1, 5, 3], [1, 1, 1, 1, 2], [3, 2, 7, 1, 2], [2, 1, 8],
         [3, 4, 1, 4, 3], [3, 6, 2, 1], [1, 3, 2, 4], [4, 5, 6], [6, 3, 8], [8, 2, 6], [6, 2, 3, 7], [4, 1, 1, 5, 5]],
        [[5, 4, 4], [5, 5, 4], [7, 6, 2, 5], [2, 3, 5], [3, 4], [1, 1, 1, 5], [1, 3, 7, 1], [3, 3, 3, 1, 1, 5],
         [2, 4, 3, 5, 1], [3, 8, 4], [3, 9, 4, 1], [5, 4, 1, 1, 1], [5, 4, 3, 3], [4, 4, 4, 3], [4, 3, 3, 2], [1, 3, 3],
         [5], [1, 2, 1], [1, 5, 3], [1, 9], [3, 1, 5], [2, 3, 2, 6], [2, 3, 6, 6], [2, 4, 8, 6], [2, 5, 5, 4, 2]])
    # pic = Picross(
    #     [[1, 3], [1, 2, 2], [3, 3], [5, 1], [5, 2, 6], [11, 2, 4], [10, 7], [9, 3], [9, 2], [9, 1], [8, 2], [8, 3, 1],
    #      [9, 4, 1], [9, 5, 2], [8, 2, 2, 1], [8, 4, 1], [8, 1], [8, 1], [8, 1, 2], [9, 1, 2, 3], [9, 1, 2, 3],
    #      [9, 1, 2, 3], [11, 1, 2, 2, 3], [12, 3, 2], [1, 6, 1, 2, 3], [1, 2, 4, 6], [1, 2, 2, 5, 2], [1, 9], [2, 8, 1],
    #      [1, 10], [3, 8, 1], [4, 9], [4, 5, 1], [5, 1, 4, 3], [8, 3, 5], [10, 1, 8], [11, 14], [12, 2, 15], [13, 16, 1],
    #      [16, 12, 1, 2], [16, 11, 4], [14, 3, 14], [15, 2, 13], [13, 4, 12], [13, 16], [17], [15]],
    #     [[5], [10], [2, 16], [10, 16], [12, 16], [16, 13], [18, 14], [20, 13], [23, 12], [1, 23, 12], [24, 11],
    #      [2, 22, 10], [1, 2, 9, 3, 9], [3, 6, 4, 2, 9], [7, 1, 2, 8], [2, 2, 3, 2, 4, 3], [1, 5, 4, 1, 3, 2, 2],
    #      [2, 3, 1, 1, 2, 2, 4], [1, 5, 1, 3, 6], [1, 4, 3, 8], [1, 2, 2, 3, 5, 1], [1, 4, 18], [2, 2, 9, 9], [2, 10, 9],
    #      [1, 9, 10], [2, 9, 11], [2, 8, 12], [3, 3, 5, 12], [4, 2, 3, 1, 14], [5, 2, 6, 11], [4, 5, 4, 4], [9, 10],
    #      [2, 2, 5], [7], [1, 3]])
    pic.resolve()
    print('durée:', time.perf_counter() - start_time)
    for i, line in enumerate(pic.matrix):
        print('%02d:%s' % (i + 1, line))
    for line in pic.matrix:
        print(''.join(map(lambda x: ' ' if x == 0 else '*', line)))
