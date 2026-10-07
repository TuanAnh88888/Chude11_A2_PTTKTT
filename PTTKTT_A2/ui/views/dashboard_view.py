"""
Algorithm Analysis & Simulation Platform
UI - Modern Dashboard View
"""
from typing import Callable
import customtkinter as ctk
from core.algorithms.registry import registry
from infrastructure.persistence.history_manager import HistoryManager
from ui.components.stat_card import ModernStatCard


class DashboardView(ctk.CTkFrame):
    """Overview dashboard displaying platform metrics, pipeline workflow, and quick actions."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller
        self.history_mgr = HistoryManager()

        self._build_ui()

    def _build_ui(self):
        # Header banner
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 16))

        title = ctk.CTkLabel(
            header,
            text="HỆ THỐNG PHÂN TÍCH & MÔ PHỎNG THUẬT TOÁN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Nền tảng học tập & nghiên cứu: Phân tích độ phức tạp Big-O, đề xuất thuật toán, mô phỏng và đo lường thực nghiệm.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # KPI Stat Cards Row
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=24, pady=8)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="card")

        total_algs = len(registry.get_all())
        history_records = self.history_mgr.load_all()
        total_analyses = len(history_records)

        self.card_total = ModernStatCard(
            cards_frame,
            title="Tổng thuật toán",
            value=f"{total_algs}",
            subtitle="Sorting & Searching có sẵn",
            accent_color="#3B82F6"
        )
        self.card_total.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.card_analyses = ModernStatCard(
            cards_frame,
            title="Bài toán đã phân tích",
            value=f"{total_analyses}",
            subtitle="Đã lưu trong lịch sử",
            accent_color="#10B981"
        )
        self.card_analyses.grid(row=0, column=1, padx=10, sticky="ew")

        self.card_bench = ModernStatCard(
            cards_frame,
            title="Độ chính xác đo",
            value="perf_counter",
            subtitle="Độc lập hoàn toàn với GUI",
            accent_color="#F59E0B"
        )
        self.card_bench.grid(row=0, column=2, padx=10, sticky="ew")

        current_rec = self.controller.current_recommendation
        rec_name = current_rec.primary_recommendation.name.replace("_", " ").title() if current_rec else "Chưa phân tích"

        self.card_rec = ModernStatCard(
            cards_frame,
            title="Đề xuất hiện tại",
            value=rec_name,
            subtitle="Dựa trên n và phân bố dữ liệu",
            accent_color="#A855F7"
        )
        self.card_rec.grid(row=0, column=3, padx=(10, 0), sticky="ew")

        # Call-to-Action big button
        cta_frame = ctk.CTkFrame(self, fg_color=("#EFF6FF", "#1E293B"), corner_radius=12, border_width=1, border_color="#3B82F6")
        cta_frame.pack(fill="x", padx=24, pady=16)

        cta_inner = ctk.CTkFrame(cta_frame, fg_color="transparent")
        cta_inner.pack(fill="x", padx=20, pady=16)

        lbl_cta_title = ctk.CTkLabel(
            cta_inner,
            text="Khám phá và trực quan hóa hoạt động thuật toán",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#1D4ED8", "#60A5FA")
        )
        lbl_cta_title.pack(side="left")

        btn_new_analysis = ctk.CTkButton(
            cta_inner,
            text="＋ MÔ PHỎNG THUẬT TOÁN",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=38,
            corner_radius=8,
            command=lambda: self.controller.navigate_to("simulation")
        )
        btn_new_analysis.pack(side="right")

        # Academic Workflow diagram / card
        workflow_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        workflow_frame.pack(fill="x", padx=24, pady=8)

        wf_title = ctk.CTkLabel(
            workflow_frame,
            text="QUY TRÌNH PHÂN TÍCH & ĐÁNH GIÁ THUẬT TOÁN CHUẨN MỰC",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#334155", "#94A3B8")
        )
        wf_title.pack(anchor="w", padx=16, pady=(14, 10))

        steps = [
            ("① Nhập bài toán", "Xác định mục tiêu & dữ liệu"),
            ("② Phân tích input", "Đo n, phân bố, tính nghịch thế"),
            ("③ Đề xuất thuật toán", "Đánh giá Time/Space & Trade-offs"),
            ("④ Mô phỏng trực quan", "Theo dõi từng bước thực thi"),
            ("⑤ Benchmark thực tế", "Đo thời gian bằng perf_counter"),
            ("⑥ So sánh & Báo cáo", "Đối chiếu lý thuyết & thực nghiệm")
        ]

        steps_row = ctk.CTkFrame(workflow_frame, fg_color="transparent")
        steps_row.pack(fill="x", padx=16, pady=(0, 16))
        steps_row.grid_columnconfigure(tuple(range(6)), weight=1)

        for idx, (s_title, s_desc) in enumerate(steps):
            box = ctk.CTkFrame(steps_row, fg_color=("#F8FAFC", "#0F172A"), corner_radius=8, border_width=1, border_color=("#E2E8F0", "#334155"))
            box.grid(row=0, column=idx, padx=4, sticky="nsew")

            ctk.CTkLabel(
                box,
                text=s_title,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("#2563EB", "#60A5FA")
            ).pack(padx=8, pady=(8, 2), anchor="w")

            ctk.CTkLabel(
                box,
                text=s_desc,
                font=ctk.CTkFont(size=9),
                text_color=("#64748B", "#94A3B8"),
                wraplength=120,
                justify="left"
            ).pack(padx=8, pady=(0, 8), anchor="w")

        # Bottom Quick Action Banner
        bottom_banner = ctk.CTkFrame(self, fg_color=("#F8FAFC", "#1E293B"), corner_radius=10)
        bottom_banner.pack(fill="x", padx=24, pady=(8, 20))

        db_title = ctk.CTkLabel(
            bottom_banner,
            text="SO SÁNH & ĐỐI CHIẾU HIỆU NĂNG THỰC NGHIỆM",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#475569", "#CBD5E1")
        )
        db_title.pack(anchor="w", padx=16, pady=(12, 6))

        db_btn = ctk.CTkButton(
            bottom_banner,
            text="⚖️ MỞ BẢNG ĐỐI CHIẾU & MA TRẬN SO SÁNH THUẬT TOÁN",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            height=36,
            corner_radius=8,
            command=lambda: self.controller.navigate_to("comparison")
        )
        db_btn.pack(fill="x", padx=16, pady=(0, 14))

    def refresh(self):
        """Called when dashboard becomes active to refresh KPI stats."""
        total_algs = len(registry.get_all())
        history_records = self.history_mgr.load_all()
        self.card_total.update_values(f"{total_algs}")
        self.card_analyses.update_values(f"{len(history_records)}")

        rec = self.controller.current_recommendation
        if rec:
            self.card_rec.update_values(rec.primary_recommendation.display_name.split("–")[0].strip())
        else:
            self.card_rec.update_values("Chưa phân tích")
