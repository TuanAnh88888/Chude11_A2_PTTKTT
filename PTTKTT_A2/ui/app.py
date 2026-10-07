"""
Algorithm Analysis & Simulation Platform
UI - Main Application Window and View Controller
"""
import tkinter as tk
from typing import Any, Dict, List, Optional
import customtkinter as ctk

from core.algorithms.base import AlgorithmCategory
from core.benchmark.metrics import MultiSizeBenchmarkResult, SingleBenchmarkMetric
from core.complexity.analyzer import InputAnalysisResult
from core.recommendation.engine import RecommendationResult
from ui.components.sidebar import ModernSidebar
from ui.views.analysis_view import AnalysisView
from ui.views.benchmark_view import BenchmarkView
from ui.views.big_o_view import BigOView
from ui.views.comparison_view import ComparisonView
from ui.views.custom_code_view import CustomCodeView
from ui.views.dashboard_view import DashboardView
from ui.views.demo_view import DemoView
from ui.views.history_view import HistoryView
from ui.views.library_view import LibraryView
from ui.views.simulation_view import SimulationView


class AlgorithmPlatformApp(ctk.CTk):
    """Main application window controlling navigation and shared session state."""

    def __init__(self):
        super().__init__()

        # Appearance & Geometry
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("CÁC KỸ THUẬT CƠ BẢN PHÂN TÍCH THUẬT TOÁN – Academic Platform")
        self.geometry("1280x800")
        self.minsize(1050, 680)

        # Global Session State
        self.current_data: List[Any] = [12, 45, 7, 23, 89, 34, 5, 91, 18, 55, 3, 42, 67, 10, 28]
        self.current_category: AlgorithmCategory = AlgorithmCategory.SORTING
        self.current_analysis: Optional[InputAnalysisResult] = None
        self.current_recommendation: Optional[RecommendationResult] = None
        self.last_benchmark_results: Optional[List[SingleBenchmarkMetric]] = None
        self.last_benchmark_multi: Optional[MultiSizeBenchmarkResult] = None

        # Build Main Frame Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left Sidebar
        self.sidebar = ModernSidebar(self, on_navigate=self.navigate_to)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Right Main Content Container
        self.content_container = ctk.CTkFrame(self, corner_radius=0, fg_color=("#F1F5F9", "#0B1120"))
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Views Dictionary
        self.views: Dict[str, ctk.CTkFrame] = {}
        self._init_views()

        # Initial Navigation to Dashboard
        self.navigate_to("dashboard")

    def _init_views(self):
        self.views["dashboard"] = DashboardView(self.content_container, app_controller=self)
        self.views["simulation"] = SimulationView(self.content_container, app_controller=self)
        self.views["benchmark"] = BenchmarkView(self.content_container, app_controller=self)
        self.views["comparison"] = ComparisonView(self.content_container, app_controller=self)
        self.views["library"] = LibraryView(self.content_container, app_controller=self)
        self.views["history"] = HistoryView(self.content_container, app_controller=self)

        # Initially map only the dashboard view
        self.views["dashboard"].grid(row=0, column=0, sticky="nsew")

    def navigate_to(self, view_name: str):
        target = self.views.get(view_name)
        if not target:
            return

        # Notify sidebar active state
        self.sidebar.set_active(view_name)

        # Hide all other views completely to prevent canvas overlapping
        for name, view in self.views.items():
            if name != view_name:
                view.grid_remove()

        # Place and raise the target view
        target.grid(row=0, column=0, sticky="nsew")
        target.tkraise()

        # Lifecycle hooks
        if view_name == "dashboard" and hasattr(target, "refresh"):
            target.refresh()
        elif view_name == "simulation" and hasattr(target, "sync_from_controller"):
            target.sync_from_controller()
        elif view_name == "history" and hasattr(target, "refresh_list"):
            target.refresh_list()
