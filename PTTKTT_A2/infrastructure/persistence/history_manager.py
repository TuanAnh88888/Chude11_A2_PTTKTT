"""
Algorithm Analysis & Simulation Platform
Infrastructure - History Persistence Manager
"""
import json
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class HistoryRecord:
    id: str
    timestamp: str
    problem_type: str
    size: int
    characteristic: str
    recommended_alg: str
    reasoning_summary: str
    benchmark_summary: str


class HistoryManager:
    """Manages persistent analysis history stored in JSON format."""

    def __init__(self, storage_path: str = "data/history.json"):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        dir_name = os.path.dirname(self.storage_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def load_all(self) -> List[Dict[str, Any]]:
        self._ensure_storage()
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_record(self, record: HistoryRecord) -> bool:
        records = self.load_all()
        # Prepend so newest is at the top
        records.insert(0, asdict(record))
        # Keep maximum 50 most recent records
        records = records[:50]
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def delete_record(self, record_id: str) -> bool:
        records = self.load_all()
        records = [r for r in records if r.get("id") != record_id]
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def clear_all(self) -> bool:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
