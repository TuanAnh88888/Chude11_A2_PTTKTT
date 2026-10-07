"""
Algorithm Analysis & Simulation Platform
Core - Static Code AST Analyzer for Custom User Algorithms
"""
import ast
from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass
class AstAnalysisReport:
    is_valid_syntax: bool
    function_name: Optional[str] = None
    total_loops: int = 0
    max_loop_nesting: int = 0
    is_recursive: bool = 0
    recursive_call_count: int = 0
    detected_builtins: List[str] = field(default_factory=list)
    estimated_time_complexity: str = "Chưa xác định"
    estimated_space_complexity: str = "O(1) (Heuristic)"
    structural_features: List[str] = field(default_factory=list)
    heuristic_explanation: str = ""
    warning_disclaimer: str = (
        "⚠️ CẢNH BÁO: Đây là phân tích tĩnh heuristic dựa trên cây cú pháp trừu tượng (AST). "
        "Phân tích cấu trúc vòng lặp và đệ quy không thể chứng minh chính xác Big-O cho mọi trường hợp "
        "(do các điều kiện dừng sớm, bài toán dừng Turing / Halting problem)."
    )
    error_message: Optional[str] = None


class StaticAstAnalyzer(ast.NodeVisitor):
    """Parses user-provided Python code using AST to identify loops, nesting depth, recursion, and patterns."""

    def __init__(self):
        self.function_names: Set[str] = set()
        self.current_function: Optional[str] = None
        self.total_loops = 0
        self.current_loop_depth = 0
        self.max_loop_depth = 0
        self.recursive_calls = 0
        self.detected_calls: List[str] = []
        self.features: List[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.function_names.add(node.name)
        prev_func = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev_func

    def visit_For(self, node: ast.For):
        self.total_loops += 1
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_loop_depth:
            self.max_loop_depth = self.current_loop_depth
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node: ast.While):
        self.total_loops += 1
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_loop_depth:
            self.max_loop_depth = self.current_loop_depth
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_Call(self, node: ast.Call):
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name:
            self.detected_calls.append(func_name)
            if self.current_function and func_name == self.current_function:
                self.recursive_calls += 1

        self.generic_visit(node)

    @classmethod
    def analyze_code(cls, source_code: str) -> AstAnalysisReport:
        if not source_code or not source_code.strip():
            return AstAnalysisReport(
                is_valid_syntax=False,
                error_message="Mã nguồn rỗng. Vui lòng nhập hàm Python."
            )

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return AstAnalysisReport(
                is_valid_syntax=False,
                error_message=f"Lỗi cú pháp Python tại dòng {e.lineno}: {e.msg}"
            )

        visitor = cls()
        visitor.visit(tree)

        primary_func = next(iter(visitor.function_names)) if visitor.function_names else "my_algorithm"
        is_recursive = visitor.recursive_calls > 0

        # Heuristic Big-O deduction
        features: List[str] = []
        features.append(f"Tổng số vòng lặp phát hiện: {visitor.total_loops}")
        features.append(f"Độ sâu lồng nhau tối đa của vòng lặp: {visitor.max_loop_depth}")
        if is_recursive:
            features.append(f"Phát hiện đệ quy: {visitor.recursive_calls} lời gọi đệ quy trực tiếp trong hàm {primary_func}")

        # Built-in calls of interest
        interesting_builtins = [
            c for c in visitor.detected_calls
            if c in ("sort", "sorted", "min", "max", "sum", "index", "count", "append", "pop", "bisect")
        ]
        if interesting_builtins:
            features.append(f"Sử dụng các hàm/phương thức tích hợp: {', '.join(set(interesting_builtins))}")

        # Estimate
        if is_recursive:
            if visitor.recursive_calls >= 2 and visitor.max_loop_depth == 0:
                est_time = "O(2ⁿ) (Đệ quy phân nhánh nhị phân, vd: Fibonacci)"
                est_space = "O(n) (Ngăn xếp đệ quy)"
                explanation = "Hàm thực hiện nhiều hơn một lời gọi đệ quy mà không có vòng lặp, thường tạo cây đệ quy phân nhánh hàm mũ."
            elif visitor.recursive_calls >= 1 and any(b in ("sort", "sorted") for b in visitor.detected_calls):
                est_time = "O(n log n) (Đệ quy kết hợp phân hoạch/trộn)"
                est_space = "O(n) hoặc O(log n)"
                explanation = "Hàm có cấu trúc Chia để trị kết hợp thao tác phân hoạch hoặc sắp xếp."
            else:
                est_time = "O(n) hoặc O(log n) (Đệ quy tuyến tính/chia đôi)"
                est_space = "O(n) call stack"
                explanation = "Hàm đệ quy đơn chuỗi."
        else:
            if visitor.max_loop_depth == 0:
                if any(b in ("sort", "sorted") for b in visitor.detected_calls):
                    est_time = "O(n log n) (Do gọi Timsort tích hợp)"
                elif any(b in ("min", "max", "sum", "count") for b in visitor.detected_calls):
                    est_time = "O(n) (Do gọi hàm quét tuyến tính tích hợp)"
                else:
                    est_time = "O(1) (Thao tác hằng số)"
                est_space = "O(1)"
                explanation = "Không chứa vòng lặp tường minh. Độ phức tạp phụ thuộc vào các hàm thư viện được gọi."
            elif visitor.max_loop_depth == 1:
                est_time = "O(n) (Vòng lặp đơn 1 cấp)"
                est_space = "O(1)"
                explanation = "Chứa vòng lặp 1 tầng không lồng nhau, thời gian tỷ lệ thuận tuyến tính với kích thước dữ liệu."
            elif visitor.max_loop_depth == 2:
                est_time = "O(n²) (Vòng lặp lồng nhau 2 cấp)"
                est_space = "O(1)"
                explanation = "Chứa 2 vòng lặp lồng nhau (vòng trong phụ thuộc hoặc quét toàn bộ), thời gian bậc hai O(n²)."
            elif visitor.max_loop_depth >= 3:
                est_time = f"O(n^{visitor.max_loop_depth}) (Vòng lặp lồng {visitor.max_loop_depth} cấp)"
                est_space = "O(1)"
                explanation = f"Chứa {visitor.max_loop_depth} vòng lặp lồng nhau, thời gian đa thức bậc cao."
            else:
                est_time = "O(n)"
                est_space = "O(1)"
                explanation = "Phân tích mặc định theo số lượng vòng lặp."

        return AstAnalysisReport(
            is_valid_syntax=True,
            function_name=primary_func,
            total_loops=visitor.total_loops,
            max_loop_nesting=visitor.max_loop_depth,
            is_recursive=is_recursive,
            recursive_call_count=visitor.recursive_calls,
            detected_builtins=list(set(interesting_builtins)),
            estimated_time_complexity=est_time,
            estimated_space_complexity=est_space,
            structural_features=features,
            heuristic_explanation=explanation
        )
