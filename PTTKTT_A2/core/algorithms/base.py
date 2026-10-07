"""
Algorithm Analysis & Simulation Platform
Core - Base Algorithm Definitions and Metadata
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Generator, List, Optional
from core.simulation.events import SimulationEvent


class AlgorithmCategory(str, Enum):
    SORTING = "SORTING"
    SEARCHING = "SEARCHING"


@dataclass
class AlgorithmMetadata:
    name: str
    display_name: str
    category: AlgorithmCategory
    description: str
    core_idea: str
    pseudocode: str
    best_case: str
    average_case: str
    worst_case: str
    space_complexity: str
    is_stable: bool
    is_in_place: bool
    recurrence_relation: Optional[str] = None
    complexity_explanation: str = ""
    advantages: List[str] = field(default_factory=list)
    disadvantages: List[str] = field(default_factory=list)
    when_to_use: str = ""


@dataclass
class ExecutionStats:
    algorithm_name: str
    execution_time: float
    comparisons: int
    swaps: int
    assignments: int
    success: bool = True
    error_message: Optional[str] = None
    result: Any = None


class BaseAlgorithm:
    """Base class for all algorithm implementations."""

    def __init__(self, metadata: AlgorithmMetadata):
        self.metadata = metadata

    def run_benchmark(self, data: List[Any], **kwargs) -> ExecutionStats:
        """Run pure algorithm execution measuring time and operation counts without yielding events."""
        raise NotImplementedError

    def simulate(self, data: List[Any], **kwargs) -> Generator[SimulationEvent, None, None]:
        """Run simulation yielding events at each critical step."""
        raise NotImplementedError
