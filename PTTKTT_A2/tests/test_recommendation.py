"""
Unit Tests for Recommendation Engine
"""
import unittest
from core.algorithms.base import AlgorithmCategory
from core.complexity.analyzer import InputAnalyzer
from core.recommendation.engine import RecommendationConstraints, RecommendationEngine


class TestRecommendationEngine(unittest.TestCase):
    def test_sorting_small_dataset(self):
        data = [5, 2, 9, 1, 3]
        analysis = InputAnalyzer.analyze(data)
        rec = RecommendationEngine.recommend(AlgorithmCategory.SORTING, analysis)
        self.assertEqual(rec.primary_recommendation.name, "insertion_sort")
        self.assertIn("nhỏ", rec.reasoning_points[0].lower())

    def test_sorting_already_sorted(self):
        data = list(range(100))
        analysis = InputAnalyzer.analyze(data)
        rec = RecommendationEngine.recommend(AlgorithmCategory.SORTING, analysis)
        self.assertEqual(rec.primary_recommendation.name, "insertion_sort")
        self.assertTrue(any("đã sắp xếp" in r.lower() for r in rec.reasoning_points))

    def test_sorting_large_dataset(self):
        data = list(range(10000, 0, -1))
        # Note: reverse sorted
        analysis = InputAnalyzer.analyze(data)
        # Not already sorted asc, size > 5000 -> quick_sort or merge_sort
        rec = RecommendationEngine.recommend(AlgorithmCategory.SORTING, analysis)
        self.assertIn(rec.primary_recommendation.name, ["quick_sort", "merge_sort"])

    def test_searching_sorted_vs_unsorted(self):
        # Sorted dataset
        sorted_data = [1, 3, 5, 7, 9, 11, 13, 15]
        analysis_sorted = InputAnalyzer.analyze(sorted_data)
        rec_sorted = RecommendationEngine.recommend(AlgorithmCategory.SEARCHING, analysis_sorted)
        self.assertEqual(rec_sorted.primary_recommendation.name, "binary_search")

        # Unsorted dataset with 1 query -> Linear Search
        unsorted_data = [15, 3, 99, 2, 7, 1]
        analysis_unsorted = InputAnalyzer.analyze(unsorted_data)
        rec_single_query = RecommendationEngine.recommend(
            AlgorithmCategory.SEARCHING,
            analysis_unsorted,
            RecommendationConstraints(query_count=1)
        )
        self.assertEqual(rec_single_query.primary_recommendation.name, "linear_search")

        # Unsorted dataset with 1000 queries -> Binary Search (pre-sorting amortized)
        rec_multi_query = RecommendationEngine.recommend(
            AlgorithmCategory.SEARCHING,
            analysis_unsorted,
            RecommendationConstraints(query_count=1000)
        )
        self.assertEqual(rec_multi_query.primary_recommendation.name, "binary_search")


if __name__ == "__main__":
    unittest.main()
