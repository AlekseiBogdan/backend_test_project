import time
from functools import cache

es = time.time()


@cache
def fibonacci_of(n: int):
    if n in [3, 4]:
        return n
    return fibonacci_of(n - 1) + fibonacci_of(n - 2)


def fib_sum():
    fib_list = [3, 4]
    f = 3
    while f:
        numb = fibonacci_of(f)
        if numb > 7000000:
            break
        if numb not in fib_list:
            fib_list.append(numb)
        f += 1
    even_fib_sum = sum(n for n in fib_list if not n % 2)
    print(even_fib_sum)
    return even_fib_sum


fib_sum()

et = time.time()

passed = et - es
print(passed, 'seconds')
