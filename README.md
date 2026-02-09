# vn-lunar-calendar 🌙

Vietnamese Lunar Calendar – A reusable Python package for Solar/Lunar date conversion, Can Chi (Sexagenary cycle), Solar Terms (Tiết Khí), and Lucky Hours (Giờ Hoàng Đạo).

## Features

- ☀️ **Solar ↔ Lunar** date conversion (Dương lịch ↔ Âm lịch)
- 🐉 **Can Chi** naming for year, month, day, hour (Thiên Can Địa Chi)
- 🌿 **24 Solar Terms** (Tiết Khí / 節氣)
- ⏰ **Lucky Hours** (Giờ Hoàng Đạo)
- 🎋 **Leap Month** detection (Tháng Nhuận)
- ✅ **Date Validation** for both solar and lunar dates
- 🇻🇳 **Vietnam timezone** (UTC+7) by default
- 📦 **Pure Python** – no external dependencies

## Installation

```bash
pip install vn-lunar-calendar
```

## Quick Start

```python
from vn_lunar_calendar import SolarDate, LunarDate

# Solar → Lunar
solar = SolarDate(2024, 2, 10)
lunar = solar.to_lunar()
print(lunar)  # LunarDate(2024, 1, 1, is_leap=False)  → Tết Nguyên Đán!

# Lunar → Solar
lunar = LunarDate(2024, 1, 1)
solar = lunar.to_solar()
print(solar)  # SolarDate(2024, 2, 10)

# Can Chi
print(lunar.year_name())   # "Giáp Thìn"
print(lunar.month_name())  # "Bính Dần"
print(lunar.day_name())    # "Canh Tuất"

# Solar Term (Tiết Khí)
print(solar.solar_term())  # "Lập xuân"

# Lucky Hours (Giờ Hoàng Đạo)
for hour in lunar.lucky_hours():
    print(f"{hour['name']}: {hour['start']}h - {hour['end']}h")

# Works with datetime
import datetime
today_lunar = LunarDate.from_date(datetime.date.today())
print(today_lunar)
```

## Algorithms

Based on **Ho Ngoc Duc's algorithm** using astronomical calculations from *"Astronomical Algorithms"* by Jean Meeus (1998). See [docs/PRD/02_Algorithm_Design.md](docs/PRD/02_Algorithm_Design.md) for details.

## Development

```bash
# Clone & install dev dependencies
git clone https://github.com/your-org/vn-lunar-calendar.git
cd vn-lunar-calendar
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=vn_lunar_calendar

# Type check & lint
mypy src/vn_lunar_calendar/
ruff check src/ tests/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
