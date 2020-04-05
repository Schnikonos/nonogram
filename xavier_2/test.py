from copy import deepcopy
from typing import List

class A:
    a: List[int]

    def __init__(self, a):
        self.a = a

    def __str__(self):
        return ",".join([str(i) for i in self.a])


class B:
    b: List[A]
    b2: List[A]

    def __init__(self, b):
        self.b = b
        self.b2 = b

    def __str__(self):
        return "B:" + "\n".join([str(i) for i in self.b]) + "\nB2:" + "\n".join([str(i) for i in self.b2])


if __name__ == '__main__':
    o = B([A([1, 1, 1]), A([2, 2, 2]), A([3, 3, 3])])
    o2 = deepcopy(o)
    o.b2[1].a[1] = 10
    print(o)
    print(o2)
    o2.b2[1].a[1] = 20
    print(o)
    print(o2)
