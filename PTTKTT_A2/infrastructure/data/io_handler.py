"""
Algorithm Analysis & Simulation Platform
Infrastructure - Input/Output & File Handler
"""
import csv
import os
import re
from typing import Any, List, Union


class DataIOHandler:
    """Handles text parsing and file importing (CSV, TXT) with robust validation."""

    @staticmethod
    def parse_string(raw_text: str) -> List[Union[int, float]]:
        """Parses comma, space, or bracket delimited string into numeric list."""
        if not raw_text or not raw_text.strip():
            raise ValueError("Dữ liệu nhập rỗng! Vui lòng nhập dãy số.")

        # Clean brackets if any
        cleaned = raw_text.strip()
        if cleaned.startswith("[") and cleaned.endswith("]"):
            cleaned = cleaned[1:-1]
        elif cleaned.startswith("(") and cleaned.endswith(")"):
            cleaned = cleaned[1:-1]

        # Split on commas, spaces, semicolons, newlines, tabs
        tokens = re.split(r"[,;\s\t\n]+", cleaned.strip())
        result: List[Union[int, float]] = []

        for token in tokens:
            if not token:
                continue
            try:
                # Try integer first
                if "." in token:
                    result.append(float(token))
                else:
                    result.append(int(token))
            except ValueError:
                raise ValueError(f"Giá trị không hợp lệ: '{token}'. Chỉ chấp nhận số nguyên hoặc số thực.")

        if not result:
            raise ValueError("Không tìm thấy số hợp lệ nào trong chuỗi nhập.")

        return result

    @staticmethod
    def load_from_file(file_path: str) -> List[Union[int, float]]:
        """Reads dataset from CSV or TXT file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in (".csv", ".txt"):
            raise ValueError("Định dạng file không được hỗ trợ! Vui lòng chọn file .csv hoặc .txt")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()

        return DataIOHandler.parse_string(content)
