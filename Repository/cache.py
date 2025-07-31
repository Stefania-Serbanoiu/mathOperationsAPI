# Repository/cache.py


from Entities.models import OperationResult, CachedOperation
from datetime import datetime


cache: dict[str, CachedOperation] = {}


def generate_key(operation: str, operand1: int, operand2: int | None) -> str:
    return f"{operation}:{operand1}:{operand2 if operand2 is not None else ''}"


def get_cached_result(key: str) -> OperationResult | None:
    entry = cache.get(key)
    return entry.value if entry else None


def set_cache(key: str, value: OperationResult):
    cache[key] = CachedOperation(key=key, value=value,
                                 cached_at_datetime=datetime.utcnow())
