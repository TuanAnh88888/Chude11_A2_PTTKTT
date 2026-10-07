"""
Algorithm Analysis & Simulation Platform
UI - Algorithm Library & Encyclopedia View
"""
import customtkinter as ctk
from core.algorithms.registry import registry


class LibraryView(ctk.CTkFrame):
    """Knowledge encyclopedia covering algorithm metadata, proofs, pseudocode and complexity breakdowns."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        self._build_ui()

    def _build_ui(self):
        # Header
        lbl_head = ctk.CTkLabel(
            self,
            text="THƯ VIỆN THUẬT TOÁN & BÁCH KHOA TOÀN THƯ",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="Tra cứu chi tiết mã giả, ý tưởng thiết kế, hệ thức truy hồi đệ quy và phân tích chứng minh độ phức tạp.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

        # Split Container: Left list of algorithms, Right detail panel
        split_box = ctk.CTkFrame(self, fg_color="transparent")
        split_box.pack(fill="both", expand=True, padx=16, pady=8)
        split_box.grid_columnconfigure(0, weight=1)
        split_box.grid_columnconfigure(1, weight=3)
        split_box.grid_rowconfigure(0, weight=1)

        # Left list
        left_frame = ctk.CTkFrame(split_box, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        left_frame.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            left_frame,
            text="DANH MỤC THUẬT TOÁN",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        ).pack(anchor="w", padx=14, pady=(14, 8))

        self.scroll_list = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.alg_buttons = {}
        for alg in registry.get_all():
            name = alg.metadata.name
            btn = ctk.CTkButton(
                self.scroll_list,
                text=alg.metadata.display_name,
                anchor="w",
                height=36,
                fg_color="transparent",
                text_color=("#1E293B", "#CBD5E1"),
                hover_color=("#E2E8F0", "#334155"),
                command=lambda n=name: self._show_algorithm(n)
            )
            btn.pack(fill="x", pady=2)
            self.alg_buttons[name] = btn

        # Right detail panel
        self.right_frame = ctk.CTkScrollableFrame(split_box, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        self.right_frame.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        self.lbl_title = ctk.CTkLabel(
            self.right_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2563EB"
        )
        self.lbl_title.pack(anchor="w", padx=16, pady=(16, 4))

        self.lbl_category = ctk.CTkLabel(
            self.right_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#64748B"
        )
        self.lbl_category.pack(anchor="w", padx=16, pady=(0, 12))

        # Complexity pills row
        self.pills_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.pills_frame.pack(fill="x", padx=16, pady=4)
        self.pills_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.pill_best = self._create_pill(self.pills_frame, 0, "Best Case", "")
        self.pill_avg = self._create_pill(self.pills_frame, 1, "Average Case", "")
        self.pill_worst = self._create_pill(self.pills_frame, 2, "Worst Case", "")
        self.pill_space = self._create_pill(self.pills_frame, 3, "Space Memory", "")

        # Detail text boxes
        self.txt_desc = ctk.CTkTextbox(self.right_frame, height=90, fg_color=("#F8FAFC", "#0F172A"))
        self.txt_desc.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(self.right_frame, text="MÃ GIẢ (PSEUDOCODE):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#10B981").pack(anchor="w", padx=16, pady=(8, 2))
        self.txt_pseudo = ctk.CTkTextbox(self.right_frame, height=130, font=ctk.CTkFont(family="Consolas", size=11), fg_color=("#F8FAFC", "#0F172A"))
        self.txt_pseudo.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkLabel(self.right_frame, text="GIẢI THÍCH ĐỘ PHỨC TẠP BIG-O & HỆ THỨC TRUY HỒI:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#A855F7").pack(anchor="w", padx=16, pady=(8, 2))
        self.txt_math = ctk.CTkTextbox(self.right_frame, height=120, fg_color=("#F8FAFC", "#0F172A"))
        self.txt_math.pack(fill="x", padx=16, pady=(0, 8))

        # Show first algorithm by default
        first_alg = registry.get_all()[0].metadata.name
        self._show_algorithm(first_alg)

    def _create_pill(self, parent, col, title, val):
        frame = ctk.CTkFrame(parent, corner_radius=6, fg_color=("#F1F5F9", "#0F172A"))
        frame.grid(row=0, column=col, padx=4, sticky="nsew")
        lbl_t = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=10), text_color="#94A3B8")
        lbl_t.pack(pady=(4, 0))
        lbl_v = ctk.CTkLabel(frame, text=val, font=ctk.CTkFont(size=12, weight="bold"), text_color="#38BDF8")
        lbl_v.pack(pady=(0, 4))
        return lbl_v

    def _show_algorithm(self, name: str):
        meta = registry.get_metadata(name)
        if not meta:
            return

        # Highlight button
        for n, btn in self.alg_buttons.items():
            if n == name:
                btn.configure(fg_color="#2563EB", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color=("#1E293B", "#CBD5E1"))

        self.lbl_title.configure(text=meta.display_name.upper())
        self.lbl_category.configure(text=f"Phân loại: {meta.category.value} | Ổn định (Stable): {'Có' if meta.is_stable else 'Không'} | Tại chỗ (In-place): {'Có' if meta.is_in_place else 'Không'}")

        self.pill_best.configure(text=meta.best_case)
        self.pill_avg.configure(text=meta.average_case)
        self.pill_worst.configure(text=meta.worst_case)
        self.pill_space.configure(text=meta.space_complexity)

        # Overview
        overview = f"【Mô tả】\n{meta.description}\n\n【Ý tưởng cốt lõi】\n{meta.core_idea}\n\n【Khi nào nên sử dụng】\n{meta.when_to_use}"
        self.txt_desc.configure(state="normal")
        self.txt_desc.delete("1.0", "end")
        self.txt_desc.insert("1.0", overview)
        self.txt_desc.configure(state="disabled")

        # Pseudocode
        self.txt_pseudo.configure(state="normal")
        self.txt_pseudo.delete("1.0", "end")
        self.txt_pseudo.insert("1.0", meta.pseudocode)
        self.txt_pseudo.configure(state="disabled")

        # Big-O & Recurrence
        math_content = f"【Hệ thức truy hồi】\n{meta.recurrence_relation or 'Không sử dụng đệ quy.'}\n\n【Giải thích Big-O chi tiết】\n{meta.complexity_explanation}"
        self.txt_math.configure(state="normal")
        self.txt_math.delete("1.0", "end")
        self.txt_math.insert("1.0", math_content)
        self.txt_math.configure(state="disabled")
