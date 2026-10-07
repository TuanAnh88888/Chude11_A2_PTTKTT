"""
Algorithm Analysis & Simulation Platform
Core - Benchmark Metrics and Results Data Structures
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SingleBenchmarkMetric:
    algorithm_name: str
    display_name: str
    size: int
    runs: int
    avg_time_ms: float
    min_time_ms: float
    max_time_ms: float
    comparisons: int
    swaps: int
    assignments: int
    theoretical_complexity: str
    space_complexity: str
    runs_times_ms: List[float] = field(default_factory=list)
    data_distribution: str = "Random"
    is_correct: bool = True
    validation_error: Optional[str] = None


@dataclass
class MultiSizeBenchmarkResult:
    sizes: List[int]
    algorithms: List[str]
    # algorithm_name -> list of SingleBenchmarkMetric ordered by size
    metrics_by_alg: Dict[str, List[SingleBenchmarkMetric]] = field(default_factory=dict)
    # raw times for plotting: algorithm_name -> [avg_time_s for each size]
    plot_series: Dict[str, List[float]] = field(default_factory=dict)
    summary_notes: List[str] = field(default_factory=list)


@dataclass
class MultiDistributionBenchmarkResult:
    distributions: List[str]
    algorithms: List[str]
    size: int
    # distribution -> list of SingleBenchmarkMetric
    metrics_by_dist: Dict[str, List[SingleBenchmarkMetric]] = field(default_factory=dict)
    # algorithm_name -> [avg_time_ms for each distribution]
    plot_series_by_alg: Dict[str, List[float]] = field(default_factory=dict)
