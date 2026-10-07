"""
Algorithm Analysis & Simulation Platform
Core - Algorithm Recommendation Engine
"""
from dataclasses import dataclass, field
from typing import Any, List, Optional
from core.algorithms.base import AlgorithmCategory, AlgorithmMetadata
from core.algorithms.registry import registry
from core.complexity.analyzer import InputAnalysisResult


@dataclass
class RecommendationConstraints:
    require_stable: bool = False
    strictly_in_place: bool = False
    query_count: int = 1  # For searching: 1 query vs multiple repeated queries


@dataclass
class RecommendationResult:
    problem_type: str
    candidates: List[AlgorithmMetadata]
    primary_recommendation: AlgorithmMetadata
    alternative_recommendations: List[AlgorithmMetadata] = field(default_factory=list)
    reasoning_points: List[str] = field(default_factory=list)
    trade_offs: List[str] = field(default_factory=list)
    caveats_and_warnings: List[str] = field(default_factory=list)
    complexity_summary: str = ""


class RecommendationEngine:
    """Intelligent recommendation engine based on asymptotic complexity,
    data properties, problem constraints, and operational trade-offs."""

    @staticmethod
    def recommend(
        category: AlgorithmCategory,
        analysis: InputAnalysisResult,
        constraints: Optional[RecommendationConstraints] = None
    ) -> RecommendationResult:
        if constraints is None:
            constraints = RecommendationConstraints()

        n = analysis.size
        candidates = [alg.metadata for alg in registry.get_by_category(category)]

        if category == AlgorithmCategory.SORTING:
            return RecommendationEngine._recommend_sorting(analysis, constraints, candidates)
        elif category == AlgorithmCategory.SEARCHING:
            return RecommendationEngine._recommend_searching(analysis, constraints, candidates)
        else:
            raise ValueError(f"Chưa hỗ trợ danh mục bài toán: {category}")

    @staticmethod
    def _recommend_sorting(
        analysis: InputAnalysisResult,
        constraints: RecommendationConstraints,
        candidates: List[AlgorithmMetadata]
    ) -> RecommendationResult:
        n = analysis.size
        reasons: List[str] = []
        trade_offs: List[str] = []
        warnings: List[str] = []
        alternatives: List[AlgorithmMetadata] = []

        quick_sort_meta = registry.get_metadata("quick_sort")
        merge_sort_meta = registry.get_metadata("merge_sort")
        insertion_sort_meta = registry.get_metadata("insertion_sort")
        bubble_sort_meta = registry.get_metadata("bubble_sort")
        selection_sort_meta = registry.get_metadata("selection_sort")

        # Scenario 1: Very small dataset (n <= 30) or nearly sorted
        if n <= 30:
            primary = insertion_sort_meta
            reasons.append(f"Kích thước dữ liệu rất nhỏ (n = {n} <= 30). Insertion Sort có hằng số ẩn (overhead) nhỏ nhất.")
            reasons.append("Sử dụng bộ nhớ O(1) in-place và duy trì tính ổn định (Stable).")
            if quick_sort_meta:
                alternatives.append(quick_sort_meta)
            trade_offs.append("Mặc dù Merge Sort/Quick Sort có Big-O tiệm cận tốt hơn O(n log n), chi phí khởi tạo ngăn xếp và chia mảng khiến chúng chậm hơn Insertion Sort ở n cực nhỏ.")

        elif analysis.is_sorted_asc:
            primary = insertion_sort_meta
            reasons.append("Dữ liệu ĐÃ SẮP XẾP TĂNG DẦN sẵn.")
            reasons.append("Insertion Sort (hoặc Bubble Sort có cờ hiệu) đạt độ phức tạp Best Case O(n) với duy nhất n - 1 phép so sánh và 0 phép hoán đổi.")
            if bubble_sort_meta:
                alternatives.append(bubble_sort_meta)
            warnings.append("CẢNH BÁO: Thuật toán Quick Sort với chốt đầu/cuối có thể bị suy biến thành O(n²) trên mảng đã sắp xếp!")
            trade_offs.append("Merge Sort vẫn tiêu tốn O(n log n) và O(n) bộ nhớ phụ, không tận dụng được tính chất đã sắp xếp như Insertion Sort.")

        elif analysis.is_nearly_sorted:
            primary = insertion_sort_meta
            reasons.append(f"Dữ liệu 'GẦN NHƯ ĐÃ SẮP XẾP' (tỷ lệ nghịch thế chỉ {analysis.inversion_ratio * 100:.2f}%).")
            reasons.append("Insertion Sort chỉ cần dịch chuyển một lượng phần tử rất nhỏ, tiệm cận thời gian O(n).")
            if merge_sort_meta:
                alternatives.append(merge_sort_meta)
            trade_offs.append("Insertion Sort vượt trội hơn Quick/Merge Sort khi số lượng vị trí sai lệch là k << n.")

        elif constraints.require_stable:
            primary = merge_sort_meta
            reasons.append("Ràng buộc yêu cầu THUẬT TOÁN ỔN ĐỊNH (Stable Sort) để bảo toàn thứ tự ban đầu của các phần tử bằng nhau.")
            reasons.append("Merge Sort bảo đảm tính ổn định và duy trì thời gian O(n log n) trong mọi trường hợp.")
            if insertion_sort_meta and n <= 100:
                alternatives.append(insertion_sort_meta)
            trade_offs.append("Đánh đổi: Merge Sort cần O(n) bộ nhớ phụ (không In-place). Nếu bộ nhớ RAM bị giới hạn ngặt nghèo, đây là một bất lợi.")

        elif constraints.strictly_in_place:
            primary = quick_sort_meta
            reasons.append("Ràng buộc BỘ NHỚ TẠI CHỖ (In-place, O(1) đến O(log n) bộ nhớ phụ).")
            reasons.append("Quick Sort thực hiện phân hoạch trực tiếp trên mảng gốc, không cần cấp phát mảng phụ O(n) như Merge Sort.")
            warnings.append("Cần lưu ý trường hợp xấu nhất O(n²) nếu gặp mảng nghịch đảo hoặc pivot chọn biên.")
            trade_offs.append("Đánh đổi: Quick Sort không có tính ổn định (Unstable).")

        else:
            # General large / medium dataset with random distribution
            # Both Quick Sort and Merge Sort are strong candidates
            if n > 5000:
                primary = quick_sort_meta
                reasons.append(f"Dữ liệu kích thước lớn (n = {n:,}) và phân bố ngẫu nhiên.")
                reasons.append("Quick Sort tận dụng tối đa kiến trúc CPU Cache L1/L2, thực thi nhanh hơn trong bộ nhớ RAM thực tế.")
                if merge_sort_meta:
                    alternatives.append(merge_sort_meta)
                    trade_offs.append("Merge Sort là phương án thay thế an toàn hơn nếu cần bảo đảm trần O(n log n) không bị suy biến worst-case.")
                warnings.append("Lưu ý: Quick Sort có thể chạm worst case O(n²) nếu dữ liệu đặc thù. Trong khi Merge Sort cam kết 100% O(n log n).")
            else:
                primary = merge_sort_meta
                reasons.append(f"Kích thước trung bình (n = {n:,}). Merge Sort bảo đảm hiệu suất ổn định O(n log n) tuyệt đối.")
                reasons.append("Không lo lắng về rủi ro suy biến O(n²) như Quick Sort.")
                if quick_sort_meta:
                    alternatives.append(quick_sort_meta)
                trade_offs.append("Quick Sort thường có thời gian thực tế nhanh hơn 20-40% trên RAM, nhưng Merge Sort đảm bảo độ tin cậy và ổn định.")

        complexity_summary = (
            f"Thời gian đề xuất: {primary.average_case} (Worst: {primary.worst_case}) | "
            f"Không gian bộ nhớ: {primary.space_complexity} | "
            f"Tính chất: {'In-place' if primary.is_in_place else 'Cần bộ nhớ phụ'}, "
            f"{'Ổn định (Stable)' if primary.is_stable else 'Không ổn định (Unstable)'}"
        )

        return RecommendationResult(
            problem_type="Sắp xếp dữ liệu (Sorting)",
            candidates=candidates,
            primary_recommendation=primary,
            alternative_recommendations=alternatives,
            reasoning_points=reasons,
            trade_offs=trade_offs,
            caveats_and_warnings=warnings,
            complexity_summary=complexity_summary
        )

    @staticmethod
    def _recommend_searching(
        analysis: InputAnalysisResult,
        constraints: RecommendationConstraints,
        candidates: List[AlgorithmMetadata]
    ) -> RecommendationResult:
        n = analysis.size
        reasons: List[str] = []
        trade_offs: List[str] = []
        warnings: List[str] = []
        alternatives: List[AlgorithmMetadata] = []

        linear_meta = registry.get_metadata("linear_search")
        binary_meta = registry.get_metadata("binary_search")
        q = constraints.query_count

        if analysis.is_sorted_asc:
            primary = binary_meta
            reasons.append("Dữ liệu ĐÃ ĐƯỢC SẮP XẾP TĂNG DẦN sẵn.")
            reasons.append(f"Binary Search khai thác tính thứ tự để giảm không gian tìm kiếm với tốc độ vượt trội O(log n).")
            reasons.append(f"Với n = {n:,}, Binary Search chỉ mất tối đa ~{int(analysis.size.bit_length())} phép so sánh (thay vì {n:,} của Linear Search).")
            if linear_meta:
                alternatives.append(linear_meta)
            trade_offs.append("Linear Search chỉ nhanh hơn nếu mục tiêu vô tình nằm ngay phần tử đầu tiên (Best case O(1)).")

        else:
            # Data is NOT sorted
            if q == 1:
                primary = linear_meta
                reasons.append("Dữ liệu CHƯA SẮP XẾP và số lượng truy vấn chỉ có 1 lần (q = 1).")
                reasons.append(f"Chi phí tìm kiếm tuần tự: O(n) = ~{n:,} phép toán.")
                reasons.append(f"Nếu muốn dùng Binary Search, bắt buộc phải sắp xếp trước tốn O(n log n) = ~{int(n * analysis.size.bit_length()):,} phép toán.")
                reasons.append("Vì vậy, tiền xử lý sắp xếp cho 1 lần tìm duy nhất là lãng phí tài nguyên!")
                if binary_meta:
                    alternatives.append(binary_meta)
                trade_offs.append("Đánh đổi: Chấp nhận O(n) cho một lần tìm kiếm để tiết kiệm toàn bộ chi phí O(n log n) sắp xếp.")
            else:
                # Multiple queries: q > 1
                # Cost of Linear Search: q * O(n)
                # Cost of Sort + Binary Search: O(n log n) + q * O(log n)
                sort_cost = n * max(1, analysis.size.bit_length())
                bin_total_cost = sort_cost + q * max(1, analysis.size.bit_length())
                lin_total_cost = q * n

                if bin_total_cost < lin_total_cost:
                    primary = binary_meta
                    reasons.append(f"Dữ liệu chưa sắp xếp NHƯNG có nhiều lượt truy vấn liên tục (q = {q:,} lượt).")
                    reasons.append(f"Chi phí Linear Search: q × O(n) ≈ {lin_total_cost:,} phép toán.")
                    reasons.append(f"Chi phí Tiền xử lý (Sort) + Binary Search: O(n log n) + q × O(log n) ≈ {bin_total_cost:,} phép toán.")
                    reasons.append("Khấu hao chi phí tiền xử lý: Số lượng truy vấn đủ lớn để việc sắp xếp 1 lần mang lại lợi nhuận hiệu năng khổng lồ.")
                    if linear_meta:
                        alternatives.append(linear_meta)
                    trade_offs.append("Cần chi trả chi phí sắp xếp mảng ban đầu và bộ nhớ phụ nếu dùng thuật toán sắp xếp ngoài.")
                else:
                    primary = linear_meta
                    reasons.append(f"Số lượng truy vấn (q = {q}) chưa đủ lớn để bù đắp chi phí tiền xử lý sắp xếp O(n log n).")
                    if binary_meta:
                        alternatives.append(binary_meta)
                    trade_offs.append("Nếu số lượt truy vấn tăng lên trong tương lai, cần chuyển đổi sang mô hình Pre-sorting + Binary Search.")

        complexity_summary = (
            f"Thời gian đề xuất: {primary.average_case} (Worst: {primary.worst_case}) | "
            f"Không gian: {primary.space_complexity}"
        )

        return RecommendationResult(
            problem_type="Tìm kiếm dữ liệu (Searching)",
            candidates=candidates,
            primary_recommendation=primary,
            alternative_recommendations=alternatives,
            reasoning_points=reasons,
            trade_offs=trade_offs,
            caveats_and_warnings=warnings,
            complexity_summary=complexity_summary
        )
