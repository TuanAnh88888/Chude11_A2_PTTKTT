"""
Algorithm Analysis & Simulation Platform
Core - Benchmark Execution Engine
"""
import copy
import threading
import time
from typing import Any, Callable, Dict, List, Optional
from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.benchmark.metrics import (
    MultiDistributionBenchmarkResult,
    MultiSizeBenchmarkResult,
    SingleBenchmarkMetric,
)
from infrastructure.data.generator import DataDistribution, DataGenerator


class BenchmarkRunner:
    """Independent benchmarking engine strictly isolated from GUI and animation logic."""

    @staticmethod
    def run_single_dataset(
        algorithm_names: List[str],
        data: List[Any],
        runs: int = 5,
        warmup: bool = True,
        target: Any = None,
        data_distribution: str = "Random",
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        cancel_event: Optional[threading.Event] = None
    ) -> List[SingleBenchmarkMetric]:
        """Runs benchmarks on a single dataset across multiple algorithms."""
        results: List[SingleBenchmarkMetric] = []
        total_tasks = len(algorithm_names) * runs
        current_step = 0

        n = len(data)

        # Precompute expected result for correctness verification
        # Determine if sorting or searching
        is_searching = any(
            (alg := registry.get_algorithm(name)) and alg.metadata.category == AlgorithmCategory.SEARCHING
            for name in algorithm_names
        )

        expected_result = None
        if not is_searching and n > 0:
            expected_result = sorted(data)
        elif is_searching and n > 0 and target is not None:
            # Expected search result
            expected_result = data.index(target) if target in data else -1

        for alg_name in algorithm_names:
            if cancel_event and cancel_event.is_set():
                break

            alg = registry.get_algorithm(alg_name)
            if not alg:
                continue

            # Warmup run (discarded)
            if warmup and n > 0:
                warmup_copy = list(data)
                alg.run_benchmark(warmup_copy, target=target)

            times: List[float] = []
            comps = 0
            swaps = 0
            assigns = 0
            last_stats = None
            is_correct = True
            val_error = None

            for r in range(runs):
                if cancel_event and cancel_event.is_set():
                    break

                current_step += 1
                if progress_callback:
                    progress_callback(
                        current_step,
                        total_tasks,
                        f"Đang đo {alg.metadata.display_name} (lần {r+1}/{runs})..."
                    )

                # Fresh copy of dataset for every run so in-place operations don't mutate shared data
                run_copy = list(data)

                # Pure timing strictly around algorithm run
                stats = alg.run_benchmark(run_copy, target=target)
                times.append(stats.execution_time)
                comps = stats.comparisons
                swaps = stats.swaps
                assigns = stats.assignments
                last_stats = stats

            if not times:
                continue

            # Correctness verification (Section 28)
            if expected_result is not None and last_stats is not None:
                if not is_searching:
                    if last_stats.result != expected_result:
                        is_correct = False
                        val_error = "Kết quả sắp xếp không đúng thứ tự mong đợi!"
                else:
                    # For search: if found, element at result index must equal target
                    res_idx = last_stats.result
                    if res_idx != -1:
                        if res_idx >= len(data) or data[res_idx] != target:
                            # Note: in binary search, if array had duplicates or binary search sorted it
                            if res_idx < len(sorted(data)) and sorted(data)[res_idx] == target:
                                pass
                            else:
                                is_correct = False
                                val_error = f"Tìm thấy chỉ số {res_idx} nhưng giá trị không khớp target!"
                    else:
                        if target in data and alg.metadata.name == "linear_search":
                            is_correct = False
                            val_error = "Không tìm thấy target dù target có trong mảng!"

            avg_time = sum(times) / len(times) if times else 0.0
            min_time = min(times) if times else 0.0
            max_time = max(times) if times else 0.0

            results.append(SingleBenchmarkMetric(
                algorithm_name=alg.metadata.name,
                display_name=alg.metadata.display_name,
                size=n,
                runs=len(times),
                avg_time_ms=avg_time * 1000.0,
                min_time_ms=min_time * 1000.0,
                max_time_ms=max_time * 1000.0,
                comparisons=comps,
                swaps=swaps,
                assignments=assigns,
                theoretical_complexity=alg.metadata.average_case,
                space_complexity=alg.metadata.space_complexity,
                runs_times_ms=[t * 1000.0 for t in times],
                data_distribution=data_distribution,
                is_correct=is_correct,
                validation_error=val_error
            ))

        return results

    @staticmethod
    def run_multi_sizes(
        algorithm_names: List[str],
        sizes: List[int],
        data_generator: Callable[[int], List[Any]],
        runs: int = 3,
        warmup: bool = True,
        data_distribution: str = "Random",
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        cancel_event: Optional[threading.Event] = None
    ) -> MultiSizeBenchmarkResult:
        """Runs benchmarks across multiple dataset sizes for scalability analysis."""
        metrics_by_alg: Dict[str, List[SingleBenchmarkMetric]] = {name: [] for name in algorithm_names}
        plot_series: Dict[str, List[float]] = {name: [] for name in algorithm_names}

        total_steps = len(sizes) * len(algorithm_names) * runs
        current_step = 0

        for sz in sizes:
            if cancel_event and cancel_event.is_set():
                break

            # Generate shared dataset for this size so all algorithms get the exact same input
            shared_data = data_generator(sz)
            expected = sorted(shared_data)

            for alg_name in algorithm_names:
                if cancel_event and cancel_event.is_set():
                    break

                alg = registry.get_algorithm(alg_name)
                if not alg:
                    continue

                if warmup and sz > 0:
                    alg.run_benchmark(list(shared_data))

                times = []
                comps = 0
                swaps = 0
                assigns = 0
                last_stats = None

                for r in range(runs):
                    if cancel_event and cancel_event.is_set():
                        break

                    current_step += 1
                    if progress_callback:
                        progress_callback(
                            current_step,
                            total_steps,
                            f"Kích thước n={sz:,} | {alg.metadata.display_name} (lần {r+1}/{runs})..."
                        )

                    data_copy = list(shared_data)
                    stats = alg.run_benchmark(data_copy)
                    times.append(stats.execution_time)
                    comps = stats.comparisons
                    swaps = stats.swaps
                    assigns = stats.assignments
                    last_stats = stats

                if not times:
                    continue

                is_correct = (last_stats.result == expected) if last_stats else True
                val_error = None if is_correct else "Kết quả sắp xếp không đúng thứ tự mong đợi!"

                avg_time = sum(times) / len(times) if times else 0.0
                min_time = min(times) if times else 0.0
                max_time = max(times) if times else 0.0

                metric = SingleBenchmarkMetric(
                    algorithm_name=alg.metadata.name,
                    display_name=alg.metadata.display_name,
                    size=sz,
                    runs=len(times),
                    avg_time_ms=avg_time * 1000.0,
                    min_time_ms=min_time * 1000.0,
                    max_time_ms=max_time * 1000.0,
                    comparisons=comps,
                    swaps=swaps,
                    assignments=assigns,
                    theoretical_complexity=alg.metadata.average_case,
                    space_complexity=alg.metadata.space_complexity,
                    runs_times_ms=[t * 1000.0 for t in times],
                    data_distribution=data_distribution,
                    is_correct=is_correct,
                    validation_error=val_error
                )

                metrics_by_alg[alg_name].append(metric)
                plot_series[alg_name].append(avg_time)

        notes = [
            "Các thuật toán cùng kích thước n đều được đo trên tập dữ liệu hoàn toàn giống nhau.",
            "Thời gian đo độc lập với giao diện GUI và không bao gồm chi phí vẽ đồ họa.",
            "Kết quả thực nghiệm thể hiện xu hướng tăng trưởng phù hợp với độ phức tạp lý thuyết Big-O."
        ]

        return MultiSizeBenchmarkResult(
            sizes=sizes,
            algorithms=algorithm_names,
            metrics_by_alg=metrics_by_alg,
            plot_series=plot_series,
            summary_notes=notes
        )

    @staticmethod
    def run_multi_distributions(
        algorithm_names: List[str],
        size: int,
        distributions: List[str],
        runs: int = 3,
        warmup: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        cancel_event: Optional[threading.Event] = None
    ) -> MultiDistributionBenchmarkResult:
        """Benchmarks algorithms across multiple data distributions on a fixed size n."""
        metrics_by_dist: Dict[str, List[SingleBenchmarkMetric]] = {dist: [] for dist in distributions}
        plot_series_by_alg: Dict[str, List[float]] = {name: [] for name in algorithm_names}

        total_steps = len(distributions) * len(algorithm_names) * runs
        current_step = 0

        for dist in distributions:
            if cancel_event and cancel_event.is_set():
                break

            dataset = DataGenerator.generate(size=size, distribution=dist)
            expected = sorted(dataset)

            for alg_name in algorithm_names:
                if cancel_event and cancel_event.is_set():
                    break

                alg = registry.get_algorithm(alg_name)
                if not alg:
                    continue

                if warmup and size > 0:
                    alg.run_benchmark(list(dataset))

                times = []
                comps = 0
                swaps = 0
                assigns = 0
                last_stats = None

                for r in range(runs):
                    if cancel_event and cancel_event.is_set():
                        break

                    current_step += 1
                    if progress_callback:
                        progress_callback(
                            current_step,
                            total_steps,
                            f"Phân bố: {dist[:15]} | {alg.metadata.display_name}..."
                        )

                    data_copy = list(dataset)
                    stats = alg.run_benchmark(data_copy)
                    times.append(stats.execution_time)
                    comps = stats.comparisons
                    swaps = stats.swaps
                    assigns = stats.assignments
                    last_stats = stats

                if not times:
                    continue

                is_correct = (last_stats.result == expected) if last_stats else True
                val_error = None if is_correct else "Kết quả sắp xếp không đúng thứ tự!"

                avg_time = sum(times) / len(times) if times else 0.0
                min_time = min(times) if times else 0.0
                max_time = max(times) if times else 0.0

                m = SingleBenchmarkMetric(
                    algorithm_name=alg.metadata.name,
                    display_name=alg.metadata.display_name,
                    size=size,
                    runs=len(times),
                    avg_time_ms=avg_time * 1000.0,
                    min_time_ms=min_time * 1000.0,
                    max_time_ms=max_time * 1000.0,
                    comparisons=comps,
                    swaps=swaps,
                    assignments=assigns,
                    theoretical_complexity=alg.metadata.average_case,
                    space_complexity=alg.metadata.space_complexity,
                    runs_times_ms=[t * 1000.0 for t in times],
                    data_distribution=dist,
                    is_correct=is_correct,
                    validation_error=val_error
                )

                metrics_by_dist[dist].append(m)
                plot_series_by_alg[alg_name].append(avg_time * 1000.0)

        return MultiDistributionBenchmarkResult(
            distributions=distributions,
            algorithms=algorithm_names,
            size=size,
            metrics_by_dist=metrics_by_dist,
            plot_series_by_alg=plot_series_by_alg
        )
