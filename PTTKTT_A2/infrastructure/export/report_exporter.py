"""
Algorithm Analysis & Simulation Platform
Infrastructure - Report Exporter (TXT, CSV, Markdown)
"""
import csv
import datetime
import os
from typing import Any, List, Optional
from core.benchmark.metrics import SingleBenchmarkMetric
from core.complexity.analyzer import InputAnalysisResult
from core.recommendation.engine import RecommendationResult


class ReportExporter:
    """Exports comprehensive algorithm analysis reports in TXT, CSV, or Markdown formats."""

    @staticmethod
    def export_text(
        filepath: str,
        problem_title: str,
        input_analysis: Optional[InputAnalysisResult],
        recommendation: Optional[RecommendationResult],
        benchmarks: Optional[List[SingleBenchmarkMetric]],
        conclusions: Optional[str] = None
    ) -> bool:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = []
        lines.append("=" * 70)
        lines.append("BÁO CÁO PHÂN TÍCH VÀ ĐÁNH GIÁ THUẬT TOÁN")
        lines.append(f"Hệ thống: Algorithm Analysis & Simulation Platform")
        lines.append(f"Thời gian lập báo cáo: {timestamp}")
        lines.append(f"Bài toán: {problem_title}")
        lines.append("=" * 70)
        lines.append("")

        if input_analysis:
            lines.append("1. ĐẶC ĐIỂM DỮ LIỆU ĐẦU VÀO")
            lines.append("-" * 50)
            lines.append(f"• Số lượng phần tử (n): {input_analysis.size:,}")
            lines.append(f"• Kiểu dữ liệu: {input_analysis.data_type}")
            lines.append(f"• Miền giá trị: [{input_analysis.min_value} .. {input_analysis.max_value}]")
            lines.append(f"• Trạng thái thứ tự: {input_analysis.characteristic}")
            lines.append(f"• Trùng lặp: {input_analysis.duplicate_count:,} phần tử ({input_analysis.unique_percentage:.1f}% duy nhất)")
            lines.append(f"• Độ phân tán (Độ lệch chuẩn): {input_analysis.std_dev:.2f}")
            lines.append("")

        if recommendation:
            lines.append("2. KẾT QUẢ PHÂN TÍCH & ĐỀ XUẤT THUẬT TOÁN")
            lines.append("-" * 50)
            lines.append(f"• Thuật toán được đề xuất: {recommendation.primary_recommendation.display_name}")
            lines.append(f"• Tóm tắt độ phức tạp: {recommendation.complexity_summary}")
            lines.append("• Lý do đề xuất:")
            for r in recommendation.reasoning_points:
                lines.append(f"   - {r}")
            if recommendation.trade_offs:
                lines.append("• Phân tích đánh đổi (Trade-offs):")
                for t in recommendation.trade_offs:
                    lines.append(f"   - {t}")
            if recommendation.caveats_and_warnings:
                lines.append("• Cảnh báo / Rủi ro tiềm ẩn:")
                for w in recommendation.caveats_and_warnings:
                    lines.append(f"   - {w}")
            if recommendation.alternative_recommendations:
                alts = ", ".join([a.display_name for a in recommendation.alternative_recommendations])
                lines.append(f"• Phương án thay thế cân nhắc: {alts}")
            lines.append("")

        if benchmarks:
            lines.append("3. KẾT QUẢ THỰC NGHIỆM (BENCHMARK)")
            lines.append("-" * 50)
            header = f"{'Thuật toán':<30} | {'n':<8} | {'Avg (ms)':<10} | {'Min (ms)':<10} | {'Max (ms)':<10} | {'So sánh':<10} | {'Đổi chỗ':<10}"
            lines.append(header)
            lines.append("-" * len(header))
            for b in benchmarks:
                row = f"{b.display_name[:28]:<30} | {b.size:<8} | {b.avg_time_ms:<10.3f} | {b.min_time_ms:<10.3f} | {b.max_time_ms:<10.3f} | {b.comparisons:<10} | {b.swaps:<10}"
                lines.append(row)
            lines.append("")

        lines.append("4. KẾT LUẬN & ĐÁNH GIÁ")
        lines.append("-" * 50)
        lines.append(conclusions or "Kết quả thực nghiệm phù hợp với lý thuyết phân tích độ phức tạp tiệm cận Big-O.")
        lines.append("=" * 70)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True

    @staticmethod
    def export_csv(filepath: str, benchmarks: List[SingleBenchmarkMetric]) -> bool:
        if not benchmarks:
            return False

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Thuật toán", "Tên mã", "Kích thước n", "Số lần chạy",
                "Thời gian TB (ms)", "Thời gian Min (ms)", "Thời gian Max (ms)",
                "Số phép so sánh", "Số phép hoán đổi", "Số phép gán",
                "Độ phức tạp lý thuyết", "Bộ nhớ phụ"
            ])
            for b in benchmarks:
                writer.writerow([
                    b.display_name, b.algorithm_name, b.size, b.runs,
                    round(b.avg_time_ms, 4), round(b.min_time_ms, 4), round(b.max_time_ms, 4),
                    b.comparisons, b.swaps, b.assignments,
                    b.theoretical_complexity, b.space_complexity
                ])
        return True
