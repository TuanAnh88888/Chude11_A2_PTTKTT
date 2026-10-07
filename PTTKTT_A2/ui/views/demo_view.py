"""
Algorithm Analysis & Simulation Platform
UI - Automated Classroom Presentation Demo View
"""
import threading
from tkinter import messagebox
import customtkinter as ctk
from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.benchmark.runner import BenchmarkRunner
from core.complexity.analyzer import InputAnalyzer
from core.recommendation.engine import RecommendationConstraints, RecommendationEngine
from infrastructure.data.generator import DataDistribution, DataGenerator
from ui.components.chart_canvas import ChartCanvas


DEMO_PRESETS = {
    "Demo 1: Linear Search vs Binary Search": {
        "desc": "So sánh tìm kiếm tuyến tính O(n) và tìm kiếm nhị phân O(log n) trên mảng đã sắp xếp và mảng ngẫu nhiên.",
        "category": AlgorithmCategory.SEARCHING,
        "size": 50000,
        "dist": DataDistribution.SORTED_ASC,
        "algs": ["linear_search", "binary_search"],
        "explanation": "Khi dữ liệu đã sắp xếp, Binary Search chỉ mất tối đa ~16 phép so sánh trên 50.000 phần tử, trong khi Linear Search trung bình mất tới 25.000 phép so sánh!"
    },
    "Demo 2: Bubble Sort vs Merge Sort vs Quick Sort": {
        "desc": "Chứng minh sự phân kỳ khổng lồ giữa thuật toán O(n²) và O(n log n) khi n tăng.",
        "category": AlgorithmCategory.SORTING,
        "size": 3000,
        "dist": DataDistribution.RANDOM,
        "algs": ["bubble_sort", "merge_sort", "quick_sort"],
        "explanation": "Với n = 3.000, Bubble Sort mất ~4.5 triệu phép so sánh O(n²), trong khi Quick Sort và Merge Sort chỉ mất ~35.000 phép so sánh O(n log n), tốc độ nhanh hơn hàng trăm lần!"
    },
    "Demo 3: Best Case & Dữ liệu gần như đã sắp xếp": {
        "desc": "Thử nghiệm trên dữ liệu gần sắp xếp (Nearly Sorted): Insertion Sort O(n) đánh bại Quick Sort.",
        "category": AlgorithmCategory.SORTING,
        "size": 5000,
        "dist": DataDistribution.NEARLY_SORTED,
        "algs": ["insertion_sort", "bubble_sort", "merge_sort", "quick_sort"],
        "explanation": "Dữ liệu gần có thứ tự giúp Insertion Sort chỉ tốn O(n) thời gian, ít overhead hơn cả Quick Sort và Merge Sort. Đây là minh chứng không có thuật toán nào 'luôn luôn tốt nhất' trong mọi tình huống."
    },
    "Demo 4: Đối chiếu Lý thuyết vs Đo đạc Thực nghiệm": {
        "desc": "Khảo sát tốc độ tăng trưởng thực tế trên mảng kích thước tăng dần.",
        "category": AlgorithmCategory.SORTING,
        "size": 5000,
        "dist": DataDistribution.RANDOM,
        "algs": ["insertion_sort", "selection_sort", "merge_sort", "quick_sort"],
        "explanation": "Biểu đồ thực nghiệm phản ánh trung thực xu hướng lý thuyết: đường bậc hai cong dốc vọt lên, trong khi đường O(n log n) tăng thoai thoải ổn định."
    }
}


class DemoView(ctk.CTkScrollableFrame):
    """Automated presentation suite executing end-to-end demo scenarios for classroom lectures."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        self._build_ui()

    def _build_ui(self):
        # Header
        lbl_head = ctk.CTkLabel(
            self,
            text="KỊCH BẢN DEMO THUYẾT TRÌNH (CLASSROOM DEMO SUITE)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Các kịch bản tự động được chuẩn bị sẵn để sinh viên trình bày trước giảng viên chỉ với 1 click.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Scenario Selector Frame
        ctrl_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        ctrl_frame.pack(fill="x", padx=16, pady=8)

        inner_ctrl = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        inner_ctrl.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(inner_ctrl, text="Chọn kịch bản thuyết trình:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")

        self.combo_demo = ctk.CTkComboBox(
            inner_ctrl,
            values=list(DEMO_PRESETS.keys()),
            width=480,
            command=self._on_demo_selected
        )
        self.combo_demo.set(list(DEMO_PRESETS.keys())[0])
        self.combo_demo.pack(anchor="w", pady=(6, 8))

        self.lbl_scenario_desc = ctk.CTkLabel(
            inner_ctrl,
            text=DEMO_PRESETS[list(DEMO_PRESETS.keys())[0]]["desc"],
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            wraplength=720,
            justify="left"
        )
        self.lbl_scenario_desc.pack(anchor="w", pady=(0, 12))

        # Big Run Button
        self.btn_run_demo = ctk.CTkButton(
            inner_ctrl,
            text="▶ BẮT ĐẦU CHẠY DEMO TỰ ĐỘNG (1-CLICK END-TO-END)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=42,
            command=self._start_demo
        )
        self.btn_run_demo.pack(fill="x")

        # Progress bar
        self.prog_bar = ctk.CTkProgressBar(self)
        self.prog_bar.set(0)
        self.prog_bar.pack(fill="x", padx=16, pady=6)

        self.lbl_status = ctk.CTkLabel(self, text="Sẵn sàng thực thi.", font=ctk.CTkFont(size=11), text_color="#64748B")
        self.lbl_status.pack(anchor="w", padx=16, pady=(0, 10))

        # Output Results Split Container
        out_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        out_frame.pack(fill="both", expand=True, padx=16, pady=8)

        ctk.CTkLabel(
            out_frame,
            text="KẾT QUẢ THỰC THI & PHÂN TÍCH HỌC THUẬT",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.box_results = ctk.CTkTextbox(out_frame, height=180, font=ctk.CTkFont(family="Consolas", size=11), fg_color=("#F8FAFC", "#0F172A"))
        self.box_results.pack(fill="x", padx=16, pady=(0, 12))
        self.box_results.insert("1.0", "Chọn kịch bản và nhấn 'BẮT ĐẦU CHẠY DEMO TỰ ĐỘNG' để xem kết quả phân tích và biểu đồ.")
        self.box_results.configure(state="disabled")

        # Chart
        self.chart = ChartCanvas(out_frame, width=740, height=340)
        self.chart.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _on_demo_selected(self, choice):
        cfg = DEMO_PRESETS.get(choice)
        if cfg:
            self.lbl_scenario_desc.configure(text=cfg["desc"])

    def _start_demo(self):
        self.btn_run_demo.configure(state="disabled")
        self.prog_bar.set(0)

        choice = self.combo_demo.get()
        cfg = DEMO_PRESETS.get(choice)

        thread = threading.Thread(target=self._run_demo_worker, args=(cfg,))
        thread.daemon = True
        thread.start()

    def _run_demo_worker(self, cfg):
        try:
            self._update_ui_status(0.1, "1/4: Đang sinh dữ liệu theo đặc tả kịch bản...")
            data = DataGenerator.generate(size=cfg["size"], distribution=cfg["dist"])

            self._update_ui_status(0.3, "2/4: Phân tích đặc điểm dữ liệu đầu vào...")
            analysis = InputAnalyzer.analyze(data)

            # Recommend
            rec = RecommendationEngine.recommend(cfg["category"], analysis)

            self._update_ui_status(0.5, f"3/4: Đang đo đạc thực tế {len(cfg['algs'])} thuật toán...")
            target = data[len(data) // 2] if cfg["category"] == AlgorithmCategory.SEARCHING else None

            metrics = BenchmarkRunner.run_single_dataset(
                algorithm_names=cfg["algs"],
                data=data,
                runs=3,
                warmup=True,
                target=target
            )

            self._update_ui_status(0.9, "4/4: Vẽ biểu đồ và tổng hợp kết luận bài toán...")

            self.after(0, lambda: self._render_demo_output(analysis, rec, metrics, cfg["explanation"]))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Lỗi Demo", str(e)))
        finally:
            self.after(0, lambda: self.btn_run_demo.configure(state="normal"))

    def _update_ui_status(self, progress, msg):
        self.after(0, lambda: self.prog_bar.set(progress))
        self.after(0, lambda: self.lbl_status.configure(text=msg))

    def _render_demo_output(self, analysis, rec, metrics, pedagogical_conclusion):
        self.prog_bar.set(1.0)
        self.lbl_status.configure(text="Demo hoàn tất thành công 100%!")

        lines = []
        lines.append(f"【ĐẶC ĐIỂM DỮ LIỆU】: n = {analysis.size:,} | {analysis.characteristic} | Miền: [{analysis.min_value}..{analysis.max_value}]")
        lines.append(f"【ĐỀ XUẤT THUẬT TOÁN】: {rec.primary_recommendation.display_name.upper()} ({rec.complexity_summary})")
        lines.append("【LÝ DO CHÍNH】: " + "; ".join(rec.reasoning_points[:2]))
        lines.append("\n【KẾT QUẢ ĐO THỰC TẾ (BENCHMARK)】:")

        header = f"{'Thuật toán':<24} | {'Avg Time (ms)':<14} | {'So sánh':<12} | {'Đổi chỗ':<10}"
        lines.append(header)
        lines.append("-" * len(header))

        names = []
        times = []
        for m in metrics:
            row = f"{m.display_name.split('–')[0].strip():<24} | {m.avg_time_ms:<14.3f} | {m.comparisons:<12,} | {m.swaps:<10,}"
            lines.append(row)
            names.append(m.display_name.split("–")[0].strip())
            times.append(m.avg_time_ms)

        lines.append("\n【KẾT LUẬN GIẢNG VIÊN / THUYẾT TRÌNH】:")
        lines.append(pedagogical_conclusion)

        self.box_results.configure(state="normal")
        self.box_results.delete("1.0", "end")
        self.box_results.insert("1.0", "\n".join(lines))
        self.box_results.configure(state="disabled")

        # Draw chart
        self.chart.plot_algorithm_bar_chart(
            names,
            times,
            title=f"Kết quả đo thực tế kịch bản Demo (n = {analysis.size:,})"
        )
