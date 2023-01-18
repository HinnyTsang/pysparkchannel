"""Utils

Important functions for the case
"""
from functools import wraps
from typing import Callable

def chained(func: Callable) -> Callable:
    """Decorator for function to allow method chaining"""
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        return_value = func(self, *args, **kwargs)
        return self if return_value is None else return_value
    return wrapped

def fluent(cls: type) -> type:
    """Decorator for function to allow method chaining for all method"""
    for name, member in cls.__dict__.items():
        if name == "__init__":
            continue
        if callable(member):
            setattr(cls, name, chained(member))
    return cls


def encode_string(string: str) -> str:
    """
    Encode normal string to ord string
    """
    return ' '.join(str(c) for c in map(ord, string))

def encode_binary_string(binary: bytes) -> str:
    """
    Encode byte string to ord string
    """
    return ' '.join(map(str, binary))
