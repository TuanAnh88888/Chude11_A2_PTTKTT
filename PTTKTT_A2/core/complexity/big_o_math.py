"""
Algorithm Analysis & Simulation Platform
Core - Big-O Mathematical Functions & Growth Curves
"""
import math
from typing import Callable, Dict, List, Tuple


def big_o_constant(n: float) -> float:
    return 1.0


def big_o_log_n(n: float) -> float:
    return math.log2(n) if n > 0 else 0.0


def big_o_n(n: float) -> float:
    return float(n)


def big_o_n_log_n(n: float) -> float:
    return n * math.log2(n) if n > 0 else 0.0


def big_o_n_squared(n: float) -> float:
    return float(n ** 2)


def big_o_2_n(n: float) -> float:
    # Cap to avoid overflow
    return float(2 ** min(n, 30))


BIG_O_FUNCTIONS: Dict[str, Tuple[str, Callable[[float], float]]] = {
    "O(1)": ("Hằng số - O(1)", big_o_constant),
    "O(log n)": ("Logarit - O(log n)", big_o_log_n),
    "O(n)": ("Tuyến tính - O(n)", big_o_n),
    "O(n log n)": ("Tuyến tính nhân Logarit - O(n log n)", big_o_n_log_n),
    "O(n²)": ("Bậc hai - O(n²)", big_o_n_squared),
    "O(2ⁿ)": ("Mũ - O(2ⁿ)", big_o_2_n),
}


def get_theoretical_growth(n_max: int = 100, num_points: int = 100) -> Dict[str, List[Tuple[float, float]]]:
    """Generate (n, f(n)) points for each Big-O complexity class up to n_max."""
    step = max(1, n_max // num_points)
    n_values = list(range(1, n_max + 1, step))
    if n_max not in n_values:
        n_values.append(n_max)

    result = {}
    for label, (_, func) in BIG_O_FUNCTIONS.items():
        points = []
        for n in n_values:
            val = func(n)
            points.append((float(n), float(val)))
        result[label] = points
    return result


def fit_theoretical_to_experimental(
    n_list: List[int],
    experimental_times: List[float],
    complexity_class: str
) -> List[float]:
    """Scale theoretical curve to fit experimental data using least squares scaling factor."""
    if not n_list or not experimental_times:
        return []

    func_entry = BIG_O_FUNCTIONS.get(complexity_class)
    if not func_entry:
        return list(experimental_times)

    _, func = func_entry
    theoretical_raw = [func(n) for n in n_list]

    # Calculate scale factor c = sum(exp * theo) / sum(theo^2)
    numerator = sum(e * t for e, t in zip(experimental_times, theoretical_raw))
    denominator = sum(t * t for t in theoretical_raw)
    scale = (numerator / denominator) if denominator > 0 else 0.0

    return [t * scale for t in theoretical_raw]
