"""
Unit Tests for Core Algorithms (Sorting & Searching)
"""
import random
import unittest
from core.algorithms.registry import registry
from core.algorithms.searching import BinarySearch, LinearSearch
from core.algorithms.sorting import (
    BubbleSort,
    InsertionSort,
    MergeSort,
    QuickSort,
    SelectionSort,
)
from core.simulation.events import EventType


class TestCoreAlgorithms(unittest.TestCase):
    def setUp(self):
        self.sorting_algorithms = [
            BubbleSort(),
            SelectionSort(),
            InsertionSort(),
            MergeSort(),
            QuickSort(),
        ]
        self.test_cases = [
            [],
            [1],
            [1, 2, 3],
            [3, 2, 1],
            [5, 5, 5],
            [12, 45, 7, 23, 89, 34, 5],
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            [random.randint(1, 1000) for _ in range(50)],
        ]

    def test_sorting_correctness(self):
        for alg in self.sorting_algorithms:
            for case in self.test_cases:
                expected = sorted(case)
                stats = alg.run_benchmark(list(case))
                self.assertEqual(
                    stats.result,
                    expected,
                    f"Algorithm {alg.metadata.name} failed on case {case[:5]}... Expected {expected[:5]}, got {stats.result[:5]}"
                )

    def test_sorting_simulation_events(self):
        for alg in self.sorting_algorithms:
            case = [5, 2, 8, 1, 9]
            events = list(alg.simulate(list(case)))
            self.assertGreater(len(events), 0, f"Algorithm {alg.metadata.name} yielded no events")
            last_event = events[-1]
            self.assertEqual(last_event.event_type, EventType.FINISHED)
            self.assertEqual(last_event.array_state, sorted(case))

    def test_linear_search(self):
        ls = LinearSearch()
        arr = [10, 20, 30, 40, 50]
        # Found
        stats = ls.run_benchmark(arr, target=30)
        self.assertEqual(stats.result, 2)
        # Not found
        stats = ls.run_benchmark(arr, target=99)
        self.assertEqual(stats.result, -1)
        # Empty
        stats = ls.run_benchmark([], target=10)
        self.assertEqual(stats.result, -1)

    def test_binary_search(self):
        bs = BinarySearch()
        sorted_arr = [5, 12, 23, 34, 45, 67, 89]
        # Found
        stats = bs.run_benchmark(sorted_arr, target=34)
        self.assertEqual(stats.result, 3)
        # Found first
        stats = bs.run_benchmark(sorted_arr, target=5)
        self.assertEqual(stats.result, 0)
        # Found last
        stats = bs.run_benchmark(sorted_arr, target=89)
        self.assertEqual(stats.result, 6)
        # Not found
        stats = bs.run_benchmark(sorted_arr, target=100)
        self.assertEqual(stats.result, -1)
        # Empty
        stats = bs.run_benchmark([], target=10)
        self.assertEqual(stats.result, -1)


if __name__ == "__main__":
    unittest.main()
