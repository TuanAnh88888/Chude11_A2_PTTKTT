"""
Algorithm Analysis & Simulation Platform
UI - Custom User Algorithm Python Code AST Analyzer View
"""
from tkinter import messagebox
import customtkinter as ctk
from core.ast_analyzer.static_analyzer import StaticAstAnalyzer


SAMPLE_CODES = {
    "Vòng lặp đơn (Linear O(n))": """def linear_sum(arr):
    total = 0
    for x in arr:
        total += x
    return total
""",
    "Hai vòng lặp lồng nhau (Quadratic O(n²))": """def bubble_pattern(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
""",
    "Đệ quy phân nhánh nhị phân (Exponential O(2ⁿ))": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
""",
    "Gọi hàm sắp xếp tích hợp (Timsort O(n log n))": """def process_and_sort(arr):
    arr.sort()
    return arr
"""
}


class CustomCodeView(ctk.CTkScrollableFrame):
    """Static AST parser view for analyzing arbitrary user-defined Python algorithms."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        self._build_ui()

    def _build_ui(self):
        # Header
        lbl_head = ctk.CTkLabel(
            self,
            text="PHÂN TÍCH MÃ PYTHON TÙY BIẾN (STATIC AST ANALYZER)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Phân tích cây cú pháp trừu tượng (AST) của mã Python để bóc tách vòng lặp, độ sâu lồng nhau và cấu trúc đệ quy.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Disclaimer banner (Required by Section 32)
        disclaimer_box = ctk.CTkFrame(self, corner_radius=8, fg_color=("#FEF3C7", "#78350F"), border_width=1, border_color="#F59E0B")
        disclaimer_box.pack(fill="x", padx=16, pady=4)

        lbl_warn = ctk.CTkLabel(
            disclaimer_box,
            text=(
                "⚠️ CẢNH BÁO QUAN TRỌNG: Đây là phân tích tĩnh heuristic dựa trên cây cú pháp trừu tượng (AST). "
                "Hệ thống không thực thi mã không an toàn và không thể chứng minh chính xác Big-O cho mọi trường hợp "
                "do giới hạn của bài toán dừng Turing."
            ),
            font=ctk.CTkFont(size=11),
            text_color=("#92400E", "#FEF3C7"),
            wraplength=760,
            justify="left"
        )
        lbl_warn.pack(padx=16, pady=10, anchor="w")

        # Code Editor Container
        editor_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        editor_frame.pack(fill="x", padx=16, pady=8)

        # Samples toolbar
        sample_bar = ctk.CTkFrame(editor_frame, fg_color="transparent")
        sample_bar.pack(fill="x", padx=16, pady=(12, 6))

        ctk.CTkLabel(sample_bar, text="Nạp mã mẫu:").pack(side="left", padx=(0, 8))
        self.combo_sample = ctk.CTkComboBox(
            sample_bar,
            values=list(SAMPLE_CODES.keys()),
            width=320,
            command=self._load_sample
        )
        self.combo_sample.set("Hai vòng lặp lồng nhau (Quadratic O(n²))")
        self.combo_sample.pack(side="left", padx=(0, 12))

        # Code Textbox
        self.txt_code = ctk.CTkTextbox(
            editor_frame,
            height=200,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.txt_code.pack(fill="x", padx=16, pady=(0, 12))
        self.txt_code.insert("1.0", SAMPLE_CODES["Hai vòng lặp lồng nhau (Quadratic O(n²))"])

        # Analyze button
        btn_analyze = ctk.CTkButton(
            editor_frame,
            text="🔍 TIẾN HÀNH PHÂN TÍCH TĨNH AST",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=38,
            command=self._analyze_code
        )
        btn_analyze.pack(fill="x", padx=16, pady=(0, 14))

        # Results Display Panel
        results_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        results_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(
            results_frame,
            text="KẾT QUẢ BÓC TÁCH CÚ PHÁP & ƯỚC TÍNH ĐỘ PHỨC TẠP",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#10B981"
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.box_ast_result = ctk.CTkTextbox(
            results_frame,
            height=180,
            font=ctk.CTkFont(size=12),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.box_ast_result.pack(fill="x", padx=16, pady=(0, 16))
        self.box_ast_result.insert("1.0", "Nhấn 'TIẾN HÀNH PHÂN TÍCH TĨNH AST' để phân tích đoạn mã trên.")
        self.box_ast_result.configure(state="disabled")

    def _load_sample(self, choice):
        code = SAMPLE_CODES.get(choice, "")
        self.txt_code.delete("1.0", "end")
        self.txt_code.insert("1.0", code)

    def _analyze_code(self):
        source = self.txt_code.get("1.0", "end")
        report = StaticAstAnalyzer.analyze_code(source)

        self.box_ast_result.configure(state="normal")
        self.box_ast_result.delete("1.0", "end")

        if not report.is_valid_syntax:
            self.box_ast_result.insert("1.0", f"❌ LỖI CÚ PHÁP:\n{report.error_message}")
            self.box_ast_result.configure(state="disabled")
            return

        lines = []
        lines.append(f"✓ Cú pháp hợp lệ! Tên hàm phát hiện: '{report.function_name}'\n")
        lines.append(f"• Ước tính Time Complexity:  {report.estimated_time_complexity}")
        lines.append(f"• Ước tính Space Complexity: {report.estimated_space_complexity}\n")
        lines.append("CÁC ĐẶC TRƯNG CẤU TRÚC PHÁT HIỆN TỪ AST:")
        for feat in report.structural_features:
            lines.append(f"  - {feat}")

        lines.append(f"\nGIẢI THÍCH HEURISTIC:\n{report.heuristic_explanation}")

        self.box_ast_result.insert("1.0", "\n".join(lines))
        self.box_ast_result.configure(state="disabled")
