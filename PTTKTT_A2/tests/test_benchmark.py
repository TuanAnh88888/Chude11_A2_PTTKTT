"""
Unit Tests for Benchmark Engine
"""
import unittest
from core.benchmark.runner import BenchmarkRunner
from infrastructure.data.generator import DataGenerator


class TestBenchmarkRunner(unittest.TestCase):
    def test_single_dataset_benchmark(self):
        data = DataGenerator.generate(size=50, min_val=1, max_val=100)
        algs = ["bubble_sort", "insertion_sort", "quick_sort"]
        metrics = BenchmarkRunner.run_single_dataset(algs, data, runs=2, warmup=True)

        self.assertEqual(len(metrics), 3)
        for m in metrics:
            self.assertGreater(m.runs, 0)
            self.assertGreaterEqual(m.avg_time_ms, 0.0)
            self.assertGreaterEqual(m.comparisons, 0)

    def test_multi_size_benchmark(self):
        sizes = [20, 50]
        algs = ["merge_sort", "quick_sort"]
        result = BenchmarkRunner.run_multi_sizes(
            algs,
            sizes,
            data_generator=lambda sz: DataGenerator.generate(size=sz),
            runs=2,
            warmup=False
        )

        self.assertEqual(result.sizes, [20, 50])
        self.assertIn("merge_sort", result.metrics_by_alg)
        self.assertEqual(len(result.metrics_by_alg["merge_sort"]), 2)


if __name__ == "__main__":
    unittest.main()
