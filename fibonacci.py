import time
from functools import cache

es = time.time()


@cache
def fibonacci_of(n):
    if n in {0, 1}:
        return n
    return fibonacci_of(n - 1) + fibonacci_of(n - 2)


def fib_sum():
    fib_list = [0]
    f = 1
    while f:
        numb = fibonacci_of(f)
        if numb > 7000000:
            break
        fib_list.append(numb)
        f += 1
    sum = 0
    for _, i in enumerate(fib_list):
        if i % 2 == 0:
            sum += i
    return sum


fib_sum()

et = time.time()

passed = et - es
print(passed, 'seconds')
