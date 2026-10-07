"""
Algorithm Analysis & Simulation Platform
UI - Interactive Big-O Complexity Family Growth Chart View
"""
import customtkinter as ctk
from core.complexity.big_o_math import get_theoretical_growth
from ui.components.chart_canvas import ChartCanvas


class BigOView(ctk.CTkScrollableFrame):
    """Visualizes Big-O asymptotic growth rate curves with interactive n_max adjustment."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        self._build_ui()

    def _build_ui(self):
        # Header
        lbl_head = ctk.CTkLabel(
            self,
            text="BIỂU ĐỒ CÁC LỚP ĐỘ PHỨC TẠP BIG-O (ASYMPTOTIC GROWTH)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Khảo sát trực quan sự chênh lệch khủng khiếp giữa các hàm thời gian khi kích thước n tăng dần.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Control panel: Slider for n_max
        ctrl_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        ctrl_frame.pack(fill="x", padx=16, pady=8)

        ctrl_inner = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        ctrl_inner.pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(ctrl_inner, text="Điều chỉnh giới hạn n max:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 10))

        self.slider_nmax = ctk.CTkSlider(
            ctrl_inner,
            from_=10,
            to=200,
            number_of_steps=19,
            width=240,
            command=self._on_slider_change
        )
        self.slider_nmax.set(50)
        self.slider_nmax.pack(side="left", padx=(0, 12))

        self.lbl_nmax_val = ctk.CTkLabel(ctrl_inner, text="n = 50", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3B82F6")
        self.lbl_nmax_val.pack(side="left")

        # Chart Container
        chart_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        chart_frame.pack(fill="both", expand=True, padx=16, pady=8)

        self.chart = ChartCanvas(chart_frame, width=760, height=360)
        self.chart.pack(fill="both", expand=True, padx=16, pady=16)

        # Big-O reference table
        ref_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        ref_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(
            ref_frame,
            text="BẢNG ĐỐI CHIẾU SỐ PHÉP TOÁN THEO KÍCH THƯỚC N",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#10B981"
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.box_table = ctk.CTkTextbox(
            ref_frame,
            height=160,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=("#F8FAFC", "#0F172A")
        )
        self.box_table.pack(fill="x", padx=16, pady=(0, 16))

        self._render_reference_table()
        self._update_chart(50)

    def _on_slider_change(self, value):
        n_max = int(value)
        self.lbl_nmax_val.configure(text=f"n = {n_max}")
        self._update_chart(n_max)

    def _update_chart(self, n_max: int):
        growth = get_theoretical_growth(n_max=n_max, num_points=100)
        self.chart.plot_big_o_family(growth, n_max=n_max)

    def _render_reference_table(self):
        text = """Class       | Tên gọi                   | n = 10      | n = 100     | n = 1,000      | n = 1,000,000  
------------|---------------------------|-------------|-------------|----------------|----------------
O(1)        | Hằng số (Constant)        | 1           | 1           | 1              | 1              
O(log n)    | Logarit (Logarithmic)     | ~3          | ~7          | ~10            | ~20            
O(n)        | Tuyến tính (Linear)       | 10          | 100         | 1,000          | 1,000,000      
O(n log n)  | Tuyến tính log (Linearith)| ~33         | ~664        | ~9,965         | ~19,931,568    
O(n²)       | Bậc hai (Quadratic)       | 100         | 10,000      | 1,000,000      | 10¹² (1 triệu tỷ)
O(2ⁿ)       | Hàm mũ (Exponential)      | 1,024       | 1.26 × 10³⁰ | Không tưởng    | Bất khả thi    
"""
        self.box_table.configure(state="normal")
        self.box_table.delete("1.0", "end")
        self.box_table.insert("1.0", text)
        self.box_table.configure(state="disabled")
