"""
Algorithm Analysis & Simulation Platform
Infrastructure - Data Generator
"""
import random
from typing import List


class DataDistribution:
    RANDOM = "Ngẫu nhiên (Random)"
    SORTED_ASC = "Đã sắp xếp tăng"
    SORTED_DESC = "Đã sắp xếp giảm (Ngược)"
    NEARLY_SORTED = "Gần như đã sắp xếp"
    MANY_DUPLICATES = "Nhiều phần tử trùng lặp"


class DataGenerator:
    """Generates synthetic datasets with various statistical distributions."""

    @staticmethod
    def generate(
        size: int,
        distribution: str = DataDistribution.RANDOM,
        min_val: int = 1,
        max_val: int = 100000,
        seed: int = None
    ) -> List[int]:
        if size <= 0:
            return []

        if seed is not None:
            random.seed(seed)

        if min_val > max_val:
            min_val, max_val = max_val, min_val

        if distribution == DataDistribution.SORTED_ASC:
            data = [random.randint(min_val, max_val) for _ in range(size)]
            data.sort()
            return data

        elif distribution == DataDistribution.SORTED_DESC:
            data = [random.randint(min_val, max_val) for _ in range(size)]
            data.sort(reverse=True)
            return data

        elif distribution == DataDistribution.NEARLY_SORTED:
            data = [random.randint(min_val, max_val) for _ in range(size)]
            data.sort()
            # Perform a small number of swaps (~2-3% of elements)
            num_swaps = max(1, int(size * 0.02))
            for _ in range(num_swaps):
                i = random.randint(0, size - 1)
                j = min(size - 1, max(0, i + random.randint(-5, 5)))
                data[i], data[j] = data[j], data[i]
            return data

        elif distribution == DataDistribution.MANY_DUPLICATES:
            # Pick only 3 to 7 distinct values
            num_unique = max(2, min(5, max_val - min_val + 1))
            distinct_pool = random.sample(range(min_val, max_val + 1), min(num_unique, max_val - min_val + 1))
            return [random.choice(distinct_pool) for _ in range(size)]

        else:  # RANDOM
            return [random.randint(min_val, max_val) for _ in range(size)]
