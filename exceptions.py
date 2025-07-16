# exceptions.py

class OperationError(Exception):
    """Base class for all operation-related exceptions"""
    pass


class MissingOperandError(OperationError):
    pass


class NegativeNumberError(OperationError):
    pass


class UnsupportedOperationError(OperationError):
    pass

class ZeroToThePowerOfZeroError(OperationError):
    pass