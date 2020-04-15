import time
from typing import List


class Picross:

    def __init__(self, row_def, col_def):
        self.row_def = row_def
        self.col_def = col_def
        self.row_len = len(col_def)  # length of a line = number of columns
        self.col_len = len(row_def)  # length of a column = number of lines
        self.matrix = []
        self.row_comb = []
        self.col_comb = []

    def resolve(self):
        def get_line_combs(line_len: int, line_def: List[int]) -> List[int]:
            result_list = []

            def combine(remaining_len: int, remaining_def: List[int], wrk_line: List[int]):
                if not remaining_def:
                    result_list.append((wrk_line + [0] * remaining_len)[:line_len])
                    return

                block = remaining_def.pop(0)
                move_range = (remaining_len
                              - block
                              - sum(remaining_def)
                              - len(remaining_def)
                              + 1)

                remain_len = remaining_len - block - 1
                for i in range(move_range):
                    combine(remain_len - i, remaining_def, wrk_line + [0] * i + [1] * block + [0])

                remaining_def.insert(0, block)
                return

            combine(line_len, line_def, [])
            return result_list

        def reduce():
            for i, comb_list in enumerate(self.row_comb):
                for j in range(self.row_len):
                    if self.matrix[i][j] == '?':
                        x = sum([row[j] for row in comb_list])
                        if x == 0:
                            self.matrix[i][j] = 0
                        elif x == len(comb_list):
                            self.matrix[i][j] = 1
            for i, comb_list in enumerate(self.col_comb):
                for j in range(self.col_len):
                    if self.matrix[j][i] == '?':
                        x = sum([col[j] for col in comb_list])
                        if x == 0:
                            self.matrix[j][i] = 0
                        elif x == len(comb_list):
                            self.matrix[j][i] = 1
            old_combs = 0
            new_combs = 0
            for i, row_comb in enumerate(self.row_comb):
                old_combs += len(row_comb)
                self.row_comb[i] = [row for row in row_comb if check_line(row, self.matrix[i])]
                new_combs += len(self.row_comb[i])
            for i, col_comb in enumerate(self.col_comb):
                old_combs += len(col_comb)
                self.col_comb[i] = [col for col in col_comb if check_line(col, [r[i] for r in self.matrix])]
                new_combs += len(self.col_comb[i])
            return new_combs < old_combs

        init_row = ['?'] * self.row_len
        self.matrix = [init_row.copy() for i in range(self.col_len)]
        self.row_comb = [get_line_combs(self.row_len, r) for r in self.row_def]
        self.col_comb = [get_line_combs(self.col_len, c) for c in self.col_def]
        while reduce():
            pass
        return


def check_line(line, pattern):
    for el_l, el_p in zip(line, pattern):
        if el_p != '?' and el_l != el_p:
            return False
    return True


if __name__ == "__main__":
    start_time = time.perf_counter()
#    pic = Picross([[1,1],[2,1],[2],[3],[3]],[[4],[4],[2],[1],[2]])
#    pic = Picross([[2,1],[1,3],[3],[4],[1,2],[1,5],[2,7],[2,5],[1,4],[2,4]],
#                 [[1,5],[3,2,1],[2,1],[6],[2,1,5],[1,1,5],[5],[4],[1,2],[1,1]])
#    pic = Picross([[2,6],[5],[4],[1,3,2],[3,3,2],[4,2],[3,1,3],[4,1,6],[10,1],[1,6,1],[1,4,1],[1,4,2],[1,4],[8,2],[11]],
#                 [[1,9],[1,5,1],[7,2],[1,1,3,2],[2,7],[2,7],[3,7],[4,8],[5,1,2],[3,3,1],[1,1,1],[3,1,2],[2,2,2],[5],[5]])
#    pic = Picross([[8,4],[2,5,3],[1,2,4],[3,4,1,1],[4,2,5],[4,3,2,2],[8,2],[6,1,1,3],[6,1,3],[6,8,1],[7,1,4],[4,3,1],[5,1],[5],[3,5],[6,3],[1,2,8,3],[13],[1,9],[9]],
#                 [[5,4,1,1],[2,8,1],[1,8,1],[2,7],[3,12],[3,11],[2,2,6],[2,3,9],[3,1,6],[5,3,4],[4,1,2],[5,4,4],[1,1,3,4,5],[8,5],[1,2,5],[1,3],[4],[1,1,4],[1,1,1,4],[1,1,1,2,3]])
    pic = Picross([[4,5,1,5],[4,5,5],[3,2,5,2,1],[3,4,3],[3,3,5,3],[3,1,3,3,3],[9,1,1,1,2],[1,4,1],[4,3],[3,3],[1,7,3],[1,10,3],[1,11,3],[1,1,5,3],[1,1,1,1,2],[3,2,7,1,2],[2,1,8],[3,4,1,4,3],[3,6,2,1],[1,3,2,4],[4,5,6],[6,3,8],[8,2,6],[6,2,3,7],[4,1,1,5,5]],
                [[5,4,4],[5,5,4],[7,6,2,5],[2,3,5],[3,4],[1,1,1,5],[1,3,7,1],[3,3,3,1,1,5],[2,4,3,5,1],[3,8,4],[3,9,4,1],[5,4,1,1,1],[5,4,3,3],[4,4,4,3],[4,3,3,2],[1,3,3],[5],[1,2,1],[1,5,3],[1,9],[3,1,5],[2,3,2,6],[2,3,6,6],[2,4,8,6],[2,5,5,4,2]])
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
    for i, line in enumerate(pic.matrix):
        print('%02d:%s' % (i + 1, line))
    for line in pic.matrix:
        print(''.join(map(lambda x: ' ' if x == 0 else '*', line)))
