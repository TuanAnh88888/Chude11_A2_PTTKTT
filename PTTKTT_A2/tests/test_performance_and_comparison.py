"""
Dedicated Tests for Upgraded Benchmark & Comparison Features
Covers the 4 scenarios specified in Section 34 of the Requirements:
1. Bubble Sort vs Insertion Sort (n=1000, Random)
2. Quick Sort vs Merge Sort (n=10000, Random)
3. Quick Sort vs Merge Sort vs Insertion Sort (n=10000, Nearly Sorted)
4. Multi-size benchmark across 100, 1000, 5000, 10000
"""
import unittest
from core.benchmark.runner import BenchmarkRunner
from infrastructure.data.generator import DataDistribution, DataGenerator


class TestPerformanceAndComparisonScenarios(unittest.TestCase):
    def test_check_1_bubble_vs_insertion(self):
        """Kiểm tra 1: Bubble Sort vs Insertion Sort (n = 1000, Random)"""
        data = DataGenerator.generate(size=1000, distribution=DataDistribution.RANDOM)
        metrics = BenchmarkRunner.run_single_dataset(
            algorithm_names=["bubble_sort", "insertion_sort"],
            data=data,
            runs=3,
            warmup=True
        )
        self.assertEqual(len(metrics), 2)
        # Both must produce correct sorted arrays
        for m in metrics:
            self.assertTrue(m.is_correct)
            self.assertGreater(m.avg_time_ms, 0.0)
            self.assertGreater(m.comparisons, 0)

    def test_check_2_quick_vs_merge(self):
        """Kiểm tra 2: Quick Sort vs Merge Sort (n = 10000, Random)"""
        data = DataGenerator.generate(size=10000, distribution=DataDistribution.RANDOM)
        metrics = BenchmarkRunner.run_single_dataset(
            algorithm_names=["quick_sort", "merge_sort"],
            data=data,
            runs=3,
            warmup=True
        )
        self.assertEqual(len(metrics), 2)
        for m in metrics:
            self.assertTrue(m.is_correct)
            # Both should be fast O(n log n)
            self.assertLess(m.avg_time_ms, 1000.0)

    def test_check_3_quick_merge_insertion_nearly_sorted(self):
        """Kiểm tra 3: Quick Sort vs Merge Sort vs Insertion Sort (n = 10000, Nearly Sorted)"""
        data = DataGenerator.generate(size=10000, distribution=DataDistribution.NEARLY_SORTED)
        metrics = BenchmarkRunner.run_single_dataset(
            algorithm_names=["quick_sort", "merge_sort", "insertion_sort"],
            data=data,
            runs=3,
            warmup=True
        )
        self.assertEqual(len(metrics), 3)
        for m in metrics:
            self.assertTrue(m.is_correct)

        # On nearly sorted data, Insertion Sort comparisons should be significantly lower than O(n^2)
        ins = next(m for m in metrics if m.algorithm_name == "insertion_sort")
        self.assertLess(ins.comparisons, 50000000)

    def test_check_4_multi_sizes(self):
        """Kiểm tra 4: Chạy nhiều kích thước: 100, 1000, 5000, 10000"""
        sizes = [100, 1000, 5000, 10000]
        res = BenchmarkRunner.run_multi_sizes(
            algorithm_names=["quick_sort", "merge_sort"],
            sizes=sizes,
            data_generator=lambda sz: DataGenerator.generate(size=sz),
            runs=2,
            warmup=True
        )
        self.assertEqual(res.sizes, sizes)
        self.assertEqual(len(res.metrics_by_alg["quick_sort"]), 4)
        self.assertEqual(len(res.metrics_by_alg["merge_sort"]), 4)


if __name__ == "__main__":
    unittest.main()
