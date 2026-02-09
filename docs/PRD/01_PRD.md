# PRD: Vietnamese Lunar Calendar Python Package
## `vn-lunar-calendar`

---

## 1. Tổng Quan (Overview)

### 1.1 Mục Tiêu
Xây dựng một **Python package** reusable, chất lượng cao để chuyển đổi và tính toán **Lịch Âm Việt Nam** (Vietnamese Lunar Calendar). Package này sẽ được thiết kế để có thể tích hợp dễ dàng vào các dự án Python khác.

### 1.2 Tên Package
`vn_lunar_calendar`

### 1.3 Phạm Vi Thời Gian Hỗ Trợ
- **Tối thiểu**: 1900 – 2100 (201 năm, tương tự wolfhong/LunarCalendar)
- **Mở rộng (tùy chọn)**: 1200 – 2199 (1000 năm, tương tự nacana22/lunar-date)

### 1.4 Đối Tượng Sử Dụng
- **Developer Python** cần tích hợp lịch âm vào ứng dụng
- **Ứng dụng Numerology/Phong Thủy** cần tính toán ngày âm, can chi, tiết khí
- **Ứng dụng Lịch** hiển thị song song dương lịch – âm lịch

---

## 2. Tính Năng (Features)

### 2.1 Core Features (Bắt buộc)

| # | Feature | Mô Tả |
|---|---------|--------|
| F1 | **Solar → Lunar** | Chuyển đổi ngày Dương lịch sang ngày Âm lịch |
| F2 | **Lunar → Solar** | Chuyển đổi ngày Âm lịch sang ngày Dương lịch |
| F3 | **Tháng nhuận** | Xác định tháng nhuận (leap month) trong năm âm lịch |
| F4 | **Kiểm tra ngày hợp lệ** | Validate ngày dương lịch / âm lịch có tồn tại hay không |
| F5 | **Julian Day Number** | Chuyển đổi qua lại giữa ngày lịch và Julian Day Number |
| F6 | **Can Chi Năm** | Tính tên năm theo Can Chi (Giáp Tý, Ất Sửu...) |
| F7 | **Can Chi Tháng** | Tính tên tháng theo Can Chi |
| F8 | **Can Chi Ngày** | Tính tên ngày theo Can Chi |
| F9 | **Can Chi Giờ** | Tính tên giờ theo Can Chi (12 canh giờ) |
| F10 | **Tiết Khí (Solar Terms)** | Tính 24 tiết khí trong năm |
| F11 | **Giờ Hoàng Đạo** | Tính giờ Hoàng Đạo theo ngày |

### 2.2 Extended Features (Giai đoạn sau)

| # | Feature | Mô Tả |
|---|---------|--------|
| F12 | **Ngày Lễ Âm Lịch** | Tết Nguyên Đán, Rằm tháng Giêng, Vu Lan, Trung Thu... |
| F13 | **Ngày Lễ Dương Lịch** | Ngày cố định (1/1, 30/4...) và không cố định (Mother's Day...) |
| F14 | **Ngày Tốt / Xấu** | Tính ngày tốt xấu cơ bản dựa trên Can Chi |
| F15 | **Multi-timezone** | Hỗ trợ tính toán theo múi giờ khác nhau (mặc định UTC+7) |
| F16 | **CLI Command** | Lệnh command-line để tra cứu nhanh |

---

## 3. Yêu Cầu Phi Chức Năng (Non-Functional Requirements)

### 3.1 Performance
- Chuyển đổi ngày đơn lẻ: **< 1ms**
- Tính toán toàn bộ lịch 1 năm: **< 50ms**
- Memory footprint: **< 5MB**

### 3.2 Accuracy
- Kết quả phải **chính xác 100%** so với dữ liệu chuẩn của Viện Vật lý Địa cầu (hoặc Microsoft ChineseLunisolarCalendar)
- Phải xử lý đúng các trường hợp đặc biệt: tháng nhuận, năm nhuận, ranh giới năm

### 3.3 Compatibility
- **Python**: 3.8+
- **Không có dependency bắt buộc** (pure Python) ngoại trừ standard library
- Hỗ trợ cả `datetime.date` và `datetime.datetime` của Python

### 3.4 Code Quality
- Type hints đầy đủ (PEP 484)
- Docstrings theo chuẩn Google/NumPy style
- Test coverage ≥ 95%
- Tuân thủ PEP 8

### 3.5 Packaging
- Cấu trúc package chuẩn với `pyproject.toml`
- Publish được lên PyPI
- Hỗ trợ cài đặt qua `pip install vn-lunar-calendar`

---

## 4. Thiết Kế API (API Design)

### 4.1 Quick Start

```python
from vn_lunar_calendar import SolarDate, LunarDate, Converter

# Solar → Lunar
solar = SolarDate(2024, 2, 10)
lunar = solar.to_lunar()
print(lunar)  # LunarDate(2024, 1, 1, leap=False)  # Tết Nguyên Đán

# Lunar → Solar
lunar = LunarDate(2024, 1, 1)
solar = lunar.to_solar()
print(solar)  # SolarDate(2024, 2, 10)

# Can Chi
print(lunar.year_name())    # "Giáp Thìn"
print(lunar.month_name())   # "Bính Dần"
print(lunar.day_name())     # "Canh Tuất"
print(lunar.hour_name())    # "Bính Tý"

# Tiết Khí
print(solar.solar_term())   # "Lập xuân"

# Giờ Hoàng Đạo
hours = lunar.lucky_hours()
# [{"name": "Tý", "time": [23, 1]}, ...]

# Tương thích datetime
import datetime
solar = SolarDate.from_date(datetime.date.today())
lunar = solar.to_lunar()
dt = solar.to_date()  # → datetime.date
```

### 4.2 Class Diagram

```
┌──────────────────────┐       ┌──────────────────────┐
│      SolarDate        │       │      LunarDate        │
├──────────────────────┤       ├──────────────────────┤
│ year: int             │       │ year: int             │
│ month: int            │       │ month: int            │
│ day: int              │       │ day: int              │
│ jd: int               │       │ jd: int               │
│                       │       │ is_leap: bool         │
├──────────────────────┤       │ leap_month: int       │
│ to_lunar() → Lunar    │       ├──────────────────────┤
│ to_date() → date      │       │ to_solar() → Solar    │
│ solar_term() → str    │       │ to_date() → date      │
│ from_date(d) → Solar  │       │ year_name() → str     │
│ from_jd(jd) → Solar   │       │ month_name() → str    │
│ jdn() → int           │       │ day_name() → str      │
│ is_valid() → bool     │       │ hour_name() → str     │
└──────────────────────┘       │ lucky_hours() → list  │
         │                      │ solar_term() → str    │
         ▼                      │ from_date(d) → Lunar  │
┌──────────────────────┐       │ from_jd(jd) → Lunar   │
│     Converter         │       │ is_valid() → bool     │
├──────────────────────┤       └──────────────────────┘
│ solar_to_lunar()      │
│ lunar_to_solar()      │
│ jdn_to_solar()        │
│ solar_to_jdn()        │
└──────────────────────┘

┌──────────────────────┐       ┌──────────────────────┐
│    CanChi              │       │    SolarTerms          │
├──────────────────────┤       ├──────────────────────┤
│ year_name(year)       │       │ get_term(jd,tz)       │
│ month_name(month,yr)  │       │ get_all_terms(year)   │
│ day_name(jd)          │       │ TERM_NAMES            │
│ hour_name(jd)         │       └──────────────────────┘
│ CAN: list[str]        │
│ CHI: list[str]        │       ┌──────────────────────┐
└──────────────────────┘       │    LuckyHours          │
                                ├──────────────────────┤
                                │ get_lucky_hours(jd)   │
                                │ LUCKY_PATTERNS        │
                                └──────────────────────┘
```

### 4.3 Error Handling

```python
from vn_lunar_calendar import DateNotExistError, OutOfRangeError

# Ngày không tồn tại
try:
    LunarDate(2024, 2, 30, is_leap=True)  # Tháng 2 nhuận 2024 không tồn tại
except DateNotExistError as e:
    print(e)

# Ngoài phạm vi
try:
    SolarDate(1800, 1, 1)  # Ngoài phạm vi 1900-2100
except OutOfRangeError as e:
    print(e)
```

---

## 5. Cấu Trúc Package (Package Structure)

```
vn_lunar_calendar/
├── __init__.py              # Public API exports
├── solar.py                 # SolarDate class
├── lunar.py                 # LunarDate class
├── converter.py             # Core conversion algorithms
├── canchi.py                # Can Chi calculations
├── solar_terms.py           # 24 Solar Terms (Tiết Khí)
├── lucky_hours.py           # Giờ Hoàng Đạo
├── constants.py             # Lookup tables, Can/Chi names, etc.
├── exceptions.py            # Custom exceptions
├── utils.py                 # Julian Day, helper functions
├── festivals.py             # [Phase 2] Festival definitions
├── py.typed                 # PEP 561 marker
└── data/
    └── lunar_data.py        # Pre-computed lunar calendar data
```

---

## 6. Test Strategy

### 6.1 Unit Tests
- Từng module riêng biệt: converter, canchi, solar_terms, lucky_hours
- Edge cases: ranh giới năm, tháng nhuận, ngày cuối tháng

### 6.2 Integration Tests
- Roundtrip: Solar → Lunar → Solar (phải ra cùng kết quả)
- So sánh kết quả với các thư viện tham khảo

### 6.3 Verification Data
- Đối chiếu với dữ liệu từ **am-lich.com** hoặc **lichvannien.net**
- Lấy mẫu ít nhất **100 ngày ngẫu nhiên** trong phạm vi hỗ trợ
- Kiểm tra đặc biệt: Tết Nguyên Đán, Trung Thu, tháng nhuận qua các năm

---

## 7. Milestones

| Phase | Nội dung | Thời gian ước tính |
|-------|----------|-------------------|
| **Phase 1** | Core: Solar↔Lunar conversion, JDN, validation | 2-3 ngày |
| **Phase 2** | Can Chi (năm, tháng, ngày, giờ) | 1 ngày |
| **Phase 3** | Tiết Khí + Giờ Hoàng Đạo | 1-2 ngày |
| **Phase 4** | Tests, docs, packaging | 1-2 ngày |
| **Phase 5** | Festivals, CLI (mở rộng) | 2-3 ngày |

---

## 8. Tham Khảo (References)

| Repository | Ngôn ngữ | Approach | Phạm vi |
|------------|----------|----------|---------|
| [wolfhong/LunarCalendar](https://github.com/wolfhong/LunarCalendar) | Python | Lookup table (packed binary) | 1900-2100 |
| [nacana22/lunar-date](https://github.com/nacana22/lunar-date) | TypeScript | Year code encoding + JDN | 1200-2199 |
| [ThienMD/lich-van-nien-flutter](https://github.com/ThienMD/lich-van-nien-flutter) | Dart | Astronomical (Jean Meeus) | Không giới hạn |
| [Ho Ngoc Duc's Algorithm](https://www.informatik.uni-leipzig.de/~duc/amlich/) | JS | Astronomical | Chuẩn gốc |
