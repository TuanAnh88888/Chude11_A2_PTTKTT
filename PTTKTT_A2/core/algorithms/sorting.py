"""
Algorithm Analysis & Simulation Platform
Core - Sorting Algorithms Implementation
"""
import time
from typing import Any, Generator, List
from core.algorithms.base import AlgorithmCategory, AlgorithmMetadata, BaseAlgorithm, ExecutionStats
from core.simulation.events import EventType, SimulationEvent


class BubbleSort(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="bubble_sort",
            display_name="Bubble Sort – Sắp xếp nổi bọt",
            category=AlgorithmCategory.SORTING,
            description="Thuật toán sắp xếp so sánh cơ bản bằng cách liên tục duyệt qua danh sách, so sánh hai phần tử liền kề và đổi chỗ nếu chúng sai thứ tự.",
            core_idea="Đẩy dần phần tử lớn nhất về cuối mảng sau mỗi lượt duyệt như bọt khí nổi lên mặt nước. Sử dụng cờ hiệu (flag) để dừng sớm nếu mảng đã sắp xếp.",
            pseudocode="""procedure bubbleSort(A : list of sortable items)
    n = length(A)
    repeat
        swapped = false
        for i = 1 to n-1 inclusive do
            if A[i-1] > A[i] then
                swap(A[i-1], A[i])
                swapped = true
            end if
        end for
        n = n - 1
    until not swapped
end procedure""",
            best_case="O(n)",
            average_case="O(n²)",
            worst_case="O(n²)",
            space_complexity="O(1)",
            is_stable=True,
            is_in_place=True,
            recurrence_relation="Không đệ quy. Tổng số phép so sánh: S = (n-1) + (n-2) + ... + 1 = n(n-1)/2",
            complexity_explanation="""• Vòng lặp ngoài duyệt tối đa (n - 1) lượt: O(n)
• Vòng lặp trong so sánh các cặp liền kề: O(n)
• Hai vòng lặp lồng nhau: O(n × n) = O(n²) trong trường hợp trung bình và xấu nhất.
• Best case O(n): Khi mảng đã có thứ tự sẵn, cờ swapped không bao giờ bật True ở lượt đầu tiên, thuật toán dừng ngay sau n-1 phép so sánh.""",
            advantages=[
                "Dễ hiểu, dễ cài đặt nhất trong các thuật toán sắp xếp.",
                "Nhận biết được mảng đã sắp xếp sẵn với độ phức tạp O(n).",
                "Là thuật toán ổn định (Stable) và tại chỗ (In-place, O(1) bộ nhớ phụ)."
            ],
            disadvantages=[
                "Hiệu suất rất kém O(n²) trên tập dữ liệu lớn.",
                "Số phép hoán đổi nhiều hơn Insertion Sort và Selection Sort."
            ],
            when_to_use="Chỉ phù hợp cho mục đích giáo dục, hoặc tập dữ liệu rất nhỏ (n < 50) và gần như đã có thứ tự."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], **kwargs) -> ExecutionStats:
        arr = list(data)
        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0

        start_time = time.perf_counter()
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                comps += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
                    swapped = True
            if not swapped:
                break
        elapsed = time.perf_counter() - start_time

        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=arr
        )

    def simulate(self, data: List[Any], **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)
        if n == 0:
            yield SimulationEvent(EventType.FINISHED, [], [], [], "Mảng rỗng, kết thúc.")
            return

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                yield SimulationEvent(
                    EventType.COMPARE,
                    [j, j + 1],
                    [arr[j], arr[j + 1]],
                    list(arr),
                    f"So sánh arr[{j}]={arr[j]} và arr[{j+1}]={arr[j+1]}"
                )
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    yield SimulationEvent(
                        EventType.SWAP,
                        [j, j + 1],
                        [arr[j], arr[j + 1]],
                        list(arr),
                        f"Đổi chỗ: {arr[j+1]} > {arr[j]} -> hoán đổi vị trí {j} và {j+1}"
                    )
            
            yield SimulationEvent(
                EventType.MARK_SORTED,
                [n - i - 1],
                [arr[n - i - 1]],
                list(arr),
                f"Phần tử arr[{n - i - 1}]={arr[n - i - 1]} đã về đúng vị trí cuối cùng của lượt."
            )
            if not swapped:
                yield SimulationEvent(
                    EventType.FINISHED,
                    [],
                    [],
                    list(arr),
                    "Không còn phép hoán đổi nào trong lượt vừa qua. Mảng đã hoàn tất sắp xếp sớm!"
                )
                return

        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Bubble Sort hoàn tất sắp xếp.")


class SelectionSort(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="selection_sort",
            display_name="Selection Sort – Sắp xếp chọn",
            category=AlgorithmCategory.SORTING,
            description="Thuật toán tìm phần tử nhỏ nhất trong đoạn chưa sắp xếp và hoán đổi nó về vị trí đầu tiên của đoạn đó.",
            core_idea="Chia danh sách làm 2 phần: phần đã sắp xếp (bên trái) và phần chưa sắp xếp (bên phải). Mỗi vòng chọn phần tử cực tiểu đưa về cuối phần đã sắp xếp.",
            pseudocode="""procedure selectionSort(A : list of sortable items)
    n = length(A)
    for i = 0 to n - 2 do
        minIndex = i
        for j = i + 1 to n - 1 do
            if A[j] < A[minIndex] then
                minIndex = j
            end if
        end for
        if minIndex != i then
            swap(A[i], A[minIndex])
        end if
    end for
end procedure""",
            best_case="O(n²)",
            average_case="O(n²)",
            worst_case="O(n²)",
            space_complexity="O(1)",
            is_stable=False,
            is_in_place=True,
            recurrence_relation="Tổng số phép so sánh luôn cố định: n(n-1)/2 trong mọi trường hợp.",
            complexity_explanation="""• Vòng ngoài lặp n - 1 lần.
• Vòng trong luôn so sánh từ i+1 đến n-1 để tìm min, bất kể mảng đã có thứ tự hay chưa.
• Tổng phép so sánh: (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n²) trong cả Best, Average và Worst case.
• Số lần hoán đổi (swaps) tối đa chỉ là n - 1 (rất ít so với Bubble Sort).""",
            advantages=[
                "Số lần hoán đổi bộ nhớ (swaps) tối thiểu: tối đa n-1 lần swap. Hữu ích khi chi phí ghi bộ nhớ (write) rất đắt.",
                "In-place O(1) bộ nhớ phụ.",
                "Cài đặt đơn giản, hoạt động tốt trên mảng nhỏ."
            ],
            disadvantages=[
                "Luôn mất O(n²) phép so sánh dù mảng đã sắp xếp trước đó.",
                "Không ổn định (Unstable) trong cách cài đặt tiêu chuẩn."
            ],
            when_to_use="Khi kích thước dữ liệu nhỏ và chi phí hoán đổi/ghi phần tử vào bộ nhớ đắt hơn nhiều so với phép so sánh."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], **kwargs) -> ExecutionStats:
        arr = list(data)
        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0

        start_time = time.perf_counter()
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                comps += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1
        elapsed = time.perf_counter() - start_time

        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=arr
        )

    def simulate(self, data: List[Any], **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)
        if n == 0:
            yield SimulationEvent(EventType.FINISHED, [], [], [], "Mảng rỗng, kết thúc.")
            return

        for i in range(n - 1):
            min_idx = i
            yield SimulationEvent(
                EventType.PIVOT,
                [i],
                [arr[i]],
                list(arr),
                f"Vòng {i}: Giả định giá trị nhỏ nhất tạm thời là arr[{i}]={arr[i]}"
            )

            for j in range(i + 1, n):
                yield SimulationEvent(
                    EventType.COMPARE,
                    [j, min_idx],
                    [arr[j], arr[min_idx]],
                    list(arr),
                    f"So sánh ứng viên arr[{j}]={arr[j]} với min hiện tại arr[{min_idx}]={arr[min_idx]}"
                )
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    yield SimulationEvent(
                        EventType.PIVOT,
                        [min_idx],
                        [arr[min_idx]],
                        list(arr),
                        f"Cập nhật min mới: arr[{min_idx}]={arr[min_idx]}"
                    )

            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                yield SimulationEvent(
                    EventType.SWAP,
                    [i, min_idx],
                    [arr[i], arr[min_idx]],
                    list(arr),
                    f"Đổi chỗ phần tử nhỏ nhất arr[{min_idx}]={arr[i]} về vị trí đã chọn arr[{i}]={arr[min_idx]}"
                )

            yield SimulationEvent(
                EventType.MARK_SORTED,
                [i],
                [arr[i]],
                list(arr),
                f"Phần tử arr[{i}]={arr[i]} đã cố định đúng vị trí."
            )

        yield SimulationEvent(
            EventType.MARK_SORTED,
            [n - 1],
            [arr[n - 1]],
            list(arr),
            f"Phần tử cuối cùng arr[{n-1}]={arr[n-1]} tự động đúng vị trí."
        )
        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Selection Sort hoàn tất sắp xếp.")


class InsertionSort(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="insertion_sort",
            display_name="Insertion Sort – Sắp xếp chèn",
            category=AlgorithmCategory.SORTING,
            description="Xây dựng mảng đã sắp xếp từng phần tử một bằng cách lấy phần tử tiếp theo và chèn vào đúng vị trí trong đoạn con đã sắp xếp phía trước.",
            core_idea="Tương tự cách xếp các quân bài tây trên tay: cầm một quân bài mới, duyệt ngược về trước để tìm chỗ thích hợp rồi chèn vào.",
            pseudocode="""procedure insertionSort(A : list of sortable items)
    n = length(A)
    for i = 1 to n - 1 do
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key do
            A[j + 1] = A[j]
            j = j - 1
        end while
        A[j + 1] = key
    end for
end procedure""",
            best_case="O(n)",
            average_case="O(n²)",
            worst_case="O(n²)",
            space_complexity="O(1)",
            is_stable=True,
            is_in_place=True,
            recurrence_relation="Không đệ quy. Số phép dịch chuyển phụ thuộc độ nghịch thế của mảng.",
            complexity_explanation="""• Vòng lặp ngoài duyệt từ phần tử thứ 2 đến n: O(n).
• Vòng while dịch chuyển các phần tử lớn hơn key:
  - Best case O(n): Khi mảng đã sắp xếp tăng sẵn, điều kiện A[j] > key sai ngay lập tức ở mỗi bước, vòng while chạy 0 lần. Chỉ mất n - 1 phép so sánh.
  - Worst case O(n²): Khi mảng bị sắp xếp ngược hoàn toàn, mỗi bước đều phải dịch toàn bộ dãy con phía trước: 1 + 2 + ... + (n-1) = n(n-1)/2 phép gán.
  - Average case O(n²): Trung bình mỗi phần tử phải dịch một nửa đoạn con phía trước.""",
            advantages=[
                "Cực kỳ hiệu quả trên dữ liệu đã sắp xếp sẵn hoặc gần như đã sắp xếp (O(n)).",
                "Hiệu quả hơn Bubble Sort và Selection Sort trên mảng nhỏ.",
                "Thuật toán ổn định (Stable) và tại chỗ (In-place).",
                "Là thuật toán trực tuyến (Online): có thể sắp xếp dữ liệu khi đang nhận dòng dữ liệu đầu vào."
            ],
            disadvantages=[
                "Độ phức tạp O(n²) khi dữ liệu ngẫu nhiên hoặc sắp xếp ngược với n lớn."
            ],
            when_to_use="Khi mảng có kích thước nhỏ (n < 50), hoặc dữ liệu đã gần như được sắp xếp sẵn (Nearly Sorted)."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], **kwargs) -> ExecutionStats:
        arr = list(data)
        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0

        start_time = time.perf_counter()
        for i in range(1, n):
            key = arr[i]
            assigns += 1
            j = i - 1
            while j >= 0:
                comps += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    assigns += 1
                    swaps += 1  # count logical shift/swap
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            assigns += 1
        elapsed = time.perf_counter() - start_time

        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=arr
        )

    def simulate(self, data: List[Any], **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)
        if n == 0:
            yield SimulationEvent(EventType.FINISHED, [], [], [], "Mảng rỗng, kết thúc.")
            return

        yield SimulationEvent(
            EventType.MARK_SORTED,
            [0],
            [arr[0]],
            list(arr),
            f"Phần tử đầu tiên arr[0]={arr[0]} tự thân xem như đoạn đã sắp xếp."
        )

        for i in range(1, n):
            key = arr[i]
            yield SimulationEvent(
                EventType.PIVOT,
                [i],
                [key],
                list(arr),
                f"Lấy khóa key = arr[{i}] = {key} để chèn vào dãy [0..{i-1}]"
            )

            j = i - 1
            while j >= 0:
                yield SimulationEvent(
                    EventType.COMPARE,
                    [j, j + 1],
                    [arr[j], key],
                    list(arr),
                    f"So sánh arr[{j}]={arr[j]} với key={key}"
                )
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    yield SimulationEvent(
                        EventType.ASSIGN,
                        [j + 1],
                        [arr[j + 1]],
                        list(arr),
                        f"Dịch arr[{j}]={arr[j]} sang phải vị trí {j+1}"
                    )
                    j -= 1
                else:
                    break

            arr[j + 1] = key
            yield SimulationEvent(
                EventType.ASSIGN,
                [j + 1],
                [key],
                list(arr),
                f"Chèn key={key} vào vị trí thích hợp {j+1}"
            )
            yield SimulationEvent(
                EventType.MARK_SORTED,
                list(range(0, i + 1)),
                [arr[k] for k in range(0, i + 1)],
                list(arr),
                f"Đoạn [0..{i}] đã được sắp xếp tăng dần."
            )

        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Insertion Sort hoàn tất sắp xếp.")


class MergeSort(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="merge_sort",
            display_name="Merge Sort – Sắp xếp trộn",
            category=AlgorithmCategory.SORTING,
            description="Thuật toán sắp xếp theo phương pháp Chia để trị (Divide and Conquer), chia đôi mảng liên tục cho đến khi còn 1 phần tử rồi trộn lại có thứ tự.",
            core_idea="Chia danh sách thành 2 nửa bằng nhau, đệ quy sắp xếp từng nửa, sau đó trộn (merge) hai nửa đã sắp xếp lại thành một mảng hoàn chỉnh.",
            pseudocode="""procedure mergeSort(A : list)
    if length(A) <= 1 then
        return A
    mid = length(A) / 2
    left = mergeSort(A[0..mid])
    right = mergeSort(A[mid..n])
    return merge(left, right)
end procedure

procedure merge(left, right)
    result = empty list
    while left is not empty and right is not empty do
        if left[0] <= right[0] then
            append left[0] to result; remove left[0]
        else
            append right[0] to result; remove right[0]
        end if
    end while
    append remaining items to result
    return result
end procedure""",
            best_case="O(n log n)",
            average_case="O(n log n)",
            worst_case="O(n log n)",
            space_complexity="O(n)",
            is_stable=True,
            is_in_place=False,
            recurrence_relation="T(n) = 2T(n/2) + O(n). Theo Định lý Thợ (Master Theorem): a=2, b=2, d=1 => log_b(a) = 1 = d => T(n) = O(n log n).",
            complexity_explanation="""• Cây đệ quy có độ sâu là log₂(n) tầng vì mỗi bước mảng bị chia đôi.
• Ở mỗi tầng của cây đệ quy, tổng chi phí để trộn (merge) tất cả các đoạn con lại là O(n).
• Nhân số tầng với chi phí mỗi tầng: log₂(n) × O(n) = O(n log n).
• Độ phức tạp O(n log n) được đảm bảo trong MỌI trường hợp (Best, Average, Worst).
• Space Complexity là O(n) do cần mảng phụ để lưu trữ tạm các phần tử trong quá trình trộn.""",
            advantages=[
                "Hiệu suất O(n log n) ổn định tuyệt đối trong mọi tình huống dữ liệu.",
                "Thuật toán ổn định (Stable) – giữ nguyên thứ tự tương đối của các phần tử bằng nhau.",
                "Rất thích hợp cho danh sách liên kết (Linked List) hoặc sắp xếp ngoài (External Sorting) trên ổ đĩa."
            ],
            disadvantages=[
                "Cần O(n) không gian bộ nhớ phụ để trộn.",
                "Hằng số ẩn lớn hơn Quick Sort trong môi trường RAM thông thường."
            ],
            when_to_use="Khi cần hiệu suất O(n log n) ổn định, không có đột biến xấu, và bộ nhớ RAM không phải là giới hạn ngặt nghèo."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], **kwargs) -> ExecutionStats:
        arr = list(data)
        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0

        start_time = time.perf_counter()

        def _merge_sort_bench(low: int, high: int):
            nonlocal comps, assigns
            if low >= high:
                return
            mid = (low + high) // 2
            _merge_sort_bench(low, mid)
            _merge_sort_bench(mid + 1, high)

            # In-place merge simulation with temp list
            left_part = arr[low:mid + 1]
            right_part = arr[mid + 1:high + 1]
            i = 0
            j = 0
            k = low

            while i < len(left_part) and j < len(right_part):
                comps += 1
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                assigns += 1
                k += 1

            while i < len(left_part):
                arr[k] = left_part[i]
                i += 1
                k += 1
                assigns += 1

            while j < len(right_part):
                arr[k] = right_part[j]
                j += 1
                k += 1
                assigns += 1

        if n > 1:
            _merge_sort_bench(0, n - 1)

        elapsed = time.perf_counter() - start_time
        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=arr
        )

    def simulate(self, data: List[Any], **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)
        if n <= 1:
            yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Mảng <= 1 phần tử, đã hoàn tất.")
            return

        def _merge_sort_sim(low: int, high: int):
            if low >= high:
                return

            mid = (low + high) // 2
            yield SimulationEvent(
                EventType.PARTITION,
                [low, mid, high],
                [arr[low], arr[mid], arr[high]],
                list(arr),
                f"Chia đoạn [{low}..{high}] thành 2 nửa: [{low}..{mid}] và [{mid+1}..{high}]"
            )

            yield from _merge_sort_sim(low, mid)
            yield from _merge_sort_sim(mid + 1, high)

            yield SimulationEvent(
                EventType.PARTITION,
                [low, high],
                [],
                list(arr),
                f"Bắt đầu trộn 2 đoạn con [{low}..{mid}] và [{mid+1}..{high}] vào mảng chính"
            )

            left_part = arr[low:mid + 1]
            right_part = arr[mid + 1:high + 1]
            i = 0
            j = 0
            k = low

            while i < len(left_part) and j < len(right_part):
                yield SimulationEvent(
                    EventType.COMPARE,
                    [k],
                    [left_part[i], right_part[j]],
                    list(arr),
                    f"So sánh phần tử trái {left_part[i]} và phần tử phải {right_part[j]}"
                )
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                yield SimulationEvent(
                    EventType.ASSIGN,
                    [k],
                    [arr[k]],
                    list(arr),
                    f"Gán arr[{k}] = {arr[k]}"
                )
                k += 1

            while i < len(left_part):
                arr[k] = left_part[i]
                yield SimulationEvent(
                    EventType.ASSIGN,
                    [k],
                    [arr[k]],
                    list(arr),
                    f"Gán phần tử còn lại từ nửa trái: arr[{k}] = {arr[k]}"
                )
                i += 1
                k += 1

            while j < len(right_part):
                arr[k] = right_part[j]
                yield SimulationEvent(
                    EventType.ASSIGN,
                    [k],
                    [arr[k]],
                    list(arr),
                    f"Gán phần tử còn lại từ nửa phải: arr[{k}] = {arr[k]}"
                )
                j += 1
                k += 1

            yield SimulationEvent(
                EventType.MARK_SORTED,
                list(range(low, high + 1)),
                [arr[idx] for idx in range(low, high + 1)],
                list(arr),
                f"Đoạn [{low}..{high}] đã trộn hoàn tất có thứ tự."
            )

        yield from _merge_sort_sim(0, n - 1)
        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Merge Sort hoàn tất sắp xếp.")


class QuickSort(BaseAlgorithm):
    def __init__(self):
        metadata = AlgorithmMetadata(
            name="quick_sort",
            display_name="Quick Sort – Sắp xếp nhanh",
            category=AlgorithmCategory.SORTING,
            description="Thuật toán Chia để trị chọn một phần tử làm chốt (pivot), phân hoạch mảng thành hai nửa: các phần tử nhỏ hơn chốt sang trái và lớn hơn chốt sang phải, rồi đệ quy sắp xếp hai nửa.",
            core_idea="Phân hoạch mảng quanh pivot sao cho sau bước phân hoạch, pivot đứng chính xác ở vị trí cuối cùng của nó trong mảng đã sắp xếp.",
            pseudocode="""procedure quickSort(A, low, high)
    if low < high then
        p = partition(A, low, high)
        quickSort(A, low, p - 1)
        quickSort(A, p + 1, high)
    end if
end procedure

procedure partition(A, low, high)
    pivot = A[high]
    i = low - 1
    for j = low to high - 1 do
        if A[j] <= pivot then
            i = i + 1
            swap(A[i], A[j])
        end if
    end for
    swap(A[i + 1], A[high])
    return i + 1
end procedure""",
            best_case="O(n log n)",
            average_case="O(n log n)",
            worst_case="O(n²)",
            space_complexity="O(log n) call stack (hoặc O(n) worst case)",
            is_stable=False,
            is_in_place=True,
            recurrence_relation="""• Average Case: T(n) = 2T(n/2) + O(n) => O(n log n)
• Worst Case: T(n) = T(n-1) + O(n) => O(n²)""",
            complexity_explanation="""• Phân hoạch Lomuto/Hoare duyệt qua mảng mất O(n) thời gian.
• Average Case: Khi pivot chia mảng thành các phần tương đối cân đối (vd: n/2 và n/2), cây đệ quy có độ sâu log₂(n) tầng. Mỗi tầng mất O(n) phân hoạch => O(n log n).
• Worst Case O(n²): Xảy ra khi pivot luôn là phần tử nhỏ nhất hoặc lớn nhất (ví dụ mảng đã sắp xếp nhưng chọn pivot ở đầu/cuối). Cây đệ quy thoái hóa thành đường thẳng độ sâu n tầng => T(n) = n + (n-1) + ... + 1 = O(n²).
• Space: O(log n) ngăn xếp đệ quy trong trường hợp tốt/trung bình.""",
            advantages=[
                "Thường là thuật toán sắp xếp nhanh nhất trong thực tế đối với mảng trong bộ nhớ RAM (hệ số ẩn nhỏ, tận dụng bộ nhớ đệm cache CPU cực tốt).",
                "Sắp xếp tại chỗ (In-place), chỉ tốn O(log n) bộ nhớ ngăn xếp đệ quy.",
                "Được nhiều ngôn ngữ lập trình chọn làm thuật toán chuẩn (C qsort, Java Dual-Pivot Quicksort)."
            ],
            disadvantages=[
                "Không ổn định (Unstable).",
                "Trường hợp xấu nhất có thể rơi vào O(n²) nếu chọn pivot không tốt.",
                "Dễ bị tấn công suy biến hiệu suất nếu dữ liệu có chủ đích độc hại."
            ],
            when_to_use="Khi cần hiệu suất sắp xếp thực tế cao nhất trên dữ liệu tổng quát và bộ nhớ phụ hạn chế."
        )
        super().__init__(metadata)

    def run_benchmark(self, data: List[Any], **kwargs) -> ExecutionStats:
        arr = list(data)
        n = len(arr)
        comps = 0
        swaps = 0
        assigns = 0

        start_time = time.perf_counter()

        # Non-recursive iterative quicksort using explicit stack to avoid Python recursion limit
        stack = [(0, n - 1)] if n > 1 else []
        while stack:
            low, high = stack.pop()
            if low < high:
                # Median-of-three or Lomuto partition
                pivot = arr[high]
                i = low - 1
                for j in range(low, high):
                    comps += 1
                    if arr[j] <= pivot:
                        i += 1
                        if i != j:
                            arr[i], arr[j] = arr[j], arr[i]
                            swaps += 1
                i += 1
                if i != high:
                    arr[i], arr[high] = arr[high], arr[i]
                    swaps += 1
                p = i

                if p - 1 > low:
                    stack.append((low, p - 1))
                if high > p + 1:
                    stack.append((p + 1, high))

        elapsed = time.perf_counter() - start_time
        return ExecutionStats(
            algorithm_name=self.metadata.name,
            execution_time=elapsed,
            comparisons=comps,
            swaps=swaps,
            assignments=assigns,
            result=arr
        )

    def simulate(self, data: List[Any], **kwargs) -> Generator[SimulationEvent, None, None]:
        arr = list(data)
        n = len(arr)
        if n <= 1:
            yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Mảng <= 1 phần tử, đã hoàn tất.")
            return

        def _quick_sort_sim(low: int, high: int):
            if low < high:
                pivot_val = arr[high]
                yield SimulationEvent(
                    EventType.PIVOT,
                    [high],
                    [pivot_val],
                    list(arr),
                    f"Chọn pivot = arr[{high}] = {pivot_val} trong đoạn [{low}..{high}]"
                )

                i = low - 1
                for j in range(low, high):
                    yield SimulationEvent(
                        EventType.COMPARE,
                        [j, high],
                        [arr[j], pivot_val],
                        list(arr),
                        f"So sánh arr[{j}]={arr[j]} với pivot={pivot_val}"
                    )
                    if arr[j] <= pivot_val:
                        i += 1
                        if i != j:
                            arr[i], arr[j] = arr[j], arr[i]
                            yield SimulationEvent(
                                EventType.SWAP,
                                [i, j],
                                [arr[i], arr[j]],
                                list(arr),
                                f"Đưa phần tử nhỏ hơn/bằng pivot sang trái: hoán đổi arr[{i}] và arr[{j}]"
                            )

                i += 1
                if i != high:
                    arr[i], arr[high] = arr[high], arr[i]
                    yield SimulationEvent(
                        EventType.SWAP,
                        [i, high],
                        [arr[i], arr[high]],
                        list(arr),
                        f"Đưa pivot arr[{high}]={pivot_val} về vị trí chốt chuẩn xác arr[{i}]"
                    )

                p = i
                yield SimulationEvent(
                    EventType.MARK_SORTED,
                    [p],
                    [arr[p]],
                    list(arr),
                    f"Pivot tại vị trí {p} (giá trị {arr[p]}) đã cố định chính xác!"
                )

                yield from _quick_sort_sim(low, p - 1)
                yield from _quick_sort_sim(p + 1, high)

        yield from _quick_sort_sim(0, n - 1)
        yield SimulationEvent(
            EventType.MARK_SORTED,
            list(range(n)),
            list(arr),
            list(arr),
            "Toàn bộ mảng đã được phân hoạch và sắp xếp hoàn chỉnh."
        )
        yield SimulationEvent(EventType.FINISHED, [], [], list(arr), "Quick Sort hoàn tất sắp xếp.")
