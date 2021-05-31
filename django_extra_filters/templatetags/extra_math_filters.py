import logging
from typing import Union, Callable, List, Optional
from decimal import Decimal
from django import template
import math
from functools import wraps

logger = logging.getLogger(__name__)
register = template.Library()


def _to_number(value: ...) -> Optional[Union[int, float, Decimal, List[int], List[float], List[Decimal]]]:
    print(type(value))
    if isinstance(value, (int, float, Decimal)) or value is None:
        return value
    if isinstance(value, list):
        return [_to_number(x) for x in value]
    try:
        return int(value)
    except ValueError:
        return float(value)


def numerify(func: Callable):
    def wrapper(*args):
        new_args = []
        try:
            new_args.append(_to_number(args[0]))
            new_args.append(_to_number(args[1]))
        except IndexError:
            pass
        return func(*new_args)

    return wrapper


def numerify(func):
    """
    Decorator for filters which should only receive strings. The object
    passed as the first positional argument will be converted to a string.
    """

    def _dec(*args, **kwargs):
        args = list(args)
        new_args = []
        try:
            new_args.append(_to_number(args[0]))
            new_args.append(_to_number(args[1]))
        except IndexError:
            pass
        return func(*new_args)

    _dec._decorated_function = getattr(func, '_decorated_function', func)

    return wraps(func)(_dec)


@register.filter
@numerify
def ceil(x):
    """Return the ceiling of x, the smallest integer greater than or equal to x"""
    return math.ceil(x)


@register.filter
@numerify
def copysign(x, y):
    """Return a float with the magnitude (absolute value) of x but the sign of y"""
    logger.info(x)
    logger.info(y)
    return math.copysign(x, y)


@register.filter
@numerify
def abs(x):
    """Return the absolute value of x"""
    return math.fabs(x)


@register.filter
@numerify
def factorial(x):
    """Return x factorial as an integer"""
    return math.factorial(x)


@register.filter
@numerify
def floor(x):
    """Return the floor of x, the largest integer less than or equal to x"""
    return math.floor(x)


@register.filter
@numerify
def fmod(x, y):
    """Return fmod(x, y), as defined by the platform C library. For Python expression x % y use mod."""
    return math.fmod(x, y)


@register.filter
@numerify
def mod(x, y):
    """Return fmod(x, y), as defined by the platform C library. For Python expression x % y use mod."""
    return x % y


@register.filter
@numerify
def fsum(x):
    """Return an accurate floating point sum of values in the iterable.
    Avoids loss of precision by tracking multiple intermediate partial sums"""
    return math.fsum(x)


@register.filter(name="sum")
@numerify
def sum_filter(x):
    """Return a sum of values in the iterable"""
    return sum(x)


@register.filter
@numerify
def gcd(x, y):
    """Return the greatest common divisor of the specified integer arguments."""
    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Greatest common divisor (GCD) can only be calculated on integers. "
                         f"Received [{type(x)}] {x} and [{type(y)}] {y}")
    return math.gcd(x, y)


@register.filter
@numerify
def isqrt(x):
    """Return the integer square root of the nonnegative integer x"""
    if not isinstance(x, int):
        raise ValueError(f"Expected integer. Received [{type(x)}] {x}.")
    if x < 0:
        raise ValueError(f"Expected non-negative integer. Received {x}.")
    return math.isqrt(x)


@register.filter
@numerify
def sqrt(x):
    """Return the square root of x"""
    if x < 0:
        raise ValueError(f"Expected non-negative number. Received {x}.")
    return math.sqrt(x)


@register.filter
@numerify
def lcm(x, y):
    """Return the greatest common divisor of the specified integer arguments."""
    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Least common multiple (LCM) can only be calculated on integers. "
                         f"Received [{type(x)}] {x} and [{type(y)}] {y}")
    return math.lcm(x, y)


@register.filter
@numerify
def ldexp(x, y):
    """Return x * (2**y)."""
    return math.ldexp(x, y)


@register.filter
@numerify
def perm(x, y=None):
    """Return the number of ways to choose k items from n items without repetition and with order."""
    if not isinstance(x, int) or (not isinstance(y, int) and y is not None):
        raise ValueError(f"Expected integers. Received [{type(x)}] {x} and [{type(y)}] {y}")
    return math.perm(x, y)


@register.filter
@numerify
def trunc(x):
    """Return the Real value x truncated to an Integral (usually an integer)."""
    return math.trunc(x)


@register.filter
@numerify
def exp(x):
    """Return e raised to the power x, where e = 2.718281… is the base of natural logarithms."""
    return math.exp(x)


@register.filter
@numerify
def expm1(x):
    """Return e raised to the power x, minus 1."""
    return math.expm1(x)


@register.filter
@numerify
def log(x, y=None):
    """Return the logarithm of x with base y (default to e)"""
    if x <= 0:
        raise ValueError(f"Expected non-negative value. Received {x}.")
    if y is not None and y <= 0:
        raise ValueError(f"Expected non-negative value. Received {y}.")
    return math.log(x, y if y else math.e)


@register.filter
@numerify
def log1p(x):
    """Return e raised to the power x, minus 1."""
    if x <= 0:
        raise ValueError(f"Expected non-negative value. Received {x}.")
    return math.log1p(x)


@register.filter
@numerify
def log2(x):
    """Return the base-2 logarithm of x."""
    if x <= 0:
        raise ValueError(f"Expected non-negative value. Received {x}.")
    return math.log2(x)


@register.filter
@numerify
def log10(x):
    """Return the base-2 logarithm of x."""
    if x <= 0:
        raise ValueError(f"Expected non-negative value. Received {x}.")
    return math.log10(x)


@register.filter
@numerify
def pow(x, y):
    """Return the logarithm of x with base y (default to e)"""
    if x <= 0 and not isinstance(y, int):
        raise ValueError(f"Exponent must be an integer if negative base. Received base {x} with exponent {y}.")
    return math.pow(x, y)