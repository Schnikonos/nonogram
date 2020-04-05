from typing import List


class A:
    a: List[int]

    def test(self):
        if hasattr(self, 'a') and len(self.a) == 0:
            print(1)
        else:
            print(0)

if __name__ == '__main__':
    o = A()
    o.a = []
    o.test()
