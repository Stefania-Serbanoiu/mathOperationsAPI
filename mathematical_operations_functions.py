# mathematical_operations_functions.py

def fib(n: int) -> int:
    a = b = c = 1
    ct = 2 # we consider just a=b=1 already known, and if n <= 2 the result (in c) would be 1

    while ct < n:
        c = a + b
        a = b
        b = c
        ct += 1

    return c


def factorial(n: int) -> int:
    result = 1
    length_range = n + 1
    for i in range(2, length_range):  # multiplying with numbers from 2 to n
        result *= i
    return result
