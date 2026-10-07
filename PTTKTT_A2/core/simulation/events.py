"""
Algorithm Analysis & Simulation Platform
Core - Simulation Events
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


class EventType(str, Enum):
    COMPARE = "COMPARE"          # So sánh 2 phần tử
    SWAP = "SWAP"                # Hoán đổi 2 phần tử
    ASSIGN = "ASSIGN"            # Gán giá trị (ví dụ trong Insertion Sort, Merge Sort)
    PIVOT = "PIVOT"              # Chọn pivot (Quick Sort)
    PARTITION = "PARTITION"      # Xác định vùng partition
    RANGE = "RANGE"              # Thu hẹp phạm vi tìm kiếm (Binary Search: low, mid, high)
    FOUND = "FOUND"              # Tìm thấy phần tử
    NOT_FOUND = "NOT_FOUND"      # Không tìm thấy
    MARK_SORTED = "MARK_SORTED"  # Đánh dấu phần tử đã ở vị trí đúng
    FINISHED = "FINISHED"        # Thuật toán kết thúc


@dataclass
class SimulationEvent:
    event_type: EventType
    indices: List[int]           # Các chỉ số liên quan (vd: [i, j])
    values: List[Any]            # Giá trị các phần tử liên quan
    array_state: List[Any]       # Trạng thái mảng tại thời điểm này
    description: str             # Giải thích bước hiện tại bằng tiếng Việt
    additional_info: Optional[dict] = None
