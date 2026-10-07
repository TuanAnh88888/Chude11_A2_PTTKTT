"""
Algorithm Analysis & Simulation Platform
UI - Modern Stat Card Component
"""
import customtkinter as ctk


class ModernStatCard(ctk.CTkFrame):
    """Modern academic dashboard KPI card."""

    def __init__(
        self,
        master,
        title: str,
        value: str,
        subtitle: str = "",
        accent_color: str = "#3B82F6",
        **kwargs
    ):
        super().__init__(master, corner_radius=10, fg_color=("#F3F4F6", "#1E293B"), border_width=1, border_color=("#E5E7EB", "#334155"), **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Title with small accent dot or label
        self.lbl_title = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#6B7280", "#94A3B8"),
            anchor="w"
        )
        self.lbl_title.grid(row=0, column=0, padx=16, pady=(12, 4), sticky="w")

        # Metric value
        self.lbl_value = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=accent_color,
            anchor="w"
        )
        self.lbl_value.grid(row=1, column=0, padx=16, pady=(0, 2), sticky="w")

        # Subtitle
        self.lbl_subtitle = ctk.CTkLabel(
            self,
            text=subtitle,
            font=ctk.CTkFont(size=12),
            text_color=("#4B5563", "#CBD5E1"),
            anchor="w"
        )
        self.lbl_subtitle.grid(row=2, column=0, padx=16, pady=(0, 12), sticky="w")

    def update_values(self, value: str, subtitle: str = None):
        self.lbl_value.configure(text=value)
        if subtitle is not None:
            self.lbl_subtitle.configure(text=subtitle)
