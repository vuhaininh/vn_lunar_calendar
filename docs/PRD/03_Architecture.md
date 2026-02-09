# Kiến Trúc Hệ Thống: Vietnamese Lunar Calendar Package
## Architecture & Technical Design

---

## 1. Kiến Trúc Tổng Quan (High-Level Architecture)

```mermaid
graph TB
    subgraph "Public API Layer"
        A[SolarDate] 
        B[LunarDate]
        C[Converter]
    end
    
    subgraph "Feature Modules"
        D[CanChi]
        E[SolarTerms]
        F[LuckyHours]
        G[Festivals]
    end
    
    subgraph "Core Engine"
        H[JulianDay Utils]
        I[NewMoon Calculator]
        J[SunLongitude Calculator]
    end
    
    subgraph "Data Layer"
        K[Constants]
        L[Exceptions]
    end
    
    A --> C
    B --> C
    A --> E
    B --> D
    B --> F
    C --> H
    C --> I
    C --> J
    D --> K
    E --> J
    F --> K
    I --> K
    J --> K
end
```

---

## 2. Chi Tiết Module

### 2.1 Module Map

| File | Responsibility | Dependencies |
|------|---------------|-------------|
| `__init__.py` | Public exports | All modules |
| `solar.py` | SolarDate class | converter, solar_terms, utils |
| `lunar.py` | LunarDate class | converter, canchi, lucky_hours, utils |
| `converter.py` | Solar↔Lunar conversion engine | utils (JDN, NewMoon, SunLong) |
| `canchi.py` | Can Chi naming | constants |
| `solar_terms.py` | 24 Tiết Khí | utils (SunLongitude) |
| `lucky_hours.py` | Giờ Hoàng Đạo | constants |
| `constants.py` | All static data (Can, Chi, patterns) | None |
| `exceptions.py` | Custom exceptions | None |
| `utils.py` | JDN, NewMoon, SunLongitude core math | math (stdlib) |
| `festivals.py` | [Phase 2] Festival definitions | converter, constants |

### 2.2 Dependency Graph (Tránh Circular Import)

```
constants.py ←── exceptions.py          (no dependencies)
     ↑               ↑
     │               │
  utils.py ──────────┘                  (depends on: constants, exceptions)
     ↑
     │
converter.py                            (depends on: utils, exceptions)
     ↑
     ├─────────────────┐
     │                  │
  solar.py          lunar.py            (depends on: converter)
     │                  │
     │              ┌───┤
     │              │   │
     │         canchi.py │
     │              lucky_hours.py
     │
  solar_terms.py                        (depends on: utils)
```

---

## 3. Class Design Chi Tiết

### 3.1 SolarDate

```python
@dataclass(frozen=True)
class SolarDate:
    """Ngày dương lịch (Gregorian Calendar)."""
    year: int
    month: int
    day: int
    
    def __post_init__(self):
        """Validate date on creation."""
        
    # Conversion methods
    def to_lunar(self, timezone: float = 7.0) -> 'LunarDate': ...
    def to_date(self) -> datetime.date: ...
    def to_jdn(self) -> int: ...
    
    # Solar term
    def solar_term(self, timezone: float = 7.0) -> str: ...
    
    # Factory methods
    @classmethod
    def from_date(cls, d: datetime.date) -> 'SolarDate': ...
    @classmethod
    def from_jdn(cls, jd: int) -> 'SolarDate': ...
    @classmethod
    def today(cls) -> 'SolarDate': ...
    
    # Comparison operators
    def __eq__, __lt__, __le__, __gt__, __ge__
```

### 3.2 LunarDate

```python
@dataclass(frozen=True)
class LunarDate:
    """Ngày âm lịch (Vietnamese Lunar Calendar)."""
    year: int
    month: int
    day: int
    is_leap: bool = False     # True nếu là tháng nhuận
    
    def __post_init__(self):
        """Validate lunar date."""
    
    # Conversion methods
    def to_solar(self, timezone: float = 7.0) -> 'SolarDate': ...
    def to_date(self) -> datetime.date: ...
    
    # Can Chi methods
    def year_name(self) -> str: ...     # "Giáp Thìn"
    def month_name(self) -> str: ...    # "Bính Dần"
    def day_name(self) -> str: ...      # "Canh Tuất"
    def hour_name(self) -> str: ...     # "Bính Tý"
    
    # Solar term & Lucky hours
    def solar_term(self, timezone: float = 7.0) -> str: ...
    def lucky_hours(self) -> list[dict]: ...
    
    # Factory methods
    @classmethod
    def from_date(cls, d: datetime.date, tz: float = 7.0) -> 'LunarDate': ...
    @classmethod
    def from_solar(cls, solar: SolarDate, tz: float = 7.0) -> 'LunarDate': ...
    @classmethod
    def today(cls, tz: float = 7.0) -> 'LunarDate': ...
    
    # Info methods
    def leap_month_of_year(self) -> int | None: ...  # Tháng nhuận trong năm
    def month_length(self) -> int: ...                # Số ngày trong tháng
```

### 3.3 Converter (Internal)

```python
class Converter:
    """Core conversion engine. Stateless, all static methods."""
    
    @staticmethod
    @lru_cache(maxsize=512)
    def solar_to_lunar(dd, mm, yy, tz=7.0) -> tuple: ...
    
    @staticmethod
    def lunar_to_solar(dd, mm, yy, leap, tz=7.0) -> tuple: ...
    
    @staticmethod
    @lru_cache(maxsize=256)
    def _get_new_moon_day(k, tz) -> int: ...
    
    @staticmethod
    @lru_cache(maxsize=256)
    def _get_lunar_month_11(yy, tz) -> int: ...
    
    @staticmethod
    def _get_leap_month_offset(a11, tz) -> int: ...
```

---

## 4. Package Configuration

### 4.1 pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "vn-lunar-calendar"
version = "0.1.0"
description = "Vietnamese Lunar Calendar converter"
requires-python = ">=3.8"
license = {text = "MIT"}
keywords = ["lunar", "calendar", "vietnamese", "am-lich", "canchi"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
]

[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "mypy", "ruff"]
```

### 4.2 Directory Structure

```
LunarCalendar/
├── docs/
│   └── PRD/
│       ├── 01_PRD.md
│       ├── 02_Algorithm_Design.md
│       └── 03_Architecture.md
├── src/
│   └── vn_lunar_calendar/
│       ├── __init__.py
│       ├── solar.py
│       ├── lunar.py
│       ├── converter.py
│       ├── canchi.py
│       ├── solar_terms.py
│       ├── lucky_hours.py
│       ├── constants.py
│       ├── exceptions.py
│       ├── utils.py
│       ├── festivals.py
│       └── py.typed
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_solar.py
│   ├── test_lunar.py
│   ├── test_canchi.py
│   ├── test_solar_terms.py
│   ├── test_lucky_hours.py
│   └── test_integration.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

---

## 5. Design Decisions & Rationale

### 5.1 Tại Sao Dùng Astronomical Calculation?

| Tiêu Chí | Lookup Table | Year Code | Astronomical |
|-----------|-------------|-----------|-------------|
| Phạm vi | 1900-2100 | 1200-2199 | Không giới hạn |
| Kích thước | ~20KB data | ~50KB data | ~0KB data |
| Tốc độ | O(1) | O(1) | O(1) + trig |
| Bảo trì | Cần update data | Cần update data | Không cần |
| Độ chính xác | Phụ thuộc data | Phụ thuộc data | Tính toán trực tiếp |
| **Được chọn** | | | ✅ |

### 5.2 Tại Sao Dùng `dataclass(frozen=True)`?
- **Immutability**: Dates không nên thay đổi sau khi tạo
- **Hashable**: Có thể dùng làm key trong dict/set
- **Thread-safe**: An toàn trong multi-threading

### 5.3 Tại Sao Timezone Mặc Định = 7.0?
- Lịch âm Việt Nam tính theo UTC+7 (Indochina Time)
- Khác với Trung Quốc (UTC+8), có thể gây lệch 1 ngày
- User có thể override cho timezone khác

### 5.4 Tại Sao Pure Python?
- Không cần C extension hoặc external dependency
- Dễ cài đặt trên mọi platform
- Performance đủ tốt nhờ caching (`lru_cache`)

---

## 6. Performance Optimization

### 6.1 Caching

```python
from functools import lru_cache

@lru_cache(maxsize=512)
def _new_moon(k: int) -> float:
    """Cache New Moon calculation."""
    ...

@lru_cache(maxsize=256)
def _get_new_moon_day(k: int, tz: float) -> int:
    """Cache timezone-adjusted New Moon day."""
    ...

@lru_cache(maxsize=128)
def _lunar_month_11(year: int, tz: float) -> int:
    """Cache Month 11 calculation per year."""
    ...
```

### 6.2 Expected Performance

| Operation | Uncached | Cached |
|-----------|----------|--------|
| Solar → Lunar | ~0.1ms | ~0.01ms |
| Lunar → Solar | ~0.1ms | ~0.01ms |
| Can Chi | ~0.001ms | N/A |
| Tiết Khí | ~0.05ms | N/A |
| Full year (365 days) | ~36ms | ~3.6ms |
