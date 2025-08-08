import logging
from Service.mathematical_operations_functions import fib, factorial
from Model.exceptions import MissingOperandError, NegativeNumberError
from Model.exceptions import ZeroToThePowerOfZeroError

"""
This service layer of the arhitecture is responsible with logging
and dealing with validation problems,
before calling the actual mathematical functions
"""


logger = logging.getLogger(__name__)


def perform_power(operand_1: float, operand_2: float | None = None) -> float:
    """
    :param operand_1: base in the power mathematical operation
    :param operand_2: exponent in the power mathematical operation
    :return: base to the power of exponent
    """
    if operand_2 is None:
        raise MissingOperandError("Missing operand2 for power operation")
    if operand_1 == 0 and operand_2 == 0:
        raise ZeroToThePowerOfZeroError("0**0 -> incorrect operation")
    return operand_1 ** operand_2


def perform_fibonacci(operand: int) -> int:
    """
    :param operand: position in the fibonacci sequence
    :return: number at the operand position in the fibonacci sequence
    """
    if operand < 0:
        raise NegativeNumberError("Fibonacci not defined for negative numbers")
    return fib(operand)


def perform_factorial(operand: int) -> int:
    """
    :param operand: number to compute the factorial for
    :return: the factorial of the operand
    """
    if operand < 0:
        raise NegativeNumberError("Factorial not defined for negative numbers")
    return factorial(operand)
