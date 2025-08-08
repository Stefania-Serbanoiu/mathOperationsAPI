class OperationError(Exception):
    """Base class for all operation-related exceptions"""
    pass


class MissingOperandError(OperationError):
    """Exception for missing mathematical operand in a mathematical function"""
    pass


class NegativeNumberError(OperationError):
    """Exception for negative number
    (in mathematical operations where a negative number is not valid)"""
    pass


class UnsupportedOperationError(OperationError):
    """Exception for mathematical operation
    which is not supported by application logic or defined
    inside the app"""
    pass


class ZeroToThePowerOfZeroError(OperationError):
    """Exception for mathematical operation 0**0 ,
     which is not defined and computed by complex processes"""
    pass
