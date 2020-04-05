
class A:
    def __init__(self, key):
        self.key = key


if __name__ == '__main__':
    a = [[1] * 5 for _ in range(3)]
    print(a)
    a[2][0] = 10
    print(a)