"""
CÁC KỸ THUẬT CƠ BẢN PHÂN TÍCH THUẬT TOÁN
Algorithm Analysis & Simulation Platform
Entry point
"""
import sys
import os

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ui.app import AlgorithmPlatformApp


def main():
    try:
        app = AlgorithmPlatformApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nỨng dụng đã kết thúc bởi người dùng.")
        sys.exit(0)
    except Exception as e:
        import traceback
        print(f"\n[CRITICAL ERROR] Khởi chạy ứng dụng thất bại: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
