"""
Algorithm Analysis & Simulation Platform
UI - Matplotlib Chart Canvas Component
"""
import tkinter as tk
from typing import Dict, List, Optional
import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class ChartCanvas(ctk.CTkFrame):
    """Reusable high-performance chart component embedded in CustomTkinter."""

    def __init__(self, master, width: int = 600, height: int = 400, **kwargs):
        super().__init__(master, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"), **kwargs)

        self.figure = Figure(figsize=(width / 100, height / 100), dpi=100)
        self.figure.patch.set_facecolor("#1E293B")
        self.ax = self.figure.add_subplot(111)
        self._style_axis(self.ax)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=8, pady=8)

        self.palette = [
            "#38BDF8",  # Sky
            "#4ADE80",  # Emerald
            "#FBBF24",  # Amber
            "#F43F5E",  # Rose
            "#A855F7",  # Purple
            "#EC4899",  # Pink
            "#60A5FA",  # Blue
            "#34D399",  # Teal
        ]

    def _style_axis(self, ax):
        ax.set_facecolor("#0F172A")
        ax.tick_params(colors="#94A3B8", labelsize=9)
        ax.xaxis.label.set_color("#CBD5E1")
        ax.yaxis.label.set_color("#CBD5E1")
        ax.title.set_color("#F8FAFC")
        for spine in ax.spines.values():
            spine.set_color("#334155")
        ax.grid(True, linestyle="--", alpha=0.3, color="#475569")

    def clear(self):
        self.ax.clear()
        self._style_axis(self.ax)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def plot_time_vs_size(self, sizes: List[int], series_data: Dict[str, List[float]], title: str = "Thời gian thực thi theo kích thước (n)"):
        """Plot execution time (ms) curves for multiple algorithms across sizes."""
        self.ax.clear()
        self._style_axis(self.ax)

        for idx, (label, times) in enumerate(series_data.items()):
            color = self.palette[idx % len(self.palette)]
            # If times are in seconds (<10 for large benchmarks), convert or check
            times_ms = [t if t > 0.05 else t * 1000.0 for t in times]
            self.ax.plot(
                sizes,
                times_ms,
                marker="o",
                linewidth=2.2,
                markersize=6,
                label=label,
                color=color
            )

        self.ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        self.ax.set_xlabel("Kích thước dữ liệu (n)", fontsize=10)
        self.ax.set_ylabel("Thời gian (ms)", fontsize=10)
        self.ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F1F5F9", fontsize=9)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def plot_algorithm_bar_chart(self, names: List[str], times_ms: List[float], title: str = "So sánh thời gian trung bình (ms)", ylabel: str = "Thời gian (ms)"):
        """Plot vertical bar chart comparing algorithms."""
        self.ax.clear()
        self._style_axis(self.ax)

        colors = [self.palette[i % len(self.palette)] for i in range(len(names))]
        bars = self.ax.bar(names, times_ms, color=colors, width=0.45)

        for bar in bars:
            height = bar.get_height()
            label_text = f"{height:.3f} ms" if "ms" in ylabel else f"{int(height):,}"
            self.ax.annotate(
                label_text,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=8,
                color="#E2E8F0"
            )

        self.ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        self.ax.set_ylabel(ylabel, fontsize=10)
        self.ax.tick_params(axis="x", rotation=12)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def plot_grouped_bar_chart(
        self,
        group_labels: List[str],
        series_dict: Dict[str, List[float]],
        title: str = "So sánh hiệu năng theo loại dữ liệu",
        ylabel: str = "Thời gian trung bình (ms)"
    ):
        """Plot grouped bar chart comparing multiple algorithms across distributions or categories."""
        self.ax.clear()
        self._style_axis(self.ax)

        n_groups = len(group_labels)
        n_series = len(series_dict)
        if n_groups == 0 or n_series == 0:
            return

        indices = np.arange(n_groups)
        total_width = 0.75
        bar_width = total_width / n_series

        for i, (alg_name, values) in enumerate(series_dict.items()):
            offset = (i - n_series / 2 + 0.5) * bar_width
            color = self.palette[i % len(self.palette)]
            bars = self.ax.bar(
                indices + offset,
                values,
                bar_width,
                label=alg_name,
                color=color
            )

        self.ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        self.ax.set_ylabel(ylabel, fontsize=10)
        self.ax.set_xticks(indices)
        self.ax.set_xticklabels(group_labels, fontsize=9)
        self.ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F1F5F9", fontsize=9)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def plot_theoretical_vs_experimental(
        self,
        sizes: List[int],
        exp_times_ms: List[float],
        fitted_theoretical_ms: List[float],
        alg_name: str,
        complexity_label: str
    ):
        """Plot theoretical curve alongside experimental measurements."""
        self.ax.clear()
        self._style_axis(self.ax)

        self.ax.plot(
            sizes,
            exp_times_ms,
            "o-",
            color="#38BDF8",
            linewidth=2.2,
            label="Thực nghiệm (Experimental)"
        )
        self.ax.plot(
            sizes,
            fitted_theoretical_ms,
            "--",
            color="#F43F5E",
            linewidth=2,
            label=f"Lý thuyết chuẩn hóa ({complexity_label})"
        )

        self.ax.set_title(f"So sánh Lý thuyết vs Thực nghiệm: {alg_name}", fontsize=11, fontweight="bold", pad=10)
        self.ax.set_xlabel("Kích thước dữ liệu (n)", fontsize=10)
        self.ax.set_ylabel("Thời gian (ms)", fontsize=10)
        self.ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F1F5F9", fontsize=9)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def plot_big_o_family(self, growth_dict: Dict[str, List[tuple]], n_max: int = 100):
        """Plot reference Big-O complexity curves."""
        self.ax.clear()
        self._style_axis(self.ax)

        colors_map = {
            "O(1)": "#10B981",       # Green
            "O(log n)": "#06B6D4",   # Cyan
            "O(n)": "#3B82F6",       # Blue
            "O(n log n)": "#F59E0B", # Amber
            "O(n²)": "#EF4444",      # Red
            "O(2ⁿ)": "#EC4899",      # Pink
        }

        y_limit = (n_max ** 2) * 1.05

        for label, points in growth_dict.items():
            xs = [p[0] for p in points]
            ys = [min(p[1], y_limit) for p in points]
            self.ax.plot(xs, ys, label=label, color=colors_map.get(label, "#94A3B8"), linewidth=2)

        self.ax.set_ylim(0, y_limit)
        self.ax.set_title(f"Biểu đồ tốc độ tăng trưởng các lớp hàm Big-O (n = 1 .. {n_max})", fontsize=11, fontweight="bold", pad=10)
        self.ax.set_xlabel("Kích thước n", fontsize=10)
        self.ax.set_ylabel("Số phép toán f(n)", fontsize=10)
        self.ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#F1F5F9", fontsize=9)
        self.figure.tight_layout()
        self.canvas.draw_idle()
