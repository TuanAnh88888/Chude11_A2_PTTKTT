"""
Algorithm Analysis & Simulation Platform
UI - Step-by-Step Algorithm Simulation View
"""
from typing import Any, List, Optional
import customtkinter as ctk
from tkinter import messagebox
from core.algorithms.base import AlgorithmCategory
from core.algorithms.registry import registry
from core.simulation.events import EventType, SimulationEvent
from ui.components.simulation_canvas import SimulationCanvas


class SimulationView(ctk.CTkFrame):
    """Visual interactive step-by-step and auto-play algorithm simulator."""

    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = app_controller

        # Simulation state
        self.generator = None
        self.is_playing = False
        self.current_step = 0
        self.delay_ms = 60
        self.sorted_indices = set()
        self.sim_data = []

        self._build_ui()

    def _build_ui(self):
        # Header title
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        lbl_head = ctk.CTkLabel(
            header,
            text="MÔ PHỎNG THỰC THI THUẬT TOÁN",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#F8FAFC")
        )
        lbl_head.pack(anchor="w")

        lbl_desc = ctk.CTkLabel(
            header,
            text="Quan sát trực quan từng bước so sánh, đổi chỗ, phân hoạch và thu hẹp không gian tìm kiếm.",
            font=ctk.CTkFont(size=12),
            text_color=("#64748B", "#94A3B8")
        )
        lbl_desc.pack(anchor="w")

        # Control Toolbar
        toolbar = ctk.CTkFrame(self, corner_radius=10, fg_color=("#FFFFFF", "#1E293B"))
        toolbar.pack(fill="x", padx=20, pady=8)

        # Left: Algorithm Selection
        tb_left = ctk.CTkFrame(toolbar, fg_color="transparent")
        tb_left.pack(side="left", padx=16, pady=12)

        ctk.CTkLabel(tb_left, text="Thuật toán:").pack(side="left", padx=(0, 6))
        self.combo_alg = ctk.CTkComboBox(
            tb_left,
            values=[alg.metadata.display_name for alg in registry.get_all()],
            width=260,
            command=self._on_alg_change
        )
        self.combo_alg.pack(side="left")

        # Right: Speed Slider & Target entry
        tb_right = ctk.CTkFrame(toolbar, fg_color="transparent")
        tb_right.pack(side="right", padx=16, pady=12)

        ctk.CTkLabel(tb_right, text="Tốc độ (ms):").pack(side="left", padx=(0, 6))
        self.slider_speed = ctk.CTkSlider(
            tb_right,
            from_=5,
            to=300,
            number_of_steps=60,
            width=140,
            command=self._on_speed_change
        )
        self.slider_speed.set(60)
        self.slider_speed.pack(side="left", padx=(0, 12))

        self.lbl_speed_val = ctk.CTkLabel(tb_right, text="60 ms", width=50)
        self.lbl_speed_val.pack(side="left")

        # Big Visual Canvas
        self.canvas_comp = SimulationCanvas(self, width=780, height=340)
        self.canvas_comp.pack(fill="both", expand=True, padx=20, pady=8)

        # Step Status / Explanation Banner
        self.status_box = ctk.CTkFrame(self, corner_radius=8, fg_color=("#F1F5F9", "#0F172A"), border_width=1, border_color=("#CBD5E1", "#334155"))
        self.status_box.pack(fill="x", padx=20, pady=4)

        self.lbl_step_counter = ctk.CTkLabel(
            self.status_box,
            text="Bước: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        )
        self.lbl_step_counter.pack(side="left", padx=16, pady=8)

        self.lbl_step_desc = ctk.CTkLabel(
            self.status_box,
            text="Sẵn sàng mô phỏng. Bấm '▶ Chạy' hoặc '⏭ Bước tiếp'.",
            font=ctk.CTkFont(size=12),
            text_color=("#1E293B", "#E2E8F0")
        )
        self.lbl_step_desc.pack(side="left", padx=8, pady=8)

        # Bottom Buttons Bar: Play, Pause, Step, Reset
        btn_bar = ctk.CTkFrame(self, fg_color="transparent")
        btn_bar.pack(fill="x", padx=20, pady=(8, 16))

        self.btn_play = ctk.CTkButton(
            btn_bar,
            text="▶ Chạy tự động",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            width=130,
            command=self.play
        )
        self.btn_play.pack(side="left", padx=(0, 8))

        self.btn_pause = ctk.CTkButton(
            btn_bar,
            text="⏸ Tạm dừng",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#D97706",
            hover_color="#B45309",
            width=110,
            command=self.pause
        )
        self.btn_pause.pack(side="left", padx=8)

        self.btn_step = ctk.CTkButton(
            btn_bar,
            text="⏭ Bước tiếp",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            width=110,
            command=self.step
        )
        self.btn_step.pack(side="left", padx=8)

        self.btn_reset = ctk.CTkButton(
            btn_bar,
            text="↻ Làm lại",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#64748B",
            hover_color="#475569",
            width=110,
            command=self.reset
        )
        self.btn_reset.pack(side="left", padx=8)

        self.btn_switch_bench = ctk.CTkButton(
            btn_bar,
            text="⚡ Chuyển sang Benchmark",
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            command=lambda: self.controller.navigate_to("benchmark")
        )
        self.btn_switch_bench.pack(side="right")

    def _on_speed_change(self, value):
        self.delay_ms = int(value)
        self.lbl_speed_val.configure(text=f"{self.delay_ms} ms")

    def _on_alg_change(self, choice):
        self.reset()

    def sync_from_controller(self):
        """Called whenever the user opens this view to synchronize selected algorithm & data."""
        rec = self.controller.current_recommendation
        if rec:
            self.combo_alg.set(rec.primary_recommendation.display_name)
        self.reset()

    def _get_active_algorithm(self):
        choice = self.combo_alg.get()
        for alg in registry.get_all():
            if alg.metadata.display_name == choice:
                return alg
        return registry.get_all()[0]

    def reset(self):
        self.is_playing = False
        self.generator = None
        self.current_step = 0
        self.sorted_indices.clear()

        # Get data from controller, or default sample
        if self.controller.current_data:
            raw = list(self.controller.current_data)
        else:
            raw = [12, 45, 7, 23, 89, 34, 5, 91, 18, 55, 3, 42, 67, 10, 28]

        # Dataset size threshold safety (Section 21)
        if len(raw) > 1000:
            msg = (
                f"Kích thước dữ liệu hiện tại (n = {len(raw):,}) quá lớn để mô phỏng từng bước trực quan "
                "bằng giao diện đồ họa (sẽ làm treo GUI).\n\n"
                "Hệ thống tự động cắt lấy 60 phần tử đại diện để mô phỏng, hoặc bạn có thể chuyển sang "
                "chế độ Benchmark để đo hiệu năng toàn bộ tập dữ liệu."
            )
            messagebox.showinfo("Giới hạn mô phỏng", msg)
            self.sim_data = raw[:60]
        elif len(raw) > 100:
            self.sim_data = raw[:100]
        else:
            self.sim_data = list(raw)

        alg = self._get_active_algorithm()
        is_searching = alg.metadata.category == AlgorithmCategory.SEARCHING

        if is_searching:
            # Target
            target = self.sim_data[len(self.sim_data) // 2] if self.sim_data else 0
            self.generator = alg.simulate(list(self.sim_data), target=target)
            self.canvas_comp.render_searching_state(self.sim_data)
        else:
            self.generator = alg.simulate(list(self.sim_data))
            self.canvas_comp.render_sorting_state(self.sim_data)

        self.lbl_step_counter.configure(text="Bước: 0")
        self.lbl_step_desc.configure(text=f"Khởi tạo {alg.metadata.display_name} với n = {len(self.sim_data)}")

    def step(self) -> bool:
        """Executes a single step. Returns True if more steps remain, False if finished."""
        if self.generator is None:
            self.reset()

        try:
            event: SimulationEvent = next(self.generator)
            self.current_step += 1
            self.lbl_step_counter.configure(text=f"Bước: {self.current_step}")
            self.lbl_step_desc.configure(text=event.description)

            alg = self._get_active_algorithm()
            is_searching = alg.metadata.category == AlgorithmCategory.SEARCHING

            if event.event_type == EventType.MARK_SORTED:
                for idx in event.indices:
                    self.sorted_indices.add(idx)

            if is_searching:
                self.canvas_comp.render_searching_state(event.array_state, event)
            else:
                self.canvas_comp.render_sorting_state(event.array_state, event, self.sorted_indices)

            if event.event_type == EventType.FINISHED:
                self.is_playing = False
                return False

            return True

        except StopIteration:
            self.is_playing = False
            self.lbl_step_desc.configure(text="Mô phỏng đã hoàn tất!")
            return False

    def play(self):
        if self.is_playing:
            return
        self.is_playing = True
        self._auto_step()

    def _auto_step(self):
        if not self.is_playing:
            return
        has_more = self.step()
        if has_more and self.is_playing:
            self.after(self.delay_ms, self._auto_step)

    def pause(self):
        self.is_playing = False
