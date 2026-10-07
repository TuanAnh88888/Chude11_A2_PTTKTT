"""
Integration & End-to-End Workflow Tests
Simulates full lifecycle from problem input to analysis, recommendation, simulation, benchmark, and export.
"""
import os
import tempfile
import unittest
from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.ast_analyzer.static_analyzer import StaticAstAnalyzer
from core.benchmark.runner import BenchmarkRunner
from core.complexity.analyzer import InputAnalyzer
from core.recommendation.engine import RecommendationConstraints, RecommendationEngine
from core.simulation.events import EventType
from infrastructure.data.generator import DataDistribution, DataGenerator
from infrastructure.data.io_handler import DataIOHandler
from infrastructure.export.report_exporter import ReportExporter
from infrastructure.persistence.history_manager import HistoryManager, HistoryRecord


class TestEndToEndWorkflow(unittest.TestCase):
    def test_full_sorting_lifecycle(self):
        # 1. Generate data
        data = DataGenerator.generate(size=60, distribution=DataDistribution.RANDOM, min_val=1, max_val=1000)
        self.assertEqual(len(data), 60)

        # 2. Analyze input
        analysis = InputAnalyzer.analyze(data)
        self.assertEqual(analysis.size, 60)
        self.assertFalse(analysis.is_sorted_asc)

        # 3. Get recommendation
        rec = RecommendationEngine.recommend(AlgorithmCategory.SORTING, analysis)
        self.assertIsNotNone(rec.primary_recommendation)
        self.assertGreater(len(rec.reasoning_points), 0)

        # 4. Simulate recommended algorithm
        recommended_alg = registry.get_algorithm(rec.primary_recommendation.name)
        events = list(recommended_alg.simulate(list(data)))
        self.assertGreater(len(events), 0)
        last_event = events[-1]
        self.assertEqual(last_event.event_type, EventType.FINISHED)
        self.assertEqual(last_event.array_state, sorted(data))

        # 5. Run real benchmark
        metrics = BenchmarkRunner.run_single_dataset(
            algorithm_names=["bubble_sort", "merge_sort", "quick_sort"],
            data=data,
            runs=3,
            warmup=True
        )
        self.assertEqual(len(metrics), 3)
        for m in metrics:
            self.assertGreater(m.avg_time_ms, 0.0)

        # 6. Export report
        with tempfile.TemporaryDirectory() as tmpdir:
            txt_path = os.path.join(tmpdir, "report.txt")
            csv_path = os.path.join(tmpdir, "benchmarks.csv")

            txt_ok = ReportExporter.export_text(
                filepath=txt_path,
                problem_title="Sắp xếp dữ liệu ngẫu nhiên",
                input_analysis=analysis,
                recommendation=rec,
                benchmarks=metrics,
                conclusions="Hoàn tất chu trình kiểm thử E2E."
            )
            self.assertTrue(txt_ok)
            self.assertTrue(os.path.exists(txt_path))

            csv_ok = ReportExporter.export_csv(csv_path, metrics)
            self.assertTrue(csv_ok)
            self.assertTrue(os.path.exists(csv_path))

    def test_full_searching_lifecycle(self):
        # 1. Sorted data for binary search
        data = DataGenerator.generate(size=500, distribution=DataDistribution.SORTED_ASC, min_val=1, max_val=10000)
        target = data[250]

        # 2. Analyze
        analysis = InputAnalyzer.analyze(data)
        self.assertTrue(analysis.is_sorted_asc)

        # 3. Recommend
        rec = RecommendationEngine.recommend(AlgorithmCategory.SEARCHING, analysis)
        self.assertEqual(rec.primary_recommendation.name, "binary_search")

        # 4. Simulate
        bs = registry.get_algorithm("binary_search")
        events = list(bs.simulate(list(data), target=target))
        found_events = [e for e in events if e.event_type == EventType.FOUND]
        self.assertEqual(len(found_events), 1)

        # 5. Benchmark
        metrics = BenchmarkRunner.run_single_dataset(
            algorithm_names=["linear_search", "binary_search"],
            data=data,
            runs=3,
            warmup=True,
            target=target
        )
        self.assertEqual(len(metrics), 2)
        # Binary search should perform fewer or equal comparisons than linear search on sorted array
        bs_metric = next(m for m in metrics if m.algorithm_name == "binary_search")
        self.assertLessEqual(bs_metric.comparisons, 15)


if __name__ == "__main__":
    unittest.main()
