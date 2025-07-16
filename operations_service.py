# operations_service.py

import logging
from mathematical_operations_functions_service import fib, factorial
from exceptions import MissingOperandError, NegativeNumberError, ZeroToThePowerOfZeroError

"""
This service layer of the arhitecture is responsible with logging and dealing with validation problems,
before calling the actual mathematical functions
"""


logger = logging.getLogger(__name__)



def perform_power(operand1: float, operand2: float | None) -> float:
    if operand2 is None:
        raise MissingOperandError("Missing operand2 for power operation")
    if operand1 == 0 and operand2 == 0:
        raise ZeroToThePowerOfZeroError("0**0 is considered an incorrect operation")
    return operand1 ** operand2


def perform_fibonacci(operand: int) -> int:
    if operand < 0:
        raise NegativeNumberError("Fibonacci not defined for negative numbers")
    return fib(operand)


def perform_factorial(operand: int) -> int:
    if operand < 0:
        raise NegativeNumberError("Factorial not defined for negative numbers")
    return factorial(operand)
