"""
Algorithm Analysis & Simulation Platform
Core - Algorithm Registry
"""
from typing import Dict, List, Optional
from core.algorithms.base import AlgorithmCategory, AlgorithmMetadata, BaseAlgorithm
from core.algorithms.searching import BinarySearch, LinearSearch
from core.algorithms.sorting import (
    BubbleSort,
    InsertionSort,
    MergeSort,
    QuickSort,
    SelectionSort,
)


class AlgorithmRegistry:
    """Central registry holding all supported algorithms and their metadata."""

    def __init__(self):
        self._algorithms: Dict[str, BaseAlgorithm] = {}
        self._register_defaults()

    def _register_defaults(self):
        defaults = [
            # Sorting
            BubbleSort(),
            SelectionSort(),
            InsertionSort(),
            MergeSort(),
            QuickSort(),
            # Searching
            LinearSearch(),
            BinarySearch(),
        ]
        for alg in defaults:
            self.register(alg)

    def register(self, algorithm: BaseAlgorithm):
        self._algorithms[algorithm.metadata.name] = algorithm

    def get_algorithm(self, name: str) -> Optional[BaseAlgorithm]:
        return self._algorithms.get(name)

    def get_metadata(self, name: str) -> Optional[AlgorithmMetadata]:
        alg = self.get_algorithm(name)
        return alg.metadata if alg else None

    def get_all(self) -> List[BaseAlgorithm]:
        return list(self._algorithms.values())

    def get_by_category(self, category: AlgorithmCategory) -> List[BaseAlgorithm]:
        return [
            alg for alg in self._algorithms.values()
            if alg.metadata.category == category
        ]

    def get_names_by_category(self, category: AlgorithmCategory) -> List[str]:
        return [
            alg.metadata.name for alg in self._algorithms.values()
            if alg.metadata.category == category
        ]


# Global singleton instance
registry = AlgorithmRegistry()
