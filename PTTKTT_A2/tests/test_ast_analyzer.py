"""
Unit Tests for Static Code AST Analyzer
"""
import unittest
from core.ast_analyzer.static_analyzer import StaticAstAnalyzer


class TestStaticAstAnalyzer(unittest.TestCase):
    def test_single_loop_linear(self):
        code = """
def linear_scan(arr):
    total = 0
    for x in arr:
        total += x
    return total
"""
        report = StaticAstAnalyzer.analyze_code(code)
        self.assertTrue(report.is_valid_syntax)
        self.assertEqual(report.total_loops, 1)
        self.assertEqual(report.max_loop_nesting, 1)
        self.assertIn("O(n)", report.estimated_time_complexity)

    def test_nested_loops_quadratic(self):
        code = """
def bubble_style(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
"""
        report = StaticAstAnalyzer.analyze_code(code)
        self.assertTrue(report.is_valid_syntax)
        self.assertEqual(report.max_loop_nesting, 2)
        self.assertIn("O(n²)", report.estimated_time_complexity)

    def test_recursion_detection(self):
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""
        report = StaticAstAnalyzer.analyze_code(code)
        self.assertTrue(report.is_valid_syntax)
        self.assertTrue(report.is_recursive)
        self.assertGreaterEqual(report.recursive_call_count, 2)
        self.assertIn("O(2ⁿ)", report.estimated_time_complexity)

    def test_syntax_error(self):
        code = "def broken_code(arr) for x in arr:"
        report = StaticAstAnalyzer.analyze_code(code)
        self.assertFalse(report.is_valid_syntax)
        self.assertIsNotNone(report.error_message)


if __name__ == "__main__":
    unittest.main()
