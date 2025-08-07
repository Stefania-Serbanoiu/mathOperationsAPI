def fib(n: int) -> int:
    """
    Compute the n-th number in the fibonacci sequence
    :param n:gives the position in the sequence(integer)
    :return:n-th fibonacci number (integer)
    """
    a = b = c = 1  # a,b,c -> numbers in the fibonacci sequence
    # we consider a=b=1, and if n <= 2 the result (in c) would be 1
    counter = 2

    # fib algorithm
    while counter < n:
        c = a + b
        a = b
        b = c
        counter += 1

    return c


def factorial(n: int) -> int:
    """
    Computes the factorial operation for a given number
    :param n: integer to compute factorial for
    :return: the factorial of parameter n (integer)
    """
    factorial_computation_result = 1
    length_range = n + 1
    for i in range(2, length_range):  # multiplying with numbers from 2 to n
        factorial_computation_result *= i
    return factorial_computation_result
