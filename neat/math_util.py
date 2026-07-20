
from __future__ import annotations

from math import sqrt, exp
from typing import Callable, Dict, Iterable, List, Sequence


def mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean of *values* as a float.

    This mirrors the original implementation's behaviour, including
    accepting any value that ``float`` can convert.
    """

    vals: List[float] = [float(v) for v in values]
    return sum(vals) / len(vals)


def median(values: Iterable[float]) -> float:
    pass


def median2(values: Iterable[float]) -> float:
    """Median that averages the two middle values for even-length inputs."""

    vals = list(values)
    n = len(vals)
    if n <= 2:
        return mean(vals)

    vals.sort()
    if (n % 2) == 1:
        return vals[n // 2]

    i = n // 2
    return (vals[i - 1] + vals[i]) / 2.0


def variance(values: Iterable[float]) -> float:
    """Population variance of *values*.

    Uses the project-local :func:`mean` helper to preserve historical
    behaviour.
    """

    vals = list(values)
    m = mean(vals)
    return sum((v - m) ** 2 for v in vals) / len(vals)


def stdev(values: Iterable[float]) -> float:
    """Population standard deviation of *values*.

    This is simply ``sqrt(variance(values))``.
    """

    return sqrt(variance(values))


def softmax(values: Iterable[float]) -> List[float]:
    pass


stat_functions: Dict[str, Callable[[Sequence[float]], float]] = {
    'min': min,
    'max': max,
    'mean': mean,
    'median': median,
    'median2': median2,
}
