"""
Algorithm Analysis & Simulation Platform
UI - Problem Input, Data Analysis & Recommendation View
"""
import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.complexity.analyzer import InputAnalyzer
from core.recommendation.engine import RecommendationConstraints, RecommendationEngine
from infrastructure.data.generator import DataDistribution, DataGenerator
from infrastructure.data.io_handler import DataIOHandler
from infrastructure.persistence.history_manager import HistoryManager, HistoryRecord


class AnalysisView(ctk.CTkScrollableFrame):
    """Core view for defining problems, loading data, inspecting traits and receiving algorithm recommendations."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller
        self.history_mgr = HistoryManager()

        self.current_data = []
        self._build_ui()

    def _build_ui(self):
        # Section Title
        lbl_head = ctk.CTkLabel(
            self,
            text="PHÂN TÍCH ĐẦU VÀO & ĐỀ XUẤT THUẬT TOÁN",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Đưa bài toán và tập dữ liệu vào hệ thống. Động cơ phân tích sẽ đánh giá cấu trúc và đề xuất thuật toán phù hợp.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Top row: Problem definition & Constraints
        top_grid = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        top_grid.pack(fill="x", padx=16, pady=8)
        top_grid.grid_columnconfigure((0, 1), weight=1)

        # Left Column: Problem Choice
        left_box = ctk.CTkFrame(top_grid, fg_color="transparent")
        left_box.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")

        ctk.CTkLabel(
            left_box,
            text="1. CHỌN LOẠI BÀI TOÁN",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w")

        self.problem_combo = ctk.CTkComboBox(
            left_box,
            values=["Sắp xếp danh sách (Sorting)", "Tìm kiếm phần tử (Searching)"],
            width=320,
            command=self._on_problem_change
        )
        self.problem_combo.set("Sắp xếp danh sách (Sorting)")
        self.problem_combo.pack(anchor="w", pady=(8, 12))

        # Right Column: Constraints
        right_box = ctk.CTkFrame(top_grid, fg_color="transparent")
        right_box.grid(row=0, column=1, padx=16, pady=16, sticky="nsew")

        ctk.CTkLabel(
            right_box,
            text="2. RÀNG BUỘC & ĐIỀU KIỆN",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w")

        self.check_stable = ctk.CTkCheckBox(right_box, text="Cần tính ổn định (Stable Sort)")
        self.check_stable.pack(anchor="w", pady=(8, 4))

        self.check_in_place = ctk.CTkCheckBox(right_box, text="Ràng buộc bộ nhớ tại chỗ (In-place, O(1) phụ)")
        self.check_in_place.pack(anchor="w", pady=4)

        # Query count frame for search
        self.query_frame = ctk.CTkFrame(right_box, fg_color="transparent")
        self.query_frame.pack(fill="x", pady=4)
        ctk.CTkLabel(self.query_frame, text="Số lượt truy vấn (Queries):").pack(side="left")
        self.entry_queries = ctk.CTkEntry(self.query_frame, width=80)
        self.entry_queries.insert(0, "1")
        self.entry_queries.pack(side="left", padx=8)

        # Search target value frame
        self.target_frame = ctk.CTkFrame(right_box, fg_color="transparent")
        self.target_frame.pack(fill="x", pady=4)
        ctk.CTkLabel(self.target_frame, text="Mục tiêu tìm kiếm (Target):").pack(side="left")
        self.entry_target = ctk.CTkEntry(self.target_frame, width=80)
        self.entry_target.insert(0, "23")
        self.entry_target.pack(side="left", padx=8)

        # Initially hide search frames if sorting is selected
        self._update_problem_ui_state()

        # Data Input Tabview
        data_input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        data_input_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(
            data_input_frame,
            text="3. NHẬP DỮ LIỆU ĐẦU VÀO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w", padx=16, pady=(16, 4))

        self.data_tabview = ctk.CTkTabview(data_input_frame)
        self.data_tabview.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        tab_direct = self.data_tabview.add("Nhập trực tiếp")
        tab_gen = self.data_tabview.add("Sinh tự động")
        tab_file = self.data_tabview.add("Nhập từ file CSV/TXT")

        # Tab 1: Direct text input
        ctk.CTkLabel(tab_direct, text="Nhập dãy số (phân cách bằng dấu phẩy, khoảng trắng hoặc dòng):").pack(anchor="w", pady=(4, 4))
        self.txt_direct = ctk.CTkTextbox(tab_direct, height=70)
        self.txt_direct.pack(fill="x", pady=4)
        self.txt_direct.insert("1.0", "12, 45, 7, 23, 89, 34, 5, 91, 18, 55, 3, 42, 67, 10, 28")

        # Tab 2: Generator controls
        gen_row1 = ctk.CTkFrame(tab_gen, fg_color="transparent")
        gen_row1.pack(fill="x", pady=4)

        ctk.CTkLabel(gen_row1, text="Số lượng n:").pack(side="left")
        self.entry_n = ctk.CTkEntry(gen_row1, width=80)
        self.entry_n.insert(0, "1000")
        self.entry_n.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(gen_row1, text="Min:").pack(side="left")
        self.entry_min = ctk.CTkEntry(gen_row1, width=70)
        self.entry_min.insert(0, "1")
        self.entry_min.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(gen_row1, text="Max:").pack(side="left")
        self.entry_max = ctk.CTkEntry(gen_row1, width=80)
        self.entry_max.insert(0, "100000")
        self.entry_max.pack(side="left", padx=(4, 16))

        ctk.CTkLabel(gen_row1, text="Đặc điểm:").pack(side="left")
        self.combo_dist = ctk.CTkComboBox(
            gen_row1,
            values=[
                DataDistribution.RANDOM,
                DataDistribution.SORTED_ASC,
                DataDistribution.SORTED_DESC,
                DataDistribution.NEARLY_SORTED,
                DataDistribution.MANY_DUPLICATES
            ],
            width=200
        )
        self.combo_dist.set(DataDistribution.RANDOM)
        self.combo_dist.pack(side="left", padx=8)

        btn_generate = ctk.CTkButton(
            tab_gen,
            text="⚡ Tạo dữ liệu ngẫu nhiên",
            fg_color="#0D9488",
            hover_color="#0F766E",
            command=self._generate_data
        )
        btn_generate.pack(anchor="w", pady=(8, 4))

        # Tab 3: File load
        file_row = ctk.CTkFrame(tab_file, fg_color="transparent")
        file_row.pack(fill="x", pady=8)

        self.entry_filepath = ctk.CTkEntry(file_row, placeholder_text="Đường dẫn file .csv hoặc .txt...")
        self.entry_filepath.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_browse = ctk.CTkButton(
            file_row,
            text="Chọn file...",
            width=100,
            command=self._browse_file
        )
        btn_browse.pack(side="right")

        # Main Analyze Button
        btn_analyze = ctk.CTkButton(
            self,
            text="🔍 TIẾN HÀNH PHÂN TÍCH & ĐỀ XUẤT THUẬT TOÁN",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=44,
            corner_radius=8,
            command=self.execute_analysis
        )
        btn_analyze.pack(fill="x", padx=16, pady=12)

        # Results Container (Cards)
        self.results_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        self.results_frame.pack(fill="x", padx=16, pady=8)

        self.lbl_results_title = ctk.CTkLabel(
            self.results_frame,
            text="4. KẾT QUẢ PHÂN TÍCH ĐẦU VÀO & ĐỀ XUẤT",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#10B981"
        )
        self.lbl_results_title.pack(anchor="w", padx=16, pady=(16, 8))

        # Input Characteristics Display Box
        self.box_input_stats = ctk.CTkTextbox(self.results_frame, height=100, fg_color=("#F8FAFC", "#0F172A"))
        self.box_input_stats.pack(fill="x", padx=16, pady=(0, 12))
        self.box_input_stats.insert("1.0", "Chưa phân tích dữ liệu. Vui lòng bấm nút 'TIẾN HÀNH PHÂN TÍCH'.")
        self.box_input_stats.configure(state="disabled")

        # Recommendation Banner Box
        self.rec_box = ctk.CTkFrame(self.results_frame, corner_radius=8, fg_color=("#EFF6FF", "#172554"), border_width=1, border_color="#3B82F6")
        self.rec_box.pack(fill="x", padx=16, pady=8)

        self.lbl_rec_name = ctk.CTkLabel(
            self.rec_box,
            text="THUẬT TOÁN ĐƯỢC ĐỀ XUẤT: (Chưa có)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2563EB"
        )
        self.lbl_rec_name.pack(anchor="w", padx=16, pady=(12, 4))

        self.lbl_rec_complexity = ctk.CTkLabel(
            self.rec_box,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("#1E293B", "#93C5FD")
        )
        self.lbl_rec_complexity.pack(anchor="w", padx=16, pady=(0, 8))

        self.box_rec_details = ctk.CTkTextbox(self.rec_box, height=130, fg_color=("#DBEAFE", "#0F172A"))
        self.box_rec_details.pack(fill="x", padx=16, pady=(0, 12))
        self.box_rec_details.configure(state="disabled")

        # Action Buttons row below recommendation
        self.action_row = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.action_row.pack(fill="x", padx=16, pady=(8, 16))

        btn_sim = ctk.CTkButton(
            self.action_row,
            text="🎬 Xem mô phỏng",
            fg_color="#059669",
            hover_color="#047857",
            command=self._go_to_simulation
        )
        btn_sim.pack(side="left", padx=(0, 8))

        btn_bench = ctk.CTkButton(
            self.action_row,
            text="⚡ Chạy Benchmark đo đạc",
            fg_color="#D97706",
            hover_color="#B45309",
            command=self._go_to_benchmark
        )
        btn_bench.pack(side="left", padx=8)

        btn_save_hist = ctk.CTkButton(
            self.action_row,
            text="💾 Lưu kết quả vào Lịch sử",
            fg_color="#6366F1",
            hover_color="#4F46E5",
            command=self._save_to_history
        )
        btn_save_hist.pack(side="right")

    def _on_problem_change(self, choice: str):
        self._update_problem_ui_state()

    def _update_problem_ui_state(self):
        is_searching = "Searching" in self.problem_combo.get()
        if is_searching:
            self.query_frame.pack(fill="x", pady=4)
            self.target_frame.pack(fill="x", pady=4)
            self.check_stable.configure(state="disabled")
            self.check_in_place.configure(state="disabled")
        else:
            self.query_frame.pack_forget()
            self.target_frame.pack_forget()
            self.check_stable.configure(state="normal")
            self.check_in_place.configure(state="normal")

    def _generate_data(self):
        try:
            n = int(self.entry_n.get())
            min_v = int(self.entry_min.get())
            max_v = int(self.entry_max.get())
            dist = self.combo_dist.get()
            data = DataGenerator.generate(size=n, distribution=dist, min_val=min_v, max_val=max_v)
            self.current_data = data
            messagebox.showinfo("Thành công", f"Đã sinh {n:,} phần tử với phân bố: {dist}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sinh dữ liệu: {e}")

    def _browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Data files", "*.csv *.txt"), ("All files", "*.*")])
        if path:
            self.entry_filepath.delete(0, "end")
            self.entry_filepath.insert(0, path)
            try:
                data = DataIOHandler.load_from_file(path)
                self.current_data = data
                messagebox.showinfo("Đã nạp file", f"Đã tải thành công {len(data):,} phần tử từ file {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Lỗi đọc file", str(e))

    def _get_active_dataset(self):
        active_tab = self.data_tabview.get()
        if active_tab == "Nhập trực tiếp":
            text = self.txt_direct.get("1.0", "end")
            return DataIOHandler.parse_string(text)
        elif active_tab == "Sinh tự động":
            if not self.current_data:
                self._generate_data()
            return self.current_data
        elif active_tab == "Nhập từ file CSV/TXT":
            fpath = self.entry_filepath.get().strip()
            if not fpath:
                raise ValueError("Vui lòng chọn đường dẫn file .csv hoặc .txt!")
            return DataIOHandler.load_from_file(fpath)
        return []

    def execute_analysis(self):
        try:
            data = self._get_active_dataset()
            if not data:
                raise ValueError("Dữ liệu đầu vào rỗng!")

            is_searching = "Searching" in self.problem_combo.get()
            category = AlgorithmCategory.SEARCHING if is_searching else AlgorithmCategory.SORTING

            # Query count
            queries = 1
            if is_searching:
                try:
                    queries = max(1, int(self.entry_queries.get()))
                except ValueError:
                    queries = 1

            constraints = RecommendationConstraints(
                require_stable=bool(self.check_stable.get()),
                strictly_in_place=bool(self.check_in_place.get()),
                query_count=queries
            )

            # Analyze input
            analysis = InputAnalyzer.analyze(data)

            # Recommend
            rec_result = RecommendationEngine.recommend(category, analysis, constraints)

            # Save state to controller
            self.controller.current_data = list(data)
            self.controller.current_analysis = analysis
            self.controller.current_recommendation = rec_result
            self.controller.current_category = category

            # Update UI Display
            self._render_analysis_results(analysis, rec_result)

        except Exception as e:
            messagebox.showerror("Lỗi phân tích", str(e))

    def _render_analysis_results(self, analysis, rec_result):
        # 1. Update Input Stats Textbox
        self.box_input_stats.configure(state="normal")
        self.box_input_stats.delete("1.0", "end")
        stat_text = (
            f"• Số lượng phần tử (n): {analysis.size:,}\n"
            f"• Kiểu dữ liệu: {analysis.data_type} | Miền giá trị: [{analysis.min_value} .. {analysis.max_value}] (Khoảng cách: {analysis.range_value})\n"
            f"• Trạng thái thứ tự: {analysis.characteristic}\n"
            f"• Tỷ lệ nghịch thế: {analysis.inversion_ratio * 100:.2f}%\n"
            f"• Trùng lặp: {analysis.duplicate_count:,} phần tử trùng ({analysis.unique_percentage:.1f}% giá trị duy nhất)\n"
            f"• Độ phân tán: Phương sai = {analysis.variance:.2f} | Độ lệch chuẩn = {analysis.std_dev:.2f}"
        )
        self.box_input_stats.insert("1.0", stat_text)
        self.box_input_stats.configure(state="disabled")

        # 2. Update Recommendation
        self.lbl_rec_name.configure(text=f"THUẬT TOÁN ĐƯỢC ĐỀ XUẤT: {rec_result.primary_recommendation.display_name.upper()}")
        self.lbl_rec_complexity.configure(text=rec_result.complexity_summary)

        self.box_rec_details.configure(state="normal")
        self.box_rec_details.delete("1.0", "end")

        detail_lines = []
        detail_lines.append("LÝ DO ĐỀ XUẤT:")
        for r in rec_result.reasoning_points:
            detail_lines.append(f"  ✓ {r}")

        if rec_result.trade_offs:
            detail_lines.append("\nĐÁNH ĐỔI (TRADE-OFFS):")
            for t in rec_result.trade_offs:
                detail_lines.append(f"  ⇄ {t}")

        if rec_result.caveats_and_warnings:
            detail_lines.append("\nCẢNH BÁO RỦI RO (CAVEATS):")
            for w in rec_result.caveats_and_warnings:
                detail_lines.append(f"  ⚠️ {w}")

        if rec_result.alternative_recommendations:
            detail_lines.append("\nPHƯƠNG ÁN THAY THẾ KHẢ THI:")
            for a in rec_result.alternative_recommendations:
                detail_lines.append(f"  • {a.display_name} ({a.average_case})")

        self.box_rec_details.insert("1.0", "\n".join(detail_lines))
        self.box_rec_details.configure(state="disabled")

    def _go_to_simulation(self):
        if not self.controller.current_data:
            messagebox.showwarning("Thông báo", "Vui lòng phân tích dữ liệu trước!")
            return
        self.controller.navigate_to("simulation")

    def _go_to_benchmark(self):
        if not self.controller.current_data:
            messagebox.showwarning("Thông báo", "Vui lòng phân tích dữ liệu trước!")
            return
        self.controller.navigate_to("benchmark")

    def _save_to_history(self):
        if not self.controller.current_analysis or not self.controller.current_recommendation:
            messagebox.showwarning("Thông báo", "Chưa có kết quả phân tích để lưu!")
            return

        import datetime
        import uuid
        analysis = self.controller.current_analysis
        rec = self.controller.current_recommendation

        record = HistoryRecord(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            problem_type=rec.problem_type,
            size=analysis.size,
            characteristic=analysis.characteristic,
            recommended_alg=rec.primary_recommendation.display_name,
            reasoning_summary="; ".join(rec.reasoning_points[:2]),
            benchmark_summary="Chưa chạy benchmark"
        )
        self.history_mgr.save_record(record)
        messagebox.showinfo("Thành công", "Đã lưu phiên phân tích vào Lịch sử!")
