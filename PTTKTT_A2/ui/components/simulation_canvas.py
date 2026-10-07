"""
Algorithm Analysis & Simulation Platform
UI - Interactive Simulation Canvas Component
"""
import tkinter as tk
from typing import Any, List, Optional
import customtkinter as ctk
from core.simulation.events import EventType, SimulationEvent


class SimulationCanvas(ctk.CTkFrame):
    """Custom canvas for rendering algorithm states, bars, pointers, and comparisons."""

    def __init__(self, master, width: int = 700, height: int = 320, **kwargs):
        super().__init__(master, corner_radius=10, fg_color=("#F1F5F9", "#0F172A"), **kwargs)

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg="#0F172A",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)

        # Color mapping
        self.COLOR_DEFAULT = "#38BDF8"       # Sky Blue
        self.COLOR_COMPARE = "#FBBF24"       # Amber
        self.COLOR_SWAP = "#EF4444"          # Red
        self.COLOR_PIVOT = "#A855F7"         # Violet
        self.COLOR_SORTED = "#10B981"        # Emerald
        self.COLOR_HIGHLIGHT = "#EC4899"     # Pink

    def clear(self):
        self.canvas.delete("all")

    def render_sorting_state(
        self,
        array: List[Any],
        event: Optional[SimulationEvent] = None,
        sorted_indices: Optional[set] = None
    ):
        """Renders vertical bar visualizer for sorting algorithms."""
        self.canvas.delete("all")
        n = len(array)
        if n == 0:
            self.canvas.create_text(
                self.winfo_width() / 2 or 350,
                self.winfo_height() / 2 or 160,
                text="Chưa có dữ liệu để mô phỏng",
                fill="#94A3B8",
                font=("Segoe UI", 12)
            )
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1:
            w = 700
        if h <= 1:
            h = 320

        padding_x = 24
        padding_y = 35
        usable_w = w - 2 * padding_x
        usable_h = h - 2 * padding_y

        bar_w = max(2.0, usable_w / n)
        gap = 1.0 if n > 120 else (2.0 if n > 50 else 4.0)
        actual_bar_w = max(1.0, bar_w - gap)

        min_val = min(array)
        max_val = max(array)
        val_range = max(1, max_val - min_val)

        # Highlight sets from event
        active_indices = set(event.indices) if event else set()
        active_type = event.event_type if event else None

        for i, val in enumerate(array):
            # Calculate bar height
            normalized = (val - min_val) / val_range if val_range > 0 else 0.5
            bar_h = max(6.0, normalized * (usable_h - 15))

            x0 = padding_x + i * bar_w
            x1 = x0 + actual_bar_w
            y1 = h - padding_y
            y0 = y1 - bar_h

            # Determine bar color
            if sorted_indices and i in sorted_indices:
                color = self.COLOR_SORTED
            elif i in active_indices:
                if active_type == EventType.COMPARE:
                    color = self.COLOR_COMPARE
                elif active_type in (EventType.SWAP, EventType.ASSIGN):
                    color = self.COLOR_SWAP
                elif active_type in (EventType.PIVOT, EventType.PARTITION):
                    color = self.COLOR_PIVOT
                elif active_type == EventType.MARK_SORTED:
                    color = self.COLOR_SORTED
                else:
                    color = self.COLOR_HIGHLIGHT
            else:
                color = self.COLOR_DEFAULT

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

            # Show value label if array is small enough
            if n <= 35:
                self.canvas.create_text(
                    (x0 + x1) / 2,
                    y0 - 8,
                    text=str(val),
                    fill="#E2E8F0",
                    font=("Segoe UI", 8, "bold")
                )
                self.canvas.create_text(
                    (x0 + x1) / 2,
                    y1 + 12,
                    text=str(i),
                    fill="#64748B",
                    font=("Segoe UI", 7)
                )

    def render_searching_state(
        self,
        array: List[Any],
        event: Optional[SimulationEvent] = None
    ):
        """Renders array block row with search pointers (low, mid, high, found)."""
        self.canvas.delete("all")
        n = len(array)
        if n == 0:
            return

        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 320

        # Show at most 25 elements horizontally
        display_n = min(n, 25)
        box_w = min(48.0, (w - 60) / display_n)
        box_h = 42.0

        start_x = (w - (display_n * box_w)) / 2
        y0 = (h - box_h) / 2
        y1 = y0 + box_h

        active_indices = set(event.indices) if event else set()
        ev_type = event.event_type if event else None

        for i in range(display_n):
            val = array[i]
            x0 = start_x + i * box_w
            x1 = x0 + box_w - 4

            # Determine color
            if ev_type == EventType.FOUND and i in active_indices:
                bg = self.COLOR_SORTED
                text_col = "#FFFFFF"
            elif i in active_indices:
                bg = self.COLOR_COMPARE if ev_type == EventType.COMPARE else self.COLOR_PIVOT
                text_col = "#000000"
            else:
                bg = "#1E293B"
                text_col = "#94A3B8"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline="#334155", width=2)
            self.canvas.create_text(
                (x0 + x1) / 2,
                (y0 + y1) / 2,
                text=str(val),
                fill=text_col,
                font=("Segoe UI", 10, "bold")
            )
            # Index below
            self.canvas.create_text(
                (x0 + x1) / 2,
                y1 + 14,
                text=str(i),
                fill="#64748B",
                font=("Segoe UI", 8)
            )

        # Draw pointers if Binary Search
        if event and event.indices and len(event.indices) >= 2:
            low_idx = event.indices[0] if len(event.indices) > 0 else None
            mid_idx = event.indices[1] if len(event.indices) > 1 else None
            high_idx = event.indices[2] if len(event.indices) > 2 else None

            if mid_idx is not None and mid_idx < display_n:
                mx = start_x + mid_idx * box_w + box_w / 2 - 2
                self.canvas.create_text(mx, y0 - 16, text="▼ MID", fill="#A855F7", font=("Segoe UI", 9, "bold"))
            if low_idx is not None and low_idx < display_n:
                lx = start_x + low_idx * box_w + box_w / 2 - 2
                self.canvas.create_text(lx, y0 - 30, text="LOW", fill="#38BDF8", font=("Segoe UI", 8, "bold"))
            if high_idx is not None and high_idx < display_n:
                hx = start_x + high_idx * box_w + box_w / 2 - 2
                self.canvas.create_text(hx, y0 - 30, text="HIGH", fill="#F43F5E", font=("Segoe UI", 8, "bold"))
