"""
Algorithm Analysis & Simulation Platform
Core - Searching Algorithms Implementation
"""
import time
from typing import Any, Generator, List, Optional
from core.algorithms.base import AlgorithmCategory, AlgorithmMetadata, BaseAlgorithm, ExecutionStats
from core.simulation.events import EventType, SimulationEvent


class LinearSearch(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="linear_search",
            display_name="Linear Search – Tìm kiếm tuyến tính",
            category=AlgorithmCategory.SEARCHING,
            description="Thuật toán tìm kiếm đơn giản nhất bằng cách duyệt tuần tự từng phần tử từ đầu đến cuối danh sách cho đến khi tìm thấy mục tiêu hoặc hết danh sách.",
            core_idea="Kiểm tra lần lượt từng phần tử: nếu A[i] == target thì trả về i, nếu đi hết mảng mà không thấy thì kết luận không tồn tại.",
            pseudocode="""procedure linearSearch(A : list, target : item)
    for i = 0 to length(A) - 1 do
        if A[i] == target then
            return i
        end if
    end for
    return -1
end procedure""",
            best_case="O(1)",
            average_case="O(n)",
            worst_case="O(n)",
            space_complexity="O(1)",
            is_stable=True,
            is_in_place=True,
            recurrence_relation="T(n) = T(n-1) + O(1) => T(n) = O(n)",
            complexity_explanation="""• Best case O(1): Phần tử cần tìm nằm ngay tại vị trí đầu tiên (A[0] == target), chỉ mất 1 phép so sánh.
• Worst case O(n): Phần tử nằm ở vị trí cuối cùng hoặc không hề tồn tại trong mảng, thuật toán phải duyệt qua toàn bộ n phần tử.
• Average case O(n): Giả sử phần tử xuất hiện ở các vị trí với xác suất đồng đều, trung bình số phép so sánh là (n + 1) / 2 = O(n).
• Bộ nhớ phụ O(1) vì không sử dụng thêm cấu trúc dữ liệu nào.""",
            advantages=[
                "Không yêu cầu dữ liệu phải sắp xếp trước (hoạt động trên mọi loại mảng).",
                "Cài đặt cực kỳ đơn giản và trực quan.",
                "Thích hợp khi chỉ cần tìm kiếm 1 lần duy nhất trên tập dữ liệu chưa có thứ tự."
            ],
            disadvantages=[
                "Hiệu suất kém khi n lớn (hàng chục nghìn đến hàng triệu phần tử).",
                "Lãng phí thời gian nếu phải thực hiện nhiều truy vấn tìm kiếm liên tục."
            ],
            when_to_use="Khi danh sách chưa được sắp xếp và số lượng truy vấn tìm kiếm rất ít (1 hoặc vài lần), hoặc khi n rất nhỏ."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], target: Any = None, **kwargs) -> ExecutionStats:
        arr = list(data)
        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0
        found_idx = -1

        if target is None:
            # Default target: pick middle or last element, or a value from array
            target = arr[len(arr) // 2] if n > 0 else 0

        start_time = time.perf_counter()
        for i in range(n):
            comps += 1
            if arr[i] == target:
                found_idx = i
                break
        elapsed = time.perf_counter() - start_time

        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=found_idx
        )

    def simulate(self, data: List[Any], target: Any = None, **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)

        if n == 0:
            yield SimulationEvent(EventType.NOT_FOUND, [], [], [], "Mảng rỗng, không tìm thấy mục tiêu.")
            yield SimulationEvent(EventType.FINISHED, [], [], [], "Kết thúc tìm kiếm.")
            return

        if target is None:
            target = arr[len(arr) // 2]

        yield SimulationEvent(
            EventType.COMPARE,
            [],
            [target],
            list(arr),
            f"Bắt đầu Linear Search tìm mục tiêu target = {target}"
        )

        found = False
        for i in range(n):
            yield SimulationEvent(
                EventType.COMPARE,
                [i],
                [arr[i], target],
                list(arr),
                f"Bước {i + 1}: So sánh arr[{i}] = {arr[i]} với target = {target}"
            )
            if arr[i] == target:
                yield SimulationEvent(
                    EventType.FOUND,
                    [i],
                    [arr[i]],
                    list(arr),
                    f"TÌM THẤY! Mục tiêu {target} nằm tại chỉ số {i}."
                )
                found = True
                break

        if not found:
            yield SimulationEvent(
                EventType.NOT_FOUND,
                [],
                [target],
                list(arr),
                f"Đã duyệt hết mảng nhưng KHÔNG TÌM THẤY mục tiêu {target}."
            )

        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Linear Search kết thúc.")


class BinarySearch(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="binary_search",
            display_name="Binary Search – Tìm kiếm nhị phân",
            category=AlgorithmCategory.SEARCHING,
            description="Thuật toán tìm kiếm theo phương pháp Chia để trị, liên tục chia đôi không gian tìm kiếm bằng cách so sánh mục tiêu với phần tử đứng giữa mảng đã sắp xếp.",
            core_idea="Xác định phần tử giữa (mid). Nếu target == mid: tìm thấy. Nếu target < mid: thu hẹp về nửa trái. Nếu target > mid: thu hẹp về nửa phải. Lặp lại cho đến khi tìm thấy hoặc không gian tìm kiếm rỗng.",
            pseudocode="""procedure binarySearch(A : sorted list, target : item)
    low = 0
    high = length(A) - 1
    while low <= high do
        mid = (low + high) / 2
        if A[mid] == target then
            return mid
        else if A[mid] < target then
            low = mid + 1
        else
            high = mid - 1
        end if
    end while
    return -1
end procedure""",
            best_case="O(1)",
            average_case="O(log n)",
            worst_case="O(log n)",
            space_complexity="O(1)",
            is_stable=True,
            is_in_place=True,
            recurrence_relation="T(n) = T(n/2) + O(1). Theo Định lý Thợ: a=1, b=2, d=0 => log_b(a) = 0 = d => T(n) = O(log n).",
            complexity_explanation="""• Mỗi bước so sánh, kích thước không gian tìm kiếm giảm đi một nửa: n -> n/2 -> n/4 -> ... -> 1.
• Số bước tối đa để giảm n về 1 là ⌈log₂(n)⌉ + 1.
• Best case O(1): Phần tử cần tìm nằm chính xác tại vị trí giữa (mid) ở lần kiểm tra đầu tiên.
• Average & Worst case O(log n): Kể cả khi n = 1.000.000 phần tử, Binary Search chỉ mất tối đa ~20 phép so sánh!
• YÊU CẦU BẮT BUỘC: Mảng phải được sắp xếp trước theo thứ tự xác định.""",
            advantages=[
                "Tốc độ tìm kiếm cực nhanh: O(log n). Với 1 tỷ phần tử chỉ mất khoảng 30 phép so sánh.",
                "Sử dụng O(1) bộ nhớ phụ (cài đặt lặp vòng while).",
                "Rất hiệu quả cho các bài toán có nhiều lượt truy vấn liên tục."
            ],
            disadvantages=[
                "BẮT BUỘC mảng đầu vào phải được sắp xếp trước.",
                "Nếu mảng chưa sắp xếp và chỉ tìm kiếm 1 lần, chi phí sắp xếp O(n log n) + O(log n) lớn hơn nhiều so với Linear Search O(n)."
            ],
            when_to_use="Khi mảng đã được sắp xếp trước, hoặc hệ thống cần thực hiện rất nhiều truy vấn tìm kiếm (khấu hao được chi phí sắp xếp ban đầu)."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], target: Any = None, **kwargs) -> ExecutionStats:
        # Note: assumes or ensures data is sorted for benchmark
        arr = list(data)
        # Check if sorted, if not sort for valid benchmark
        # Note: prompt states fair benchmark; we document if sorting was needed
        is_sorted = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
        if not is_sorted:
            arr.sort()

        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0
        found_idx = -1

        if target is None:
            target = arr[len(arr) // 2] if n > 0 else 0

        start_time = time.perf_counter()
        low = 0
        high = n - 1
        while low <= high:
            mid = (low + high) // 2
            comps += 1
            if arr[mid] == target:
                found_idx = mid
                break
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        elapsed = time.perf_counter() - start_time

        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=found_idx
        )

    def simulate(self, data: List[Any], target: Any = None, **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)

        if n == 0:
            yield SimulationEvent(EventType.NOT_FOUND, [], [], [], "Mảng rỗng, không tìm thấy mục tiêu.")
            yield SimulationEvent(EventType.FINISHED, [], [], [], "Kết thúc tìm kiếm.")
            return

        is_sorted = all(arr[i] <= arr[i + 1] for i in range(n - 1))
        if not is_sorted:
            yield SimulationEvent(
                EventType.COMPARE,
                [],
                [],
                list(arr),
                "CẢNH BÁO: Mảng chưa được sắp xếp! Binary Search tự động sắp xếp trước để hoạt động chính xác."
            )
            arr.sort()

        if target is None:
            target = arr[len(arr) // 2]

        yield SimulationEvent(
            EventType.RANGE,
            [0, n - 1],
            [arr[0], arr[n - 1]],
            list(arr),
            f"Bắt đầu Binary Search: tìm target = {target} trong phạm vi [0..{n-1}]"
        )

        low = 0
        high = n - 1
        found = False

        while low <= high:
            mid = (low + high) // 2
            yield SimulationEvent(
                EventType.RANGE,
                [low, mid, high],
                [arr[low], arr[mid], arr[high]],
                list(arr),
                f"Không gian tìm kiếm [{low}..{high}]: phần tử giữa mid = {mid} (giá trị = {arr[mid]})"
            )
            yield SimulationEvent(
                EventType.COMPARE,
                [mid],
                [arr[mid], target],
                list(arr),
                f"So sánh arr[{mid}] = {arr[mid]} với target = {target}"
            )

            if arr[mid] == target:
                yield SimulationEvent(
                    EventType.FOUND,
                    [mid],
                    [arr[mid]],
                    list(arr),
                    f"TÌM THẤY! target = {target} tại chỉ số {mid}."
                )
                found = True
                break
            elif arr[mid] < target:
                yield SimulationEvent(
                    EventType.RANGE,
                    [mid + 1, high],
                    [],
                    list(arr),
                    f"Vì {arr[mid]} < {target}, loại bỏ nửa trái [0..{mid}]. Tiếp tục tìm trong [{mid+1}..{high}]"
                )
                low = mid + 1
            else:
                yield SimulationEvent(
                    EventType.RANGE,
                    [low, mid - 1],
                    [],
                    list(arr),
                    f"Vì {arr[mid]} > {target}, loại bỏ nửa phải [{mid}..{high}]. Tiếp tục tìm trong [{low}..{mid-1}]"
                )
                high = mid - 1

        if not found:
            yield SimulationEvent(
                EventType.NOT_FOUND,
                [],
                [target],
                list(arr),
                f"Phạm vi tìm kiếm rỗng (low > high). KHÔNG TÌM THẤY {target} trong mảng."
            )

        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Binary Search kết thúc.")
