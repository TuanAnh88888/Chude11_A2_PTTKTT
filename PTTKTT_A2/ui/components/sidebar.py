"""
Algorithm Analysis & Simulation Platform
UI - Modern Sidebar Navigation Component
"""
from typing import Callable, Dict
import customtkinter as ctk


class ModernSidebar(ctk.CTkFrame):
    """Sidebar navigation with consistent academic styling and active state indicators."""

    def __init__(self, master, on_navigate: Callable[[str], None], **kwargs):
        super().__init__(
            master,
            width=260,
            corner_radius=0,
            fg_color=("#F8FAFC", "#0F172A"),
            border_width=1,
            border_color=("#E2E8F0", "#1E293B"),
            **kwargs
        )
        self.on_navigate = on_navigate
        self.buttons: Dict[str, ctk.CTkButton] = {}
        self.current_view = "dashboard"

        # App Brand Header
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_frame.pack(fill="x", padx=16, pady=(20, 16))

        self.lbl_app_tag = ctk.CTkLabel(
            self.logo_frame,
            text="ALGORITHM PLATFORM",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#3B82F6"
        )
        self.lbl_app_tag.pack(anchor="w")

        self.lbl_app_title = ctk.CTkLabel(
            self.logo_frame,
            text="PHÂN TÍCH THUẬT TOÁN",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        self.lbl_app_title.pack(anchor="w")

        # Separator line
        self.sep = ctk.CTkFrame(self, height=1, fg_color=("#E2E8F0", "#1E293B"))
        self.sep.pack(fill="x", padx=16, pady=(0, 12))

        # Nav items definition: (view_id, label, icon)
        self.nav_items = [
            ("dashboard", "📊 Tổng quan"),
            ("simulation", "🎬 Mô phỏng thuật toán"),
            ("benchmark", "⚡ Đo hiệu năng thuật toán"),
            ("comparison", "⚖️ So sánh thuật toán"),
            ("library", "📚 Thư viện thuật toán"),
            ("history", "🕒 Lịch sử & Báo cáo"),
        ]

        # Buttons container
        self.scroll_nav = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_nav.pack(fill="both", expand=True, padx=8, pady=4)

        for view_id, label in self.nav_items:
            btn = ctk.CTkButton(
                self.scroll_nav,
                text=label,
                anchor="w",
                height=38,
                corner_radius=8,
                font=ctk.CTkFont(size=12, weight="normal"),
                fg_color="transparent",
                text_color=("#334155", "#94A3B8"),
                hover_color=("#E2E8F0", "#1E293B"),
                command=lambda vid=view_id: self._handle_click(vid)
            )
            btn.pack(fill="x", pady=2)
            self.buttons[view_id] = btn

        # Footer
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=16, pady=16)

        self.lbl_version = ctk.CTkLabel(
            self.footer_frame,
            text="Phiên bản 1.0 • Academic Edition",
            font=ctk.CTkFont(size=10),
            text_color=("#94A3B8", "#64748B")
        )
        self.lbl_version.pack(anchor="w")

        # Set initial active button
        self.set_active("dashboard")

    def _handle_click(self, view_id: str):
        self.set_active(view_id)
        self.on_navigate(view_id)

    def set_active(self, view_id: str):
        self.current_view = view_id
        for vid, btn in self.buttons.items():
            if vid == view_id:
                btn.configure(
                    fg_color=("#2563EB", "#2563EB"),
                    text_color="#FFFFFF",
                    font=ctk.CTkFont(size=12, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("#334155", "#94A3B8"),
                    font=ctk.CTkFont(size=12, weight="normal")
                )
