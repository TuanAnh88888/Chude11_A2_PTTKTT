"""
Algorithm Analysis & Simulation Platform
UI - Performance Benchmark Engine View (ĐO HIỆU NĂNG THUẬT TOÁN)
"""
import os
import threading
from tkinter import filedialog, messagebox
from typing import Any, Dict, List, Optional
import customtkinter as ctk

from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.benchmark.metrics import (
    MultiDistributionBenchmarkResult,
    MultiSizeBenchmarkResult,
    SingleBenchmarkMetric,
)
from core.benchmark.runner import BenchmarkRunner
from infrastructure.data.generator import DataDistribution, DataGenerator
from infrastructure.export.report_exporter import ReportExporter
from ui.components.chart_canvas import ChartCanvas


class BenchmarkView(ctk.CTkScrollableFrame):
    """Upgraded benchmark engine measuring real execution times, operations, correctness, and multi-case analytics."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        # Benchmark State
        self.is_running = False
        self.cancel_event = threading.Event()
        self.latest_single_metrics: List[SingleBenchmarkMetric] = []
        self.latest_multi_size: Optional[MultiSizeBenchmarkResult] = None
        self.latest_multi_dist: Optional[MultiDistributionBenchmarkResult] = None

        self._build_ui()

    def _build_ui(self):
        # Header title
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 4))

        lbl_head = ctk.CTkLabel(
            header,
            text="ĐO HIỆU NĂNG THUẬT TOÁN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w")

        lbl_desc = ctk.CTkLabel(
            header,
            text="Đo lường thời gian thực tế bằng `time.perf_counter()`, đếm số phép so sánh, hoán đổi trên cùng bản sao dữ liệu đầu vào.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", pady=(2, 0))

        # Main Configuration Card
        cfg_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        cfg_frame.pack(fill="x", padx=16, pady=8)

        # Row 1: Problem category & Data distribution selection
        row1 = ctk.CTkFrame(cfg_frame, fg_color="transparent")
        row1.pack(fill="x", padx=16, pady=(14, 8))
        row1.grid_columnconfigure((0, 1), weight=1)

        # Problem category
        box_problem = ctk.CTkFrame(row1, fg_color="transparent")
        box_problem.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(box_problem, text="Loại bài toán:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.combo_category = ctk.CTkComboBox(
            box_problem,
            values=["Sắp xếp (Sorting)", "Tìm kiếm (Searching)"],
            width=260,
            command=self._on_category_changed
        )
        self.combo_category.set("Sắp xếp (Sorting)")
        self.combo_category.pack(anchor="w", pady=(4, 0))

        # Data Distribution
        box_dist = ctk.CTkFrame(row1, fg_color="transparent")
        box_dist.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(box_dist, text="Dữ liệu đầu vào:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.combo_distribution = ctk.CTkComboBox(
            box_dist,
            values=[
                "Ngẫu nhiên (Random)",
                "Đã sắp xếp (Sorted)",
                "Đảo ngược (Reverse Sorted)",
                "Gần sắp xếp (Nearly Sorted)",
                "Nhiều phần tử trùng (Duplicates)",
                "Khảo sát tất cả các trường hợp"
            ],
            width=260
        )
        self.combo_distribution.set("Ngẫu nhiên (Random)")
        self.combo_distribution.pack(anchor="w", pady=(4, 0))

        # Row 2: Algorithm Checklist
        box_algs = ctk.CTkFrame(cfg_frame, fg_color="transparent")
        box_algs.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(box_algs, text="Chọn thuật toán tham gia đo:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 6))
        self.algs_checkbox_container = ctk.CTkFrame(box_algs, fg_color="transparent")
        self.algs_checkbox_container.pack(fill="x")
        self.alg_checks: Dict[str, ctk.CTkCheckBox] = {}
        self._populate_algorithm_checkboxes(AlgorithmCategory.SORTING)

        # Row 3: Data Size & Runs Count
        row3 = ctk.CTkFrame(cfg_frame, fg_color="transparent")
        row3.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(row3, text="Kích thước dữ liệu (n):", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 6))
        self.entry_size = ctk.CTkEntry(row3, width=110)
        self.entry_size.insert(0, "1000")
        self.entry_size.pack(side="left", padx=(0, 16))

        # Preset sizes chips
        for sz_label in ["100", "500", "1.000", "5.000", "10.000"]:
            btn_sz = ctk.CTkButton(
                row3,
                text=sz_label,
                width=55,
                height=26,
                font=ctk.CTkFont(size=10),
                fg_color="#334155",
                hover_color="#475569",
                command=lambda val=sz_label.replace(".", ""): self._set_preset_size(val)
            )
            btn_sz.pack(side="left", padx=2)

        ctk.CTkLabel(row3, text="Số lần chạy:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(20, 6))
        self.combo_runs = ctk.CTkComboBox(row3, values=["1", "3", "5", "10"], width=75)
        self.combo_runs.set("5")
        self.combo_runs.pack(side="left")

        # Multi-size scaling checkbox
        self.check_multisize = ctk.CTkCheckBox(
            cfg_frame,
            text="Đo mở rộng theo nhiều kích thước (n = 100, 500, 1000, 5000, 10000) để vẽ biểu đồ tăng trưởng",
            font=ctk.CTkFont(size=11)
        )
        self.check_multisize.pack(anchor="w", padx=16, pady=(6, 12))

        # Action Buttons Row (BẮT ĐẦU ĐO HIỆU NĂNG + HỦY)
        btn_action_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_action_row.pack(fill="x", padx=16, pady=6)

        self.btn_start = ctk.CTkButton(
            btn_action_row,
            text="⚡ BẮT ĐẦU ĐO HIỆU NĂNG",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=44,
            corner_radius=8,
            command=self._start_benchmark
        )
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_cancel = ctk.CTkButton(
            btn_action_row,
            text="⏹ HỦY BENCHMARK",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            height=44,
            width=140,
            state="disabled",
            command=self._cancel_benchmark
        )
        self.btn_cancel.pack(side="left", padx=4)

        self.btn_export = ctk.CTkButton(
            btn_action_row,
            text="📥 Xuất báo cáo (CSV/TXT)",
            font=ctk.CTkFont(size=12),
            fg_color="#059669",
            hover_color="#047857",
            height=44,
            width=180,
            command=self._export_results
        )
        self.btn_export.pack(side="right")

        # Progress bar & status
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=16, pady=(4, 2))

        self.lbl_progress = ctk.CTkLabel(
            self,
            text="Sẵn sàng thực hiện phép đo.",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        self.lbl_progress.pack(anchor="w", padx=16, pady=(0, 10))

        # Area 1: Summary Results Table
        table_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        table_frame.pack(fill="x", padx=16, pady=8)

        lbl_tbl_title = ctk.CTkLabel(
            table_frame,
            text="1. BẢNG KẾT QUẢ ĐO HIỆU NĂNG",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3B82F6"
        )
        lbl_tbl_title.pack(anchor="w", padx=16, pady=(14, 6))

        self.box_summary_table = ctk.CTkTextbox(
            table_frame,
            height=160,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.box_summary_table.pack(fill="x", padx=16, pady=(0, 10))
        self.box_summary_table.insert("1.0", "Chưa có kết quả. Chọn thuật toán và bấm 'BẮT ĐẦU ĐO HIỆU NĂNG'.")
        self.box_summary_table.configure(state="disabled")

        # Area 1b: Per-Run Table (Lần 1, 2, 3, 4, 5, Trung bình)
        ctk.CTkLabel(
            table_frame,
            text="CHI TIẾT TỪNG LẦN CHẠY BENCHMARK:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=16, pady=(4, 4))

        self.box_runs_table = ctk.CTkTextbox(
            table_frame,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.box_runs_table.pack(fill="x", padx=16, pady=(0, 14))
        self.box_runs_table.configure(state="disabled")

        # Area 2: Analytical Explanation & Case Suitability
        analysis_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        analysis_frame.pack(fill="x", padx=16, pady=8)
        analysis_frame.grid_columnconfigure((0, 1), weight=1)

        # Left Column: General Performance Explanation
        box_left_ana = ctk.CTkFrame(analysis_frame, fg_color="transparent")
        box_left_ana.grid(row=0, column=0, padx=16, pady=14, sticky="nsew")

        ctk.CTkLabel(
            box_left_ana,
            text="2. PHÂN TÍCH HIỆU NĂNG THỰC NGHIỆM",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#10B981"
        ).pack(anchor="w", pady=(0, 6))

        self.box_analysis = ctk.CTkTextbox(
            box_left_ana,
            height=190,
            font=ctk.CTkFont(size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.box_analysis.pack(fill="both", expand=True)
        self.box_analysis.insert("1.0", "Phân tích số liệu và lý do chênh lệch thời gian sẽ hiển thị tại đây sau khi đo.")
        self.box_analysis.configure(state="disabled")

        # Right Column: Performance by Data Type / Case Analysis
        box_right_case = ctk.CTkFrame(analysis_frame, fg_color="transparent")
        box_right_case.grid(row=0, column=1, padx=16, pady=14, sticky="nsew")

        ctk.CTkLabel(
            box_right_case,
            text="3. HIỆU NĂNG THEO TRƯỜNG HỢP DỮ LIỆU",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#A855F7"
        ).pack(anchor="w", pady=(0, 6))

        self.box_case_analysis = ctk.CTkTextbox(
            box_right_case,
            height=190,
            font=ctk.CTkFont(size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.box_case_analysis.pack(fill="both", expand=True)
        self.box_case_analysis.insert("1.0", "Đánh giá các trường hợp dữ liệu (Random, Sorted, Reverse, Nearly Sorted, Duplicates).")
        self.box_case_analysis.configure(state="disabled")

        # Area 3: Visual Charts (3 Charts)
        charts_container = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        charts_container.pack(fill="x", padx=16, pady=8)

        chart_head_row = ctk.CTkFrame(charts_container, fg_color="transparent")
        chart_head_row.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            chart_head_row,
            text="4. BIỂU ĐỒ HIỆU NĂNG (VISUALIZATION)",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#F59E0B"
        ).pack(side="left")

        # Chart selector tabs
        self.seg_chart = ctk.CTkSegmentedButton(
            chart_head_row,
            values=[
                "Biểu đồ 1: So sánh thời gian (Bar)",
                "Biểu đồ 2: Thời gian vs Kích thước (n)",
                "Biểu đồ 3: Hiệu năng theo loại dữ liệu"
            ],
            command=self._switch_chart
        )
        self.seg_chart.set("Biểu đồ 1: So sánh thời gian (Bar)")
        self.seg_chart.pack(side="right")

        self.chart = ChartCanvas(charts_container, width=760, height=360)
        self.chart.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Area 4: Final Scientific Verdict (NO absolute best claim)
        verdict_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#EFF6FF", "#172554"), border_width=1, border_color="#3B82F6")
        verdict_frame.pack(fill="x", padx=16, pady=(8, 20))

        lbl_verdict_title = ctk.CTkLabel(
            verdict_frame,
            text="5. KẾT LUẬN THỰC NGHIỆM & ĐÁNH GIÁ ĐIỀU KIỆN",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2563EB"
        )
        lbl_verdict_title.pack(anchor="w", padx=16, pady=(12, 6))

        self.lbl_verdict_content = ctk.CTkLabel(
            verdict_frame,
            text="Chưa có kết luận. Vui lòng thực hiện đo hiệu năng.",
            font=ctk.CTkFont(size=12),
            text_color=("#1E293B", "#DBEAFE"),
            justify="left",
            wraplength=760
        )
        self.lbl_verdict_content.pack(anchor="w", padx=16, pady=(0, 14))

    def _set_preset_size(self, size_str: str):
        self.entry_size.delete(0, "end")
        self.entry_size.insert(0, size_str)

    def _on_category_changed(self, choice: str):
        is_searching = "Searching" in choice
        cat = AlgorithmCategory.SEARCHING if is_searching else AlgorithmCategory.SORTING
        self._populate_algorithm_checkboxes(cat)

    def _populate_algorithm_checkboxes(self, category: AlgorithmCategory):
        for w in self.algs_checkbox_container.winfo_children():
            w.destroy()
        self.alg_checks.clear()

        algs = registry.get_by_category(category)
        for alg in algs:
            name = alg.metadata.name
            disp = alg.metadata.display_name.split("–")[0].strip()
            chk = ctk.CTkCheckBox(self.algs_checkbox_container, text=disp)
            chk.select()
            chk.pack(side="left", padx=8, pady=4)
            self.alg_checks[name] = chk

    def _get_selected_algorithm_names(self) -> List[str]:
        return [name for name, chk in self.alg_checks.items() if chk.get()]

    def _map_distribution_str(self, raw: str) -> str:
        if "Sorted" in raw and "Nearly" not in raw and "Reverse" not in raw:
            return DataDistribution.SORTED_ASC
        elif "Reverse" in raw:
            return DataDistribution.SORTED_DESC
        elif "Nearly" in raw:
            return DataDistribution.NEARLY_SORTED
        elif "Duplicate" in raw or "trùng" in raw:
            return DataDistribution.MANY_DUPLICATES
        return DataDistribution.RANDOM

    def _start_benchmark(self):
        selected_algs = self._get_selected_algorithm_names()
        if not selected_algs:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất 1 thuật toán để đo!")
            return

        try:
            size_n = int(self.entry_size.get().strip().replace(".", "").replace(",", ""))
            if size_n <= 0:
                raise ValueError("Kích thước n phải lớn hơn 0")
        except ValueError:
            messagebox.showerror("Lỗi", "Kích thước dữ liệu n không hợp lệ!")
            return

        runs = int(self.combo_runs.get())
        is_multisize = bool(self.check_multisize.get())
        dist_choice = self.combo_distribution.get()

        # UI state during run
        self.is_running = True
        self.cancel_event.clear()
        self.btn_start.configure(state="disabled")
        self.btn_cancel.configure(state="normal")
        self.progress_bar.set(0)

        # Worker thread
        thread = threading.Thread(
            target=self._benchmark_worker,
            args=(selected_algs, size_n, runs, is_multisize, dist_choice)
        )
        thread.daemon = True
        thread.start()

    def _cancel_benchmark(self):
        if self.is_running:
            self.cancel_event.set()
            self.lbl_progress.configure(text="Đang hủy benchmark theo yêu cầu người dùng...")

    def _benchmark_worker(
        self,
        algorithm_names: List[str],
        size_n: int,
        runs: int,
        is_multisize: bool,
        dist_choice: str
    ):
        try:
            def progress_cb(cur, total, msg):
                frac = cur / total if total > 0 else 0
                self.after(0, lambda: self._update_progress_ui(frac, msg))

            # Case A: Multi-distribution testing
            if "Khảo sát tất cả" in dist_choice:
                distributions = [
                    DataDistribution.RANDOM,
                    DataDistribution.SORTED_ASC,
                    DataDistribution.SORTED_DESC,
                    DataDistribution.NEARLY_SORTED,
                    DataDistribution.MANY_DUPLICATES
                ]
                multi_dist_res = BenchmarkRunner.run_multi_distributions(
                    algorithm_names=algorithm_names,
                    size=size_n,
                    distributions=distributions,
                    runs=runs,
                    warmup=True,
                    progress_callback=progress_cb,
                    cancel_event=self.cancel_event
                )
                self.latest_multi_dist = multi_dist_res
                # Flatten single metrics using random
                self.latest_single_metrics = multi_dist_res.metrics_by_dist.get(DataDistribution.RANDOM, [])

            # Case B: Multi-size scaling
            elif is_multisize:
                sizes = [100, 500, 1000, 2000, 5000]
                if size_n not in sizes and size_n <= 10000:
                    sizes.append(size_n)
                    sizes.sort()

                dist = self._map_distribution_str(dist_choice)
                multi_size_res = BenchmarkRunner.run_multi_sizes(
                    algorithm_names=algorithm_names,
                    sizes=sizes,
                    data_generator=lambda sz: DataGenerator.generate(sz, distribution=dist),
                    runs=runs,
                    warmup=True,
                    data_distribution=dist,
                    progress_callback=progress_cb,
                    cancel_event=self.cancel_event
                )
                self.latest_multi_size = multi_size_res
                # Save the metrics for size_n or last size
                target_sz = size_n if size_n in sizes else sizes[-1]
                self.latest_single_metrics = [
                    m for alg in algorithm_names
                    for m in multi_size_res.metrics_by_alg.get(alg, [])
                    if m.size == target_sz
                ]

            # Case C: Standard single dataset benchmark
            else:
                dist = self._map_distribution_str(dist_choice)
                dataset = DataGenerator.generate(size=size_n, distribution=dist)
                target_val = dataset[len(dataset) // 2] if dataset else None

                single_metrics = BenchmarkRunner.run_single_dataset(
                    algorithm_names=algorithm_names,
                    data=dataset,
                    runs=runs,
                    warmup=True,
                    target=target_val,
                    data_distribution=dist,
                    progress_callback=progress_cb,
                    cancel_event=self.cancel_event
                )
                self.latest_single_metrics = single_metrics

            self.controller.last_benchmark_results = self.latest_single_metrics

            # Render all views on completion
            self.after(0, self._render_all_benchmark_results)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi thực thi", str(e)))
        finally:
            self.is_running = False
            self.after(0, lambda: self.btn_start.configure(state="normal"))
            self.after(0, lambda: self.btn_cancel.configure(state="disabled"))

    def _update_progress_ui(self, fraction: float, message: str):
        self.progress_bar.set(fraction)
        self.lbl_progress.configure(text=f"[{int(fraction * 100)}%] {message}")

    def _render_all_benchmark_results(self):
        if self.cancel_event.is_set():
            self.lbl_progress.configure(text="Benchmark đã dừng theo yêu cầu của bạn.")
        else:
            self.progress_bar.set(1.0)
            self.lbl_progress.configure(text="Hoàn thành đo lường hiệu năng 100%!")

        metrics = self.latest_single_metrics
        if not metrics:
            return

        # 1. Render Summary Table
        self.box_summary_table.configure(state="normal")
        self.box_summary_table.delete("1.0", "end")

        header = f"{'Thuật toán':<22} | {'Avg Time':<12} | {'Min':<10} | {'Max':<10} | {'Compare':<11} | {'Swap':<10} | {'Space':<9} | {'Chính xác'}\n"
        sep = "=" * 105 + "\n"
        self.box_summary_table.insert("end", header)
        self.box_summary_table.insert("end", sep)

        for m in metrics:
            disp = m.display_name.split("–")[0].strip()
            swaps_str = f"{m.swaps:,}" if m.swaps > 0 else "-"
            valid_str = "✓ ĐÚNG" if m.is_correct else f"❌ LỖI ({m.validation_error})"
            row = (
                f"{disp:<22} | "
                f"{m.avg_time_ms:>8.3f} ms | "
                f"{m.min_time_ms:>7.3f} ms | "
                f"{m.max_time_ms:>7.3f} ms | "
                f"{m.comparisons:>11,} | "
                f"{swaps_str:>10} | "
                f"{m.space_complexity:<9} | "
                f"{valid_str}\n"
            )
            self.box_summary_table.insert("end", row)
        self.box_summary_table.configure(state="disabled")

        # 2. Render Per-Run Table (Lần 1, 2, 3, 4, 5, Trung bình)
        self.box_runs_table.configure(state="normal")
        self.box_runs_table.delete("1.0", "end")

        max_runs = max((len(m.runs_times_ms) for m in metrics), default=1)
        runs_header = f"{'Thuật toán':<22} | " + " | ".join([f"Lần {i+1:<5}" for i in range(max_runs)]) + " | Trung bình\n"
        sep_runs = "-" * len(runs_header) + "\n"
        self.box_runs_table.insert("end", runs_header)
        self.box_runs_table.insert("end", sep_runs)

        for m in metrics:
            disp = m.display_name.split("–")[0].strip()
            times_str = " | ".join([f"{t:6.3f}ms" for t in m.runs_times_ms])
            row = f"{disp:<22} | {times_str} | {m.avg_time_ms:6.3f}ms\n"
            self.box_runs_table.insert("end", row)

        self.box_runs_table.configure(state="disabled")

        # 3. Render Analytical Explanation
        self._render_analytical_explanation(metrics)

        # 4. Render Case Analysis
        self._render_case_analysis(metrics)

        # 5. Render Charts
        self._switch_chart(self.seg_chart.get())

        # 6. Render Scientific Verdict (NO absolute best claim)
        self._render_verdict(metrics)

    def _render_analytical_explanation(self, metrics: List[SingleBenchmarkMetric]):
        self.box_analysis.configure(state="normal")
        self.box_analysis.delete("1.0", "end")

        lines = []
        fastest_metric = min(metrics, key=lambda m: m.avg_time_ms)
        slowest_metric = max(metrics, key=lambda m: m.avg_time_ms)
        dist = metrics[0].data_distribution
        n = metrics[0].size

        lines.append(f"• Trong thử nghiệm với n = {n:,} và phân bố '{dist}':")
        lines.append(f"  - {fastest_metric.display_name.split('–')[0].strip()} đạt thời gian trung bình thấp nhất ({fastest_metric.avg_time_ms:.3f} ms) với {fastest_metric.comparisons:,} phép so sánh.")
        lines.append(f"  - {slowest_metric.display_name.split('–')[0].strip()} mất nhiều thời gian nhất ({slowest_metric.avg_time_ms:.3f} ms).")

        # Explain why
        lines.append("\n• Giải thích nguyên nhân chênh lệch:")
        has_log_algs = any("log" in m.theoretical_complexity for m in metrics)
        has_quad_algs = any("²" in m.theoretical_complexity for m in metrics)

        if has_log_algs and has_quad_algs:
            lines.append("  - Sự phân kỳ mạnh mẽ bắt nguồn từ độ phức tạp tiệm cận: các thuật toán O(n log n) tăng trưởng logarit tuyến tính, trong khi O(n²) bùng nổ theo hàm bậc hai.")

        if any(m.algorithm_name == "insertion_sort" for m in metrics):
            ins = next(m for m in metrics if m.algorithm_name == "insertion_sort")
            if "Sorted" in dist or "Nearly" in dist:
                lines.append(f"  - Insertion Sort phát huy tối đa lợi thế khi dữ liệu có thứ tự sẵn/gần sắp xếp (chỉ tốn {ins.comparisons:,} phép so sánh, Best Case O(n)).")

        lines.append(f"\n• Đo lường độc lập bằng `perf_counter` bảo đảm tính trung thực tuyệt đối của số liệu.")

        self.box_analysis.insert("1.0", "\n".join(lines))
        self.box_analysis.configure(state="disabled")

    def _render_case_analysis(self, metrics: List[SingleBenchmarkMetric]):
        self.box_case_analysis.configure(state="normal")
        self.box_case_analysis.delete("1.0", "end")

        lines = []
        lines.append("【HIỆU NĂNG THEO CÁC TRƯỜNG HỢP DỮ LIỆU】\n")
        lines.append("• Dữ liệu Ngẫu nhiên (Random):")
        lines.append("  Quick Sort và Merge Sort đạt hiệu năng vượt trội nhờ độ phức tạp trung bình O(n log n). Quick Sort thường nhỉnh hơn nhờ hằng số ẩn và bộ nhớ đệm cache nhỏ.")
        lines.append("\n• Dữ liệu Gần sắp xếp (Nearly Sorted):")
        lines.append("  Insertion Sort là ứng viên hàng đầu do chi phí dịch chuyển cực ít, tiệm cận thời gian O(n), không tốn bộ nhớ phụ.")
        lines.append("\n• Dữ liệu Đảo ngược (Reverse Sorted):")
        lines.append("  Bubble Sort và Insertion Sort rơi vào Worst Case O(n²). Quick Sort nếu chọn pivot đầu/cuối có thể suy biến; Merge Sort luôn đảm bảo an toàn tuyệt đối O(n log n).")
        lines.append("\n• Dữ liệu Lớn (n > 5.000):")
        lines.append("  Các thuật toán O(n log n) là bắt buộc. Thuật toán O(n²) không khả thi trong môi trường thực tế.")

        self.box_case_analysis.insert("1.0", "\n".join(lines))
        self.box_case_analysis.configure(state="disabled")

    def _switch_chart(self, chart_choice: str):
        metrics = self.latest_single_metrics
        if not metrics:
            return

        if "Biểu đồ 1" in chart_choice:
            # Bar chart: Algorithm vs Time
            names = [m.display_name.split("–")[0].strip() for m in metrics]
            times = [m.avg_time_ms for m in metrics]
            self.chart.plot_algorithm_bar_chart(
                names,
                times,
                title=f"Biểu đồ 1: Thời gian trung bình (ms) trên n = {metrics[0].size:,} ({metrics[0].data_distribution})"
            )

        elif "Biểu đồ 2" in chart_choice:
            # Line chart: Time vs Input Size
            if self.latest_multi_size and self.latest_multi_size.plot_series:
                self.chart.plot_time_vs_size(
                    self.latest_multi_size.sizes,
                    self.latest_multi_size.plot_series,
                    title="Biểu đồ 2: Tăng trưởng thời gian thực thi (ms) theo quy mô n"
                )
            else:
                # Generate sample multi-size points from current algorithms for illustration
                sizes = [100, 500, 1000, 2000, 5000]
                series = {}
                for m in metrics:
                    alg = registry.get_algorithm(m.algorithm_name)
                    points = []
                    for sz in sizes:
                        d = DataGenerator.generate(sz)
                        st = alg.run_benchmark(d)
                        points.append(st.execution_time * 1000.0)
                    series[m.display_name.split("–")[0].strip()] = points
                self.chart.plot_time_vs_size(sizes, series, title="Biểu đồ 2: Thời gian thực thi (ms) theo kích thước n")

        elif "Biểu đồ 3" in chart_choice:
            # Grouped bar chart by data distribution
            if self.latest_multi_dist and self.latest_multi_dist.plot_series_by_alg:
                groups = [d.split("(")[0].strip() for d in self.latest_multi_dist.distributions]
                series = {
                    registry.get_metadata(alg).display_name.split("–")[0].strip(): vals
                    for alg, vals in self.latest_multi_dist.plot_series_by_alg.items()
                }
                self.chart.plot_grouped_bar_chart(groups, series, title="Biểu đồ 3: So sánh hiệu năng theo loại dữ liệu")
            else:
                # Run quick measurements across 4 standard distributions
                dists = [
                    DataDistribution.RANDOM,
                    DataDistribution.SORTED_ASC,
                    DataDistribution.SORTED_DESC,
                    DataDistribution.NEARLY_SORTED
                ]
                groups = ["Random", "Sorted", "Reverse", "Nearly Sorted"]
                series = {}
                sz = min(1000, metrics[0].size)
                for m in metrics:
                    alg = registry.get_algorithm(m.algorithm_name)
                    vals = []
                    for dist in dists:
                        d = DataGenerator.generate(sz, distribution=dist)
                        st = alg.run_benchmark(d)
                        vals.append(st.execution_time * 1000.0)
                    series[m.display_name.split("–")[0].strip()] = vals
                self.chart.plot_grouped_bar_chart(groups, series, title=f"Biểu đồ 3: Hiệu năng theo loại dữ liệu (n = {sz:,})")

    def _render_verdict(self, metrics: List[SingleBenchmarkMetric]):
        fastest = min(metrics, key=lambda m: m.avg_time_ms)
        fastest_name = fastest.display_name.split("–")[0].strip()
        n = metrics[0].size
        dist = metrics[0].data_distribution

        verdict_text = (
            f"KẾT LUẬN THỰC NGHIỆM:\n"
            f"• Theo tiêu chí: Thời gian thực thi, số phép so sánh, kích thước dữ liệu n = {n:,} và phân bố '{dist}', "
            f"thuật toán [{fastest_name}] là THUẬT TOÁN CÓ HIỆU NĂNG CAO NHẤT trong thử nghiệm này ({fastest.avg_time_ms:.3f} ms).\n"
            f"• LƯU Ý KHOA HỌC: Kết quả này KHÔNG đồng nghĩa [{fastest_name}] luôn là thuật toán tốt nhất tuyệt đối trong mọi tình huống. "
            f"Nếu yêu cầu bài toán thay đổi (ví dụ: cần bảo toàn tính ổn định Stable, hạn chế tối đa bộ nhớ phụ In-place, "
            f"hoặc dữ liệu có tính chất đặc thù gần có thứ tự), các thuật toán khác như Merge Sort hay Insertion Sort có thể phù hợp hơn.\n"
            f"• Kết quả trên phản ánh chính xác môi trường và bộ dữ liệu đã được thử nghiệm thực tế."
        )
        self.lbl_verdict_content.configure(text=verdict_text)

    def _export_results(self):
        if not self.latest_single_metrics:
            messagebox.showwarning("Thông báo", "Chưa có kết quả để xuất báo cáo!")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV file", "*.csv"), ("Text Report", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()
        if ext == ".txt":
            ok = ReportExporter.export_text(
                filepath=path,
                problem_title=f"Đo hiệu năng thuật toán ({self.combo_category.get()})",
                input_analysis=self.controller.current_analysis,
                recommendation=self.controller.current_recommendation,
                benchmarks=self.latest_single_metrics,
                conclusions=self.lbl_verdict_content.cget("text")
            )
        else:
            ok = ReportExporter.export_csv(path, self.latest_single_metrics)

        if ok:
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo thành công ra file:\n{path}")
