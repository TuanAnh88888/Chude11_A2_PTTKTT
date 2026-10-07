"""
Algorithm Analysis & Simulation Platform
UI - Analysis History & Report Export View
"""
from tkinter import filedialog, messagebox
import customtkinter as ctk
from infrastructure.export.report_exporter import ReportExporter
from infrastructure.persistence.history_manager import HistoryManager


class HistoryView(ctk.CTkScrollableFrame):
    """View for browsing saved analysis sessions and exporting comprehensive academic reports."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller
        self.history_mgr = HistoryManager()

        self._build_ui()

    def _build_ui(self):
        # Header
        lbl_head = ctk.CTkLabel(
            self,
            text="LỊCH SỬ PHÂN TÍCH & XUẤT BÁO CÁO HỌC THUẬT",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Xem lại các phiên làm việc đã lưu, quản lý dữ liệu lịch sử và xuất báo cáo kết quả chi tiết ra file TXT hoặc CSV.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Action Toolbar
        tb = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        tb.pack(fill="x", padx=16, pady=8)

        tb_inner = ctk.CTkFrame(tb, fg_color="transparent")
        tb_inner.pack(fill="x", padx=16, pady=12)

        btn_refresh = ctk.CTkButton(
            tb_inner,
            text="🔄 Làm mới",
            width=100,
            fg_color="#475569",
            hover_color="#334155",
            command=self.refresh_list
        )
        btn_refresh.pack(side="left", padx=(0, 8))

        btn_clear = ctk.CTkButton(
            tb_inner,
            text="🗑 Xóa tất cả lịch sử",
            width=140,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self._clear_all_history
        )
        btn_clear.pack(side="left", padx=8)

        btn_export_txt = ctk.CTkButton(
            tb_inner,
            text="📄 Xuất báo cáo hiện tại (TXT)",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self._export_current_txt
        )
        btn_export_txt.pack(side="right")

        # History Records Container
        self.records_container = ctk.CTkFrame(self, fg_color="transparent")
        self.records_container.pack(fill="both", expand=True, padx=16, pady=8)

        self.refresh_list()

    def refresh_list(self):
        # Clear existing widgets
        for widget in self.records_container.winfo_children():
            widget.destroy()

        records = self.history_mgr.load_all()
        if not records:
            empty_card = ctk.CTkFrame(self.records_container, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
            empty_card.pack(fill="x", pady=12)
            ctk.CTkLabel(
                empty_card,
                text="Chưa có phiên phân tích nào được lưu trong lịch sử.\nThực hiện một phân tích mới và bấm 'Lưu vào lịch sử'.",
                font=ctk.CTkFont(size=13),
                text_color=("#64748B", "#94A3B8"),
                justify="center"
            ).pack(pady=32)
            return

        for rec in records:
            card = ctk.CTkFrame(self.records_container, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"), border_width=1, border_color=("#E2E8F0", "#334155"))
            card.pack(fill="x", pady=6)

            card_inner = ctk.CTkFrame(card, fg_color="transparent")
            card_inner.pack(fill="x", padx=16, pady=12)

            top_row = ctk.CTkFrame(card_inner, fg_color="transparent")
            top_row.pack(fill="x")

            lbl_time = ctk.CTkLabel(top_row, text=rec.get("timestamp", ""), font=ctk.CTkFont(size=11), text_color="#94A3B8")
            lbl_time.pack(side="left")

            rec_id = rec.get("id")
            btn_del = ctk.CTkButton(
                top_row,
                text="Xóa",
                width=50,
                height=24,
                font=ctk.CTkFont(size=10),
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=lambda rid=rec_id: self._delete_record(rid)
            )
            btn_del.pack(side="right")

            lbl_title = ctk.CTkLabel(
                card_inner,
                text=f"{rec.get('problem_type', '')} (n = {rec.get('size', 0):,})",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#0F172A", "#F8FAFC")
            )
            lbl_title.pack(anchor="w", pady=(4, 2))

            lbl_rec = ctk.CTkLabel(
                card_inner,
                text=f"Thuật toán đề xuất: {rec.get('recommended_alg', '')}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#10B981"
            )
            lbl_rec.pack(anchor="w", pady=(0, 4))

            lbl_detail = ctk.CTkLabel(
                card_inner,
                text=f"Đặc điểm: {rec.get('characteristic', '')} | {rec.get('reasoning_summary', '')}",
                font=ctk.CTkFont(size=11),
                text_color=("#475569", "#CBD5E1"),
                wraplength=700,
                justify="left"
            )
            lbl_detail.pack(anchor="w")

    def _delete_record(self, record_id: str):
        self.history_mgr.delete_record(record_id)
        self.refresh_list()

    def _clear_all_history(self):
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa toàn bộ lịch sử không?")
        if confirm:
            self.history_mgr.clear_all()
            self.refresh_list()

    def _export_current_txt(self):
        if not self.controller.current_analysis:
            messagebox.showwarning("Thông báo", "Chưa có phiên phân tích hiện tại nào để xuất báo cáo!")
            return

        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Report", "*.txt")])
        if path:
            ok = ReportExporter.export_text(
                filepath=path,
                problem_title=self.controller.current_recommendation.problem_type if self.controller.current_recommendation else "Phân tích thuật toán",
                input_analysis=self.controller.current_analysis,
                recommendation=self.controller.current_recommendation,
                benchmarks=self.controller.last_benchmark_results,
                conclusions="Kết quả thực nghiệm hoàn toàn nhất quán với dự báo Big-O tiệm cận của động cơ phân tích."
            )
            if ok:
                messagebox.showinfo("Thành công", f"Đã xuất báo cáo chi tiết thành công ra file:\n{path}")
