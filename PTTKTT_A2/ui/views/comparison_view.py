"""
Algorithm Analysis & Simulation Platform
UI - Dedicated Algorithm Comparison View (SO SÁNH THUẬT TOÁN)
"""
import os
import threading
from tkinter import filedialog, messagebox
from typing import Dict, List, Optional
import customtkinter as ctk

from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.benchmark.metrics import SingleBenchmarkMetric
from core.benchmark.runner import BenchmarkRunner
from infrastructure.data.generator import DataDistribution, DataGenerator
from infrastructure.export.report_exporter import ReportExporter
from ui.components.chart_canvas import ChartCanvas


class ComparisonView(ctk.CTkScrollableFrame):
    """Dedicated 2-3 algorithm comparative analysis engine matching academic standards."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        self.is_comparing = False
        self.cancel_event = threading.Event()
        self.latest_comp_metrics: List[SingleBenchmarkMetric] = []
        self.latest_multi_case_data: Optional[Dict[str, Dict[str, float]]] = None

        self._build_ui()

    def _build_ui(self):
        # Header
        lbl_head = ctk.CTkLabel(
            self,
            text="SO SÁNH THUẬT TOÁN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Chọn trực tiếp 2 hoặc 3 thuật toán để đối chiếu đa chiều: Lý thuyết Big-O, Thực nghiệm thời gian, Số phép toán và Trường hợp sử dụng.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Main Selection Form Card
        form_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        form_frame.pack(fill="x", padx=16, pady=8)

        # Form Title
        ctk.CTkLabel(
            form_frame,
            text="THIẾT LẬP SO SÁNH (2 HOẶC 3 THUẬT TOÁN)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w", padx=16, pady=(14, 10))

        # Row 1: Algorithm Dropdowns (Alg 1, Alg 2, Alg 3 optional)
        row_algs = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_algs.pack(fill="x", padx=16, pady=4)
        row_algs.grid_columnconfigure((0, 1, 2), weight=1)

        alg_options = [alg.metadata.display_name for alg in registry.get_all()]

        # Thuật toán 1
        box_a1 = ctk.CTkFrame(row_algs, fg_color="transparent")
        box_a1.grid(row=0, column=0, padx=6, sticky="ew")
        ctk.CTkLabel(box_a1, text="Thuật toán 1:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.combo_alg1 = ctk.CTkComboBox(box_a1, values=alg_options, width=220)
        self.combo_alg1.set("Quick Sort – Sắp xếp nhanh")
        self.combo_alg1.pack(fill="x", pady=4)

        # Thuật toán 2
        box_a2 = ctk.CTkFrame(row_algs, fg_color="transparent")
        box_a2.grid(row=0, column=1, padx=6, sticky="ew")
        ctk.CTkLabel(box_a2, text="Thuật toán 2:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.combo_alg2 = ctk.CTkComboBox(box_a2, values=alg_options, width=220)
        self.combo_alg2.set("Merge Sort – Sắp xếp trộn")
        self.combo_alg2.pack(fill="x", pady=4)

        # Thuật toán 3 (Tùy chọn)
        box_a3 = ctk.CTkFrame(row_algs, fg_color="transparent")
        box_a3.grid(row=0, column=2, padx=6, sticky="ew")
        ctk.CTkLabel(box_a3, text="Thuật toán 3 (Tùy chọn):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        alg3_options = ["(Không chọn)"] + alg_options
        self.combo_alg3 = ctk.CTkComboBox(box_a3, values=alg3_options, width=220)
        self.combo_alg3.set("Insertion Sort – Sắp xếp chèn")
        self.combo_alg3.pack(fill="x", pady=4)

        # Row 2: Data size, Data Type & Options
        row_data = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_data.pack(fill="x", padx=16, pady=10)
        row_data.grid_columnconfigure((0, 1), weight=1)

        # Size
        box_sz = ctk.CTkFrame(row_data, fg_color="transparent")
        box_sz.grid(row=0, column=0, padx=6, sticky="ew")
        ctk.CTkLabel(box_sz, text="Kích thước dữ liệu (n):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        sz_sub = ctk.CTkFrame(box_sz, fg_color="transparent")
        sz_sub.pack(fill="x", pady=4)
        self.entry_size = ctk.CTkEntry(sz_sub, width=90)
        self.entry_size.insert(0, "1000")
        self.entry_size.pack(side="left", padx=(0, 8))

        for p in ["100", "500", "1.000", "5.000"]:
            ctk.CTkButton(
                sz_sub,
                text=p,
                width=50,
                height=26,
                font=ctk.CTkFont(size=10),
                fg_color="#334155",
                hover_color="#475569",
                command=lambda val=p.replace(".", ""): self._set_size(val)
            ).pack(side="left", padx=2)

        # Data type
        box_type = ctk.CTkFrame(row_data, fg_color="transparent")
        box_type.grid(row=0, column=1, padx=6, sticky="ew")
        ctk.CTkLabel(box_type, text="Loại dữ liệu:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.combo_dist = ctk.CTkComboBox(
            box_type,
            values=[
                "Ngẫu nhiên (Random)",
                "Đã sắp xếp (Sorted)",
                "Đảo ngược (Reverse Sorted)",
                "Gần sắp xếp (Nearly Sorted)",
                "Nhiều phần tử trùng (Duplicates)",
                "Khảo sát đa trường hợp (Random, Sorted, Reverse...)"
            ],
            width=260
        )
        self.combo_dist.set("Ngẫu nhiên (Random)")
        self.combo_dist.pack(fill="x", pady=4)

        # Action Buttons
        btn_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(8, 16))

        self.btn_compare = ctk.CTkButton(
            btn_row,
            text="⚖️ BẮT ĐẦU SO SÁNH",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=42,
            command=self._start_comparison
        )
        self.btn_compare.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_cancel = ctk.CTkButton(
            btn_row,
            text="⏹ HỦY",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            height=42,
            width=90,
            state="disabled",
            command=self._cancel_comparison
        )
        self.btn_cancel.pack(side="left", padx=4)

        self.btn_export = ctk.CTkButton(
            btn_row,
            text="📥 Xuất bảng CSV/TXT",
            font=ctk.CTkFont(size=12),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=42,
            width=170,
            command=self._export_comparison
        )
        self.btn_export.pack(side="right")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=16, pady=4)

        self.lbl_progress = ctk.CTkLabel(self, text="Sẵn sàng so sánh.", font=ctk.CTkFont(size=11), text_color="#64748B")
        self.lbl_progress.pack(anchor="w", padx=16, pady=(0, 10))

        # ================= 4 OUTPUT AREAS (Section 26) =================
        # AREA 1: KẾT QUẢ BENCHMARK
        self.area1_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        self.area1_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(
            self.area1_frame,
            text="1. KẾT QUẢ BENCHMARK THỰC NGHIỆM",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w", padx=16, pady=(14, 6))

        self.txt_bench_results = ctk.CTkTextbox(
            self.area1_frame,
            height=140,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.txt_bench_results.pack(fill="x", padx=16, pady=(0, 14))
        self.txt_bench_results.insert("1.0", "Chọn 2 hoặc 3 thuật toán và nhấn 'BẮT ĐẦU SO SÁNH'.")
        self.txt_bench_results.configure(state="disabled")

        # AREA 2: SO SÁNH ĐỘ PHỨC TẠP
        self.area2_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        self.area2_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(
            self.area2_frame,
            text="2. SO SÁNH ĐỘ PHỨC TẠP LÝ THUYẾT & TÍNH CHẤT",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#10B981"
        ).pack(anchor="w", padx=16, pady=(14, 6))

        self.txt_complexity_table = ctk.CTkTextbox(
            self.area2_frame,
            height=140,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.txt_complexity_table.pack(fill="x", padx=16, pady=(0, 14))
        self.txt_complexity_table.configure(state="disabled")

        # AREA 3: BIỂU ĐỒ
        self.area3_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        self.area3_frame.pack(fill="x", padx=16, pady=8)

        chart_head = ctk.CTkFrame(self.area3_frame, fg_color="transparent")
        chart_head.pack(fill="x", padx=16, pady=(14, 6))

        ctk.CTkLabel(
            chart_head,
            text="3. BIỂU ĐỒ SO SÁNH TRỰC QUAN",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#F59E0B"
        ).pack(side="left")

        self.seg_chart_type = ctk.CTkSegmentedButton(
            chart_head,
            values=["Thời gian thực thi", "Số phép so sánh", "Đa trường hợp dữ liệu"],
            command=self._redraw_chart
        )
        self.seg_chart_type.set("Thời gian thực thi")
        self.seg_chart_type.pack(side="right")

        self.chart = ChartCanvas(self.area3_frame, width=760, height=340)
        self.chart.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # AREA 4: PHÂN TÍCH VÀ TRƯỜNG HỢP SỬ DỤNG
        self.area4_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        self.area4_frame.pack(fill="x", padx=16, pady=(8, 20))

        ctk.CTkLabel(
            self.area4_frame,
            text="4. PHÂN TÍCH KẾT QUẢ & KHI NÀO NÊN SỬ DỤNG?",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#A855F7"
        ).pack(anchor="w", padx=16, pady=(14, 6))

        self.txt_analysis_usecases = ctk.CTkTextbox(
            self.area4_frame,
            height=260,
            font=ctk.CTkFont(size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.txt_analysis_usecases.pack(fill="x", padx=16, pady=(0, 14))
        self.txt_analysis_usecases.configure(state="disabled")

    def _set_size(self, val: str):
        self.entry_size.delete(0, "end")
        self.entry_size.insert(0, val)

    def _get_chosen_algorithm_names(self) -> List[str]:
        names = []
        for combo in [self.combo_alg1, self.combo_alg2, self.combo_alg3]:
            val = combo.get()
            if val and "(Không chọn)" not in val:
                # Find matching registry key
                for alg in registry.get_all():
                    if alg.metadata.display_name == val:
                        if alg.metadata.name not in names:
                            names.append(alg.metadata.name)
                        break
        return names

    def _start_comparison(self):
        alg_names = self._get_chosen_algorithm_names()
        if len(alg_names) < 2:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất 2 thuật toán khác nhau để so sánh!")
            return

        try:
            size_n = int(self.entry_size.get().strip().replace(".", "").replace(",", ""))
            if size_n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Kích thước dữ liệu n không hợp lệ!")
            return

        dist_choice = self.combo_dist.get()

        self.is_comparing = True
        self.cancel_event.clear()
        self.btn_compare.configure(state="disabled")
        self.btn_cancel.configure(state="normal")
        self.progress_bar.set(0)

        thread = threading.Thread(
            target=self._comparison_worker,
            args=(alg_names, size_n, dist_choice)
        )
        thread.daemon = True
        thread.start()

    def _cancel_comparison(self):
        if self.is_comparing:
            self.cancel_event.set()
            self.lbl_progress.configure(text="Đang hủy so sánh...")

    def _comparison_worker(self, alg_names: List[str], size_n: int, dist_choice: str):
        try:
            def progress_cb(cur, total, msg):
                frac = cur / total if total > 0 else 0
                self.after(0, lambda: self._update_progress_ui(frac, msg))

            # Check if multi-case requested
            if "Khảo sát đa trường hợp" in dist_choice:
                cases = [
                    DataDistribution.RANDOM,
                    DataDistribution.SORTED_ASC,
                    DataDistribution.SORTED_DESC,
                    DataDistribution.NEARLY_SORTED
                ]
                multi_dist = BenchmarkRunner.run_multi_distributions(
                    algorithm_names=alg_names,
                    size=size_n,
                    distributions=cases,
                    runs=5,
                    warmup=True,
                    progress_callback=progress_cb,
                    cancel_event=self.cancel_event
                )
                self.latest_comp_metrics = multi_dist.metrics_by_dist.get(DataDistribution.RANDOM, [])

                # Build multi-case matrix data
                matrix: Dict[str, Dict[str, float]] = {}
                for dist in cases:
                    matrix[dist] = {}
                    for m in multi_dist.metrics_by_dist.get(dist, []):
                        matrix[dist][m.algorithm_name] = m.avg_time_ms
                self.latest_multi_case_data = matrix

            else:
                # Single distribution
                dist = self._map_dist(dist_choice)
                dataset = DataGenerator.generate(size=size_n, distribution=dist)
                target_val = dataset[len(dataset) // 2] if dataset else None

                metrics = BenchmarkRunner.run_single_dataset(
                    algorithm_names=alg_names,
                    data=dataset,
                    runs=5,
                    warmup=True,
                    target=target_val,
                    data_distribution=dist,
                    progress_callback=progress_cb,
                    cancel_event=self.cancel_event
                )
                self.latest_comp_metrics = metrics
                self.latest_multi_case_data = None

            self.after(0, self._render_all_comparison_outputs)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi so sánh", str(e)))
        finally:
            self.is_comparing = False
            self.after(0, lambda: self.btn_compare.configure(state="normal"))
            self.after(0, lambda: self.btn_cancel.configure(state="disabled"))

    def _map_dist(self, raw: str) -> str:
        if "Sorted" in raw and "Nearly" not in raw and "Reverse" not in raw:
            return DataDistribution.SORTED_ASC
        elif "Reverse" in raw:
            return DataDistribution.SORTED_DESC
        elif "Nearly" in raw:
            return DataDistribution.NEARLY_SORTED
        elif "Duplicate" in raw or "trùng" in raw:
            return DataDistribution.MANY_DUPLICATES
        return DataDistribution.RANDOM

    def _update_progress_ui(self, fraction: float, msg: str):
        self.progress_bar.set(fraction)
        self.lbl_progress.configure(text=f"[{int(fraction * 100)}%] {msg}")

    def _render_all_comparison_outputs(self):
        if self.cancel_event.is_set():
            self.lbl_progress.configure(text="Quá trình so sánh đã dừng.")
        else:
            self.progress_bar.set(1.0)
            self.lbl_progress.configure(text="So sánh hoàn tất 100%!")

        metrics = self.latest_comp_metrics
        if not metrics:
            return

        # 1. Benchmark Results Area
        self._render_area1_benchmark(metrics)

        # 2. Complexity Table Area
        self._render_area2_complexity(metrics)

        # 3. Chart Area
        self._redraw_chart(self.seg_chart_type.get())

        # 4. Analysis and Use Cases Area
        self._render_area4_analysis(metrics)

    def _render_area1_benchmark(self, metrics: List[SingleBenchmarkMetric]):
        self.txt_bench_results.configure(state="normal")
        self.txt_bench_results.delete("1.0", "end")

        lines = []
        header = f"{'Tiêu chí':<22} | " + " | ".join([f"{m.display_name.split('–')[0].strip():<16}" for m in metrics])
        sep = "=" * len(header)
        lines.append(header)
        lines.append(sep)

        # Rows
        lines.append(f"{'Thời gian TB (ms)':<22} | " + " | ".join([f"{m.avg_time_ms:>13.3f} ms" for m in metrics]))
        lines.append(f"{'Thời gian Min (ms)':<22} | " + " | ".join([f"{m.min_time_ms:>13.3f} ms" for m in metrics]))
        lines.append(f"{'Thời gian Max (ms)':<22} | " + " | ".join([f"{m.max_time_ms:>13.3f} ms" for m in metrics]))
        lines.append(f"{'Số phép so sánh':<22} | " + " | ".join([f"{m.comparisons:>16,}" for m in metrics]))
        lines.append(f"{'Số lần hoán đổi':<22} | " + " | ".join([f"{m.swaps if m.swaps > 0 else '-':>16}" for m in metrics]))
        lines.append(f"{'Kiểm tra tính đúng':<22} | " + " | ".join([f"{'✓ CHÍNH XÁC':>16}" if m.is_correct else f"{'❌ SAI':>16}" for m in metrics]))

        # Multi-case matrix if available
        if self.latest_multi_case_data:
            lines.append("\n" + "-" * len(header))
            lines.append("MA TRẬN HIỆU NĂNG THEO LOẠI DỮ LIỆU (Avg Time ms):")
            lines.append(f"{'Trường hợp dữ liệu':<22} | " + " | ".join([f"{m.display_name.split('–')[0].strip():<16}" for m in metrics]))
            lines.append("-" * len(header))
            for dist, alg_times in self.latest_multi_case_data.items():
                row_str = f"{dist[:20]:<22} | " + " | ".join([f"{alg_times.get(m.algorithm_name, 0.0):>13.3f} ms" for m in metrics])
                lines.append(row_str)

        self.txt_bench_results.insert("1.0", "\n".join(lines))
        self.txt_bench_results.configure(state="disabled")

    def _render_area2_complexity(self, metrics: List[SingleBenchmarkMetric]):
        self.txt_complexity_table.configure(state="normal")
        self.txt_complexity_table.delete("1.0", "end")

        lines = []
        header = f"{'Tiêu chí lý thuyết':<24} | " + " | ".join([f"{m.display_name.split('–')[0].strip():<16}" for m in metrics])
        sep = "-" * len(header)
        lines.append(header)
        lines.append(sep)

        metas = [registry.get_metadata(m.algorithm_name) for m in metrics]

        lines.append(f"{'Best Case':<24} | " + " | ".join([f"{meta.best_case:<16}" for meta in metas]))
        lines.append(f"{'Average Case':<24} | " + " | ".join([f"{meta.average_case:<16}" for meta in metas]))
        lines.append(f"{'Worst Case':<24} | " + " | ".join([f"{meta.worst_case:<16}" for meta in metas]))
        lines.append(f"{'Space Complexity':<24} | " + " | ".join([f"{meta.space_complexity:<16}" for meta in metas]))
        lines.append(f"{'Tính ổn định (Stable)':<24} | " + " | ".join([f"{'Có (Stable)' if meta.is_stable else 'Không':<16}" for meta in metas]))
        lines.append(f"{'Bộ nhớ tại chỗ (In-place)':<24} | " + " | ".join([f"{'Có' if meta.is_in_place else 'Không':<16}" for meta in metas]))

        self.txt_complexity_table.insert("1.0", "\n".join(lines))
        self.txt_complexity_table.configure(state="disabled")

    def _redraw_chart(self, choice: str):
        metrics = self.latest_comp_metrics
        if not metrics:
            return

        names = [m.display_name.split("–")[0].strip() for m in metrics]

        if "Thời gian" in choice:
            times = [m.avg_time_ms for m in metrics]
            self.chart.plot_algorithm_bar_chart(
                names,
                times,
                title=f"So sánh thời gian trung bình (ms) trên n = {metrics[0].size:,} ({metrics[0].data_distribution})",
                ylabel="Thời gian (ms)"
            )
        elif "so sánh" in choice:
            comps = [m.comparisons for m in metrics]
            self.chart.plot_algorithm_bar_chart(
                names,
                comps,
                title=f"So sánh số phép toán so sánh (Comparisons) trên n = {metrics[0].size:,}",
                ylabel="Số phép so sánh"
            )
        elif "Đa trường hợp" in choice:
            if self.latest_multi_case_data:
                groups = [d.split("(")[0].strip() for d in self.latest_multi_case_data.keys()]
                series = {}
                for m in metrics:
                    alg_label = m.display_name.split("–")[0].strip()
                    series[alg_label] = [self.latest_multi_case_data[d].get(m.algorithm_name, 0.0) for d in self.latest_multi_case_data.keys()]
                self.chart.plot_grouped_bar_chart(
                    groups,
                    series,
                    title="So sánh thời gian (ms) qua các trường hợp dữ liệu",
                    ylabel="Thời gian (ms)"
                )
            else:
                # Default bar chart if multi-case was not checked
                times = [m.avg_time_ms for m in metrics]
                self.chart.plot_algorithm_bar_chart(names, times, title="Thời gian trung bình (ms)")

    def _render_area4_analysis(self, metrics: List[SingleBenchmarkMetric]):
        self.txt_analysis_usecases.configure(state="normal")
        self.txt_analysis_usecases.delete("1.0", "end")

        lines = []
        n = metrics[0].size
        dist = metrics[0].data_distribution
        fastest = min(metrics, key=lambda m: m.avg_time_ms)
        fastest_name = fastest.display_name.split("–")[0].strip()

        # Section A: Phân tích kết quả
        lines.append("【PHÂN TÍCH KẾT QUẢ THỰC NGHIỆM】")
        lines.append(f"• Trên bộ dữ liệu thử nghiệm hiện tại (n = {n:,}, phân bố '{dist}'):")
        for m in metrics:
            disp = m.display_name.split("–")[0].strip()
            lines.append(f"  - {disp}: Thời gian TB = {m.avg_time_ms:.3f} ms | Số phép so sánh = {m.comparisons:,} | Space = {m.space_complexity}")

        lines.append(f"\n• Nhận xét chênh lệch:")
        lines.append(f"  Thuật toán [{fastest_name}] đạt thời gian thực thi thấp hơn trong bài đo này.")
        
        # Add comparative trade-off insights
        metas = {m.algorithm_name: registry.get_metadata(m.algorithm_name) for m in metrics}
        if "quick_sort" in metas and "merge_sort" in metas:
            lines.append(
                "  Tuy nhiên, Quick Sort có rủi ro Worst Case O(n²) và không bảo toàn tính ổn định (Unstable), "
                "trong khi Merge Sort cam kết 100% trần O(n log n) và là Stable Sort (nhưng đánh đổi tốn O(n) bộ nhớ phụ)."
            )
        if "insertion_sort" in metas:
            lines.append(
                "  Insertion Sort đạt hiệu quả rất cao khi dữ liệu đã gần có thứ tự (Best Case O(n)) "
                "và có overhead nhỏ nhất trên mảng kích thước nhỏ."
            )

        # Section B: Khi nào nên sử dụng
        lines.append("\n" + "=" * 60)
        lines.append("【KHI NÀO NÊN SỬ DỤNG? (TRƯỜNG HỢP ÁP DỤNG CỤ THỂ)】")
        for m in metrics:
            meta = metas.get(m.algorithm_name)
            if meta:
                disp = meta.display_name.split("–")[0].strip()
                lines.append(f"\n▶ {disp.upper()}:")
                lines.append(f"  • Đặc điểm: {meta.description}")
                lines.append(f"  • Phù hợp nhất khi: {meta.when_to_use}")
                lines.append(f"  • Ưu điểm: {'; '.join(meta.advantages)}")
                lines.append(f"  • Nhược điểm: {'; '.join(meta.disadvantages)}")

        # Section C: Kết luận theo điều kiện (KHÔNG DÙNG "TỐT NHẤT" TUYỆT ĐỐI)
        lines.append("\n" + "=" * 60)
        lines.append("【KẾT LUẬN & ĐÁNH GIÁ ĐIỀU KIỆN】")
        lines.append(
            f"Theo các tiêu chí được đo lường (Thời gian, Số phép toán, Kích thước n = {n:,}, Đặc điểm '{dist}'), "
            f"thuật toán [{fastest_name}] là THUẬT TOÁN CÓ HIỆU NĂNG CAO NHẤT trong thử nghiệm này.\n"
            f"Khuyến nghị lựa chọn trong thực tế:\n"
            f"- Cần tốc độ trung bình cao nhất trên RAM: Quick Sort.\n"
            f"- Cần bảo đảm thời gian ổn định không suy biến & giữ nguyên thứ tự: Merge Sort.\n"
            f"- Dữ liệu nhỏ (n < 50) hoặc gần sắp xếp sẵn: Insertion Sort."
        )

        self.txt_analysis_usecases.insert("1.0", "\n".join(lines))
        self.txt_analysis_usecases.configure(state="disabled")

    def _export_comparison(self):
        if not self.latest_comp_metrics:
            messagebox.showwarning("Thông báo", "Chưa có dữ liệu so sánh để xuất!")
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
                problem_title="Báo cáo so sánh đối chiếu thuật toán",
                input_analysis=self.controller.current_analysis,
                recommendation=self.controller.current_recommendation,
                benchmarks=self.latest_comp_metrics,
                conclusions=self.txt_analysis_usecases.get("1.0", "end")
            )
        else:
            ok = ReportExporter.export_csv(path, self.latest_comp_metrics)

        if ok:
            messagebox.showinfo("Thành công", f"Đã xuất báo cáo so sánh ra file:\n{path}")
