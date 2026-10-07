# CHỦ ĐỀ 11
# CÁC KỸ THUẬT CƠ BẢN PHÂN TÍCH THUẬT TOÁN
## ALGORITHM ANALYSIS & SIMULATION PLATFORM

> Nền tảng phân tích, mô phỏng và kiểm chứng thực nghiệm thuật toán phục vụ môn học **Phân tích và Thiết kế Thuật toán**.

---

## 1. GIỚI THIỆU & MỤC TIÊU DỰ ÁN

Hệ thống được thiết kế theo mô hình **Algorithm Analysis & Simulation Platform** chuyên sâu, không phải là một ứng dụng CRUD thông thường. Nền tảng giải quyết bài toán cốt lõi:

* Không chỉ chạy một thuật toán được chỉ định trước, mà tiếp nhận bài toán và tập dữ liệu đầu vào.
* Tự động bóc tách các đặc tính thống kê của dữ liệu (kích thước $n$, trạng thái thứ tự, tỷ lệ nghịch thế, số lượng phần tử trùng lặp, độ phân tán).
* Xác định danh sách các thuật toán ứng viên (Candidates).
* Phân tích độ phức tạp tiệm cận (Big-O Asymptotic Complexity): Best Case, Average Case, Worst Case, và Space Complexity.
* **Động cơ Đề xuất Thông minh (Recommendation Engine)** đưa ra **"Thuật toán được đề xuất" (Recommended Algorithm)** cùng lập luận khoa học, phân tích đánh đổi (trade-offs) và cảnh báo trường hợp suy biến (worst-case caveats).
* Mô phỏng từng bước (Step-by-step Simulation) trực quan với cơ chế tách biệt hoàn toàn giữa Thuật toán và Giao diện đồ họa thông qua chuỗi sự kiện `yield SimulationEvent`.
* **Đo lường Benchmark độc lập** bằng `time.perf_counter()`, đo lường thời gian thực thi thuần túy, số phép so sánh, hoán đổi mà không bị sai lệch bởi GUI/Animation.
* Đối chiếu xu hướng tăng trưởng giữa **Lý thuyết Big-O** và **Kết quả thực nghiệm**.

---

## 2. KIẾN TRÚC HỆ THỐNG

Dự án áp dụng kiến trúc phân tầng chuẩn mực (Layered Architecture & Separation of Concerns):

```text
PTTKTT_A2/
│
├── core/                               # Tầng Logic cốt lõi (Hoàn toàn độc lập GUI)
│   ├── algorithms/                     # Cài đặt thuật toán & Metadata Registry
│   │   ├── base.py                     # Lớp cơ sở BaseAlgorithm, Metadata, ExecutionStats
│   │   ├── sorting.py                  # Bubble, Selection, Insertion, Merge, Quick Sort
│   │   ├── searching.py                # Linear Search, Binary Search
│   │   └── registry.py                 # Centralized Algorithm Registry
│   ├── complexity/                     # Phân tích độ phức tạp & Toán học Big-O
│   │   ├── analyzer.py                 # Phân tích đặc tính tập dữ liệu đầu vào
│   │   └── big_o_math.py               # Hàm tăng trưởng lý thuyết & curve fitting
│   ├── recommendation/                 # Động cơ đề xuất thuật toán
│   │   └── engine.py                   # Multi-criteria decision engine & trade-offs
│   ├── simulation/                     # Sự kiện mô phỏng
│   │   └── events.py                   # SimulationEvent, EventType (Compare, Swap, Pivot...)
│   ├── benchmark/                      # Động cơ đo đạc hiệu năng thực tế
│   │   ├── runner.py                   # Đo thời gian bằng perf_counter, kiểm soát warm-up
│   │   └── metrics.py                  # Single & Multi-size Benchmark Metrics
│   └── ast_analyzer/                   # Phân tích tĩnh mã nguồn Python người dùng
│       └── static_analyzer.py          # Bóc tách AST: vòng lặp, lồng nhau, đệ quy
│
├── infrastructure/                     # Tầng hạ tầng dữ liệu & tiện ích
│   ├── data/                           # Sinh và nạp dữ liệu
│   │   ├── generator.py                # Sinh Random, Sorted, Reverse, Nearly Sorted, Duplicates
│   │   └── io_handler.py               # Xử lý chuỗi nhập, file CSV và TXT
│   ├── persistence/                    # Lưu trữ lịch sử phân tích
│   │   └── history_manager.py          # Quản lý file data/history.json
│   └── export/                         # Xuất báo cáo học thuật
│       └── report_exporter.py          # Xuất báo cáo đầy đủ ra TXT và CSV
│
├── ui/                                 # Giao diện người dùng (Modern Academic Dashboard)
│   ├── components/                     # Các khối UI tái sử dụng
│   │   ├── sidebar.py                  # Thanh điều hướng Sidebar hiện đại
│   │   ├── stat_card.py                # Thẻ thống kê KPI
│   │   ├── chart_canvas.py             # Khung vẽ biểu đồ Matplotlib tương tác
│   │   └── simulation_canvas.py        # Khung vẽ cột và mảng mô phỏng hoạt họa
│   ├── views/                          # 10 Màn hình chức năng chính
│   │   ├── dashboard_view.py           # Tổng quan, KPI, quy trình 6 bước
│   │   ├── analysis_view.py            # Nhập bài toán, dữ liệu, phân tích & đề xuất
│   │   ├── simulation_view.py          # Mô phỏng từng bước / tự động / thanh tốc độ
│   │   ├── benchmark_view.py           # Benchmark độc lập (Single & Multi-size)
│   │   ├── comparison_view.py          # Ma trận so sánh & Lý thuyết vs Thực nghiệm
│   │   ├── big_o_view.py               # Biểu đồ họ đường cong Big-O tương tác
│   │   ├── library_view.py             # Bách khoa toàn thư thuật toán & hệ thức đệ quy
│   │   ├── custom_code_view.py         # Phân tích tĩnh AST mã Python tùy biến
│   │   ├── history_view.py             # Lịch sử phiên làm việc & xuất báo cáo
│   │   └── demo_view.py                # Không gian Demo thuyết trình (4 kịch bản)
│   └── app.py                          # Cửa sổ chính & Điều hướng ứng dụng
│
├── tests/                              # Bộ kiểm thử tự động (Unit & Integration tests)
│   ├── test_algorithms.py              # Test tính đúng đắn của 7 thuật toán & mô phỏng
│   ├── test_recommendation.py          # Test động cơ đề xuất trên nhiều mẫu dữ liệu
│   ├── test_benchmark.py               # Test động cơ đo đạc hiệu năng
│   ├── test_ast_analyzer.py            # Test bộ phân tích cú pháp AST
│   └── test_integration_e2e.py         # Test chu trình tích hợp End-to-End
│
├── main.py                             # Điểm khởi chạy ứng dụng chính
├── requirements.txt                    # Thư viện phụ thuộc
└── README.md                           # Tài liệu hướng dẫn sử dụng
```

---

## 3. CÁC THUẬT TOÁN HỖ TRỢ & ĐỘ PHỨC TẠP LÝ THUYẾT

### Nhóm Thuật toán Tìm kiếm (Searching)
| Thuật toán | Best Case | Average Case | Worst Case | Bộ nhớ phụ | Ràng buộc đầu vào |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | Mọi danh sách |
| **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | **Bắt buộc mảng đã sắp xếp** |

### Nhóm Thuật toán Sắp xếp (Sorting)
| Thuật toán | Best Case | Average Case | Worst Case | Space | Ổn định (Stable) | Tại chỗ (In-place) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Có | Có |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Không | Có |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Có | Có |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Có | Không |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | Không | Có |

### Hệ thức truy hồi đệ quy (Recurrence Relations)
* **Merge Sort**: 
  $$T(n) = 2T(n/2) + O(n) \implies O(n \log n)$$ (theo Định lý Thợ - Master Theorem với $a=2, b=2, d=1$).
* **Quick Sort**:
  * Trường hợp trung bình: $T(n) = 2T(n/2) + O(n) \implies O(n \log n)$
  * Trường hợp xấu nhất (suy biến): $T(n) = T(n-1) + O(n) \implies O(n^2)$
* **Binary Search**:
  $$T(n) = T(n/2) + O(1) \implies O(\log n)$$

---

## 4. QUY TRÌNH HOẠT ĐỘNG CHÍNH CỦA HỆ THỐNG

```text
NHẬP BÀI TOÁN / THUẬT TOÁN
            ↓
      NHẬP DỮ LIỆU (Trực tiếp / Tự sinh / File CSV, TXT)
            ↓
     PHÂN TÍCH ĐẦU VÀO (Size, Kiểu, Thứ tự, Nghịch thế, Trùng lặp, Phân tán)
            ↓
  XÁC ĐỊNH THUẬT TOÁN CÓ THỂ DÙNG (Candidates)
            ↓
  PHÂN TÍCH TIME + SPACE COMPLEXITY (Best, Avg, Worst, Phân tích đệ quy)
            ↓
   ĐỀ XUẤT THUẬT TOÁN PHÙ HỢP (Lý do khoa học, Đánh đổi, Cảnh báo suy biến)
            ↓
       CHẠY MÔ PHỎNG (Sự kiện tách biệt, Từng bước, Tự động, Điều chỉnh tốc độ)
            ↓
      ĐO THỜI GIAN THỰC TẾ (perf_counter, Số phép so sánh, Số phép hoán đổi)
            ↓
       BENCHMARK ĐA QUY MÔ (Đo trên nhiều n khác nhau, cùng tập dữ liệu)
            ↓
       SO SÁNH THUẬT TOÁN (Đối chiếu ma trận & Lý thuyết vs Thực nghiệm)
            ↓
     BIỂU ĐỒ & BÁO CÁO KẾT QUẢ (Xuất báo cáo chi tiết TXT / CSV)
```

---

## 5. CÀI ĐẶT & KHỞI CHẠY

### Yêu cầu môi trường
* Python 3.8 trở lên (Khuyến nghị Python 3.10, 3.11, 3.12, 3.13)
* Hệ điều hành: Windows, macOS, hoặc Linux

### Bước 1: Mở Terminal tại thư mục dự án
```bash
cd f:\PTTKTT_A2
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Khuyến nghị)
* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt)**:
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```

### Bước 3: Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 4: Chạy kiểm thử tự động (Unit Tests)
```bash
python -m unittest discover tests
```
Tất cả 16 bài kiểm tra sẽ hoàn thành trong vòng < 0.1s.

### Bước 5: Khởi chạy ứng dụng
```bash
python main.py
```

---

## 6. KỊCH BẢN DEMO THUYẾT TRÌNH TRƯỚC GIẢNG VIÊN

Hệ thống tích hợp sẵn tab **"🚀 Kịch bản Demo"** giúp sinh viên thực hiện bài thuyết trình mượt mà:

### Kịch bản Demo 1: Linear Search vs Binary Search
1. Chọn bài toán Tìm kiếm với $n = 50.000$ phần tử đã sắp xếp.
2. Hệ thống phân tích và đề xuất: **Binary Search** ($O(\log n)$).
3. Chạy đo thực nghiệm:
   * Binary Search chỉ mất tối đa **~16 phép so sánh** ($\approx 0.005\text{ ms}$).
   * Linear Search mất trung bình **~25.000 phép so sánh** ($\approx 1.2\text{ ms}$).
4. Giải thích thêm bài toán kinh tế tiền xử lý: Nếu mảng chưa sắp xếp và chỉ tìm kiếm 1 lần duy nhất ($q = 1$), Linear Search $O(n)$ có lợi hơn chi phí sắp xếp $O(n \log n)$ của Binary Search!

### Kịch bản Demo 2: Phân kỳ $O(n^2)$ vs $O(n \log n)$ (Bubble vs Merge vs Quick)
1. Chọn dữ liệu ngẫu nhiên $n = 3.000$.
2. Hệ thống phân tích và chỉ ra sự chênh lệch:
   * Bubble Sort tiêu tốn gần **4.5 triệu phép so sánh** ($O(n^2)$), mất hàng trăm mili-giây.
   * Quick Sort & Merge Sort chỉ tốn khoảng **35.000 phép so sánh** ($O(n \log n)$), hoàn thành trong vài mili-giây.

### Kịch bản Demo 3: Dữ liệu gần sắp xếp (Nearly Sorted) – Best Case của Insertion Sort
1. Chọn phân bố "Gần như đã sắp xếp" với $n = 5.000$.
2. Hệ thống đề xuất: **Insertion Sort** thay vì Quick Sort hay Merge Sort.
3. Giải thích: Tỷ lệ nghịch thế rất nhỏ ($< 2\%$), Insertion Sort tiệm cận thời gian tuyến tính $O(n)$, overhead nhỏ hơn Quick/Merge Sort và không tốn bộ nhớ phụ $O(n)$. Đây là minh chứng rõ ràng nhất cho việc: **Không có thuật toán nào là tối ưu tuyệt đối trong mọi hoàn cảnh.**

### Kịch bản Demo 4: Đối chiếu Đường cong Lý thuyết vs Thực nghiệm
1. Chạy đa quy mô $n \in [100, 500, 1000, 2000, 5000]$.
2. Quan sát đồ thị: Đường thực nghiệm khớp với hàm Big-O lý thuyết đã được chuẩn hóa qua thuật toán Least Squares.

---

## 7. CÁC TÍNH NĂNG NỔI BẬT KHÁC

* **Phân tích tĩnh mã Python (Static AST Analyzer)**: Cho phép người dùng nhập trực tiếp một hàm Python bất kỳ, bóc tách số lượng vòng lặp, độ sâu lồng nhau, nhận diện hàm đệ quy để đưa ra ước tính Big-O sơ bộ kèm cảnh báo bài toán dừng Turing.
* **Biểu đồ Big-O tương tác**: Thanh trượt $n_{max}$ trực quan hóa tốc độ bùng nổ của hàm mũ $O(2^n)$ và bậc hai $O(n^2)$ so với các hàm logarit.
* **Xuất báo cáo học thuật**: Hỗ trợ xuất kết quả phân tích đầy đủ và bảng đo thời gian ra định dạng `.txt` và `.csv`.
* **Cơ chế an toàn hiệu năng**: Tự động cảnh báo và chuyển từ chế độ mô phỏng đồ họa sang Benchmark thuần túy khi $n > 1000$ để chống treo giao diện.

---

## 8. TÁC GIẢ & THÔNG TIN ĐỒ ÁN
* **Môn học**: Phân tích và Thiết kế Thuật toán (PTTKTT)
* **Phiên bản**: 1.0 Academic Edition
* **Nền tảng**: Python 3.x • CustomTkinter • Matplotlib
