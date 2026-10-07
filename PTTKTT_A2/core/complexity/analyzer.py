"""
Algorithm Analysis & Simulation Platform
Core - Input Data Complexity & Characteristics Analyzer
"""
import math
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class InputAnalysisResult:
    size: int
    data_type: str
    min_value: Any
    max_value: Any
    range_value: Any
    is_sorted_asc: bool
    is_sorted_desc: bool
    is_nearly_sorted: bool
    inversion_ratio: float
    duplicate_count: int
    unique_count: int
    unique_percentage: float
    mean: float
    variance: float
    std_dev: float
    characteristic: str
    summary_text: str


class InputAnalyzer:
    """Analyzes input dataset characteristics to feed the recommendation engine."""

    @staticmethod
    def analyze(data: List[Any]) -> InputAnalysisResult:
        n = len(data)
        if n == 0:
            return InputAnalysisResult(
                size=0,
                data_type="Empty",
                min_value=None,
                max_value=None,
                range_value=0,
                is_sorted_asc=True,
                is_sorted_desc=True,
                is_nearly_sorted=True,
                inversion_ratio=0.0,
                duplicate_count=0,
                unique_count=0,
                unique_percentage=100.0,
                mean=0.0,
                variance=0.0,
                std_dev=0.0,
                characteristic="Rỗng",
                summary_text="Dữ liệu rỗng."
            )

        # Detect data type
        types = set(type(x).__name__ for x in data)
        if len(types) == 1:
            data_type = next(iter(types))
        else:
            data_type = f"Mixed ({', '.join(types)})"

        # Check numeric
        is_numeric = all(isinstance(x, (int, float)) for x in data)
        min_val = min(data)
        max_val = max(data)
        range_val = (max_val - min_val) if is_numeric else "N/A"

        # Unique & Duplicates
        unique_set = set(data)
        unique_count = len(unique_set)
        duplicate_count = n - unique_count
        unique_pct = (unique_count / n) * 100.0

        # Sorted checks
        is_sorted_asc = True
        is_sorted_desc = True
        adjacent_inversions = 0
        for i in range(n - 1):
            if data[i] > data[i + 1]:
                is_sorted_asc = False
                adjacent_inversions += 1
            if data[i] < data[i + 1]:
                is_sorted_desc = False

        inversion_ratio = (adjacent_inversions / (n - 1)) if n > 1 else 0.0
        # Nearly sorted if < 5% adjacent inversions and not completely reverse
        is_nearly_sorted = (inversion_ratio < 0.05 and not is_sorted_desc) if n > 10 else False

        # Numeric statistics
        if is_numeric and n > 0:
            mean = sum(data) / n
            var = sum((x - mean) ** 2 for x in data) / n
            std = math.sqrt(var)
        else:
            mean = 0.0
            var = 0.0
            std = 0.0

        # Characteristic classification
        if is_sorted_asc:
            characteristic = "Đã sắp xếp tăng"
        elif is_sorted_desc:
            characteristic = "Đã sắp xếp giảm (Ngược hoàn toàn)"
        elif is_nearly_sorted:
            characteristic = "Gần như đã sắp xếp"
        elif unique_pct < 20.0:
            characteristic = "Nhiều phần tử trùng lặp"
        else:
            characteristic = "Phân bố ngẫu nhiên"

        summary = (
            f"Kích thước n = {n:,} | Kiểu dữ liệu: {data_type} | Miền giá trị: [{min_val} .. {max_val}] | "
            f"Đặc điểm: {characteristic} (Trùng lặp: {duplicate_count:,} phần tử / {unique_pct:.1f}% duy nhất)"
        )

        return InputAnalysisResult(
            size=n,
            data_type=data_type,
            min_value=min_val,
            max_value=max_val,
            range_value=range_val,
            is_sorted_asc=is_sorted_asc,
            is_sorted_desc=is_sorted_desc,
            is_nearly_sorted=is_nearly_sorted,
            inversion_ratio=inversion_ratio,
            duplicate_count=duplicate_count,
            unique_count=unique_count,
            unique_percentage=unique_pct,
            mean=mean,
            variance=var,
            std_dev=std,
            characteristic=characteristic,
            summary_text=summary
        )
